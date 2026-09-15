# 17 — Group Anagrams

**Theme:** array + hash map. One of the specific "extra reps" LeetCode names flagged
in the top-level `README.md`'s Field notes as reported in real 2025 Microsoft
write-ups.

## Problem

```python
def group_anagrams(strs: List[str]) -> List[List[str]]:
    """Group strings that are anagrams of each other. Return the groups in any
    order; within a group, strings may be in any order."""
```

## Examples

```
group_anagrams(["eat","tea","tan","ate","nat","bat"])
    -> [["eat","tea","ate"], ["tan","nat"], ["bat"]]   (order of groups/within groups doesn't matter)

group_anagrams([""]) -> [[""]]
group_anagrams(["a"]) -> [["a"]]
```

## Constraints

- Strings contain only lowercase English letters.
- An empty list returns `[]`.
- Every input string must appear in exactly one output group.

## Hints

- The canonical key for "these two strings are anagrams" is either the sorted
  character tuple (`tuple(sorted(s))`) or a 26-length character-count tuple — the
  sorted version is simpler to write correctly under time pressure, the count version
  is O(n) per string instead of O(n log n) if asked for the follow-up optimization.
- One pass, one hash map from key -> list of strings. Don't do pairwise comparisons.

## Run

```bash
pytest challenges/17_group_anagrams -v
```
