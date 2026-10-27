import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = (
        "practice_delegated_access_resolver"
        if use_practice
        else "solution_delegated_access_resolver"
    )
    return importlib.import_module(module_name)


impl = _load_impl()

ROLE_PERMISSIONS = {
    "reader": {"billing.read", "users.read"},
    "helpdesk": {"tickets.write"},
    "user_admin": {"users.write"},
    "global_admin": {"tenant.delete"},
}
ROLE_INHERITS = {
    "helpdesk": ["reader"],
    "user_admin": ["reader"],
    "global_admin": ["helpdesk", "user_admin"],  # diamond through reader
}
TENANT_PARENT = {
    "provider": None,
    "reseller_a": "provider",
    "reseller_b": "provider",
    "contoso": "reseller_a",
    "fabrikam": "reseller_b",
}


@pytest.fixture
def resolver(fake_clock):
    return impl.AccessResolver(ROLE_PERMISSIONS, ROLE_INHERITS, TENANT_PARENT, clock=fake_clock)


def test_direct_grant(resolver):
    resolver.grant("alice", "reader", "contoso")
    assert resolver.is_allowed("alice", "billing.read", "contoso")
    assert not resolver.is_allowed("alice", "users.write", "contoso")


def test_transitive_role_inheritance(resolver):
    resolver.grant("alice", "global_admin", "contoso")
    assert resolver.effective_permissions("alice", "contoso") == {
        "billing.read",
        "users.read",
        "tickets.write",
        "users.write",
        "tenant.delete",
    }


def test_grant_flows_down_tenant_tree(resolver):
    resolver.grant("alice", "reader", "reseller_a")
    assert resolver.is_allowed("alice", "billing.read", "reseller_a")
    assert resolver.is_allowed("alice", "billing.read", "contoso")


def test_grant_does_not_flow_up_or_sideways(resolver):
    resolver.grant("alice", "reader", "reseller_a")
    assert not resolver.is_allowed("alice", "billing.read", "provider")
    assert not resolver.is_allowed("alice", "billing.read", "reseller_b")
    assert not resolver.is_allowed("alice", "billing.read", "fabrikam")


def test_grants_combine_across_levels(resolver):
    resolver.grant("alice", "reader", "provider")
    resolver.grant("alice", "user_admin", "contoso")
    assert resolver.is_allowed("alice", "users.write", "contoso")
    assert not resolver.is_allowed("alice", "users.write", "fabrikam")
    assert resolver.is_allowed("alice", "billing.read", "fabrikam")


def test_grants_are_per_principal(resolver):
    resolver.grant("alice", "reader", "contoso")
    assert not resolver.is_allowed("bob", "billing.read", "contoso")


def test_expiry_is_exclusive_at_expires_at(resolver, fake_clock):
    resolver.grant("alice", "reader", "contoso", expires_at=100)
    fake_clock.advance(99.9)
    assert resolver.is_allowed("alice", "billing.read", "contoso")
    fake_clock.advance(0.1)
    assert not resolver.is_allowed("alice", "billing.read", "contoso")


def test_regrant_replaces_expiry(resolver, fake_clock):
    resolver.grant("alice", "reader", "contoso", expires_at=10)
    resolver.grant("alice", "reader", "contoso", expires_at=None)
    fake_clock.advance(1000)
    assert resolver.is_allowed("alice", "billing.read", "contoso")

    resolver.grant("alice", "reader", "contoso", expires_at=1001)
    fake_clock.advance(1)
    assert not resolver.is_allowed("alice", "billing.read", "contoso")


def test_revoke_removes_only_that_grant(resolver):
    resolver.grant("alice", "reader", "contoso")
    resolver.grant("alice", "helpdesk", "contoso")
    resolver.revoke("alice", "helpdesk", "contoso")
    assert not resolver.is_allowed("alice", "tickets.write", "contoso")
    assert resolver.is_allowed("alice", "billing.read", "contoso")


def test_revoke_missing_grant_is_noop(resolver):
    resolver.revoke("nobody", "reader", "contoso")
    resolver.grant("alice", "reader", "provider")
    resolver.revoke("alice", "reader", "contoso")  # granted at provider, not contoso
    assert resolver.is_allowed("alice", "billing.read", "contoso")


def test_queries_fail_closed(resolver):
    resolver.grant("alice", "reader", "contoso")
    assert resolver.effective_permissions("alice", "no_such_tenant") == set()
    assert not resolver.is_allowed("alice", "no.such.permission", "contoso")
    assert resolver.effective_permissions("ghost", "contoso") == set()


def test_returned_set_is_not_internal_state(resolver):
    resolver.grant("alice", "reader", "contoso")
    perms = resolver.effective_permissions("alice", "contoso")
    perms.add("tenant.delete")
    assert not resolver.is_allowed("alice", "tenant.delete", "contoso")


def test_grant_unknown_role_or_tenant_raises(resolver):
    with pytest.raises(ValueError):
        resolver.grant("alice", "superuser", "contoso")
    with pytest.raises(ValueError):
        resolver.grant("alice", "reader", "no_such_tenant")


def test_unknown_inherited_role_raises():
    with pytest.raises(ValueError):
        impl.AccessResolver({"a": set()}, {"a": ["missing"]}, {"t": None})


def test_role_cycle_raises():
    with pytest.raises(impl.CycleError):
        impl.AccessResolver(
            {"a": set(), "b": set(), "c": set()},
            {"a": ["b"], "b": ["c"], "c": ["a"]},
            {"t": None},
        )


def test_role_self_loop_raises():
    with pytest.raises(impl.CycleError):
        impl.AccessResolver({"a": set()}, {"a": ["a"]}, {"t": None})


def test_cycle_error_is_a_value_error():
    assert issubclass(impl.CycleError, ValueError)
