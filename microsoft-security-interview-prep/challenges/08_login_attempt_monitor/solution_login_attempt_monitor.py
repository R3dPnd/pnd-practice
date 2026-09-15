"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Need a *sliding window* count of recent failures per identifier (username/IP) —
   not a simple running total, since failures should stop counting once they age out
   of the window. A deque of failure timestamps per key is the natural fit: append
   on the right (newest), drop from the left (oldest) once they're stale.
2. `_prune` computes the window cutoff (`now - window_seconds`) and pops stale
   timestamps off the front of the deque — done lazily, on demand, rather than via a
   background timer.
3. `is_locked` prunes first (so it never checks against stale data), then compares
   the remaining count to `max_attempts`.
4. `record_success` clears the identifier's history entirely — a successful login
   resets the lockout counter completely, matching common real auth lockout policy
   (as opposed to, say, only decrementing by one).

COMMON INTERVIEWER FOLLOW-UPS:
- "Why a deque of timestamps instead of just an incrementing counter?" — a plain
  counter has no way to "expire" individual old failures — a true sliding window
  needs each failure's own timestamp to know exactly when it should stop counting.
- "How does this behave with multiple app server instances?" — it doesn't share
  state, same limitation as the rate limiter (`01`). Production would need a shared
  store — Redis sorted sets (score = timestamp) are the standard structure for this
  exact "sliding window of recent events" problem, distributed.
- "Why reset the whole history on success instead of partially decaying it?" —
  simpler, and matches typical real lockout policy; call out the tradeoff that a
  strict full reset could theoretically let a very patient, slow brute-force attacker
  interleave occasional successes to keep resetting the counter — worth flagging as
  a known tradeoff if pushed.
- "How is this different from the rate limiter in `01`?" — different semantics
  entirely: the rate limiter *permits* a steady/bursty rate via continuous refill;
  this is a hard lockout after N failures within a rolling window, fully reset by a
  single success.
"""
import time
from collections import defaultdict, deque
from typing import Callable, Deque, Dict


class LoginAttemptMonitor:
    def __init__(
        self,
        max_attempts: int,
        window_seconds: float,
        clock: Callable[[], float] = time.monotonic,
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        self._max_attempts = max_attempts
        self._window_seconds = window_seconds
        self._clock = clock
        self._failures: Dict[str, Deque[float]] = defaultdict(deque)

    def _prune(self, identifier: str) -> None:
        cutoff = self._clock() - self._window_seconds
        history = self._failures[identifier]
        while history and history[0] <= cutoff:
            history.popleft()

    def record_failure(self, identifier: str) -> None:
        self._prune(identifier)
        self._failures[identifier].append(self._clock())

    def is_locked(self, identifier: str) -> bool:
        self._prune(identifier)
        return len(self._failures[identifier]) >= self._max_attempts

    def record_success(self, identifier: str) -> None:
        self._failures[identifier].clear()
