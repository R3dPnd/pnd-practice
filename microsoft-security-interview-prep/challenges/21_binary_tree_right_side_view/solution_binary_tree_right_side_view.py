"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Reframe "what's visible from the right" as "the last node processed at each BFS
   level," if children are always enqueued left-before-right.
2. BFS level by level (the same level-by-level structure as a standard level-order
   traversal): process the entire current level's queue, but only keep the *last*
   node's value from each level — that's `queue[-1].val`.
3. The subtlety this handles correctly "for free": if a node's right child is
   missing but its left child (or a descendant of it) exists at that depth, that
   left-side node ends up being the last one enqueued for that level anyway — because
   whatever there *is* at that depth with nothing after it in enqueue order is, by
   construction, the rightmost *visible* thing, whether or not it came from a
   structurally "right" branch.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why does taking the last queue entry work even when a right child is missing?" —
  because enqueue order (left before right, level by level) guarantees the last node
  processed at any level is whatever has nothing to its right at that depth — exactly
  the definition of "visible from the right," regardless of which branch it came from.
- "What's the complexity?" — O(n) time and space; BFS visits every node once, and the
  queue can grow up to the width of the widest level.
- "How would you solve this with DFS instead, and why might that be better?" —
  traverse right subtree before left, and record the first node encountered at each
  new depth (a `len(result) == depth` check). This uses O(h) extra space (the
  recursion stack) instead of O(w) (the widest level's queue) — a meaningful win on a
  very "bushy," shallow-but-wide tree.
- "How does this relate to `19_max_depth_binary_tree` and `20_diameter_binary_tree`?"
  — all three are tree traversals computing a different aggregate property (depth,
  diameter, per-level visibility) over the same basic tree-walk shape — recognizing
  "one traversal pattern, different bookkeeping" across all three is a strong signal.
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def right_side_view(root: Optional[TreeNode]) -> List[int]:
    if root is None:
        return []

    result: List[int] = []
    queue = [root]

    while queue:
        result.append(queue[-1].val)
        next_queue = []
        for node in queue:
            if node.left:
                next_queue.append(node.left)
            if node.right:
                next_queue.append(node.right)
        queue = next_queue

    return result
