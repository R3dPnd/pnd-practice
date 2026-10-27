# 03 — Event registration with capacity + waitlist (Python)

Full rules and talking points: [`../../../challenges/03_event_registration/README.md`](../../../challenges/03_event_registration/README.md).

```python
e = Event(capacity)
e.register(player_id) -> Status          # Status.CONFIRMED / Status.WAITLISTED; raises AlreadyRegistered
e.cancel(player_id) -> str | None         # promoted player id; raises NotRegistered
e.confirmed() -> list[str]                # copies, in order
e.waitlist() -> list[str]
```
Must be thread-safe (`threading.Lock`). Python note: the GIL does **not** make
check-then-append atomic — the test hammers it from 50 threads.
