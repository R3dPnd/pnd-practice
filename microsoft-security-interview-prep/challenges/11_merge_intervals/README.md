# 11 — Merge Intervals

**Theme:** sort + linear sweep. Extremely common — shows up directly, and also as a
sub-step inside bigger scheduling/calendar-style problems.

## Problem

```python
def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """Given a list of [start, end] intervals (end is exclusive-or-inclusive,
    your call, just be consistent — this version treats touching intervals as
    overlapping, e.g. [1,4] and [4,5] merge into [1,5]), merge all overlapping
    intervals and return the merged list, sorted by start."""
```

## Examples

```
merge_intervals([[1,3],[2,6],[8,10],[15,18]]) -> [[1,6],[8,10],[15,18]]
merge_intervals([[1,4],[4,5]])                -> [[1,5]]
merge_intervals([])                           -> []
```

## Constraints

- Input is **not** guaranteed sorted — sort first (by start), then do a single linear
  pass. Don't do an O(n²) pairwise-compare-and-merge-repeat.
- Don't mutate the caller's input list/sub-lists.
- `end < start` inputs won't be tested — assume each interval is well-formed.

## Talking points

- Why sorting first turns this into O(n log n) + O(n) instead of something worse.
- How you'd extend it to "insert a new interval into an already-sorted, already-merged
  list" (a very common LeetCode follow-up) — you can binary-search for the insertion
  point instead of re-sorting everything.

## Run

```bash
pytest challenges/11_merge_intervals -v
```
