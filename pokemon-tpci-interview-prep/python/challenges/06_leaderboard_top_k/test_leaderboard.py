import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    return importlib.import_module("practice_leaderboard" if use_practice else "solution_leaderboard")


impl = _load_impl()


def seeded():
    lb = impl.Leaderboard()
    lb.award("ash", 200)
    lb.award("misty", 350)
    lb.award("brock", 200)
    lb.award("gary", 500)
    lb.award("gary", -100)
    return lb


def test_top_k():
    assert seeded().top_k(3) == [("gary", 400), ("misty", 350), ("ash", 200)]


def test_k_larger_than_n():
    got = seeded().top_k(10)
    assert len(got) == 4 and got[3] == ("brock", 200)


def test_totals_and_empty():
    lb = seeded()
    assert lb.total("gary") == 400 and lb.total("nobody") == 0
    assert lb.top_k(0) == [] and impl.Leaderboard().top_k(3) == []
