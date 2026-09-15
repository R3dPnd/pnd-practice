# 10 — Longest Substring Without Repeating Characters

**Theme:** sliding window on a string. One of the most commonly asked medium problems
industry-wide, and a very common Microsoft phone/onsite question — tests whether you
reach for a window with a "last seen index" map instead of a brute-force O(n²)/O(n³)
scan.

## Problem

```python
def length_of_longest_substring(s: str) -> int:
    """Return the length of the longest substring of `s` with no repeated
    characters."""
```

## Examples

```
length_of_longest_substring("abcabcbb") -> 3   ("abc")
length_of_longest_substring("bbbbb")    -> 1   ("b")
length_of_longest_substring("pwwkew")   -> 3   ("wke")
length_of_longest_substring("")         -> 0
```

## Constraints

- **O(n) time.** Don't re-scan the window from scratch on every character — when you
  hit a repeat, jump the window's left edge directly to just past the previous
  occurrence (using a `char -> last index seen` map), not one step at a time.
- Careful with the classic off-by-one: the previous occurrence of the repeated char
  might be *before* the current window's left edge already (e.g. `"abba"`) — don't let
  the left edge move backwards.

## Run

```bash
pytest challenges/10_longest_substring_without_repeating -v
```
