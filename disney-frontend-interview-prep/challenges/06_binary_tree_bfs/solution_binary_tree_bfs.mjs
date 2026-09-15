export class TreeNode {
  constructor(val, left = null, right = null, next = null) {
    this.val = val;
    this.left = left;
    this.right = right;
    this.next = next;
  }
}

export function levelOrder(root) {
  if (!root) return [];

  const result = [];
  let queue = [root];

  while (queue.length > 0) {
    const level = [];
    const nextQueue = [];
    for (const node of queue) {
      level.push(node.val);
      if (node.left) nextQueue.push(node.left);
      if (node.right) nextQueue.push(node.right);
    }
    result.push(level);
    queue = nextQueue;
  }

  return result;
}

// Assumes a perfect binary tree. O(1) extra space: use the level we already
// connected to walk and connect the level below it, instead of a queue.
export function connect(root) {
  if (!root) return root;

  let leftmost = root;
  while (leftmost.left) {
    let head = leftmost;
    while (head) {
      head.left.next = head.right;
      if (head.next) head.right.next = head.next.left;
      head = head.next;
    }
    leftmost = leftmost.left;
  }

  return root;
}
