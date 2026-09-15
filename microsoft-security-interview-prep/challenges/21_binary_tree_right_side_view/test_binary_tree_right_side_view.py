import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = (
        "practice_binary_tree_right_side_view"
        if use_practice
        else "solution_binary_tree_right_side_view"
    )
    return importlib.import_module(module_name)


impl = _load_impl()


def test_empty_tree():
    assert impl.right_side_view(None) == []


def test_single_node():
    assert impl.right_side_view(impl.TreeNode(1)) == [1]


def test_complete_tree():
    #     1
    #    / \
    #   2   3
    root = impl.TreeNode(1, impl.TreeNode(2), impl.TreeNode(3))
    assert impl.right_side_view(root) == [1, 3]


def test_missing_right_child_reveals_left_descendant():
    #     1
    #    / \
    #   2   3
    #    \   \
    #     5   4
    root = impl.TreeNode(
        1,
        impl.TreeNode(2, right=impl.TreeNode(5)),
        impl.TreeNode(3, right=impl.TreeNode(4)),
    )
    assert impl.right_side_view(root) == [1, 3, 4]


def test_left_only_skewed_tree_shows_every_node():
    root = impl.TreeNode(1, impl.TreeNode(2, impl.TreeNode(3)))
    assert impl.right_side_view(root) == [1, 2, 3]
