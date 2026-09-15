# 13 — Linked List Basics (Reverse, Cycle Detection, Merge)

**Theme:** the three linked-list fundamentals interviewers chain together in a single
round ("now do it without extra space", "now what if it has a cycle"). Getting the
pointer manipulation right *without* a bug on the first try, out loud, is the actual
skill being tested here.

## Problem

A `ListNode` is provided:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

Implement three functions:

```python
def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse the list in place and return the new head. O(1) extra space —
    iterative pointer rewiring, not a new list / stack of values."""

def has_cycle(head: Optional[ListNode]) -> bool:
    """True if the list contains a cycle (Floyd's fast/slow pointer — O(1)
    space, don't use a seen-set for this one, that's the whole point of the
    exercise)."""

def merge_two_sorted_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """Merge two already-sorted linked lists into one sorted linked list by
    splicing existing nodes (no new node values, no converting to a Python
    list and re-building)."""
```

## Constraints / edge cases

- All three must handle an **empty list** (`None`) and a **single-node list**.
- `has_cycle` must run in **O(1) space** — that's the specific ask (a `seen` set would
  work but defeats the purpose of the exercise; use two pointers, one stepping 1 node
  at a time and one stepping 2).
- `merge_two_sorted_lists` should be stable-ish and not lose any nodes — the output
  length must equal the sum of the two input lengths (accounting for ties either way is
  fine).

## Run

```bash
pytest challenges/13_linked_list_basics -v
```
