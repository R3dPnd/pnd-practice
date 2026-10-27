"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/02_delegated_access_resolver -v` to check yourself, or
`PRACTICE=0 pytest challenges/02_delegated_access_resolver -v` to see the
reference solution's tests pass instead.
"""
import time
from typing import Callable, Dict, List, Optional, Set


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
        raise NotImplementedError

    def grant(
        self,
        principal: str,
        role: str,
        tenant: str,
        expires_at: Optional[float] = None,
    ) -> None:
        raise NotImplementedError

    def revoke(self, principal: str, role: str, tenant: str) -> None:
        raise NotImplementedError

    def effective_permissions(self, principal: str, tenant: str) -> Set[str]:
        raise NotImplementedError

    def is_allowed(self, principal: str, permission: str, tenant: str) -> bool:
        raise NotImplementedError
