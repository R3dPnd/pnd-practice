"""Event registration with capacity + FIFO waitlist — reference solution.

Big picture:
  - `_confirmed` is the list of players with a seat (in the order they got one).
  - `_waitlist` is a queue of players waiting (first in, first out).
  - `_status` maps player -> CONFIRMED / WAITLISTED, so "is this player registered,
    and where?" is an O(1) dict lookup instead of scanning both lists.
  - Every public method grabs `_lock` first, so two threads can never interleave a
    "check capacity" and an "append" — that interleaving is exactly how you oversell.
"""
import threading
from collections import deque

from models_registration import AlreadyRegistered, NotRegistered, Status


class Event:
    def __init__(self, capacity: int):
        # One lock guards ALL the state below. Simple and correct; good enough here.
        self._lock = threading.Lock()
        self._capacity = capacity
        self._confirmed: list[str] = []
        # deque = double-ended queue. popleft() is O(1); list.pop(0) would be O(n)
        # because every remaining element has to shift left.
        self._waitlist: deque[str] = deque()
        self._status: dict[str, Status] = {}

    def register(self, player_id: str) -> Status:
        # `with self._lock:` acquires the lock and ALWAYS releases it when the block
        # exits — even if we raise an exception inside. Equivalent to try/finally.
        with self._lock:
            # Already confirmed OR waitlisted → reject the duplicate.
            if player_id in self._status:
                raise AlreadyRegistered(player_id)

            # The check-then-act below is the critical section. Without the lock, two
            # threads could both see len == capacity - 1 and both append → oversold.
            # (Python's GIL does NOT protect you here: a thread can be switched out
            # between the `if` and the `append`.)
            if len(self._confirmed) < self._capacity:
                self._confirmed.append(player_id)
                status = Status.CONFIRMED
            else:
                self._waitlist.append(player_id)   # join the back of the line
                status = Status.WAITLISTED

            self._status[player_id] = status
            return status

    def cancel(self, player_id: str) -> str | None:
        with self._lock:
            # pop(key, None) removes the key and returns its value, or None if absent —
            # a lookup and a delete in one step.
            status = self._status.pop(player_id, None)
            if status is None:
                raise NotRegistered(player_id)

            # A waitlisted player leaving frees no seat, so nobody gets promoted.
            # (deque.remove is O(n), which is fine for a cancel.)
            if status is Status.WAITLISTED:
                self._waitlist.remove(player_id)
                return None

            # A confirmed player leaving frees exactly one seat.
            self._confirmed.remove(player_id)

            # Nobody waiting? Then the seat just stays open.
            if not self._waitlist:
                return None

            # Promote the person at the FRONT of the line (FIFO = fair).
            nxt = self._waitlist.popleft()
            self._confirmed.append(nxt)
            self._status[nxt] = Status.CONFIRMED
            return nxt   # tell the caller who got promoted (e.g. to email them)

    def confirmed(self) -> list[str]:
        with self._lock:
            # Return a COPY. Handing out the real list would let callers mutate our
            # internal state without holding the lock.
            return list(self._confirmed)

    def waitlist(self) -> list[str]:
        with self._lock:
            # list(deque) also makes a copy, and converts it to a plain list.
            return list(self._waitlist)
