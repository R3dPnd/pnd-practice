"""Login throttle / lockout — reference solution.

Big picture, per user:
  - `_failures[user]` is a deque of timestamps of recent failed logins, oldest first.
  - `_locked_until[user]` is the time the user's current lockout ends (if any).
  - On each failure: drop timestamps older than the window, add "now", and if the
    count reaches the limit, lock the user out and wipe their history.

The clock is INJECTED (passed in) instead of calling time.monotonic() directly. That's
what lets the tests fast-forward time with `fake_clock.advance(600)` instead of sleeping.
"""
import threading
import time
from collections import defaultdict, deque
from typing import Callable


class LoginThrottle:
    def __init__(self, max_failures: int, window_s: float, lockout_s: float,
                 clock: Callable[[], float] = time.monotonic):
        self._max = max_failures      # e.g. 3 failures...
        self._window = window_s       # ...within 60 seconds...
        self._lockout = lockout_s     # ...locks you out for 600 seconds.
        # time.monotonic never jumps backwards (unlike wall-clock time.time, which can
        # change with NTP or DST), so it's the right choice for measuring durations.
        self._clock = clock
        self._lock = threading.Lock()
        # defaultdict(deque): a missing user automatically gets an empty deque.
        self._failures: dict[str, deque[float]] = defaultdict(deque)
        self._locked_until: dict[str, float] = {}

    def allowed(self, user: str) -> bool:
        with self._lock:
            # Allowed if the current time is at or past the lockout's end.
            # .get(user, -inf) means "never locked": any time is >= negative infinity.
            return self._clock() >= self._locked_until.get(user, float("-inf"))

    def record_failure(self, user: str) -> None:
        with self._lock:
            now = self._clock()

            # Currently locked out? Ignore the failure entirely, so hammering the login
            # during a lockout doesn't extend or stack anything.
            if now < self._locked_until.get(user, float("-inf")):
                return

            failures = self._failures[user]

            # Slide the window: the deque is in time order, so expired timestamps are
            # all at the LEFT end. Pop them off until the oldest one is recent enough.
            # Each timestamp is appended once and popped at most once → amortized O(1).
            while failures and failures[0] <= now - self._window:
                failures.popleft()

            # Record this failure.
            failures.append(now)

            # Hit the limit? Lock out until now + lockout, and clear the history so the
            # user starts fresh once the lockout ends.
            if len(failures) >= self._max:
                self._locked_until[user] = now + self._lockout
                failures.clear()

    def record_success(self, user: str) -> None:
        with self._lock:
            # A successful login wipes the failure history. pop(user, None) is safe even
            # if the user has no entry.
            self._failures.pop(user, None)
