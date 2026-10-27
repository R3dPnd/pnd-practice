import importlib
import os

import pytest

from models_standings import Match


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    return importlib.import_module("practice_standings" if use_practice else "solution_standings")


impl = _load_impl()


def test_owp_breaks_point_tie():
    got = impl.compute([
        Match("A", "B", "P1"), Match("C", "D", "P1"),
        Match("A", "C", "P1"), Match("D", "B", "P1"),
    ])
    assert [s.id for s in got] == ["A", "C", "D", "B"]
    want = {"A": (0.375, 0.75), "B": (0.75, 0.375), "C": (0.75, 0.375), "D": (0.375, 0.75)}
    for s in got:
        assert (s.owp, s.oowp) == pytest.approx(want[s.id])
    assert got[0].points == 6 and got[0].wins == 2 and got[3].losses == 2


def test_bye_is_win_but_not_opponent():
    got = impl.compute([Match("A", None, "P1")])
    assert len(got) == 1
    s = got[0]
    assert (s.points, s.wins, s.owp, s.oowp) == (3, 1, 0.0, 0.0)


def test_ties_and_floor():
    got = impl.compute([Match("A", "B", "TIE"), Match("C", "B", "P1")])
    by_id = {s.id: s for s in got}
    assert (by_id["A"].points, by_id["B"].points, by_id["C"].points) == (1, 1, 3)
    assert by_id["A"].owp == pytest.approx(0.25)   # B is 0-for-2 → floored
    assert by_id["B"].owp == pytest.approx(0.625)  # (0.25 + 1.0) / 2
    assert [s.id for s in got] == ["C", "B", "A"]
