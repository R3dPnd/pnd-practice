"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Brute force: check every pair of indices, O(n^2) time, O(1) space. Always state
   this first out loud before optimizing — it shows you can identify the naive
   baseline before jumping to the trick.
2. Key insight: for each number `n`, the value you'd need to see *earlier* to make a
   valid pair is `target - n` (the "complement"). If you've already seen that
   complement, you have your answer immediately — no need to look ahead or restart.
3. One linear pass with a hash map from value -> index already seen. At each index,
   check whether the complement is already in the map *before* inserting the current
   value — this ordering is what correctly handles duplicates (see follow-ups).

COMMON INTERVIEWER FOLLOW-UPS:
- "Why check for the complement before inserting the current value?" — so a number
  never gets paired with itself when it appears only once. Duplicates like
  `nums=[3,3], target=6` still work correctly: the first `3` is inserted, then when
  the second `3` is processed its complement (`3`) is already in the map, pointing at
  a *different* index.
- "What if there are multiple valid pairs?" — this returns the first one found while
  scanning; clarify with the interviewer whether they want any valid pair, all pairs,
  or something more specific, rather than assuming.
- "What's the complexity?" — O(n) time, O(n) space — the classic time/space tradeoff
  versus the O(n^2)/O(1) brute force.
- "What if the array were already sorted?" — a two-pointer scan from both ends would
  solve it in O(n) time and O(1) extra space, no hash map needed — good to mention
  even though this problem doesn't guarantee sorted input.
"""
from typing import Dict, List


def two_sum(nums: List[int], target: int) -> List[int]:
    seen: Dict[int, int] = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    raise ValueError("no two numbers sum to target")
