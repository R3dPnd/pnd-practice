"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Brute-force recursion (try every possible first-word split, recurse on the rest)
   works but re-solves the same subproblems exponentially — e.g. the substring
   starting at index 5 might get checked many times across different recursive
   branches. State this and the fix (memoization) explicitly, even though the final
   code below is written bottom-up rather than top-down-with-a-cache.
2. Define `dp[i]` = "can the prefix `s[:i]` be fully segmented into dictionary
   words." `dp[0] = True` — the empty prefix is trivially breakable (base case).
3. For each end position `i`, try every possible position `j < i` for where the
   *last* word in the segmentation could start: if `dp[j]` is already known True
   (everything before `j` is breakable) and `s[j:i]` is itself a dictionary word,
   then `dp[i]` is True too — no need to check further split points once one works.
4. The answer is `dp[n]` — is the *entire* string breakable.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why not just brute-force recursion?" — it re-solves overlapping subproblems (the
  same prefix gets re-checked from multiple recursive paths), causing exponential
  blowup in the worst case; bottom-up DP (or memoized recursion) solves each
  subproblem exactly once.
- "What's the complexity?" — O(n^2) for the nested loop over string positions
  (substring slicing/hashing cost is subsumed into that, since slices here are
  bounded by n); O(n) space for the `dp` array.
- "How would you return the actual word segmentation, not just True/False?" — track,
  at each `dp[i] = True`, which `j` produced it (a parent-pointer array), then
  backtrack from `n` to `0` to reconstruct the list of words.
- "How would you optimize for a very large dictionary?" — build a Trie of the
  dictionary words so you're checking one character at a time as you extend `i`,
  instead of re-hashing/re-checking every candidate substring independently against
  a big set.
"""
from typing import List


def word_break(s: str, word_dict: List[str]) -> bool:
    word_set = set(word_dict)
    n = len(s)

    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]
