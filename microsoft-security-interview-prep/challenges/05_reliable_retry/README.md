# 05 — Retry with Backoff + Circuit Breaker

**Theme:** debugging & reliability — explicitly called out in the recruiter email as its
own coding-interview focus area, separate from raw algorithms.

## Part A — `retry_with_backoff`

```python
def retry_with_backoff(
    func: Callable[[], Any],
    max_attempts: int,
    base_delay: float,
    exceptions: tuple = (Exception,),
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    """Call func(). If it raises one of `exceptions`, retry with exponential
    backoff: sleep(base_delay * 2**attempt) between attempts (attempt starts at
    0 for the delay after the first failure). Return the value on success.
    If all `max_attempts` attempts fail, re-raise the last exception.
    Exceptions NOT in `exceptions` should propagate immediately, no retry."""
```

`sleep` is injected so tests don't actually wait — a fake `sleep` can just record the
delays it was called with.

## Part B — `CircuitBreaker`

```python
class CircuitOpenError(Exception):
    ...

class CircuitBreaker:
    def __init__(self, failure_threshold: int, recovery_timeout: float, clock: Callable[[], float] = time.monotonic):
        ...

    def call(self, func: Callable[[], Any]) -> Any:
        """Execute func() through the breaker.

        - CLOSED (normal): run func(). A success keeps it closed. A failure
          increments a consecutive-failure counter; hitting `failure_threshold`
          OPENS the circuit.
        - OPEN: calls are rejected immediately by raising CircuitOpenError,
          WITHOUT calling func() — until `recovery_timeout` seconds have
          elapsed since it opened. Once elapsed, allow exactly one HALF-OPEN
          trial call through.
        - HALF-OPEN trial: success -> circuit CLOSES, failure counter resets.
          failure -> circuit re-OPENS (timer restarts).
        """
```

## Why this matters for Security

Both patterns exist for the same reason: a downstream dependency (auth service, a
security-scanning API, a key vault) will occasionally fail or degrade, and naive code
either hammers it into the ground (no backoff) or cascades the outage to every caller
(no circuit breaker). Be ready to discuss: what should `exceptions` include in
practice (you generally do **not** want to retry on a 4xx-style "this request is
invalid" error, only on transient/5xx/timeout-style failures), and what "jitter" adds
to plain exponential backoff (avoids synchronized retry storms across many clients).

## Run

```bash
pytest challenges/05_reliable_retry -v
```
