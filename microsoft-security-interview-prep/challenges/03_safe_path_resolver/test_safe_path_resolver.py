import importlib
import os
import os.path
import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_safe_path_resolver" if use_practice else "solution_safe_path_resolver"
    return importlib.import_module(module_name)


impl = _load_impl()


@pytest.fixture
def base(tmp_path):
    d = tmp_path / "base"
    d.mkdir()
    (d / "subdir").mkdir()
    return str(d)


def test_simple_filename(base):
    result = impl.safe_resolve(base, "report.pdf")
    assert result == os.path.join(os.path.abspath(base), "report.pdf")


def test_nested_contained_path(base):
    result = impl.safe_resolve(base, "subdir/report.pdf")
    assert result == os.path.join(os.path.abspath(base), "subdir", "report.pdf")


def test_internal_dotdot_that_stays_contained(base):
    result = impl.safe_resolve(base, "subdir/../report.pdf")
    assert result == os.path.join(os.path.abspath(base), "report.pdf")


def test_rejects_traversal_above_base(base):
    with pytest.raises(impl.PathTraversalError):
        impl.safe_resolve(base, "../../etc/passwd")


def test_rejects_nested_traversal_that_nets_escape(base):
    with pytest.raises(impl.PathTraversalError):
        impl.safe_resolve(base, "subdir/../../../etc/passwd")


def test_rejects_absolute_path(base):
    with pytest.raises(impl.PathTraversalError):
        impl.safe_resolve(base, "/etc/passwd")


def test_rejects_null_byte(base):
    with pytest.raises(impl.PathTraversalError):
        impl.safe_resolve(base, "report.pdf\x00.png")


def test_rejects_empty_string(base):
    with pytest.raises(impl.PathTraversalError):
        impl.safe_resolve(base, "")


def test_rejects_none(base):
    with pytest.raises(impl.PathTraversalError):
        impl.safe_resolve(base, None)
