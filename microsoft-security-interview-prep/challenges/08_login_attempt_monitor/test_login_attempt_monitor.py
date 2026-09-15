import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_login_attempt_monitor" if use_practice else "solution_login_attempt_monitor"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_locks_after_max_attempts_within_window(fake_clock):
    monitor = impl.LoginAttemptMonitor(max_attempts=3, window_seconds=10, clock=fake_clock)
    assert monitor.is_locked("alice") is False

    monitor.record_failure("alice")
    monitor.record_failure("alice")
    assert monitor.is_locked("alice") is False

    monitor.record_failure("alice")
    assert monitor.is_locked("alice") is True


def test_window_slides_and_old_failures_expire(fake_clock):
    monitor = impl.LoginAttemptMonitor(max_attempts=3, window_seconds=10, clock=fake_clock)
    monitor.record_failure("alice")  # t=0

    fake_clock.advance(1)
    monitor.record_failure("alice")  # t=1

    fake_clock.advance(1)
    monitor.record_failure("alice")  # t=2
    assert monitor.is_locked("alice") is True

    fake_clock.advance(9)  # now t=11, the t=0 failure has aged out (window=10)
    assert monitor.is_locked("alice") is False


def test_record_success_clears_history(fake_clock):
    monitor = impl.LoginAttemptMonitor(max_attempts=2, window_seconds=10, clock=fake_clock)
    monitor.record_failure("alice")
    monitor.record_success("alice")
    monitor.record_failure("alice")
    assert monitor.is_locked("alice") is False  # only 1 failure since the reset


def test_identifiers_are_independent(fake_clock):
    monitor = impl.LoginAttemptMonitor(max_attempts=1, window_seconds=10, clock=fake_clock)
    monitor.record_failure("alice")
    assert monitor.is_locked("alice") is True
    assert monitor.is_locked("bob") is False


def test_unknown_identifier_is_not_locked(fake_clock):
    monitor = impl.LoginAttemptMonitor(max_attempts=1, window_seconds=10, clock=fake_clock)
    assert monitor.is_locked("nobody") is False


def test_rejects_non_positive_max_attempts(fake_clock):
    with pytest.raises(ValueError):
        impl.LoginAttemptMonitor(max_attempts=0, window_seconds=10, clock=fake_clock)


def test_failures_spread_beyond_window_never_lock(fake_clock):
    monitor = impl.LoginAttemptMonitor(max_attempts=2, window_seconds=5, clock=fake_clock)
    monitor.record_failure("alice")  # t=0

    fake_clock.advance(6)  # t=6, first failure now outside the 5s window
    monitor.record_failure("alice")  # only 1 failure inside the current window
    assert monitor.is_locked("alice") is False
