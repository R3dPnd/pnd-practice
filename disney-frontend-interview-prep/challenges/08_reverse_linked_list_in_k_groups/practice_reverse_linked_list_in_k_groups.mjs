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
  throw new Error("not implemented");
}
