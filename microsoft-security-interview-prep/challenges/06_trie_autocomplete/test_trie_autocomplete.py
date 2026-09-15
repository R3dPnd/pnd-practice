import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_trie_autocomplete" if use_practice else "solution_trie_autocomplete"
    return importlib.import_module(module_name)


impl = _load_impl()


def _trie(words):
    t = impl.Trie()
    for w in words:
        t.insert(w)
    return t


def test_search_exact_match():
    t = _trie(["apple", "app", "application"])
    assert t.search("apple") is True
    assert t.search("app") is True
    assert t.search("appl") is False
    assert t.search("banana") is False


def test_starts_with():
    t = _trie(["apple", "banana"])
    assert t.starts_with("app") is True
    assert t.starts_with("ap") is True
    assert t.starts_with("ban") is True
    assert t.starts_with("orange") is False


def test_autocomplete_returns_sorted_matches():
    t = _trie(["cat", "car", "cart", "dog", "care"])
    assert t.autocomplete("car") == ["car", "care", "cart"]


def test_autocomplete_no_matches():
    t = _trie(["cat", "dog"])
    assert t.autocomplete("z") == []


def test_autocomplete_empty_prefix_returns_all_sorted():
    t = _trie(["dog", "cat", "bird"])
    assert t.autocomplete("") == ["bird", "cat", "dog"]


def test_autocomplete_respects_limit():
    t = _trie(["a1", "a2", "a3", "a4"])
    assert t.autocomplete("a", limit=2) == ["a1", "a2"]


def test_autocomplete_includes_prefix_itself_if_a_word():
    t = _trie(["car", "carpet", "carton"])
    result = t.autocomplete("car")
    assert result == ["car", "carpet", "carton"]


def test_duplicate_inserts_do_not_duplicate_results():
    t = _trie(["dup", "dup", "dup"])
    assert t.autocomplete("dup") == ["dup"]
