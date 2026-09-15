import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_group_anagrams" if use_practice else "solution_group_anagrams"
    return importlib.import_module(module_name)


impl = _load_impl()


def _normalize(groups):
    return sorted(sorted(group) for group in groups)


def test_basic_grouping():
    result = impl.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    expected = [["ate", "eat", "tea"], ["nat", "tan"], ["bat"]]
    assert _normalize(result) == _normalize(expected)


def test_empty_list():
    assert impl.group_anagrams([]) == []


def test_single_empty_string():
    assert impl.group_anagrams([""]) == [[""]]


def test_no_anagrams_each_its_own_group():
    result = impl.group_anagrams(["abc", "def", "ghi"])
    assert _normalize(result) == _normalize([["abc"], ["def"], ["ghi"]])


def test_every_string_appears_exactly_once():
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    result = impl.group_anagrams(strs)
    flattened = [s for group in result for s in group]
    assert sorted(flattened) == sorted(strs)


def test_identical_strings_group_together():
    result = impl.group_anagrams(["aa", "aa", "aa"])
    assert _normalize(result) == [["aa", "aa", "aa"]]
