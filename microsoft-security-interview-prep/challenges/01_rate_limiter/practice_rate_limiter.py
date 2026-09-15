"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/01_rate_limiter -v` to check yourself, or
`PRACTICE=0 pytest challenges/01_rate_limiter -v` to see the reference
solution's tests pass instead.
"""
import time
from typing import Callable


class TokenBucketRateLimiter:
    def __init__(
        self,
        capacity: int,
        refill_rate: float,
        clock: Callable[[], float] = time.monotonic,
    ):
        raise NotImplementedError

    def allow(self, key: str) -> bool:
        raise NotImplementedError
