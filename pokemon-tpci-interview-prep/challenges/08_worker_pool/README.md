# 08 — Bounded worker pool with cancellation

**Pattern:** goroutines, channels / semaphore, `context`, `errgroup`-style first-error · **Go idioms**

After a Regional, results for hundreds of events/divisions get uploaded and processed
(points awarded, emails sent). Process them concurrently — but bounded, so you don't
exhaust DB connections or hit rate limits.

## Task

```go
func Map[T, R any](ctx context.Context, items []T, workers int,
	fn func(context.Context, T) (R, error)) ([]R, error)
```

- Run `fn` over every item with **at most `workers` calls in flight**.
- Results are returned **in input order**.
- On the first error, cancel the context passed to remaining calls, stop starting new work,
  and return that error (results may be nil).
- If the parent `ctx` is cancelled, return `ctx.Err()`.
- `workers <= 0` → treat as 1.

Write it with plain `sync`/channels first. Then mention `golang.org/x/sync/errgroup` with
`g.SetLimit(n)` — that's what you'd use in real code.

## Talking points
- Why not one goroutine per item? (Unbounded fan-out → connection pool exhaustion.)
- Ordering: write into `results[i]` from each goroutine — no mutex needed since each index
  is written by exactly one goroutine.
- In AWS: SQS + Lambda with reserved concurrency is the same idea at the infra level.
