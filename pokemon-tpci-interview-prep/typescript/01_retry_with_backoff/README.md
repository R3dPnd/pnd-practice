# TS 01 — retry with exponential backoff

```ts
retry<T>(fn: (attempt: number) => Promise<T>, opts: {
  retries: number;            // extra attempts after the first
  baseMs: number;             // delay before retry n = baseMs * 2^(n-1)
  shouldRetry?: (err: unknown) => boolean;  // default: always
  sleep?: (ms: number) => Promise<void>;    // injectable for tests
}): Promise<T>
```
- `attempt` starts at 1. Rethrow the last error when retries are exhausted, or immediately
  if `shouldRetry` returns false (e.g. a 400 — don't retry client errors; do retry 429/5xx).
- Talking points: jitter (thundering herd), idempotency of the retried call, retry budgets,
  why the AWS SDK already does this for you.
