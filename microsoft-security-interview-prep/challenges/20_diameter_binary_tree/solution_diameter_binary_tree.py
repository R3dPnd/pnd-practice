"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Naive idea: for every node, compute the height of its left and right subtrees
   separately and add them, tracking the max over all nodes. This is correct but
   O(n^2) worst case, because computing height from scratch at every node re-walks
   subtrees that were already walked by an ancestor's height computation.
2. The fix: compute height and diameter together in a **single** post-order
   traversal. The `height` helper does what `19_max_depth_binary_tree` does, but adds
   one side effect: at every node, `left_height + right_height` is a *candidate*
   diameter (the longest path that passes through this specific node), so update a
   running `diameter` (via `nonlocal`) as you go.
3. This works because diameter is measured in edges, and any path between two nodes
   has some single highest point where it "turns" from going down-left to down-right
   (or is entirely one-sided) — checking `left_height + right_height` at *every* node
   guarantees you check every possible turning point exactly once.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why compute height and diameter together instead of two separate traversals?" —
  two separate traversals (recomputing height fresh at every node to check its
  diameter) is O(n^2) in the worst case; folding the diameter check into the same
  post-order pass that already computes height is O(n).
- "Why check diameter at every node, not just the root?" — the longest path in the
  tree might be entirely contained within one subtree that never funnels through the
  true root at all — see this challenge's `test_diameter_not_through_root` test case.
- "Is diameter measured in nodes or edges?" — edges, per the standard definition used
  here — worth clarifying explicitly with the interviewer, since a node-count answer
  would be off by exactly one.
- "How does this relate to `19_max_depth_binary_tree`?" — the `height` helper here
  *is* `max_depth`'s logic, extended with a side effect that tracks the best diameter
  seen so far — recognizing and naming that relationship out loud is a good signal.
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    diameter = 0

    def height(node: Optional[TreeNode]) -> int:
        nonlocal diameter
        if node is None:
            return 0
        left_height = height(node.left)
        right_height = height(node.right)
        diameter = max(diameter, left_height + right_height)
        return 1 + max(left_height, right_height)

    height(root)
    return diameter
