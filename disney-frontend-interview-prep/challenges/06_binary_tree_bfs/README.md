# 06 — Binary Tree BFS

**Theme:** tree, level-order traversal / BFS. Directly reported real question:
**"BFS of a binary tree."** `connect` matches Disney's LeetCode-tagged **"Populating
Next Right Pointers in Each Node."**

## Problem

```js
export class TreeNode {
  constructor(val, left = null, right = null, next = null) { ... }
}

export function levelOrder(root) {
  /* returns an array of arrays: each inner array is one level's values,
     top to bottom, left to right */
}

export function connect(root) {
  /* for a PERFECT binary tree (every level fully populated), sets each node's
     `.next` pointer to the node immediately to its right at the same level
     (or null for the rightmost node in a level). Returns root. */
}
```

## Constraints / edge cases to think about

- `levelOrder(null)` returns `[]`.
- `connect` assumes a perfect binary tree (this is the standard LeetCode 116 framing —
  say so out loud if asked, and mention that a general/incomplete tree needs an extra
  step to find each level's "next" via BFS instead of via already-set `.next` pointers,
  which is LeetCode 117's follow-up).
- Aim for O(1) extra space on `connect` beyond the tree itself, using already-connected
  levels to find each next level's connections (no queue) — that's the actual point of
  the problem versus just doing a levelOrder-style BFS and connecting queue neighbors.

## Why this matters for FE

Binary trees don't come up directly in app code much, but BFS/level-order traversal is
the exact same shape as walking a DOM tree, a component tree, or a nested comments/
category tree breadth-first (e.g., rendering breadcrumbs, computing tree depth for a
virtualized tree view). Interviewers use tree BFS as a clean, fast way to check pointer/
reference discipline without needing a UI at all.

## Run

```bash
node --test challenges/06_binary_tree_bfs -v
```
