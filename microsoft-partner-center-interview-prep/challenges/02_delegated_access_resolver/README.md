# 02 — Delegated Access Resolver (Graph DFS + Tree Walk)

**Theme:** authorization, the core of this team's work. In Partner Center, a CSP
partner's admins get **delegated, time-boxed, role-based** access to customer tenants
(GDAP, *granular delegated admin privileges*). In the two-tier model, an indirect
provider sits above resellers, and resellers sit above customers. This is a simplified
version of that model. Coding-wise it's two classics combined: **DFS with cycle
detection** (role inheritance) and **walking up a tree to the root** (tenant hierarchy).

## Problem

```python
class CycleError(ValueError): ...

class AccessResolver:
    def __init__(
        self,
        role_permissions: Dict[str, Set[str]],   # role -> permissions it grants directly
        role_inherits: Dict[str, List[str]],     # role -> roles it inherits from
        tenant_parent: Dict[str, Optional[str]], # tenant -> parent tenant (None = root)
        clock: Callable[[], float] = time.monotonic,
    ): ...

    def grant(self, principal: str, role: str, tenant: str,
              expires_at: Optional[float] = None) -> None: ...
    def revoke(self, principal: str, role: str, tenant: str) -> None: ...
    def effective_permissions(self, principal: str, tenant: str) -> Set[str]: ...
    def is_allowed(self, principal: str, permission: str, tenant: str) -> bool: ...
```

## Rules

1. **Role inheritance is transitive.** If `admin` inherits `editor` and `editor`
   inherits `reader`, then `admin` has all three roles' permissions.
2. **Validate the role graph at construction.** If a role inherits from a role that
   isn't in `role_permissions` → `ValueError`. If the inheritance graph has a cycle
   (including a self-loop) → `CycleError`.
3. **Grants flow down the tenant tree.** A grant on tenant `T` applies to `T` and every
   tenant below it. `tenant_parent` is guaranteed to be a forest (no tenant cycles).
4. **Grants can expire.** A grant with `expires_at` stops applying once
   `clock() >= expires_at`. `expires_at=None` means it never expires.
5. **Re-granting the same `(principal, role, tenant)` replaces the old grant**,
   including its expiry. Grants don't stack.
6. `revoke` removes exactly one `(principal, role, tenant)` grant. Revoking a grant
   that doesn't exist does nothing.
7. `grant` with an unknown role or tenant → `ValueError`.
8. **Queries fail closed.** An unknown principal, tenant, or permission returns
   `False` / `set()`. Never raise from a read path.

## Example

```python
r = AccessResolver(
    role_permissions={"reader": {"billing.read"}, "admin": {"users.write"}},
    role_inherits={"admin": ["reader"]},
    tenant_parent={"provider": None, "reseller": "provider", "contoso": "reseller"},
    clock=clock,
)
r.grant("alice", "admin", "reseller", expires_at=100)
r.is_allowed("alice", "billing.read", "contoso")   # True  (inherited role + child tenant)
r.is_allowed("alice", "billing.read", "provider")  # False (grants don't flow UP)
clock.advance(100)
r.is_allowed("alice", "billing.read", "contoso")   # False (expired)
```

## Hints

- Compute each role's full permission set once, in `__init__`, using DFS with three
  states (unvisited / in progress / done). Reaching an "in progress" role means the
  graph has a cycle. Cache the result for each role when it finishes so diamond
  inheritance isn't recomputed.
- For a query, walk from `tenant` up through each parent to the root, and collect the
  principal's grants at each step.
- Store grants as `{(principal, tenant): {role: expires_at}}`. That makes rule 5 a
  plain dict assignment.

## Run

```bash
pytest challenges/02_delegated_access_resolver -v
```
