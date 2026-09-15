"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/10_longest_substring_without_repeating -v` to check
yourself, or `PRACTICE=0 pytest challenges/10_longest_substring_without_repeating -v`
to see the reference solution's tests pass instead.
"""


def length_of_longest_substring(s: str) -> int:
    max_len = 0

    l = 0
    seen_map = {}

    for i in range(len(s)):
        curr = s[i]
        if curr in seen_map:
            l = max(l, seen_map[curr] + 1)
        seen_map[curr] = i
        max_len = max(max_len, i - l + 1)

    return max_len
