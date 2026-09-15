"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at each piece:
- `reverse_linked_list`: classic three-pointer walk. At each node, save `next`
  before overwriting `current.next` to point *backward* at `prev` — you must save it
  first or you lose the rest of the list. Advance `prev`/`current` and repeat; the
  final `prev` (the old tail) becomes the new head.
- `has_cycle` (Floyd's tortoise and hare): a slow pointer moves one step, a fast
  pointer moves two. If there's a cycle, the fast pointer's extra speed means it's
  effectively "lapping" the slow one inside the loop, and the two are guaranteed to
  land on the same node eventually. If there's no cycle, the fast pointer simply
  reaches the end (`None`) first.
- `merge_two_sorted_lists`: use a dummy head node purely to avoid special-casing "is
  this the very first node of the result" — attach whichever of the two current
  nodes is smaller, advance that list, repeat; once one list is exhausted, attach
  whatever remains of the other (it's already sorted, no more comparisons needed).

COMMON INTERVIEWER FOLLOW-UPS:
- "Why does Floyd's algorithm actually work?" — inside a cycle, the fast pointer
  gains one node of relative distance on the slow pointer every step; a gap that
  shrinks by one each step must eventually hit zero (they meet) rather than the fast
  pointer somehow "jumping over" the slow one.
- "What's the space advantage over a hash-set-of-visited-nodes approach?" — Floyd's
  is O(1) space; a visited-set approach is O(n) space — this contrast is usually the
  actual point of asking for cycle detection specifically.
- "Why use a dummy head in the merge?" — it removes the need for an if/else to
  initialize the result list's very first node — a small but genuinely reusable
  linked-list pattern worth having memorized.
- "How would you reverse only a sublist, positions m to n?" — find the boundary
  nodes first (the node just before position m, and position m itself), apply the
  same three-pointer reversal only within that sub-range, then reconnect both ends
  back into the rest of the list.
"""
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None
    current = head
    while current is not None:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev


def has_cycle(head: Optional[ListNode]) -> bool:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def merge_two_sorted_lists(
    l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy

    while l1 is not None and l2 is not None:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 if l1 is not None else l2
    return dummy.next
