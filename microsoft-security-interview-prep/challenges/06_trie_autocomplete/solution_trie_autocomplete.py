"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Each trie node needs: a way to reach its children by character (a dict keyed by
   character is simpler to write correctly under time pressure than a fixed-size
   array, though an array is faster for a known small alphabet), and an `is_word`
   flag — a node can be *both* a valid prefix and a complete word at once (e.g.
   "cat" and "cats" share the "cat" node, which is `is_word=True` and also has a
   child for "cats").
2. `insert`: walk the string character by character, creating any missing child
   nodes as you go (`setdefault`), then mark the final node `is_word = True`.
3. `search` and `starts_with` are the same walk with different endings — factor the
   shared "walk to the node representing this string, or None if any character is
   missing" logic into one `_find_node` helper.
4. `autocomplete`: find the node at the end of `prefix` (reusing `_find_node`), then
   DFS from there collecting every `is_word` node underneath it. Sort children
   alphabetically at each step so results come back in a predictable order, and
   short-circuit the DFS once `limit` results have been found.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why a trie over just filtering a list of strings with `str.startswith`?" — trie
  prefix lookup is O(prefix length), independent of how many total words exist;
  filtering a flat list is O(n * prefix length) per query — this matters at the scale
  a real autocomplete system operates at (millions of terms).
- "What's the memory tradeoff?" — a trie can use more memory than a sorted list plus
  binary search for prefix queries, especially over a sparse alphabet — worth
  mentioning binary-search-over-sorted-list as an alternative with a different
  space/time tradeoff.
- "How would you rank results by popularity instead of alphabetically?" — store a
  frequency/weight per word (e.g. at the terminal node), and use a heap during
  collection instead of a plain alphabetical DFS.
- "How would you support typo-tolerant ('fuzzy') autocomplete?" — not with a plain
  trie as-is; that needs edit-distance-aware search (e.g. a BK-tree) or a separate
  fuzzy index layered on top.
"""
from typing import Dict, List, Optional


class _TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self):
        self.children: Dict[str, "_TrieNode"] = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self._root = _TrieNode()

    def insert(self, word: str) -> None:
        node = self._root
        for ch in word:
            node = node.children.setdefault(ch, _TrieNode())
        node.is_word = True

    def _find_node(self, prefix: str) -> Optional[_TrieNode]:
        node = self._root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def autocomplete(self, prefix: str, limit: Optional[int] = None) -> List[str]:
        start = self._find_node(prefix)
        if start is None:
            return []

        results: List[str] = []

        def dfs(node: _TrieNode, path: str) -> bool:
            """Return True if collection should stop (limit reached)."""
            if node.is_word:
                results.append(path)
                if limit is not None and len(results) >= limit:
                    return True
            for ch in sorted(node.children):
                if dfs(node.children[ch], path + ch):
                    return True
            return False

        dfs(start, prefix)
        return results
