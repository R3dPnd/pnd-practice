"""Bounded concurrency with cancellation (asyncio) — reference solution.

Big picture:
  - Start one task per item, but each task must acquire a Semaphore before calling fn.
    A Semaphore(n) is a counter of n "permits": at most n tasks can hold one at a time,
    and the rest wait. That gives us "at most `workers` calls in flight".
  - Each task writes its result into results[i], its OWN slot, so the output comes back
    in input order no matter which task finishes first.
  - asyncio.TaskGroup (Python 3.11+) does the error handling for us: if any task raises,
    it CANCELS all the other tasks in the group, waits for them to stop, and then raises
    an ExceptionGroup.

Note: this creates all len(items) tasks up front (most just wait on the semaphore).
Fine for thousands of items. For millions, use N worker tasks pulling from an
asyncio.Queue instead, so you only ever have N tasks.
"""
import asyncio
from typing import Awaitable, Callable, TypeVar

# TypeVars make this generic: if items are T and fn returns R, we return list[R].
T = TypeVar("T")
R = TypeVar("R")


async def bounded_map(items: list[T], workers: int, fn: Callable[[T], Awaitable[R]]) -> list[R]:
    # max(1, workers): treat 0 or negative as 1 instead of deadlocking on a 0-permit
    # semaphore.
    sem = asyncio.Semaphore(max(1, workers))

    # Pre-size the results list so each task can write to its own index.
    results: list[R] = [None] * len(items)  # type: ignore[list-item]

    async def run(i: int, item: T) -> None:
        # `async with sem:` waits for a free permit, then releases it when the block exits
        # (including when fn raises or the task is cancelled).
        async with sem:
            results[i] = await fn(item)
        # No lock is needed around results[i]: asyncio runs on ONE thread and only switches
        # tasks at an `await`, and every task writes a different index anyway.

    try:
        # Leaving the `async with` block waits for ALL tasks to finish.
        async with asyncio.TaskGroup() as tg:
            for i, item in enumerate(items):
                tg.create_task(run(i, item))   # schedule the task; it starts at the next await
    except ExceptionGroup as eg:
        # TaskGroup wraps failures in an ExceptionGroup (there could be several if tasks
        # failed at the same moment). Callers expect the plain original error (e.g.
        # ValueError), so re-raise the first one.
        # `from None` hides the "during handling of the above exception..." chain in tracebacks.
        raise eg.exceptions[0] from None

    return results
