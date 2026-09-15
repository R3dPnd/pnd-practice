"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/06_trie_autocomplete -v` to check yourself, or
`PRACTICE=0 pytest challenges/06_trie_autocomplete -v` to see the reference
solution's tests pass instead.
"""
from typing import List, Optional


class Trie:
    def __init__(self):
        raise NotImplementedError

    def insert(self, word: str) -> None:
        raise NotImplementedError

    def search(self, word: str) -> bool:
        raise NotImplementedError

    def starts_with(self, prefix: str) -> bool:
        raise NotImplementedError

    def autocomplete(self, prefix: str, limit: Optional[int] = None) -> List[str]:
        raise NotImplementedError
