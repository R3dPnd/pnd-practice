import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_diameter_binary_tree" if use_practice else "solution_diameter_binary_tree"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_empty_tree():
    assert impl.diameter_of_binary_tree(None) == 0


def test_single_node():
    assert impl.diameter_of_binary_tree(impl.TreeNode(1)) == 0


def test_diameter_through_root():
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    root = impl.TreeNode(
        1,
        impl.TreeNode(2, impl.TreeNode(4), impl.TreeNode(5)),
        impl.TreeNode(3),
    )
    assert impl.diameter_of_binary_tree(root) == 3


def test_diameter_not_through_root():
    # Root has only one child, so the root itself can only ever contribute a
    # one-sided path. The longest path (5-3-2-4-6, 4 edges) is entirely inside
    # the subtree rooted at node 2, not through the true root (node 1) at all.
    #         1
    #        /
    #       2
    #      / \
    #     3   4
    #    /     \
    #   5       6
    left_of_2 = impl.TreeNode(3, impl.TreeNode(5))
    right_of_2 = impl.TreeNode(4, right=impl.TreeNode(6))
    node2 = impl.TreeNode(2, left_of_2, right_of_2)
    root = impl.TreeNode(1, node2)
    assert impl.diameter_of_binary_tree(root) == 4


def test_skewed_tree_diameter_equals_edge_count():
    # A straight-line tree of 4 nodes has a diameter of 3 edges.
    root = impl.TreeNode(1, impl.TreeNode(2, impl.TreeNode(3, impl.TreeNode(4))))
    assert impl.diameter_of_binary_tree(root) == 3
