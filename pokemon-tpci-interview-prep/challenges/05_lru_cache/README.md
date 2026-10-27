# 05 — Generic LRU cache

**Pattern:** hash map + doubly linked list (`container/list`), Go generics · **Classic**

Cache card/product lookups in front of Postgres. The canonical "design a data structure" ask.

## Task

```go
c := New[string, int](capacity)
v, ok := c.Get(key)    // marks key most-recently-used
c.Put(key, value)      // insert or update (also marks MRU); evicts LRU when over capacity
c.Len()
```
Both `Get` and `Put` must be O(1). Capacity ≤ 0 means the cache stores nothing.

## Talking points
- Why not a slice? (O(n) moves.) Why a map of `*list.Element`?
- Thread safety: add a `sync.Mutex` — note `Get` mutates (moves to front), so `RWMutex`
  doesn't buy you much.
- Production: ElastiCache/Redis with `maxmemory-policy allkeys-lru`; TTLs; cache stampede.
