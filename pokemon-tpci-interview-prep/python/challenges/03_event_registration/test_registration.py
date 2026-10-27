import importlib
import os
from concurrent.futures import ThreadPoolExecutor

import pytest

from models_registration import AlreadyRegistered, NotRegistered, Status


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    return importlib.import_module("practice_registration" if use_practice else "solution_registration")


impl = _load_impl()


def test_fills_then_waitlists():
    e = impl.Event(2)
    assert e.register("ash") is Status.CONFIRMED
    assert e.register("misty") is Status.CONFIRMED
    assert e.register("brock") is Status.WAITLISTED
    with pytest.raises(AlreadyRegistered):
        e.register("ash")
    with pytest.raises(AlreadyRegistered):
        e.register("brock")


def test_cancel_confirmed_promotes_fifo():
    e = impl.Event(1)
    for p in ("ash", "misty", "brock"):
        e.register(p)
    assert e.cancel("ash") == "misty"
    assert e.confirmed() == ["misty"]
    assert e.waitlist() == ["brock"]
    assert e.register("ash") is Status.WAITLISTED  # can re-register after cancelling


def test_cancel_waitlisted_does_not_promote():
    e = impl.Event(1)
    for p in ("ash", "misty", "brock"):
        e.register(p)
    assert e.cancel("misty") is None
    assert e.waitlist() == ["brock"]
    with pytest.raises(NotRegistered):
        e.cancel("gary")


def test_accessors_return_copies():
    e = impl.Event(2)
    e.register("ash")
    e.confirmed().append("hacked")
    assert e.confirmed() == ["ash"]


def test_concurrent_registration_never_oversells():
    e = impl.Event(100)
    with ThreadPoolExecutor(max_workers=50) as pool:
        list(pool.map(e.register, [f"p{i}" for i in range(1000)]))
    assert len(e.confirmed()) == 100
    assert len(e.waitlist()) == 900
