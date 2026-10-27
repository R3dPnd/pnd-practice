from enum import Enum


class Status(Enum):
    CONFIRMED = "confirmed"
    WAITLISTED = "waitlisted"


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass
