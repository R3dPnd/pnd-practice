"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Before coding, write the transition table down as data and confirm it with the
   interviewer. A dict of `(state, event) -> next_state` beats a chain of if/elif. It
   can be read at a glance, it's easy to extend, and "is this allowed" becomes one lookup.
2. Get the order of checks right. This is where the bugs are:
   validate the event name → look up the partner → **check the idempotency key** →
   check the transition → mutate → record the key. A key check that comes after the
   transition check breaks retries, because a retried submit would hit
   PENDING+submit, which is invalid.
3. Store the full request identity with each key, `(partner_id, event)`, not just the
   result. Otherwise you can't tell a real retry from a client bug that reused a key.

COMMON INTERVIEWER FOLLOW-UPS:
- "Two requests with the same key arrive at the same time on two servers?" — this
  in-memory dict doesn't handle it. In production, the key insert and the state change
  must be atomic. Options: a unique constraint on the key column in the same DB
  transaction as the state update, or an optimistic-concurrency version/ETag on the
  enrollment row (compare-and-swap). This is the real answer they want.
- "Keys grow forever?" — give them a TTL (Stripe uses 24h). Clients must not retry
  after the TTL, and that's part of the API contract.
- "Approval calls an external verification service (tax ID, domain)." — don't make
  that call inside the request. Move to PENDING, put a verification job on a queue,
  and have the worker apply `approve`/`reject` with its *own* idempotency key derived
  from the job id. Worker retries then become safe for free.
- "How would you audit this?" — `history` is already an event log. Make it the
  source of truth (event sourcing) and derive `status` from it. Then add actor and
  timestamp to each entry.
"""
from typing import Dict, List, Tuple

MAX_REJECTIONS = 3

_TRANSITIONS: Dict[Tuple[str, str], str] = {
    ("DRAFT", "submit"): "PENDING",
    ("REJECTED", "submit"): "PENDING",
    ("PENDING", "approve"): "ACTIVE",
    ("PENDING", "reject"): "REJECTED",
    ("ACTIVE", "suspend"): "SUSPENDED",
    ("SUSPENDED", "reinstate"): "ACTIVE",
}
_EVENTS = {event for _, event in _TRANSITIONS}


class InvalidTransition(ValueError):
    pass


class IdempotencyConflict(ValueError):
    pass


class EnrollmentService:
    def __init__(self):
        self._status: Dict[str, str] = {}
        self._rejections: Dict[str, int] = {}
        self._history: Dict[str, List[Tuple[str, str]]] = {}
        # key -> (partner_id, event, resulting_status)
        self._keys: Dict[str, Tuple[str, str, str]] = {}

    def start(self, partner_id: str) -> str:
        if partner_id not in self._status:
            self._status[partner_id] = "DRAFT"
            self._rejections[partner_id] = 0
            self._history[partner_id] = []
        return self._status[partner_id]

    def apply(self, partner_id: str, event: str, idempotency_key: str) -> str:
        if event not in _EVENTS:
            raise ValueError(f"unknown event {event!r}")
        current = self.status(partner_id)

        if idempotency_key in self._keys:
            seen_partner, seen_event, result = self._keys[idempotency_key]
            if (seen_partner, seen_event) != (partner_id, event):
                raise IdempotencyConflict(
                    f"key {idempotency_key!r} already used for {seen_event!r} on {seen_partner!r}"
                )
            return result

        next_status = _TRANSITIONS.get((current, event))
        if next_status is None:
            raise InvalidTransition(f"cannot {event!r} from {current!r}")

        if event == "reject":
            self._rejections[partner_id] += 1
            if self._rejections[partner_id] >= MAX_REJECTIONS:
                next_status = "LOCKED"

        self._status[partner_id] = next_status
        self._history[partner_id].append((event, next_status))
        self._keys[idempotency_key] = (partner_id, event, next_status)
        return next_status

    def status(self, partner_id: str) -> str:
        if partner_id not in self._status:
            raise KeyError(partner_id)
        return self._status[partner_id]

    def history(self, partner_id: str) -> List[Tuple[str, str]]:
        if partner_id not in self._history:
            raise KeyError(partner_id)
        return list(self._history[partner_id])
