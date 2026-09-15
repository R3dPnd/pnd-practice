"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. `retry_with_backoff`: loop up to `max_attempts` times, catch only the specified
   exception types (not a bare `except:` — an unrelated bug shouldn't be silently
   retried), and sleep with exponential backoff (`base_delay * 2**attempt`) between
   attempts. On the *last* attempt, re-raise instead of swallowing the error — a
   caller needs to know it ultimately failed.
2. `CircuitBreaker` needs three genuinely distinct behaviors, so model them as three
   explicit states (closed/open/half_open) rather than as one or two booleans, which
   would force awkward combinations to represent the same states.
3. **Closed** (normal operation): calls go through; count consecutive failures, and
   once they hit `failure_threshold`, flip to **open**.
4. **Open** (failing fast): reject calls immediately *without* invoking the real
   function, until `recovery_timeout` has elapsed — this is what protects an already
   struggling dependency from being hammered further.
5. **Half-open** (probing recovery): after the timeout, let exactly one real call
   through as a test. Success -> back to closed (fully reset). Failure -> back to
   open, restarting the recovery timer.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why exponential backoff instead of a fixed delay between retries?" — a fixed
  delay across many concurrent callers retries all at once and can synchronize into
  a "thundering herd" against a dependency that's already struggling; exponential
  backoff spreads attempts out over time. (Adding random jitter on top is the further
  real-world refinement this solution doesn't implement — worth mentioning.)
- "Why do you need a circuit breaker if you already have retries?" — retries handle
  brief, transient blips; a circuit breaker protects against a *sustained* outage by
  stopping wasted calls and latency once failure is clearly systemic, rather than
  retrying forever into a dependency that isn't coming back soon.
- "What's the difference between open and half-open?" — open = fail fast, zero real
  calls reach the dependency; half-open = allow exactly one probe call through to
  test whether it's safe to resume.
- "How would you make this safe under concurrent callers?" — state transitions need a
  lock; the trickiest invariant to preserve under concurrency is "half-open allows
  exactly one trial call," since multiple threads could otherwise all see half-open
  and all probe simultaneously.
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
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions:
            if attempt == max_attempts - 1:
                raise
            sleep(base_delay * (2 ** attempt))


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    _CLOSED = "closed"
    _OPEN = "open"
    _HALF_OPEN = "half_open"

    def __init__(
        self,
        failure_threshold: int,
        recovery_timeout: float,
        clock: Callable[[], float] = time.monotonic,
    ):
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be >= 1")
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._clock = clock
        self._state = self._CLOSED
        self._failure_count = 0
        self._opened_at = None

    def call(self, func: Callable[[], Any]) -> Any:
        if self._state == self._OPEN:
            if self._clock() - self._opened_at < self._recovery_timeout:
                raise CircuitOpenError("circuit is open")
            self._state = self._HALF_OPEN

        try:
            result = func()
        except Exception:
            self._on_failure()
            raise
        else:
            self._on_success()
            return result

    def _on_success(self) -> None:
        self._state = self._CLOSED
        self._failure_count = 0
        self._opened_at = None

    def _on_failure(self) -> None:
        if self._state == self._HALF_OPEN:
            self._state = self._OPEN
            self._opened_at = self._clock()
            return

        self._failure_count += 1
        if self._failure_count >= self._failure_threshold:
            self._state = self._OPEN
            self._opened_at = self._clock()
