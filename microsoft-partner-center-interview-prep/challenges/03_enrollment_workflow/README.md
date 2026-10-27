# 03 — Partner Enrollment Workflow (State Machine + Idempotency)

**Theme:** partner onboarding and program enrollment, which this team owns. A real
enrollment API sits behind flaky networks and retrying clients, so **the same request
will arrive twice**. Whether you can make that safe is a standard senior distributed-
systems question. Coding-wise it's a hash-map-driven state machine plus careful edge
cases. It's the "clean, maintainable code" kind of round, not an algorithm puzzle.

## States and transitions

```
                submit                 approve
  DRAFT ─────────────────► PENDING ─────────────► ACTIVE ◄──┐
                             │  ▲                   │       │ reinstate
                      reject │  │ submit     suspend│       │
                             ▼  │                   ▼       │
                          REJECTED              SUSPENDED ──┘

  The 3rd rejection goes to LOCKED instead of REJECTED. LOCKED is terminal.
```

| Event | Allowed from | Goes to |
|---|---|---|
| `submit` | `DRAFT`, `REJECTED` | `PENDING` |
| `approve` | `PENDING` | `ACTIVE` |
| `reject` | `PENDING` | `REJECTED`, or `LOCKED` on the 3rd rejection |
| `suspend` | `ACTIVE` | `SUSPENDED` |
| `reinstate` | `SUSPENDED` | `ACTIVE` |

## API

```python
class InvalidTransition(ValueError): ...
class IdempotencyConflict(ValueError): ...

class EnrollmentService:
    def start(self, partner_id: str) -> str: ...
    def apply(self, partner_id: str, event: str, idempotency_key: str) -> str: ...
    def status(self, partner_id: str) -> str: ...
    def history(self, partner_id: str) -> List[Tuple[str, str]]: ...
```

## Rules

1. `start` creates an enrollment in `DRAFT` and returns `"DRAFT"`. Calling it again
   for an existing partner is **idempotent**: it changes nothing and returns the
   current status.
2. `apply` performs one transition and returns the new status.
3. **Idempotency keys are global** (not per partner):
   - Same key, same `(partner_id, event)` → return the **original** result. Don't
     apply the event again, and don't add it to history again. This holds even if
     the state has changed since then.
   - Same key, different `partner_id` or `event` → `IdempotencyConflict`.
4. An event not allowed from the current state → `InvalidTransition`. State and
   history are unchanged, and **the key is not consumed**, so the client can reuse it
   later.
5. Unknown event name (not one of the five) → `ValueError`.
6. Unknown `partner_id` for `apply`, `status`, or `history` → `KeyError`.
7. `history` returns the applied transitions in order as `(event, resulting_status)`
   pairs. `start` is not included. Return a copy.

## Hints

- Put the transition table in a dict: `{(state, event): next_state}`. Then rule 4 is
  a single lookup. Handle `reject` + the 3-rejection count as a special case after
  the lookup.
- Check the idempotency key **before** checking the transition. A retried `submit`
  must succeed even though `PENDING --submit-->` isn't a valid transition anymore.
- Save the key only **after** the transition succeeds.

## Run

```bash
pytest challenges/03_enrollment_workflow -v
```
