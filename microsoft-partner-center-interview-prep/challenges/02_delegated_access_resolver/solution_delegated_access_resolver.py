"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Split the problem into two independent parts and say so out loud:
   (a) "what permissions does a role grant?", which depends only on the role graph and
       can be computed once up front, and
   (b) "which grants apply to this principal at this tenant right now?", which
       is a per-query tree walk.
2. (a) is DFS over the role-inheritance graph with three states. VISITING means "on
   the current DFS path". Reaching a VISITING role again is a back edge, which means a
   cycle. Store each finished role's closure in `_closure`, so the "done" state is
   simply `role in self._closure`.
3. (b) walks from the tenant up to the root, at most depth-of-tree steps. At each
   ancestor, look up this principal's grants, skip expired ones, and union their
   precomputed closures.
4. Fail closed: an unknown tenant means an empty walk, which returns an empty set.

COMMON INTERVIEWER FOLLOW-UPS:
- "Complexity?" — construction is O(R + E) DFS. Storing the closures costs
  O(R * P) memory. A query is O(depth * grants_per_level * P) for the unions.
  `is_allowed` can stop as soon as it finds the permission.
- "This is on the hot path for every API call. How do you make it fast?" — cache
  `effective_permissions` per (principal, tenant) with a short TTL, and invalidate on
  grant/revoke. The TTL has to be shorter than the time you'd tolerate a revoked
  user keeping access. That tradeoff is the interesting part of the answer.
- "Add explicit DENY?" — evaluate deny before allow and let any matching deny win.
  This is how Azure RBAC deny assignments work. Keep allows and denies in separate
  collections, so you can't accidentally combine them in one union.
- "How would you audit this?" — have every grant and revoke write an append-only
  event (who, what, when, granted by). For security reviews, "why does alice have
  users.write on contoso?" needs an answer. A version of `effective_permissions`
  that returns the grant chain makes that easy.
- "Why validate the role graph at construction instead of at query time?" — a
  config error should fail at deploy time, not at 3am on the first request that
  touches the bad role.
"""
import time
from typing import Callable, Dict, List, Optional, Set, Tuple


class CycleError(ValueError):
    pass


class AccessResolver:
    def __init__(
        self,
        role_permissions: Dict[str, Set[str]],
        role_inherits: Dict[str, List[str]],
        tenant_parent: Dict[str, Optional[str]],
        clock: Callable[[], float] = time.monotonic,
    ):
        self._tenant_parent = dict(tenant_parent)
        self._clock = clock
        self._grants: Dict[Tuple[str, str], Dict[str, Optional[float]]] = {}
        self._closure = self._build_role_closures(role_permissions, role_inherits)

    @staticmethod
    def _build_role_closures(
        role_permissions: Dict[str, Set[str]],
        role_inherits: Dict[str, List[str]],
    ) -> Dict[str, Set[str]]:
        for role, parents in role_inherits.items():
            for parent in [role, *parents]:
                if parent not in role_permissions:
                    raise ValueError(f"unknown role {parent!r}")

        closure: Dict[str, Set[str]] = {}
        visiting: Set[str] = set()

        def visit(role: str) -> Set[str]:
            if role in closure:
                return closure[role]
            if role in visiting:
                raise CycleError(f"role inheritance cycle through {role!r}")
            visiting.add(role)
            perms = set(role_permissions[role])
            for parent in role_inherits.get(role, []):
                perms |= visit(parent)
            visiting.remove(role)
            closure[role] = perms
            return perms

        for role in role_permissions:
            visit(role)
        return closure

    def grant(
        self,
        principal: str,
        role: str,
        tenant: str,
        expires_at: Optional[float] = None,
    ) -> None:
        if role not in self._closure:
            raise ValueError(f"unknown role {role!r}")
        if tenant not in self._tenant_parent:
            raise ValueError(f"unknown tenant {tenant!r}")
        self._grants.setdefault((principal, tenant), {})[role] = expires_at

    def revoke(self, principal: str, role: str, tenant: str) -> None:
        self._grants.get((principal, tenant), {}).pop(role, None)

    def effective_permissions(self, principal: str, tenant: str) -> Set[str]:
        now = self._clock()
        perms: Set[str] = set()
        current: Optional[str] = tenant if tenant in self._tenant_parent else None
        while current is not None:
            for role, expires_at in self._grants.get((principal, current), {}).items():
                if expires_at is None or now < expires_at:
                    perms |= self._closure[role]
            current = self._tenant_parent.get(current)
        return perms

    def is_allowed(self, principal: str, permission: str, tenant: str) -> bool:
        return permission in self.effective_permissions(principal, tenant)
