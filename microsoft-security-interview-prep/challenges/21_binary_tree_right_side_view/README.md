# 21 — Binary Tree Right Side View

**Theme:** tree, level-order/BFS. One of the "extra reps" LeetCode names flagged in
the top-level `README.md`'s Field notes — a good pairing with `12_number_of_islands`
since both are BFS, just over different shapes.

## Problem

```python
def right_side_view(root: Optional[TreeNode]) -> List[int]:
    """Imagine standing to the right of the tree. Return the values of the nodes
    you can see, ordered from top to bottom (i.e. the rightmost node at each
    level, top to bottom)."""
```

## Examples

```
     1
    / \
   2   3
    \   \
     5   4

right_side_view(root) -> [1, 3, 4]
```

## Constraints / the actual trap in this problem

- `right_side_view(None) == []`.
- **The rightmost *visible* node at a level is not always the deepest-right node
  structurally** — if the right child is missing but the left child (or its
  descendant) exists at that depth, that left-side node is what's visible from the
  right, because there's nothing to its right blocking the view. See the second test
  case below.

## Hints

- BFS level-by-level, take the **last** node processed at each level (if you enqueue
  left before right, the last node in each level's queue is the rightmost one at that
  level) — this naturally handles the "missing right child" case correctly, since
  whatever ends up last in that level's queue by definition has nothing to its right.
- A DFS (right subtree first, record the first node seen at each new depth) also
  works and uses less extra space — mention it as an alternative if asked to optimize
  space from O(w) (widest level) to O(h) (height).

## Run

```bash
pytest challenges/21_binary_tree_right_side_view -v
```
