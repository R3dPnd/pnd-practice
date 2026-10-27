"""LRU cache — reference solution (hash map + doubly linked list).

Big picture:
  - A dict maps key -> node, so we can FIND any entry in O(1).
  - A doubly linked list keeps entries in recency order, so we can MOVE any node to the
    front, or REMOVE the last node, in O(1) (just re-point a few pointers).
  - Front of the list (right after `_head`) = most recently used.
    Back of the list (right before `_tail`) = least recently used → evicted first.

Two "sentinel" (dummy) nodes, `_head` and `_tail`, are always present. Because of them,
every real node always has a real prev and next, so unlink/insert never needs special
cases for "empty list" or "this is the first node".

    _head <-> [MRU] <-> ... <-> [LRU] <-> _tail

Shortcut version: collections.OrderedDict does all of this for you
(move_to_end(key, last=False) and popitem(last=True)). Know both.
"""
from typing import Any, Hashable


class _Node:
    # __slots__ stops Python from giving each node a per-instance __dict__.
    # It's a memory optimization, not a correctness requirement.
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key, self.value = key, value
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCache:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._items: dict[Hashable, _Node] = {}
        # Create the two sentinels and link them to each other: an "empty" list.
        self._head, self._tail = _Node(), _Node()
        self._head.next, self._tail.prev = self._tail, self._head

    def _unlink(self, node: _Node) -> None:
        # Splice `node` out by making its neighbors point at each other:
        #   before: prev <-> node <-> next
        #   after:  prev <-> next
        # (node's own pointers are left dangling; they're overwritten on the next insert.)
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node: _Node) -> None:
        # Insert `node` right after _head (the most-recently-used position):
        #   before: _head <-> first
        #   after:  _head <-> node <-> first
        node.prev, node.next = self._head, self._head.next   # node points at its new neighbors
        self._head.next.prev = node                          # old first now points back at node
        self._head.next = node                               # head now points forward to node

    def get(self, key: Hashable) -> Any | None:
        node = self._items.get(key)
        if node is None:
            return None        # cache miss
        # Cache hit: reading counts as "using", so move the node to the front.
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key: Hashable, value: Any) -> None:
        # A cache with no room can't store anything.
        if self._capacity <= 0:
            return

        node = self._items.get(key)
        if node is not None:
            # Key already present: update its value and mark it most recently used.
            # The size doesn't change, so there's no eviction check.
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return

        # New key: create a node, index it in the dict, and put it at the front.
        node = _Node(key, value)
        self._items[key] = node
        self._push_front(node)

        # Over capacity? Evict the least recently used node, which sits just before _tail.
        if len(self._items) > self._capacity:
            lru = self._tail.prev
            self._unlink(lru)
            # This is WHY the node stores its own key: we need it to delete the matching
            # dict entry. Without node.key we'd have no O(1) way to find it.
            del self._items[lru.key]

    def __len__(self) -> int:
        # Defining __len__ makes len(cache) work.
        return len(self._items)
