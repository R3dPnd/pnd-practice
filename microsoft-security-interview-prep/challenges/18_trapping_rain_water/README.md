# 18 — Trapping Rain Water

**Theme:** array, two pointers. One of the specific "extra reps" LeetCode names
flagged in the top-level `README.md`'s Field notes — named directly by 2025
candidates alongside merge intervals and anagram problems.

## Problem

```python
def trap(height: List[int]) -> int:
    """height[i] is the elevation at position i (width-1 bars). Return the total
    volume of rainwater trapped between the bars after it rains."""
```

## Examples

```
trap([0,1,0,2,1,0,1,3,2,1,2,1]) -> 6
trap([4,2,0,3,2,5])             -> 9
trap([])                        -> 0
trap([1,2,3,4,5])               -> 0   (monotonic - nothing can pool)
```

## Constraints

- `height` values are non-negative integers.
- An empty or single-element input traps 0 water (nothing to hold it in).

## Hints

- Water trapped above position `i` is bounded by
  `min(max(height to the left of i), max(height to the right of i)) - height[i]`
  (never negative).
- The O(n) trick: two pointers from both ends, tracking `left_max`/`right_max` as you
  go. At each step, advance whichever side has the smaller max — you always know the
  true bound on that side already, even without having scanned the other side fully.
  A brute-force per-index left/right max scan is O(n²) and still correct — mention it
  first, then optimize, rather than jumping straight to two pointers without narrating
  the simpler version.

## Run

```bash
pytest challenges/18_trapping_rain_water -v
```
