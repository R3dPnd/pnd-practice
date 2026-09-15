# 16 — Word Break

**Theme:** dynamic programming on strings. If a coding round goes DP, this is one of
the most common shapes: "can this be built by combining pieces from a fixed set" —
same idea as coin-change / combination-sum, just on substrings instead of numbers.

## Problem

```python
def word_break(s: str, word_dict: List[str]) -> bool:
    """Return True if s can be segmented into a space-separated sequence of
    one or more words, each of which appears in word_dict. Words in
    word_dict may be reused any number of times."""
```

## Examples

```
word_break("leetcode", ["leet", "code"])          -> True   ("leet" + "code")
word_break("applepenapple", ["apple", "pen"])      -> True   ("apple" + "pen" + "apple")
word_break("catsandog", ["cats","dog","sand","and","cat"]) -> False
```

## Constraints

- Aim for **O(n²)** DP: `dp[i]` = "can `s[:i]` be segmented?", with
  `dp[i] = any(dp[j] and s[j:i] in word_set for j in range(i))`. Naive recursion without
  memoization is exponential — re-solving the same suffix repeatedly — so either
  memoize the recursion or build the DP table bottom-up.
- Use a **set** for `word_dict` lookups, not a list — an `in` check against a list is
  O(len(word_dict)) each time, which turns your O(n²) DP into O(n² · m).
- `word_dict` can be empty (→ `False` unless `s` is also empty, treat empty `s` as
  trivially `True` if you want to special-case it, tests only exercise non-empty `s`).

## Run

```bash
pytest challenges/16_word_break -v
```
