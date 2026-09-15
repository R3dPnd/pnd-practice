"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. First step regardless of approach: count frequency of every element
   (`collections.Counter`) — O(n).
2. Naive-but-reasonable: sort all distinct elements by frequency and take the top k —
   O(d log d) where d = number of distinct elements. Perfectly fine to state as your
   first working answer.
3. The O(n) trick — bucket sort by frequency: since a frequency can only range from 1
   to n (you can't appear more times than the array's length), create n+1 buckets
   indexed by frequency, and drop each distinct value into the bucket matching its
   count.
4. Walk the buckets from highest frequency down to 1, collecting values into the
   result until you have k of them — this reaches k without ever fully sorting
   anything.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why not just use a heap (`heapq.nlargest`)?" — a heap-based approach is O(n log k),
  which is genuinely worse asymptotically than bucket sort's O(n) here, but is
  simpler to write correctly under time pressure. Mention both; lead with the heap as
  the fast-to-write answer, then bucket sort as "here's how to actually get O(n)."
- "Why does bounding the frequency range make bucket sort possible at all?" — because
  you know the full range of possible keys (1..n) in advance — that's exactly the
  precondition that lets bucket/counting sort beat the O(n log n) lower bound that
  applies to general comparison-based sorting.
- "What if k is larger than the number of distinct elements?" — this solution
  validates that and raises `ValueError` — call out that you considered the
  degenerate input rather than silently returning a short list.
- "What's the overall complexity?" — O(n) time and space, dominated by building the
  counter and the bucket array, both linear in the input size.
"""
from collections import Counter
from typing import List


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    if k < 1:
        raise ValueError("k must be >= 1")

    counts = Counter(nums)
    if k > len(counts):
        raise ValueError("k exceeds number of distinct elements")

    # Bucket sort by frequency: O(n) instead of sorting all distinct elements.
    buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]
    for value, freq in counts.items():
        buckets[freq].append(value)

    result: List[int] = []
    for freq in range(len(buckets) - 1, 0, -1):
        for value in buckets[freq]:
            result.append(value)
            if len(result) == k:
                return result
    return result
