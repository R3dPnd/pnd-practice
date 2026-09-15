"""Shared pytest fixtures for the challenge suites."""
import pytest


class FakeClock:
    """A controllable monotonic clock for testing time-based logic
    (rate limiters, circuit breakers, sliding windows) without real sleeps."""

    def __init__(self, start: float = 0.0):
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


@pytest.fixture
def fake_clock():
    return FakeClock()
