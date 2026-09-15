"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Key insight: two strings are anagrams of each other if and only if they contain
   exactly the same multiset of characters. Sorting a string's characters produces a
   canonical form that's *identical* for every anagram in a group, and different for
   any string that isn't an anagram of them.
2. One linear pass: compute each string's sorted-character key, and append it to a
   dict bucket keyed by that value.
3. Return the dict's values as the groups — the problem doesn't require any
   particular order for groups or within a group.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why `tuple(sorted(s))` instead of just `sorted(s)` as the key?" — `sorted()`
  returns a list, and lists aren't hashable in Python — a dict key needs something
  immutable, so it's wrapped in a tuple (or you could use `"".join(sorted(s))` as a
  string key instead, equally valid).
- "What's the complexity?" — O(n * k log k), where n = number of strings and k = max
  string length, dominated by sorting each string.
- "How would you optimize if strings are very long?" — use a fixed-length
  character-count tuple (26 counts for lowercase English letters) as the key instead
  of sorting — O(k) per string instead of O(k log k), trading a slightly more complex
  key construction for better asymptotic behavior.
- "What about Unicode or mixed-case input?" — sorting still produces a valid
  canonical key regardless of alphabet, as long as equal-content strings sort
  identically; case-sensitivity would need explicit normalization (e.g. `.lower()`)
  first if "Eat" and "eat" should be treated as anagrams.
"""
from collections import defaultdict
from typing import Dict, List, Tuple


def group_anagrams(strs: List[str]) -> List[List[str]]:
    groups: Dict[Tuple[str, ...], List[str]] = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())
