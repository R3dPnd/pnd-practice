"""Fill this in. See README.md for the problem statement."""
import time
from typing import Callable


class LoginThrottle:
    def __init__(self, max_failures: int, window_s: float, lockout_s: float,
                 clock: Callable[[], float] = time.monotonic):
        raise NotImplementedError

    def allowed(self, user: str) -> bool:
        raise NotImplementedError

    def record_failure(self, user: str) -> None:
        raise NotImplementedError

    def record_success(self, user: str) -> None:
        raise NotImplementedError
