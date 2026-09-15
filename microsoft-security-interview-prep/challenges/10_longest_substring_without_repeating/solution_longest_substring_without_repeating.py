"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Brute force: check every substring for repeated characters, O(n^3) (or O(n^2)
   with a smarter repeat check) — state it, then motivate the better approach.
2. Sliding window: maintain a window `[left, right]` that's always repeat-free,
   expanding `right` one character at a time.
3. Track the *last seen index* of every character. When the character at `right` was
   seen before, that only matters if that earlier occurrence is still **inside** the
   current window (`last_seen[ch] >= left`) — if it's already outside the window, it's
   irrelevant and the window can keep growing.
4. When a same-window repeat is found, jump `left` to just past the earlier
   occurrence (`last_seen[ch] + 1`) — this is a jump, not an incremental shrink, which
   is what keeps the whole scan O(n) instead of O(n^2).
5. Track the best (max) window length seen after each expansion.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why check `last_seen[ch] >= left` instead of just 'have I seen this character
  before, anywhere'?" — without that check, you could incorrectly move `left`
  *backward* based on a stale occurrence that's already outside the current window,
  which would corrupt the window boundary.
- "What's the complexity?" — O(n) time (each index visited a bounded number of
  times), O(min(n, alphabet size)) space for the last-seen map.
- "How would you return the actual substring, not just its length?" — track the
  best window's start/end indices alongside `best` whenever it updates, then slice
  the string at the end using those indices.
- "Does this work for non-ASCII/Unicode input?" — yes, Python iterates strings by
  code point already, so no special handling is needed — good to state explicitly if
  asked rather than assuming it's an issue.
"""
from typing import Dict


def length_of_longest_substring(s: str) -> int:
    last_seen: Dict[str, int] = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)

    return best
