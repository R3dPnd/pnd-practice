"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/05_reliable_retry -v` to check yourself, or
`PRACTICE=0 pytest challenges/05_reliable_retry -v` to see the reference
solution's tests pass instead.
"""
import time
from typing import Any, Callable, Tuple, Type


def retry_with_backoff(
    func: Callable[[], Any],
    max_attempts: int,
    base_delay: float,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    raise NotImplementedError


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int,
        recovery_timeout: float,
        clock: Callable[[], float] = time.monotonic,
    ):
        raise NotImplementedError

    def call(self, func: Callable[[], Any]) -> Any:
        raise NotImplementedError
