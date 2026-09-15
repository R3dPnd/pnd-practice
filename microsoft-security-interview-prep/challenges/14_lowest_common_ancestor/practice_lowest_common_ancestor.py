"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/14_lowest_common_ancestor -v` to check yourself, or
`PRACTICE=0 pytest challenges/14_lowest_common_ancestor -v` to see the
reference solution's tests pass instead.
"""
import re
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor(
    root: Optional[TreeNode], p: TreeNode, q: TreeNode
) -> Optional[TreeNode]:
    def find_path(n, curr, path):
        if not curr:
            return False
        path.append(curr)
        if curr.val == n.val:
            return True
        if find_path(n, curr.left, path) or find_path(n, curr.right, path):
            return True
        path.pop()
        return False
    p_path = []
    q_path = []
    if find_path(p, root, p_path) and find_path(q, root, q_path):
        print(f"{p_path}:{q_path}")
        for i in range(min(len(p_path), len(q_path))):
            if p_path[i].val != q_path[i].val:
                return p_path[i-1]
        return p_path[-1]
    else: 
        print("Error")