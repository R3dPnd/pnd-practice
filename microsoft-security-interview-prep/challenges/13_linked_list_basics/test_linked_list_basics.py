import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_linked_list_basics" if use_practice else "solution_linked_list_basics"
    return importlib.import_module(module_name)


impl = _load_impl()


def _build(values):
    head = None
    tail = None
    for v in values:
        node = impl.ListNode(v)
        if head is None:
            head = tail = node
        else:
            tail.next = node
            tail = node
    return head


def _to_list(head):
    values = []
    while head is not None:
        values.append(head.val)
        head = head.next
    return values


# --- reverse_linked_list ---


def test_reverse_empty_list():
    assert impl.reverse_linked_list(None) is None


def test_reverse_single_node():
    head = _build([1])
    result = impl.reverse_linked_list(head)
    assert _to_list(result) == [1]


def test_reverse_multiple_nodes():
    head = _build([1, 2, 3, 4, 5])
    result = impl.reverse_linked_list(head)
    assert _to_list(result) == [5, 4, 3, 2, 1]


# --- has_cycle ---


def test_no_cycle_on_normal_list():
    head = _build([1, 2, 3])
    assert impl.has_cycle(head) is False


def test_no_cycle_on_empty_list():
    assert impl.has_cycle(None) is False


def test_detects_cycle_back_to_head():
    head = _build([1, 2, 3])
    tail = head
    while tail.next is not None:
        tail = tail.next
    tail.next = head  # create a cycle back to the start
    assert impl.has_cycle(head) is True


def test_detects_cycle_into_middle():
    a = impl.ListNode(1)
    b = impl.ListNode(2)
    c = impl.ListNode(3)
    d = impl.ListNode(4)
    a.next, b.next, c.next, d.next = b, c, d, b  # d -> b, cycle not at head
    assert impl.has_cycle(a) is True


def test_single_node_no_self_cycle():
    head = _build([1])
    assert impl.has_cycle(head) is False


# --- merge_two_sorted_lists ---


def test_merge_interleaved():
    l1 = _build([1, 3, 5])
    l2 = _build([2, 4, 6])
    result = impl.merge_two_sorted_lists(l1, l2)
    assert _to_list(result) == [1, 2, 3, 4, 5, 6]


def test_merge_one_empty():
    l1 = _build([])
    l2 = _build([1, 2, 3])
    result = impl.merge_two_sorted_lists(l1, l2)
    assert _to_list(result) == [1, 2, 3]


def test_merge_both_empty():
    result = impl.merge_two_sorted_lists(None, None)
    assert result is None


def test_merge_with_duplicate_values():
    l1 = _build([1, 2, 2])
    l2 = _build([2, 3])
    result = impl.merge_two_sorted_lists(l1, l2)
    assert _to_list(result) == [1, 2, 2, 2, 3]


def test_merge_different_lengths():
    l1 = _build([1, 10, 20, 30])
    l2 = _build([5])
    result = impl.merge_two_sorted_lists(l1, l2)
    assert _to_list(result) == [1, 5, 10, 20, 30]
