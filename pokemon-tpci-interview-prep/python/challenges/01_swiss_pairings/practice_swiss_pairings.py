"""Fill this in. See README.md for the problem statement."""
from models_swiss import Player, Round


def pair(players: list[Player], history: list[tuple[str, str]]) -> Round:
    sorted_player = sorted(players, key=lambda p: (p.points, p.id))
    raise NotImplementedError
