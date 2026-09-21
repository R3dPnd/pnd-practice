# 02 — Token bucket pacer

**Theme:** lazy time-based refill, correctness under concurrency. Models the pacing
budget allocator from `../../system_design/examples/04_ad_pacing_budget_service.md` — a
campaign gets a slice of budget that refills smoothly over time rather than all at once.

## Problem

```java
class TokenBucket {
    TokenBucket(double capacity, double refillPerSecond) { /* starts full */ }

    // Atomically: refill based on elapsed time since the last refill (capped at
    // `capacity`), then consume `tokens` if enough are available. Returns true and
    // deducts on success, false (no deduction) if insufficient tokens are available.
    boolean tryConsume(double tokens) { /* ... */ }
}
```

## Constraints / edge cases to think about

- **Lazy refill, not a background thread.** Don't spin up a `ScheduledExecutorService`
  ticking every N ms — compute elapsed time since the last refill *inside*
  `tryConsume` itself (`System.nanoTime()` diff), and only ever refill up to `capacity`.
  This is both simpler and avoids a whole class of "is the scheduler thread even
  running" bugs.
- **Atomicity**: refill-then-consume has to happen as one atomic unit under concurrent
  callers — two threads must never both read "4.5 tokens available, need 3" and both
  succeed, leaving the bucket negative.
- Starts **full** (`availableTokens = capacity`), matching how a campaign is usually
  given its full initial budget slice up front, not built up from zero.

## Why this matters for the role

Token bucket (or its cousin, leaky bucket) is the standard primitive behind both rate
limiting *and* pacing/budget smoothing — the exact "correct pacing" language in the JD.
It's also a very common general backend interview question independent of Disney, so
it's worth having cold regardless of how this specific loop goes.

## Run

```bash
javac Practice.java && java Practice
javac Solution.java && java Solution
```
