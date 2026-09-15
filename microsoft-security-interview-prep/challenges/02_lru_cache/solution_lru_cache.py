"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Need O(1) get and O(1) put, including O(1) "find and evict the least-recently-used
   entry." A plain dict alone gives O(1) lookup but has no cheap way to track or
   update recency order.
2. Combine two structures: a hash map (key -> node) for O(1) lookup, and a doubly
   linked list ordered by recency for O(1) reordering and O(1) eviction from either
   end.
3. Use sentinel head/tail nodes (not real entries) so insert-at-front and
   remove-from-anywhere never need special-case null checks at the list boundaries —
   this is the detail that keeps the pointer bookkeeping clean.
4. `get`: if the key exists, unlink its node and reinsert it at the front (mark
   most-recently-used), then return its value; on a miss, return None.
5. `put`: if the key already exists, update the value and move it to the front. If
   it's new and the cache is at capacity, evict the node just before the tail
   sentinel (the true least-recently-used) before inserting the new node at the front.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why not just use `collections.OrderedDict`?" — it would work (`move_to_end` +
  `popitem(last=False)`), and is a fine production answer. Building it by hand
  demonstrates you understand *why* it's O(1) under the hood, which is the actual
  point of being asked to implement this from scratch.
- "What's the time/space complexity?" — O(1) time for both `get` and `put`, O(capacity)
  space.
- "How would you make this thread-safe?" — wrap the mutating sections in a lock;
  flag that a single coarse lock serializes all access, and be ready to discuss
  finer-grained alternatives if pushed further.
- "What if capacity is 0?" — this implementation validates `capacity >= 1` and raises
  `ValueError` otherwise — call out that you considered and rejected the degenerate
  case rather than letting it silently misbehave.
- "How would you turn this into an LFU (least-frequently-used) cache?" — you'd need
  frequency buckets instead of pure recency ordering — a good "what would you change"
  extension to have thought through before it's asked.
"""
from typing import Any, Dict, Optional


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev: Optional["_Node"] = None
        self.next: Optional["_Node"] = None


class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._map: Dict[Any, _Node] = {}
        # sentinel head/tail: head.next is most-recently-used, tail.prev is least
        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node: _Node) -> None:
        node.next = self._head.next
        node.prev = self._head
        self._head.next.prev = node
        self._head.next = node

    def get(self, key) -> Any:
        node = self._map.get(key)
        if node is None:
            return None
        self._remove(node)
        self._insert_front(node)
        return node.value

    def put(self, key, value) -> None:
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._remove(node)
            self._insert_front(node)
            return

        if len(self._map) >= self._capacity:
            lru = self._tail.prev
            self._remove(lru)
            del self._map[lru.key]

        node = _Node(key, value)
        self._map[key] = node
        self._insert_front(node)
