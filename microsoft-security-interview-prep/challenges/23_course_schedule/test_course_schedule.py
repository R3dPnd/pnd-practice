import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_course_schedule" if use_practice else "solution_course_schedule"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_simple_chain_is_finishable():
    assert impl.can_finish(2, [[1, 0]]) is True


def test_direct_cycle_is_not_finishable():
    assert impl.can_finish(2, [[1, 0], [0, 1]]) is False


def test_no_prerequisites_is_finishable():
    assert impl.can_finish(3, []) is True


def test_self_loop_is_a_cycle():
    assert impl.can_finish(1, [[0, 0]]) is False


def test_longer_cycle_is_not_finishable():
    assert impl.can_finish(4, [[1, 0], [2, 1], [3, 2], [0, 3]]) is False


def test_disconnected_components_all_finishable():
    assert impl.can_finish(4, [[1, 0], [3, 2]]) is True


def test_diamond_dependency_is_finishable():
    # 0 depends on nothing; 1 and 2 depend on 0; 3 depends on both 1 and 2.
    assert impl.can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True
