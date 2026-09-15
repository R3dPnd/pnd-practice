"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/02_lru_cache -v` to check yourself, or
`PRACTICE=0 pytest challenges/02_lru_cache -v` to see the reference
solution's tests pass instead.
"""
from typing import Any


class LRUCache:
    def __init__(self, capacity: int):
        raise NotImplementedError

    def get(self, key) -> Any:
        raise NotImplementedError

    def put(self, key, value) -> None:
        raise NotImplementedError
