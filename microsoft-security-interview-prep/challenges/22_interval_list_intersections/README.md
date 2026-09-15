# 22 — Interval List Intersections

**Theme:** two pointers over sorted intervals. One of the "extra reps" LeetCode names
flagged in the top-level `README.md`'s Field notes — a natural follow-up problem after
`11_merge_intervals` since it's the same domain (intervals) with a different pointer
technique.

## Problem

```python
def interval_intersections(
    first: List[List[int]], second: List[List[int]]
) -> List[List[int]]:
    """first and second are each lists of CLOSED intervals ([start, end], end
    inclusive), each individually sorted by start and pairwise disjoint (no two
    intervals within the same list overlap or touch). Return the intersection of
    the two interval sets, as a list of closed intervals sorted by start."""
```

## Examples

```
first  = [[0,2],[5,10],[13,23],[24,25]]
second = [[1,5],[8,12],[15,24],[25,26]]
interval_intersections(first, second)
    -> [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
```

## Constraints

- Either list may be empty -> result is `[]`.
- Intervals within each input list are already sorted and non-overlapping — you don't
  need to sort or merge within a single list first.
- A single point of overlap (e.g. `[5,10]` and `[8,12]` sharing just endpoint `10`... 
  actually `[5,10]` ends at 10 and next starts elsewhere) still counts — see the
  `[5,5]` and `[24,24]` results above, where two intervals only touch at one point.

## Hints

- Two pointers, one per list. At each step, compute the overlap of the two intervals
  currently pointed to: `lo = max(a.start, b.start)`, `hi = min(a.end, b.end)` — if
  `lo <= hi`, that's a valid intersection, append it.
- Advance whichever interval **ends first** — it can't possibly overlap with anything
  later in the other list, so it's fully "consumed." This is the same "advance the
  pointer that's exhausted" idea as merging two sorted lists.

## Run

```bash
pytest challenges/22_interval_list_intersections -v
```
