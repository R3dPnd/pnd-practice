import importlib
import os

from models_swiss import Player


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    return importlib.import_module("practice_swiss_pairings" if use_practice else "solution_swiss_pairings")


impl = _load_impl()


def four():
    return [Player("D", 0), Player("B", 3), Player("A", 6), Player("C", 3)]


def test_no_history_pairs_top_down():
    r = impl.pair(four(), [])
    assert r.pairings == [("A", "B"), ("C", "D")]
    assert r.bye is None


def test_avoids_rematch():
    assert impl.pair(four(), [("B", "A")]).pairings == [("A", "C"), ("B", "D")]


def test_backtracks_when_greedy_forces_rematch():
    assert impl.pair(four(), [("C", "D")]).pairings == [("A", "C"), ("B", "D")]


def test_odd_count_bye_to_lowest_without_bye():
    players = [Player("A", 6), Player("B", 3), Player("C", 3), Player("D", 0), Player("E", 0, had_bye=True)]
    r = impl.pair(players, [])
    assert r.bye == "D"
    assert r.pairings == [("A", "B"), ("C", "E")]


def test_everyone_had_bye_falls_back_to_lowest():
    players = [Player("A", 3, True), Player("B", 0, True), Player("C", 0, True)]
    assert impl.pair(players, []).bye == "C"


def test_impossible_round_still_pairs_everyone():
    everyone = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D")]
    assert impl.pair(four(), everyone).pairings == [("A", "B"), ("C", "D")]


def test_does_not_mutate_input():
    players = four()
    impl.pair(players, [])
    assert players[0].id == "D"
