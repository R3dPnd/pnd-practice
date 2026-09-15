# 06 — Trie-based Autocomplete

**Theme:** classic data structure, commonly asked to check comfort with trees/recursion
beyond arrays and hash maps.

## Problem

```python
class Trie:
    def insert(self, word: str) -> None: ...
    def search(self, word: str) -> bool:
        """Exact match only."""
    def starts_with(self, prefix: str) -> bool:
        """True if any inserted word starts with `prefix` (prefix itself need not
        have been inserted as a whole word)."""
    def autocomplete(self, prefix: str, limit: Optional[int] = None) -> List[str]:
        """All inserted words starting with `prefix`, sorted alphabetically.
        If limit is given, return at most `limit` results (still the
        alphabetically-first ones)."""
```

## Constraints

- Case-sensitive, ASCII lowercase letters only is fine to assume for inputs.
- `autocomplete("")` should return all inserted words (up to `limit`).
- `autocomplete` on a prefix nothing matches returns `[]`.
- Don't just collect *all* words and filter with `str.startswith` in a loop — walk the
  trie down to the prefix node, then collect from there. (Talk through why: a hash-set
  + linear filter is `O(n * len(prefix))` per query and defeats the point of the
  data structure; a trie walk is `O(len(prefix) + results)`.)

## Run

```bash
pytest challenges/06_trie_autocomplete -v
```
