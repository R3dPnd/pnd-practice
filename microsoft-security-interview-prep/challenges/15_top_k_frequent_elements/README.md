# 15 — Top K Frequent Elements

**Theme:** hash map + heap. Common "count things, then pick the top N" pattern —
shows up directly, and as a building block in log-analysis-style prompts.

## Problem

```python
def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """Return the k most frequent elements in nums, in any order.
    1 <= k <= number of distinct elements in nums."""
```

## Example

```
top_k_frequent([1,1,1,2,2,3], 2) -> [1, 2]   (order doesn't matter)
```

## Constraints

- Don't fully sort all distinct elements by frequency when you only need the top `k` —
  that's O(n log n) when O(n log k) (a size-`k` heap) is available. Sorting everything
  is an acceptable first pass to get something working, but be ready to name the
  better approach and why (or implement it if asked to optimize).
- Ties in frequency: any valid set of k elements achieving the correct set of frequency
  values is acceptable (tests check via frequency count, not exact element identity,
  where ties exist).

## Talking points

- `heapq.nlargest(k, counts, key=counts.get)` is O(n log k) internally and is a
  legitimate answer, but be ready to explain what it's doing under the hood (a min-heap
  of size k) rather than just citing the stdlib call — interviewers will ask.
- The O(n) bucket-sort alternative (bucket index = frequency, since frequency is
  bounded by `len(nums)`) is worth mentioning as the theoretically optimal approach.

## Run

```bash
pytest challenges/15_top_k_frequent_elements -v
```
