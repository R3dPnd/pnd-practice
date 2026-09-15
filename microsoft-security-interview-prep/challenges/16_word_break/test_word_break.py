import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_word_break" if use_practice else "solution_word_break"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_simple_two_word_split():
    assert impl.word_break("leetcode", ["leet", "code"]) is True


def test_word_reused_multiple_times():
    assert impl.word_break("applepenapple", ["apple", "pen"]) is True


def test_no_valid_segmentation():
    assert impl.word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False


def test_single_word_match():
    assert impl.word_break("cat", ["cat"]) is True


def test_single_word_no_match():
    assert impl.word_break("cat", ["dog"]) is False


def test_exponential_blowup_case_still_returns_quickly():
    # classic worst case for un-memoized recursion: many partial matches that
    # all eventually fail. Must complete quickly if memoized correctly.
    s = "a" * 25 + "b"
    word_dict = ["a" * i for i in range(1, 21)]
    assert impl.word_break(s, word_dict) is False


def test_empty_word_dict():
    assert impl.word_break("abc", []) is False
