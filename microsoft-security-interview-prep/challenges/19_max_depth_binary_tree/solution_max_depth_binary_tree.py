"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Base case: an empty tree (`None`) has depth 0 — there's nothing to descend into.
2. Recursive case: a tree's depth is `1` (counting the current node itself) plus
   whichever of its two subtrees is deeper.
3. This is a post-order traversal in disguise — you need the answer from *both*
   subtrees before you can compute the answer for the current node, so both
   recursive calls happen before the `+1 and max`.

COMMON INTERVIEWER FOLLOW-UPS:
- "What's the complexity?" — O(n) time (every node visited exactly once), O(h) space
  for the recursion call stack, where h is the tree's height — worst case O(n) for a
  completely skewed (linked-list-shaped) tree.
- "How would you do this iteratively instead of recursively?" — BFS level by level,
  incrementing a counter each time you finish a full level, until the queue empties —
  this also sidesteps recursion-depth limits on very deep/skewed trees.
- "Why might an interviewer ask this before a harder tree question?" — it's a fast,
  low-stakes way to confirm baseline comfort with tree recursion before raising the
  difficulty (diameter, right-side view, LCA) in the same round.
- "What happens on a very deep, skewed tree with this recursive version?" — it can
  hit Python's recursion limit — a real, practical downside of the recursive
  approach that the iterative BFS version doesn't share.
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
