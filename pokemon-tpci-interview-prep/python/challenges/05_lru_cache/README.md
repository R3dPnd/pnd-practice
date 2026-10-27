# 05 — LRU cache (Python)

Talking points: [`../../../challenges/05_lru_cache/README.md`](../../../challenges/05_lru_cache/README.md).

```python
c = LRUCache(capacity)
c.get(key) -> value | None   # marks most-recently-used
c.put(key, value)            # insert/update (marks MRU); evict LRU over capacity
len(c)
```
O(1) both ops. Capacity ≤ 0 stores nothing. Implement it **twice**: once with
`collections.OrderedDict` (`move_to_end`, `popitem(last=False)`), and once with a hand-rolled
dict + doubly linked list — interviewers often say "now without OrderedDict."
The reference uses the linked list.
