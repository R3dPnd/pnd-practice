import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = (
        "practice_duplicate_partner_merge" if use_practice else "solution_duplicate_partner_merge"
    )
    return importlib.import_module(module_name)


impl = _load_impl()


def test_no_shared_identifiers():
    records = [
        ("r2", ["domain:fabrikam.com"]),
        ("r1", ["domain:contoso.com"]),
    ]
    assert impl.merge_partner_records(records) == [["r1"], ["r2"]]


def test_direct_share():
    records = [
        ("r1", ["domain:contoso.com", "tax:111"]),
        ("r2", ["tax:111"]),
    ]
    assert impl.merge_partner_records(records) == [["r1", "r2"]]


def test_transitive_share():
    records = [
        ("a", ["domain:contoso.com"]),
        ("b", ["domain:contoso.com", "tax:999"]),
        ("c", ["tax:999", "email:ops@contoso.com"]),
        ("d", ["email:ops@contoso.com"]),
        ("z", ["domain:unrelated.com"]),
    ]
    assert impl.merge_partner_records(records) == [["a", "b", "c", "d"], ["z"]]


def test_merge_happens_late():
    # Two groups formed separately, then a later record bridges them.
    records = [
        ("a", ["x"]),
        ("b", ["x"]),
        ("c", ["y"]),
        ("d", ["y"]),
        ("e", ["x", "y"]),
    ]
    assert impl.merge_partner_records(records) == [["a", "b", "c", "d", "e"]]


def test_identifiers_are_normalized():
    records = [
        ("r1", ["Domain:Contoso.COM "]),
        ("r2", ["  domain:contoso.com"]),
    ]
    assert impl.merge_partner_records(records) == [["r1", "r2"]]


def test_blank_identifiers_do_not_link():
    records = [
        ("r1", ["", "   "]),
        ("r2", ["  ", ""]),
        ("r3", []),
    ]
    assert impl.merge_partner_records(records) == [["r1"], ["r2"], ["r3"]]


def test_output_ordering():
    records = [
        ("m", ["k1"]),
        ("c", ["k2"]),
        ("a", ["k1"]),
        ("b", ["k2"]),
    ]
    assert impl.merge_partner_records(records) == [["a", "m"], ["b", "c"]]


def test_empty_input():
    assert impl.merge_partner_records([]) == []


def test_long_chain_does_not_hit_recursion_limit():
    n = 20_000
    records = [(f"r{i:05d}", [f"link:{i}", f"link:{i + 1}"]) for i in range(n)]
    result = impl.merge_partner_records(records)
    assert len(result) == 1
    assert len(result[0]) == n
    assert result[0][0] == "r00000"
