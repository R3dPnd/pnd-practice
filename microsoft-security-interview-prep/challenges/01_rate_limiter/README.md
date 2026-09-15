# 01 — Token Bucket Rate Limiter

**Theme:** algorithms + security (abuse/DoS prevention). Good warm-up; a real
per-client API rate limiter is a very plausible Microsoft Security coding prompt.

## Problem

Implement a per-key token-bucket rate limiter:

```python
class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float, clock: Callable[[], float] = time.monotonic):
        ...

    def allow(self, key: str) -> bool:
        """Return True and consume one token if `key` has a token available,
        otherwise return False. Each key gets its own independent bucket."""
```

- `capacity` — max tokens (= max burst size) a bucket can hold.
- `refill_rate` — tokens added per second, continuously (not in discrete ticks).
- A bucket starts **full** (`capacity` tokens) the first time a key is seen.
- `clock` is injected so it's testable without real sleeps — always call `self._clock()`,
  never `time.monotonic()` directly.

## Constraints / edge cases to think about

- Two different keys must not interfere with each other.
- A bucket must never exceed `capacity`, even after a long idle period.
- Fractional refill (e.g. `refill_rate=0.5` token/sec) should work correctly over
  partial-second gaps, not just whole seconds.
- `allow()` on a brand-new key with `capacity=0` should return `False`.

## Why this matters for Security

This is the shape of the first line of defense against credential-stuffing / brute-force
/ scraping — the same pattern shows up later in `08_login_attempt_monitor` for the
"lock the account after N failures" case. Be ready to discuss: what key would you use in
production (IP? user ID? API key?), what happens under a distributed/multi-instance
deployment (this in-memory version doesn't share state — you'd need Redis or similar),
and what you return to the client (429 + `Retry-After`).

## Run

```bash
pytest challenges/01_rate_limiter -v
```
