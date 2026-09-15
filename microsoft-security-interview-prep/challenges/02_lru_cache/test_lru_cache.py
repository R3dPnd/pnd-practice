import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_lru_cache" if use_practice else "solution_lru_cache"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_basic_get_put():
    cache = impl.LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    assert cache.get(1) == "a"
    assert cache.get(2) == "b"
    assert cache.get(3) is None


def test_evicts_least_recently_used():
    cache = impl.LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.put(3, "c")  # evicts 1 (least recently used)
    assert cache.get(1) is None
    assert cache.get(2) == "b"
    assert cache.get(3) == "c"


def test_get_refreshes_recency():
    cache = impl.LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.get(1)  # 1 is now most recently used, 2 is now LRU
    cache.put(3, "c")  # should evict 2, not 1
    assert cache.get(2) is None
    assert cache.get(1) == "a"
    assert cache.get(3) == "c"


def test_put_on_existing_key_updates_value_and_recency():
    cache = impl.LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.put(1, "updated")  # refreshes 1, 2 is now LRU
    cache.put(3, "c")  # should evict 2
    assert cache.get(1) == "updated"
    assert cache.get(2) is None
    assert cache.get(3) == "c"


def test_capacity_one():
    cache = impl.LRUCache(1)
    cache.put(1, "a")
    cache.put(2, "b")
    assert cache.get(1) is None
    assert cache.get(2) == "b"


def test_rejects_non_positive_capacity():
    with pytest.raises(ValueError):
        impl.LRUCache(0)


def test_many_operations_stay_consistent():
    cache = impl.LRUCache(3)
    for i in range(10):
        cache.put(i, i * i)
    # only the last 3 keys (7, 8, 9) should survive
    for i in range(7):
        assert cache.get(i) is None
    for i in range(7, 10):
        assert cache.get(i) == i * i
