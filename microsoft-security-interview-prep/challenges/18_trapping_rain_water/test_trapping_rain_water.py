import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_trapping_rain_water" if use_practice else "solution_trapping_rain_water"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_classic_example():
    assert impl.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6


def test_second_classic_example():
    assert impl.trap([4, 2, 0, 3, 2, 5]) == 9


def test_empty_input():
    assert impl.trap([]) == 0


def test_single_bar():
    assert impl.trap([5]) == 0


def test_monotonic_increasing_traps_nothing():
    assert impl.trap([1, 2, 3, 4, 5]) == 0


def test_monotonic_decreasing_traps_nothing():
    assert impl.trap([5, 4, 3, 2, 1]) == 0


def test_simple_basin():
    assert impl.trap([3, 0, 3]) == 3


def test_flat_bars_trap_nothing():
    assert impl.trap([2, 2, 2, 2]) == 0
