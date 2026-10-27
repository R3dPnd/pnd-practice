from dataclasses import dataclass
from typing import Literal

Result = Literal["P1", "P2", "TIE"]


@dataclass(frozen=True)
class Match:
    p1: str
    p2: str | None
    result: Result


@dataclass
class Standing:
    id: str
    points: int
    wins: int
    losses: int
    ties: int
    owp: float
    oowp: float
