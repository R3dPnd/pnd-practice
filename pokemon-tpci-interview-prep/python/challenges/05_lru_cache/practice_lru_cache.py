"""Fill this in. See README.md for the problem statement."""
from typing import Any, Hashable


class LRUCache:
    def __init__(self, capacity: int):
        raise NotImplementedError

    def get(self, key: Hashable) -> Any | None:
        raise NotImplementedError

    def put(self, key: Hashable, value: Any) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
