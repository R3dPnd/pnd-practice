"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/03_enrollment_workflow -v` to check yourself, or
`PRACTICE=0 pytest challenges/03_enrollment_workflow -v` to see the
reference solution's tests pass instead.
"""
from typing import List, Tuple


class InvalidTransition(ValueError):
    pass


class IdempotencyConflict(ValueError):
    pass


class EnrollmentService:
    def __init__(self):
        raise NotImplementedError

    def start(self, partner_id: str) -> str:
        raise NotImplementedError

    def apply(self, partner_id: str, event: str, idempotency_key: str) -> str:
        raise NotImplementedError

    def status(self, partner_id: str) -> str:
        raise NotImplementedError

    def history(self, partner_id: str) -> List[Tuple[str, str]]:
        raise NotImplementedError
