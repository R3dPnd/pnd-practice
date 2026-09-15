# 08 — Login Attempt Monitor (Sliding Window)

**Theme:** security-minded engineering + sliding-window technique. Brute-force /
credential-stuffing lockout logic is a very plausible Security coding prompt — and the
sliding-window pattern here is the same skill tested by classic "max in a window" /
"requests in the last N seconds" problems, just framed for the domain.

## Problem

```python
class LoginAttemptMonitor:
    def __init__(self, max_attempts: int, window_seconds: float, clock: Callable[[], float] = time.monotonic):
        ...

    def record_failure(self, identifier: str) -> None:
        """Record a failed login attempt for `identifier` (e.g. username or IP)."""

    def is_locked(self, identifier: str) -> bool:
        """True if `identifier` has had >= max_attempts failures within the
        last `window_seconds` (a sliding window ending "now")."""

    def record_success(self, identifier: str) -> None:
        """A successful login clears that identifier's failure history."""
```

## Constraints

- The window **slides** — failures older than `window_seconds` no longer count, even
  without a success in between. (E.g. `max_attempts=3`, failures at t=0, t=1, t=2 →
  locked at t=2. But by t=11 with `window_seconds=10`, the t=0 failure has aged out —
  if there were no other failures, it should no longer be locked.)
- Each `identifier` is tracked independently.
- `record_success` fully resets that identifier (not just decrements).
- Don't recompute an unbounded scan of *all* history on every check — expired entries
  should get pruned (e.g. from the front of a deque, since they're recorded in time
  order) rather than kept forever.

## Why this matters for Security

This is literally account-lockout / brute-force-protection logic. Good discussion
points if asked to extend it: what do you return to the caller so the UI can show
"try again in N seconds"; per-identifier vs per-IP vs both (an attacker rotating IPs
still hits the same username); how this interacts with legitimate users who mistype
their password a few times (don't lock too aggressively); and how it'd need to become
distributed/shared state (this in-memory version is single-process) in a real service —
same tradeoff discussion as `01_rate_limiter`.

## Run

```bash
pytest challenges/08_login_attempt_monitor -v
```
