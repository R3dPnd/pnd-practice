import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    return importlib.import_module("practice_login_throttle" if use_practice else "solution_login_throttle")


impl = _load_impl()


@pytest.fixture
def th(fake_clock):
    return impl.LoginThrottle(max_failures=3, window_s=60, lockout_s=600, clock=fake_clock)


def test_locks_after_max_failures(th, fake_clock):
    for _ in range(2):
        th.record_failure("ash")
        fake_clock.advance(1)
    assert th.allowed("ash")
    th.record_failure("ash")
    assert not th.allowed("ash")
    assert th.allowed("misty")


def test_lockout_expires(th, fake_clock):
    for _ in range(3):
        th.record_failure("ash")
    fake_clock.advance(599)
    th.record_failure("ash")  # ignored while locked
    assert not th.allowed("ash")
    fake_clock.advance(1)
    assert th.allowed("ash")
    th.record_failure("ash")
    assert th.allowed("ash"), "fresh start after lockout"


def test_old_failures_slide_out(th, fake_clock):
    th.record_failure("ash")
    th.record_failure("ash")
    fake_clock.advance(61)
    th.record_failure("ash")
    assert th.allowed("ash")


def test_success_resets(th):
    th.record_failure("ash")
    th.record_failure("ash")
    th.record_success("ash")
    th.record_failure("ash")
    assert th.allowed("ash")
