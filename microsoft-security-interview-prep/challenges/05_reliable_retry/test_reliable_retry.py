import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_reliable_retry" if use_practice else "solution_reliable_retry"
    return importlib.import_module(module_name)


impl = _load_impl()


class FlakyError(Exception):
    pass


class OtherError(Exception):
    pass


def _recorder():
    calls = []

    def sleep(delay):
        calls.append(delay)

    return calls, sleep


# --- retry_with_backoff ---


def test_succeeds_on_first_try_no_sleep():
    calls, sleep = _recorder()
    result = impl.retry_with_backoff(lambda: "ok", max_attempts=3, base_delay=1, sleep=sleep)
    assert result == "ok"
    assert calls == []


def test_retries_then_succeeds():
    attempts = {"n": 0}

    def flaky():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise FlakyError("boom")
        return "ok"

    calls, sleep = _recorder()
    result = impl.retry_with_backoff(
        flaky, max_attempts=5, base_delay=1, exceptions=(FlakyError,), sleep=sleep
    )
    assert result == "ok"
    assert attempts["n"] == 3
    assert calls == [1, 2]  # base_delay * 2**0, base_delay * 2**1


def test_exhausts_attempts_and_raises_last_exception():
    def always_fails():
        raise FlakyError("nope")

    calls, sleep = _recorder()
    with pytest.raises(FlakyError):
        impl.retry_with_backoff(
            always_fails, max_attempts=3, base_delay=1, exceptions=(FlakyError,), sleep=sleep
        )
    assert calls == [1, 2]  # slept between attempts, not after the final failure


def test_does_not_retry_on_unlisted_exception():
    calls, sleep = _recorder()

    def raises_other():
        raise OtherError("nope")

    with pytest.raises(OtherError):
        impl.retry_with_backoff(
            raises_other, max_attempts=5, base_delay=1, exceptions=(FlakyError,), sleep=sleep
        )
    assert calls == []


def test_backoff_delays_grow_exponentially():
    calls, sleep = _recorder()

    def always_fails():
        raise FlakyError("nope")

    with pytest.raises(FlakyError):
        impl.retry_with_backoff(
            always_fails, max_attempts=4, base_delay=2, exceptions=(FlakyError,), sleep=sleep
        )
    assert calls == [2, 4, 8]


# --- CircuitBreaker ---


def test_circuit_stays_closed_on_success(fake_clock):
    breaker = impl.CircuitBreaker(failure_threshold=2, recovery_timeout=10, clock=fake_clock)
    assert breaker.call(lambda: "ok") == "ok"
    assert breaker.call(lambda: "ok") == "ok"


def test_circuit_opens_after_threshold_failures(fake_clock):
    breaker = impl.CircuitBreaker(failure_threshold=2, recovery_timeout=10, clock=fake_clock)

    def fails():
        raise RuntimeError("down")

    with pytest.raises(RuntimeError):
        breaker.call(fails)
    with pytest.raises(RuntimeError):
        breaker.call(fails)

    calls = {"n": 0}

    def should_not_run():
        calls["n"] += 1
        return "ok"

    with pytest.raises(impl.CircuitOpenError):
        breaker.call(should_not_run)
    assert calls["n"] == 0  # circuit rejected without calling func


def test_circuit_half_opens_after_timeout_and_closes_on_success(fake_clock):
    breaker = impl.CircuitBreaker(failure_threshold=1, recovery_timeout=10, clock=fake_clock)

    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("down")))

    with pytest.raises(impl.CircuitOpenError):
        breaker.call(lambda: "ok")

    fake_clock.advance(10)
    assert breaker.call(lambda: "recovered") == "recovered"

    # circuit is closed again; failure counter was reset
    assert breaker.call(lambda: "ok") == "ok"


def test_circuit_reopens_if_half_open_trial_fails(fake_clock):
    breaker = impl.CircuitBreaker(failure_threshold=1, recovery_timeout=10, clock=fake_clock)

    def fails():
        raise RuntimeError("down")

    with pytest.raises(RuntimeError):
        breaker.call(fails)

    fake_clock.advance(10)
    with pytest.raises(RuntimeError):
        breaker.call(fails)  # half-open trial also fails -> reopen

    # immediately after, still open (timer restarted)
    with pytest.raises(impl.CircuitOpenError):
        breaker.call(lambda: "ok")


def test_failure_counter_resets_on_success_between_failures(fake_clock):
    breaker = impl.CircuitBreaker(failure_threshold=3, recovery_timeout=10, clock=fake_clock)

    def fails():
        raise RuntimeError("down")

    with pytest.raises(RuntimeError):
        breaker.call(fails)
    with pytest.raises(RuntimeError):
        breaker.call(fails)
    assert breaker.call(lambda: "ok") == "ok"  # resets consecutive count

    # two more failures should NOT be enough to open (threshold=3, only 2 consecutive)
    with pytest.raises(RuntimeError):
        breaker.call(fails)
    with pytest.raises(RuntimeError):
        breaker.call(fails)
    assert breaker.call(lambda: "still fine") == "still fine"
