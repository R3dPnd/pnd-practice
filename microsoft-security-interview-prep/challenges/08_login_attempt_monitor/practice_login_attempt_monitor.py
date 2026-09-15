"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/08_login_attempt_monitor -v` to check yourself, or
`PRACTICE=0 pytest challenges/08_login_attempt_monitor -v` to see the
reference solution's tests pass instead.
"""
import time
from typing import Callable


class LoginAttemptMonitor:
    def __init__(
        self,
        max_attempts: int,
        window_seconds: float,
        clock: Callable[[], float] = time.monotonic,
    ):
        raise NotImplementedError

    def record_failure(self, identifier: str) -> None:
        raise NotImplementedError

    def is_locked(self, identifier: str) -> bool:
        raise NotImplementedError

    def record_success(self, identifier: str) -> None:
        raise NotImplementedError
