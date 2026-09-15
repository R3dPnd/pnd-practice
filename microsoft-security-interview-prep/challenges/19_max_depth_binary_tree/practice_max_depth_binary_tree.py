"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/19_max_depth_binary_tree -v` to check yourself, or
`PRACTICE=0 pytest challenges/19_max_depth_binary_tree -v` to see the
reference solution's tests pass instead.
"""
import re
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + max(max_depth(root.right), max_depth(root.left))

