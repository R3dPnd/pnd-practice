import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = (
        "practice_dependency_cycle_detector" if use_practice else "solution_dependency_cycle_detector"
    )
    return importlib.import_module(module_name)


impl = _load_impl()


def test_no_cycle_in_simple_dag():
    graph = {"app": ["lib_a", "lib_b"], "lib_a": ["lib_c"], "lib_b": ["lib_c"], "lib_c": []}
    assert impl.has_cycle(graph) is False


def test_detects_direct_cycle():
    graph = {"a": ["b"], "b": ["a"]}
    assert impl.has_cycle(graph) is True


def test_detects_indirect_cycle():
    graph = {"a": ["b"], "b": ["c"], "c": ["a"]}
    assert impl.has_cycle(graph) is True


def test_detects_self_loop():
    graph = {"a": ["a"]}
    assert impl.has_cycle(graph) is True


def test_disconnected_components_no_cycle():
    graph = {"a": ["b"], "b": [], "x": ["y"], "y": []}
    assert impl.has_cycle(graph) is False


def test_leaf_dependency_not_a_top_level_key():
    # "lib_c" is never a key, only ever a value -> should be treated as a leaf
    graph = {"app": ["lib_c"]}
    assert impl.has_cycle(graph) is False
    order = impl.topological_order(graph)
    assert set(order) == {"app", "lib_c"}


def test_topological_order_respects_edges():
    graph = {"app": ["lib_a", "lib_b"], "lib_a": ["lib_c"], "lib_b": ["lib_c"], "lib_c": []}
    order = impl.topological_order(graph)

    assert set(order) == {"app", "lib_a", "lib_b", "lib_c"}
    positions = {node: i for i, node in enumerate(order)}
    for node, deps in graph.items():
        for dep in deps:
            assert positions[dep] < positions[node]


def test_topological_order_raises_on_cycle():
    graph = {"a": ["b"], "b": ["a"]}
    with pytest.raises(impl.CycleError):
        impl.topological_order(graph)


def test_topological_order_covers_disconnected_components():
    graph = {"a": ["b"], "b": [], "x": ["y"], "y": []}
    order = impl.topological_order(graph)
    assert set(order) == {"a", "b", "x", "y"}
