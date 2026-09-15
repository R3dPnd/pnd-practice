"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Naive idea: a per-key counter reset once a second. Reject it out loud — it allows
   up to 2x the intended rate right at a window boundary (a burst just before the
   reset, then another right after).
2. Token bucket model: each key gets a bucket holding up to `capacity` tokens,
   refilled continuously at `refill_rate` tokens/sec (not in discrete ticks).
3. Key insight: don't run a background timer thread to "refill" buckets. Refill
   lazily — on each `allow()` call, compute elapsed time since the bucket was last
   touched and top it up then, capped at `capacity`. This keeps the whole thing O(1)
   per call with no background work.
4. A bucket is created full the first time its key is seen (a brand-new client
   shouldn't be immediately throttled).
5. Consume one token if available (return True), otherwise return False — no token
   is consumed on a rejected call.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why token bucket over a fixed window counter?" — fixed window allows a 2x burst
  at the window boundary; token bucket enforces the rate smoothly at any instant.
- "How does this work across multiple server instances?" — it doesn't, as written;
  each process has its own in-memory buckets. In production you'd move bucket state
  to a shared, fast store (Redis) and make the check-and-decrement atomic (e.g. a
  Lua script or `INCR`+`EXPIRE`) so concurrent instances can't race past the limit.
- "What do you return to a throttled client?" — HTTP 429 with a `Retry-After` header,
  not a silent drop.
- "How did you test this without real sleeps?" — the clock is injected
  (`clock: Callable[[], float]`), so tests pass a fake/controllable clock instead of
  waiting on `time.monotonic()` — see `conftest.py`'s `fake_clock` fixture.
- "What happens to memory over time?" — buckets for keys that stop being used are
  never evicted here; a production version would need a TTL/sweep to bound memory.
"""
import time
from typing import Callable, Dict


class _Bucket:
    __slots__ = ("tokens", "last_refill")

    def __init__(self, tokens: float, last_refill: float):
        self.tokens = tokens
        self.last_refill = last_refill


class TokenBucketRateLimiter:
    def __init__(
        self,
        capacity: int,
        refill_rate: float,
        clock: Callable[[], float] = time.monotonic,
    ):
        if capacity < 0:
            raise ValueError("capacity must be >= 0")
        if refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._clock = clock
        self._buckets: Dict[str, _Bucket] = {}

    def allow(self, key: str) -> bool:
        now = self._clock()
        bucket = self._buckets.get(key)
        if bucket is None:
            bucket = _Bucket(tokens=float(self._capacity), last_refill=now)
            self._buckets[key] = bucket
        else:
            elapsed = max(0.0, now - bucket.last_refill)
            bucket.tokens = min(self._capacity, bucket.tokens + elapsed * self._refill_rate)
            bucket.last_refill = now

        if bucket.tokens >= 1:
            bucket.tokens -= 1
            return True
        return False
