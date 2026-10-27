# 03 — Event registration with capacity + waitlist (concurrency-safe)

**Pattern:** mutex-guarded state, FIFO queue · **Domain:** League Challenge / Regionals registration

Popular events (Regionals, Worlds side events) sell out in seconds. Registration must never
oversell, must be fair (FIFO waitlist), and must be safe under concurrent requests.

## Task

```go
e := NewEvent(capacity)
status, err := e.Register(playerID)   // Confirmed or Waitlisted; ErrAlreadyRegistered on dup
promoted, err := e.Cancel(playerID)   // ErrNotRegistered if unknown; returns promoted ID ("" if none)
e.Confirmed()                          // []string in confirmation order
e.Waitlist()                           // []string in FIFO order
```

- Cancelling a **confirmed** player promotes the head of the waitlist (appended to the end
  of `Confirmed()`), and returns their ID.
- Cancelling a **waitlisted** player just removes them; nobody is promoted.
- All methods must be safe for concurrent use. Run tests with `-race`.

## Talking points
- In-memory mutex works for one process. How do you do this across 50 Lambda instances?
  → Postgres: `UPDATE events SET taken = taken + 1 WHERE id=$1 AND taken < capacity RETURNING ...`
  (conditional update, row lock) or DynamoDB `UpdateItem` with a `ConditionExpression`.
- Thundering herd at ticket drop: queue (SQS) + virtual waiting room, idempotency keys so a
  retried request doesn't double-register.
- Accessors return copies — why? (Callers can't mutate internal state without the lock.)
