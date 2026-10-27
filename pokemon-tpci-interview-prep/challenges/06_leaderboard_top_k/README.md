# 06 — Championship Points leaderboard (top-K)

**Pattern:** hash map + heap / sort · **Domain:** Championship Points standings

Players earn Championship Points (CP) at League Cups, Regionals, Internationals. Keep running
totals and answer "top K players" queries.

## Task

```go
lb := NewLeaderboard()
lb.Award(playerID, points)    // points may be negative (penalty / correction)
lb.Total(playerID) int
lb.TopK(k) []Entry             // highest total first; ties by ID asc; k > n → all players
```

Aim for `TopK` in O(n log k) with a min-heap of size k (`container/heap`), then mention that
sorting everything (O(n log n)) is fine for small n and simpler.

## Talking points
- If `TopK` is hot and `Award` is rare, keep a sorted structure instead (skip list / Redis ZSET).
- Redis `ZINCRBY` + `ZREVRANGE` is the production answer for a real-time leaderboard.
- Idempotency: an event's results uploaded twice must not double-award — key awards by
  `(eventID, playerID)`.
