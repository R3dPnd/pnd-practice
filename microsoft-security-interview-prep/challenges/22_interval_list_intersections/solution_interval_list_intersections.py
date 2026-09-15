"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Both input lists are already sorted and internally non-overlapping — that
   precondition is what makes a single linear two-pointer scan possible (no sorting
   needed here, unlike `11_merge_intervals`).
2. At each step, the two pointers point at one interval from each list. Their overlap
   (if any) is `[max(starts), min(ends)]` — this is only a *real* interval if
   `lo <= hi`; otherwise the two current intervals simply don't overlap at all.
3. Key insight for advancing: whichever of the two current intervals **ends first**
   cannot possibly overlap with anything *later* in the other list (since that list
   is sorted and disjoint, everything later starts even further to the right) — so
   it's safe to advance only that one pointer and never reconsider that interval again.
4. Repeat until either list is exhausted.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why advance the pointer whose interval ends first?" — once an interval's own list
  guarantees nothing *after* it starts any earlier than where it ends, that interval
  has no remaining overlaps left to contribute — it's fully "used up" and can be
  retired.
- "What's the complexity?" — O(n + m), where n and m are the two lists' lengths — a
  single linear merge-style pass, with no sorting step needed given the stated
  preconditions.
- "How does this differ from `11_merge_intervals`?" — that problem merges overlapping
  intervals *within one list*; this finds the intersection *between two separate,
  already-sorted lists* — a different operation from the same "sorted intervals +
  linear scan" family of techniques.
- "What if the inputs aren't actually pre-sorted/disjoint?" — the algorithm assumes
  that precondition (stated in the README); violating it would require sorting
  and/or merging each list first, adding an O(n log n) step before this scan.
"""
from typing import List


def interval_intersections(
    first: List[List[int]], second: List[List[int]]
) -> List[List[int]]:
    result: List[List[int]] = []
    i, j = 0, 0

    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])
        hi = min(first[i][1], second[j][1])
        if lo <= hi:
            result.append([lo, hi])

        if first[i][1] < second[j][1]:
            i += 1
        else:
            j += 1

    return result
