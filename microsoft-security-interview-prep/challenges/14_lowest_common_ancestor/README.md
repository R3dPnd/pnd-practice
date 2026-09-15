# 14 — Lowest Common Ancestor of a Binary Tree

**Theme:** tree recursion. One of the highest-signal "can you reason about recursive
return values" problems — a very common Microsoft-tagged question, both as a BST
variant (easier, use ordering) and the general binary tree variant (harder, no ordering
to exploit). This version is the general (non-BST) case.

## Problem

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """Return the lowest (deepest) node in the tree that has both p and q as
    descendants (a node is allowed to be a descendant of itself). p and q are
    guaranteed to exist somewhere in the tree rooted at root, and node values
    in the test tree are unique."""
```

## Constraints

- **This is a general binary tree, not a BST** — you cannot use value comparisons to
  decide which subtree to go into; you have to actually search both.
- `p` or `q` might **be** an ancestor of the other — in that case the answer is
  whichever one is the ancestor.
- Aim for a single O(n) traversal, not "find path to p, find path to q, compare paths"
  with redundant re-traversal (that also works and is a fine thing to mention as a
  simpler-but-slower alternative).

## Hints

- Recursive idea: `lca(node)` returns `node` if `node` is `p` or `q`; otherwise it
  recurses into both children. If **both** sides return non-`None`, `node` itself is
  the LCA (p and q are in different subtrees). If only one side returns non-`None`,
  propagate that result up unchanged.

## Run

```bash
pytest challenges/14_lowest_common_ancestor -v
```
