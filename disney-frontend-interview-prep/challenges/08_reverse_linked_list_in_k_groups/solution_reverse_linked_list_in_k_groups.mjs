export class ListNode {
  constructor(val, next = null) {
    this.val = val;
    this.next = next;
  }
}

export function fromArray(values) {
  const dummy = new ListNode(null);
  let tail = dummy;
  for (const value of values) {
    tail.next = new ListNode(value);
    tail = tail.next;
  }
  return dummy.next;
}

export function toArray(head) {
  const values = [];
  let node = head;
  while (node) {
    values.push(node.val);
    node = node.next;
  }
  return values;
}

export function reverseKGroup(head, k) {
  if (k <= 1) return head;

  // Check there are at least k nodes left; if not, leave this final stretch as-is.
  let node = head;
  let count = 0;
  while (node && count < k) {
    node = node.next;
    count += 1;
  }
  if (count < k) return head;

  // `node` is now the head of the remainder, already fully processed recursively.
  const newHead = reverseKGroup(node, k);

  // Reverse this group of k nodes, pointing the tail (the original `head`) at newHead.
  let prev = newHead;
  let curr = head;
  for (let i = 0; i < k; i += 1) {
    const next = curr.next;
    curr.next = prev;
    prev = curr;
    curr = next;
  }

  return prev;
}
