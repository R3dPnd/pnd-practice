import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_lowest_common_ancestor" if use_practice else "solution_lowest_common_ancestor"
    return importlib.import_module(module_name)


impl = _load_impl()


def _build_tree():
    r"""Classic LCA example tree:

              3
            /   \
           5     1
          / \   / \
         6   2 0   8
            / \
           7   4

    Returns (root, nodes) where nodes maps val -> TreeNode.
    """
    nodes = {v: impl.TreeNode(v) for v in [3, 5, 1, 6, 2, 0, 8, 7, 4]}
    nodes[3].left, nodes[3].right = nodes[5], nodes[1]
    nodes[5].left, nodes[5].right = nodes[6], nodes[2]
    nodes[1].left, nodes[1].right = nodes[0], nodes[8]
    nodes[2].left, nodes[2].right = nodes[7], nodes[4]
    return nodes[3], nodes


def test_lca_across_subtrees():
    root, nodes = _build_tree()
    result = impl.lowest_common_ancestor(root, nodes[5], nodes[1])
    assert result is nodes[3]


def test_lca_where_one_node_is_ancestor_of_other():
    root, nodes = _build_tree()
    result = impl.lowest_common_ancestor(root, nodes[5], nodes[4])
    assert result is nodes[5]


def test_lca_deep_in_same_subtree():
    root, nodes = _build_tree()
    result = impl.lowest_common_ancestor(root, nodes[7], nodes[4])
    assert result is nodes[2]


def test_lca_in_different_top_level_subtrees():
    root, nodes = _build_tree()
    result = impl.lowest_common_ancestor(root, nodes[7], nodes[8])
    assert result is nodes[3]


def test_lca_of_node_with_itself():
    root, nodes = _build_tree()
    result = impl.lowest_common_ancestor(root, nodes[5], nodes[5])
    assert result is nodes[5]


def test_single_node_tree():
    root = impl.TreeNode(1)
    result = impl.lowest_common_ancestor(root, root, root)
    assert result is root
