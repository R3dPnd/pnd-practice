# 07 — Schedule intervals (Python)

Full rules: [`../../../challenges/07_schedule_intervals/README.md`](../../../challenges/07_schedule_intervals/README.md).
Intervals are half-open `(start, end)` tuples.

```python
merge(intervals) -> list[tuple[int, int]]   # touching ones merge; sorted by start
has_conflict(intervals) -> bool             # touching is NOT a conflict
min_tables(intervals) -> int                # Meeting Rooms II
```
Don't mutate the input.
