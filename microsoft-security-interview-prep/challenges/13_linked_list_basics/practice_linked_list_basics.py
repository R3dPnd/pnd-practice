"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/13_linked_list_basics -v` to check yourself, or
`PRACTICE=0 pytest challenges/13_linked_list_basics -v` to see the reference
solution's tests pass instead.
"""
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    fake_head = ListNode()
    fake_head.next = head
    queue = []
    while fake_head.next is not None:
        queue.append(fake_head.next)
        fake_head.next = fake_head.next.next
    while queue:
        node = queue.pop()
        node.next = fake_head.next
        fake_head.next = node
    return fake_head.next


def has_cycle(head: Optional[ListNode]) -> bool:
    raise NotImplementedError


def merge_two_sorted_lists(
    l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    raise NotImplementedError
