# 19 — Maximum Depth of Binary Tree

**Theme:** tree recursion. One of the "extra reps" LeetCode names flagged in the
top-level `README.md`'s Field notes — usually a fast warm-up before a harder tree
question in the same round (e.g. `20_diameter_binary_tree`, `14_lowest_common_ancestor`).

## Problem

```python
def max_depth(root: Optional[TreeNode]) -> int:
    """Return the number of nodes along the longest path from root to a leaf
    (an empty tree has depth 0; a single node has depth 1)."""
```

`TreeNode` is provided:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        ...
```

## Constraints

- `max_depth(None) == 0`.
- A single-node tree has depth 1.
- Works for unbalanced trees (depth is the *longest* path, not any particular path).

## Hints

- One line of real logic: `1 + max(max_depth(root.left), max_depth(root.right))`, with
  the base case `if root is None: return 0`. If you find yourself writing more than
  that, you're probably overcomplicating it.
- Worth mentioning out loud: this is O(n) time, O(h) space for the call stack (h =
  tree height), and an iterative BFS level-count is an easy alternative if asked to
  avoid recursion.

## Run

```bash
pytest challenges/19_max_depth_binary_tree -v
```
