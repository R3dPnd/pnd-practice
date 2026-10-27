"""Fill this in. See README.md for the problem statement."""
from models_registration import AlreadyRegistered, NotRegistered, Status


class Event:
    def __init__(self, capacity: int):
        raise NotImplementedError

    def register(self, player_id: str) -> Status:
        raise NotImplementedError

    def cancel(self, player_id: str) -> str | None:
        raise NotImplementedError

    def confirmed(self) -> list[str]:
        raise NotImplementedError

    def waitlist(self) -> list[str]:
        raise NotImplementedError
