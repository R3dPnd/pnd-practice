import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    return importlib.import_module("practice_lru_cache" if use_practice else "solution_lru_cache")


impl = _load_impl()


def test_evicts_least_recently_used():
    c = impl.LRUCache(2)
    c.put("pikachu", 25)
    c.put("eevee", 133)
    c.get("pikachu")
    c.put("snorlax", 143)
    assert c.get("eevee") is None
    assert c.get("pikachu") == 25
    assert len(c) == 2


def test_update_refreshes_recency():
    c = impl.LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)
    c.put("c", 3)
    assert c.get("b") is None
    assert c.get("a") == 10


def test_zero_capacity():
    c = impl.LRUCache(0)
    c.put(1, 1)
    assert c.get(1) is None
    assert len(c) == 0
