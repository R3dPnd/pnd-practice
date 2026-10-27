from dataclasses import dataclass, field


@dataclass(frozen=True)
class Player:
    id: str
    points: int
    had_bye: bool = False


@dataclass
class Round:
    pairings: list[tuple[str, str]] = field(default_factory=list)
    bye: str | None = None
