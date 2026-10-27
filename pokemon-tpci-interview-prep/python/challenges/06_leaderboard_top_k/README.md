# 06 — Championship Points leaderboard (Python)

Talking points: [`../../../challenges/06_leaderboard_top_k/README.md`](../../../challenges/06_leaderboard_top_k/README.md).

```python
lb = Leaderboard()
lb.award(player_id, points)        # may be negative
lb.total(player_id) -> int         # 0 if unknown
lb.top_k(k) -> list[tuple[str, int]]  # highest first; ties by id asc; k <= 0 → []
```
Aim for O(n log k) with `heapq` (hint: `heapq.nsmallest(k, items, key=lambda kv: (-kv[1], kv[0]))`
is a one-liner — be ready to explain what it does under the hood, or write the size-k heap by hand).
