"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Overlap between arbitrary pairs is expensive to detect directly (comparing every
   pair is O(n^2)) — but if intervals are ordered by start, overlap can only ever
   happen between an interval and its *immediate* neighbor in the merged-so-far
   result, never something further back. That's what makes a single linear pass
   possible.
2. Sort by start first: O(n log n).
3. One pass: keep a running "last merged interval" in the output. If the next
   interval's start is `<=` the last one's end, they overlap (or touch) — extend the
   last interval's end. Otherwise, the next interval starts a brand-new group.
4. Use `max(last[1], end)`, not just `end`, when extending — a later interval can be
   fully *contained* inside an earlier, wider one (e.g. `[1,10]` then `[2,3]`), and
   naively overwriting the end would incorrectly shrink the merged interval.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why sort first?" — without sorting, detecting all overlaps requires comparing
  every pair, O(n^2); sorting turns it into one O(n) linear scan afterward, for
  O(n log n) total.
- "Why `max(last[1], end)` instead of just `end`?" — to correctly handle a smaller
  interval fully nested inside a larger already-merged one, which would otherwise
  silently shrink the output.
- Follow-up: "insert a new interval into an already-sorted, already-merged list" —
  binary search for the correct insertion point instead of re-sorting the whole list
  from scratch, since the list is already known to be sorted and merged.
- "What's the complexity?" — O(n log n), dominated by the sort; the merge pass
  itself is a single O(n) linear scan.
"""
from typing import List


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda iv: iv[0])
    merged: List[List[int]] = [list(sorted_intervals[0])]

    for start, end in sorted_intervals[1:]:
        last = merged[-1]
        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return merged
