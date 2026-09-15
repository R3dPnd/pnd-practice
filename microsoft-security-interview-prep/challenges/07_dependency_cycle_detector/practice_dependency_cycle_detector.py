"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/07_dependency_cycle_detector -v` to check yourself, or
`PRACTICE=0 pytest challenges/07_dependency_cycle_detector -v` to see the
reference solution's tests pass instead.
"""
from typing import Dict, List


class CycleError(ValueError):
    pass


def has_cycle(graph: Dict[str, List[str]]) -> bool:
    raise NotImplementedError


def topological_order(graph: Dict[str, List[str]]) -> List[str]:
    raise NotImplementedError
