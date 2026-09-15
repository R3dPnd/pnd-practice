import { test } from "node:test";
import assert from "node:assert/strict";
import { loadImpl } from "../_lib/load-impl.mjs";

const { TreeNode, levelOrder, connect } = await loadImpl(import.meta.url, "binary_tree_bfs");

function buildPerfectTree() {
  //         1
  //       /   \
  //      2     3
  //     / \   / \
  //    4   5 6   7
  const n4 = new TreeNode(4);
  const n5 = new TreeNode(5);
  const n6 = new TreeNode(6);
  const n7 = new TreeNode(7);
  const n2 = new TreeNode(2, n4, n5);
  const n3 = new TreeNode(3, n6, n7);
  return new TreeNode(1, n2, n3);
}

test("levelOrder returns [] for an empty tree", () => {
  assert.deepEqual(levelOrder(null), []);
});

test("levelOrder returns one level for a single node", () => {
  assert.deepEqual(levelOrder(new TreeNode(1)), [[1]]);
});

test("levelOrder returns each level top-to-bottom, left-to-right", () => {
  const root = buildPerfectTree();
  assert.deepEqual(levelOrder(root), [[1], [2, 3], [4, 5, 6, 7]]);
});

test("levelOrder handles an unbalanced tree", () => {
  const root = new TreeNode(1, new TreeNode(2, new TreeNode(3)), null);
  assert.deepEqual(levelOrder(root), [[1], [2], [3]]);
});

test("connect links every node to its right neighbor at the same level", () => {
  const root = buildPerfectTree();
  connect(root);

  assert.equal(root.next, null);
  assert.equal(root.left.next, root.right);
  assert.equal(root.right.next, null);
  assert.equal(root.left.left.next, root.left.right);
  assert.equal(root.left.right.next, root.right.left);
  assert.equal(root.right.left.next, root.right.right);
  assert.equal(root.right.right.next, null);
});

test("connect returns the (possibly null) root", () => {
  assert.equal(connect(null), null);
  const single = new TreeNode(1);
  assert.equal(connect(single), single);
  assert.equal(single.next, null);
});
