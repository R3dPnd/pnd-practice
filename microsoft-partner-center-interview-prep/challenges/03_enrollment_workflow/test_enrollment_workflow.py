import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_enrollment_workflow" if use_practice else "solution_enrollment_workflow"
    return importlib.import_module(module_name)


impl = _load_impl()


@pytest.fixture
def svc():
    s = impl.EnrollmentService()
    s.start("p1")
    return s


def test_start_is_draft_and_idempotent(svc):
    assert svc.status("p1") == "DRAFT"
    svc.apply("p1", "submit", "k1")
    assert svc.start("p1") == "PENDING"  # does not reset
    assert svc.status("p1") == "PENDING"


def test_happy_path(svc):
    assert svc.apply("p1", "submit", "k1") == "PENDING"
    assert svc.apply("p1", "approve", "k2") == "ACTIVE"
    assert svc.apply("p1", "suspend", "k3") == "SUSPENDED"
    assert svc.apply("p1", "reinstate", "k4") == "ACTIVE"
    assert svc.history("p1") == [
        ("submit", "PENDING"),
        ("approve", "ACTIVE"),
        ("suspend", "SUSPENDED"),
        ("reinstate", "ACTIVE"),
    ]


def test_reject_and_resubmit(svc):
    svc.apply("p1", "submit", "k1")
    assert svc.apply("p1", "reject", "k2") == "REJECTED"
    assert svc.apply("p1", "submit", "k3") == "PENDING"
    assert svc.apply("p1", "approve", "k4") == "ACTIVE"


def test_third_rejection_locks(svc):
    for i in range(2):
        svc.apply("p1", "submit", f"s{i}")
        assert svc.apply("p1", "reject", f"r{i}") == "REJECTED"
    svc.apply("p1", "submit", "s2")
    assert svc.apply("p1", "reject", "r2") == "LOCKED"
    with pytest.raises(impl.InvalidTransition):
        svc.apply("p1", "submit", "s3")


def test_rejection_count_is_per_partner(svc):
    svc.start("p2")
    for i in range(2):
        svc.apply("p1", "submit", f"p1s{i}")
        svc.apply("p1", "reject", f"p1r{i}")
    svc.apply("p2", "submit", "p2s0")
    assert svc.apply("p2", "reject", "p2r0") == "REJECTED"


def test_invalid_transition_leaves_state_unchanged(svc):
    with pytest.raises(impl.InvalidTransition):
        svc.apply("p1", "approve", "k1")
    assert svc.status("p1") == "DRAFT"
    assert svc.history("p1") == []


def test_invalid_transition_does_not_consume_key(svc):
    with pytest.raises(impl.InvalidTransition):
        svc.apply("p1", "approve", "k1")
    svc.apply("p1", "submit", "k0")
    assert svc.apply("p1", "approve", "k1") == "ACTIVE"


def test_retry_with_same_key_returns_original_result(svc):
    assert svc.apply("p1", "submit", "k1") == "PENDING"
    assert svc.apply("p1", "submit", "k1") == "PENDING"  # retry, not an invalid transition
    assert svc.history("p1") == [("submit", "PENDING")]


def test_retry_after_state_moved_on_returns_original_result(svc):
    svc.apply("p1", "submit", "k1")
    svc.apply("p1", "approve", "k2")
    assert svc.apply("p1", "submit", "k1") == "PENDING"
    assert svc.status("p1") == "ACTIVE"
    assert len(svc.history("p1")) == 2


def test_retry_does_not_double_count_rejections(svc):
    svc.apply("p1", "submit", "s0")
    svc.apply("p1", "reject", "r0")
    svc.apply("p1", "reject", "r0")
    svc.apply("p1", "reject", "r0")
    svc.apply("p1", "submit", "s1")
    assert svc.apply("p1", "reject", "r1") == "REJECTED"  # only the 2nd real rejection


def test_key_reused_for_different_event_conflicts(svc):
    svc.apply("p1", "submit", "k1")
    with pytest.raises(impl.IdempotencyConflict):
        svc.apply("p1", "approve", "k1")
    assert svc.status("p1") == "PENDING"


def test_key_reused_for_different_partner_conflicts(svc):
    svc.start("p2")
    svc.apply("p1", "submit", "k1")
    with pytest.raises(impl.IdempotencyConflict):
        svc.apply("p2", "submit", "k1")
    assert svc.status("p2") == "DRAFT"


def test_unknown_event_raises_value_error(svc):
    with pytest.raises(ValueError):
        svc.apply("p1", "delete_everything", "k1")


def test_unknown_partner_raises_key_error(svc):
    with pytest.raises(KeyError):
        svc.apply("ghost", "submit", "k1")
    with pytest.raises(KeyError):
        svc.status("ghost")
    with pytest.raises(KeyError):
        svc.history("ghost")


def test_history_is_a_copy(svc):
    svc.apply("p1", "submit", "k1")
    h = svc.history("p1")
    h.append(("approve", "ACTIVE"))
    assert svc.history("p1") == [("submit", "PENDING")]


def test_error_types_are_value_errors():
    assert issubclass(impl.InvalidTransition, ValueError)
    assert issubclass(impl.IdempotencyConflict, ValueError)
