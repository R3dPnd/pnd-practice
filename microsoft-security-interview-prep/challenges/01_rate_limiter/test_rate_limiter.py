import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_rate_limiter" if use_practice else "solution_rate_limiter"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_allows_up_to_capacity_then_blocks(fake_clock):
    limiter = impl.TokenBucketRateLimiter(capacity=3, refill_rate=1, clock=fake_clock)
    assert limiter.allow("a") is True
    assert limiter.allow("a") is True
    assert limiter.allow("a") is True
    assert limiter.allow("a") is False


def test_refills_over_time(fake_clock):
    limiter = impl.TokenBucketRateLimiter(capacity=2, refill_rate=1, clock=fake_clock)
    assert limiter.allow("a") is True
    assert limiter.allow("a") is True
    assert limiter.allow("a") is False

    fake_clock.advance(1.0)
    assert limiter.allow("a") is True
    assert limiter.allow("a") is False


def test_never_exceeds_capacity_after_long_idle(fake_clock):
    limiter = impl.TokenBucketRateLimiter(capacity=2, refill_rate=5, clock=fake_clock)
    assert limiter.allow("a") is True
    assert limiter.allow("a") is True

    fake_clock.advance(1000.0)
    assert limiter.allow("a") is True
    assert limiter.allow("a") is True
    assert limiter.allow("a") is False


def test_keys_are_independent(fake_clock):
    limiter = impl.TokenBucketRateLimiter(capacity=1, refill_rate=1, clock=fake_clock)
    assert limiter.allow("a") is True
    assert limiter.allow("a") is False
    assert limiter.allow("b") is True


def test_fractional_refill_rate(fake_clock):
    limiter = impl.TokenBucketRateLimiter(capacity=1, refill_rate=0.5, clock=fake_clock)
    assert limiter.allow("a") is True
    assert limiter.allow("a") is False

    fake_clock.advance(1.0)  # only half a token back
    assert limiter.allow("a") is False

    fake_clock.advance(1.0)  # now a full token back
    assert limiter.allow("a") is True


def test_zero_capacity_never_allows(fake_clock):
    limiter = impl.TokenBucketRateLimiter(capacity=0, refill_rate=1, clock=fake_clock)
    assert limiter.allow("a") is False


def test_rejects_negative_capacity(fake_clock):
    with pytest.raises(ValueError):
        impl.TokenBucketRateLimiter(capacity=-1, refill_rate=1, clock=fake_clock)
