"""Fill this in. See README.md for the problem statement."""
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


async def bounded_map(items: list[T], workers: int, fn: Callable[[T], Awaitable[R]]) -> list[R]:
    raise NotImplementedError
