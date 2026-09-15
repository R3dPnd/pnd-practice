"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/17_group_anagrams -v` to check yourself, or
`PRACTICE=0 pytest challenges/17_group_anagrams -v` to see the reference
solution's tests pass instead.
"""
from typing import List


def group_anagrams(strs: List[str]) -> List[List[str]]:
    dict = {}
    for str in strs:
        key = tuple(sorted(str))
        if key in dict:
            dict[key].append(str)
        else:
            dict[key] = [str]
    return dict.values
