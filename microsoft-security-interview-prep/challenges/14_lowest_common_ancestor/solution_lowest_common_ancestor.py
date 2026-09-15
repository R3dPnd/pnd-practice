"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Base case: if the current node is `None`, or *is* one of the two targets (`p` or
   `q`), it's itself a valid candidate answer at this point — return it up the call
   stack unchanged.
2. Recurse into both the left and right subtrees, asking each "did you find p or q
   (or their LCA) somewhere in here?"
3. Key insight: if *both* the left and right recursive calls come back non-null, that
   means `p` and `q` were found in *different* subtrees of the current node — which,
   by definition, makes the current node exactly where their paths diverge, i.e. the
   LCA.
4. If only one side is non-null, the answer (either `p`/`q` itself, or their LCA)
   must live entirely within that one side — just propagate it up unchanged.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why does 'both sides non-null' guarantee this node is the LCA?" — because `p` and
  `q` can only end up on opposite sides of a node at exactly the point where their
  paths to the root split apart — that's the literal definition of lowest common
  ancestor.
- "What if the tree isn't guaranteed to contain both `p` and `q`?" — this solution
  assumes both exist in the tree; state that assumption explicitly. Handling "might
  not exist" would require a first pass to confirm both are actually present before
  trusting the result.
- "What's the complexity?" — O(n) time in the worst case (may visit every node), O(h)
  space for the recursion stack, where h is the tree's height.
- "How would this differ for a Binary *Search* Tree specifically?" — you could
  exploit BST ordering (compare `p.val`/`q.val` against `root.val` to decide whether
  to go left, right, or stop) instead of always recursing into both sides — O(h) time
  instead of O(n), a very common and expected follow-up for this exact problem.
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor(
    root: Optional[TreeNode], p: TreeNode, q: TreeNode
) -> Optional[TreeNode]:
    if root is None or root is p or root is q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left is not None and right is not None:
        return root
    return left if left is not None else right
