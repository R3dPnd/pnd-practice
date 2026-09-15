"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/20_diameter_binary_tree -v` to check yourself, or
`PRACTICE=0 pytest challenges/20_diameter_binary_tree -v` to see the
reference solution's tests pass instead.
"""
import re
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    diameter = 0
    def height(curr):
        nonlocal diameter
        if curr is None:
            return 0
        left = height(curr.left)
        right = height(curr.right)

        diameter = max(diameter, left + right)
        return 1 + max(left,right)
    height(root)
    return diameter
