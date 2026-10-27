import asyncio
import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    return importlib.import_module("practice_bounded_map" if use_practice else "solution_bounded_map")


impl = _load_impl()


async def test_preserves_order():
    async def square(n):
        await asyncio.sleep(n / 1000)
        return n * n

    assert await impl.bounded_map([5, 1, 4, 2, 3], 3, square) == [25, 1, 16, 4, 9]


async def test_bounds_concurrency():
    in_flight = peak = 0

    async def work(_):
        nonlocal in_flight, peak
        in_flight += 1
        peak = max(peak, in_flight)
        await asyncio.sleep(0.002)
        in_flight -= 1

    await impl.bounded_map(list(range(50)), 4, work)
    assert 2 <= peak <= 4


async def test_first_error_cancels_rest():
    started = finished = 0

    async def work(n):
        nonlocal started, finished
        started += 1
        if n == 3:
            raise ValueError("boom")
        await asyncio.sleep(0.005)
        finished += 1
        return n

    with pytest.raises(ValueError, match="boom"):
        await impl.bounded_map(list(range(100)), 2, work)
    assert finished < 20, "should stop doing work after the error"


async def test_zero_workers_treated_as_one():
    async def ident(n):
        return n

    assert await impl.bounded_map([1, 2, 3], 0, ident) == [1, 2, 3]
