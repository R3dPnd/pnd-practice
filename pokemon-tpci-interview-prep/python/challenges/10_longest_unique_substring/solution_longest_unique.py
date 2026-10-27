"""Longest substring without repeating characters — reference solution (sliding window).

Big picture: keep a window s[left..i] that contains no duplicates.
  - Move the right edge `i` forward one character at a time.
  - If the new character already appears INSIDE the window, jump `left` to just past
    that earlier occurrence, so the window is duplicate-free again.
  - Track the biggest window seen.

Each index is visited once → O(n) time. The dict holds at most one entry per distinct
character.

Walkthrough on "abba":
  i=0 'a': window "a"    (left=0)  best=1
  i=1 'b': window "ab"   (left=0)  best=2
  i=2 'b': 'b' last seen at 1 → left=2, window "b"   best=2
  i=3 'a': 'a' last seen at 0 → left=max(2, 1)=2 (NOT 1!), window "ba"  best=2
"""


def longest_unique(s: str) -> int:
    last: dict[str, int] = {}   # character -> index where we LAST saw it
    best = left = 0             # best length so far; left edge of the current window

    for i, ch in enumerate(s):
        if ch in last:
            # We've seen ch before. If that earlier occurrence is inside the current
            # window, the window must start right after it.
            # Why max()? The earlier occurrence might be to the LEFT of the window already
            # (see 'a' at i=3 in the docstring walkthrough). Without max(), `left` would
            # move backwards and the window would contain a duplicate again.
            left = max(left, last[ch] + 1)

        # Remember the newest position of ch.
        last[ch] = i

        # The window s[left..i] is now duplicate-free; its length is i - left + 1.
        best = max(best, i - left + 1)

    return best
