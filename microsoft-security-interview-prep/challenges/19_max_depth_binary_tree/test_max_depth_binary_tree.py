import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_max_depth_binary_tree" if use_practice else "solution_max_depth_binary_tree"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_empty_tree():
    assert impl.max_depth(None) == 0


def test_single_node():
    assert impl.max_depth(impl.TreeNode(1)) == 1


def test_balanced_tree():
    root = impl.TreeNode(
        1,
        impl.TreeNode(2, impl.TreeNode(4), impl.TreeNode(5)),
        impl.TreeNode(3),
    )
    assert impl.max_depth(root) == 3


def test_left_skewed_tree():
    root = impl.TreeNode(1, impl.TreeNode(2, impl.TreeNode(3, impl.TreeNode(4))))
    assert impl.max_depth(root) == 4


def test_unbalanced_tree_uses_longest_path():
    # right subtree is much deeper than left
    right = impl.TreeNode(3, impl.TreeNode(4, impl.TreeNode(5)))
    root = impl.TreeNode(1, impl.TreeNode(2), right)
    assert impl.max_depth(root) == 4
