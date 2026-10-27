"""Fill this in. See README.md for the problem statement."""


class Leaderboard:
    def __init__(self):
        raise NotImplementedError

    def award(self, player_id: str, points: int) -> None:
        raise NotImplementedError

    def total(self, player_id: str) -> int:
        raise NotImplementedError

    def top_k(self, k: int) -> list[tuple[str, int]]:
        raise NotImplementedError
