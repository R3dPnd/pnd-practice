"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/21_binary_tree_right_side_view -v` to check yourself, or
`PRACTICE=0 pytest challenges/21_binary_tree_right_side_view -v` to see the
reference solution's tests pass instead.
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def right_side_view(root: Optional[TreeNode]) -> List[int]:
    raise NotImplementedError
