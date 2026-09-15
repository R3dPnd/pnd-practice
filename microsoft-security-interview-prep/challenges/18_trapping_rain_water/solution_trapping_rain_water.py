"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Core physical fact: the water level trapped *above* position i is bounded by
   `min(tallest bar to i's left, tallest bar to i's right) - height[i]` (never
   negative — a position can't trap water if it's already at or above that bound).
2. Brute force: for every position, scan left and scan right for the max — O(n^2).
   State this first.
3. Better: precompute `left_max[]` and `right_max[]` in two separate O(n) passes, then
   a third O(n) pass to sum up trapped water at each position — O(n) time, O(n) space.
4. Best — two pointers from both ends, each tracking a running max as they move
   inward: at every step, advance whichever side currently has the *smaller* running
   max. That side's position can be resolved immediately, because its own running max
   is already known to be the binding (smaller) constraint — regardless of what the
   far side's exact value turns out to be. This collapses the extra array away
   entirely: O(n) time, O(1) space.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why is it safe to resolve the side with the smaller running max immediately?" —
  because the trapped-water bound at that position is `min(left_max, right_max)`, and
  you already know your side's max is `<=` the other side's max — so your side's max
  *is* the binding constraint, no matter what's further along the other side.
- "Walk me through the complexity progression." — O(n^2) brute force → O(n) time /
  O(n) space with precomputed max arrays → O(n) time / O(1) space with two pointers.
  Narrating this progression live is usually worth more than jumping straight to the
  optimal answer.
- "What if heights can be negative?" — not physically meaningful for this problem;
  the stated constraints assume non-negative elevations.
- "How does this get harder in 2D ('Trapping Rain Water II')?" — you can no longer
  sweep from two flat ends; it requires a priority queue seeded from the boundary
  cells, processing inward by height — a good "I know roughly how much harder this
  gets" answer if asked to extend the problem.
"""
from typing import List


def trap(height: List[int]) -> int:
    if not height:
        return 0

    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    total = 0

    while left < right:
        if left_max <= right_max:
            left += 1
            left_max = max(left_max, height[left])
            total += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            total += right_max - height[right]

    return total
