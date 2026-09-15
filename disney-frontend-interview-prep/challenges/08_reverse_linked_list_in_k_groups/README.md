# 08 — Reverse Linked List In K-Groups

**Theme:** linked list, pointer manipulation. Directly reported real question:
**"linked list flip every two nodes"** (that's the `k = 2` case of this problem).

## Problem

```js
export class ListNode {
  constructor(val, next = null) { this.val = val; this.next = next; }
}

export function reverseKGroup(head, k) {
  /* reverses the nodes of the list k at a time, and returns the new head.
     If the number of remaining nodes at the end is not a multiple of k, that
     final partial group is left as-is (not reversed). */
}
```

Two small helpers are also provided/expected for testing convenience:

```js
export function fromArray(values) { /* build a list from a plain array */ }
export function toArray(head) { /* read a list back into a plain array */ }
```

## Constraints / edge cases to think about

- `k = 1` is a no-op — return the list unchanged.
- An empty list (`head = null`) returns `null`.
- A list shorter than `k` is left entirely unreversed.
- Aim for O(1) extra space (in-place pointer rewiring) rather than building a new list
  or using an array as scratch space — this is usually the actual follow-up question.
- Talk through the recursive vs. iterative tradeoff if asked: recursion is cleaner to
  write here but costs O(n/k) stack depth; a fully iterative version avoids that at the
  cost of more fiddly pointer bookkeeping.

## Why this matters for FE

Pure linked-list manipulation almost never appears in app code, but it's still a
reported real question here, and it's a fast way for an interviewer to check whether
you can hold multiple pointers in your head correctly without off-by-one errors — the
same skill that shows up when debugging, say, a custom doubly-linked-list-backed LRU
cache for a client-side data cache.

## Run

```bash
node --test challenges/08_reverse_linked_list_in_k_groups -v
```
