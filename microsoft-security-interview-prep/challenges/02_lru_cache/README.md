# 02 — LRU Cache (O(1) get/put)

**Theme:** classic data structures. Extremely common coding-round staple — expect it or
a close variant.

## Problem

Implement an LRU (least-recently-used) cache with O(1) `get` and `put`:

```python
class LRUCache:
    def __init__(self, capacity: int):
        ...

    def get(self, key) -> Any:
        """Return the value for key, or None if absent. Counts as a use
        (refreshes recency)."""

    def put(self, key, value) -> None:
        """Insert/update key. If inserting a new key would exceed capacity,
        evict the least-recently-used entry first. Updating an existing key
        also refreshes its recency."""
```

## Constraints

- `get`/`put` must be **O(1)** average time — don't scan a list for recency. (Use a hash
  map + doubly linked list, not `collections.OrderedDict` — the point is to show you can
  build the mechanism, not call a library that does it for you.)
- `capacity >= 1`.
- Overwriting an existing key with `put` counts as accessing it (moves it to
  most-recently-used) and does **not** count against the eviction budget.

## Talking points if asked to extend it

- Thread-safety (a lock around the critical section, and where exactly it needs to go).
- TTL / expiry per entry.
- How this maps to a real cache (Redis `maxmemory-policy allkeys-lru` is this exact
  algorithm at a different layer).

## Run

```bash
pytest challenges/02_lru_cache -v
```
