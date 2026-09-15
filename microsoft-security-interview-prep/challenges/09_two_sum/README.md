# 09 — Two Sum

**Theme:** classic array/hash-map warmup. Extremely likely as an opener (either a
standalone quick problem or the first 5 minutes of a round before it escalates) —
the interviewer is checking you reach for O(n), not O(n²), without being told to.

## Problem

```python
def two_sum(nums: List[int], target: int) -> List[int]:
    """Return the indices [i, j] (i != j) of the two numbers in nums that add
    up to target. Raise ValueError if no such pair exists."""
```

## Constraints

- Don't use the same element twice (two *different* indices), but the same *value*
  appearing at two different indices is fine (`[3, 3]`, target `6` → `[0, 1]`).
- Aim for **O(n) time / O(n) space** with a single pass and a hash map — the naive
  O(n²) double loop is the thing to explicitly avoid and be ready to explain why.
- Assume `nums` may contain negative numbers.

## Talking points

- Why a single pass works: for each number, check if its complement (`target - num`)
  has *already been seen*, then record the current number — this avoids matching a
  number with itself and avoids a second pass.
- What changes if the interviewer asks for "all pairs" instead of "the first pair" —
  now you need to handle duplicate values carefully so you don't double count.

## Run

```bash
pytest challenges/09_two_sum -v
```
