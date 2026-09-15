# 20 — Diameter of Binary Tree

**Theme:** tree recursion, "compute two things at once." One of the "extra reps"
LeetCode names flagged in the top-level `README.md`'s Field notes.

## Problem

```python
def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """The diameter is the length (in EDGES, not node count) of the longest path
    between any two nodes in the tree. The path does not have to pass through
    the root."""
```

`TreeNode` is provided (same shape as `19_max_depth_binary_tree`).

## Examples

```
      1
     / \
    2   3
   / \
  4   5

diameter_of_binary_tree(root) -> 3   (path 4 -> 2 -> 1 -> 3, or 4 -> 2 -> 5, both 3 edges — the answer is the longest, 4-2-1-3)
```

## Constraints

- `diameter_of_binary_tree(None) == 0`.
- Single node -> `0` (no path at all).
- **The longest path does not have to pass through the root** — this is the actual
  trap in this problem. A tree that's "bushy" deep in one subtree but shallow near the
  root can have its diameter entirely inside that one subtree.

## Hints

- Don't compute height and diameter as two separate tree walks (that's O(n²) in the
  worst case, recomputing height repeatedly). Compute both in **one** post-order
  traversal: a helper returns the height of a subtree, and updates a running "best
  diameter seen so far" as a side effect (`left_height + right_height` at every node is
  a *candidate* diameter, since that's the longest path passing through that node).
- This is the same "compute a value bottom-up while also tracking a global best"
  pattern as `14_lowest_common_ancestor`'s recursion — recognize the shape.

## Run

```bash
pytest challenges/20_diameter_binary_tree -v
```
