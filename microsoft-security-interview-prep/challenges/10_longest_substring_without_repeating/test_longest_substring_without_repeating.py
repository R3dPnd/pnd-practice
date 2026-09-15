import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = (
        "practice_longest_substring_without_repeating"
        if use_practice
        else "solution_longest_substring_without_repeating"
    )
    return importlib.import_module(module_name)


impl = _load_impl()


def test_classic_examples():
    assert impl.length_of_longest_substring("abcabcbb") == 3
    assert impl.length_of_longest_substring("bbbbb") == 1
    assert impl.length_of_longest_substring("pwwkew") == 3


def test_empty_string():
    assert impl.length_of_longest_substring("") == 0


def test_all_unique():
    assert impl.length_of_longest_substring("abcdef") == 6


def test_repeat_that_is_already_outside_window():
    # regression case for the off-by-one: left edge must not move backwards
    assert impl.length_of_longest_substring("abba") == 2


def test_single_character():
    assert impl.length_of_longest_substring("a") == 1


def test_repeat_at_the_end():
    assert impl.length_of_longest_substring("tmmzuxt") == 5  # "mzuxt"
