# 04 — Login throttle / lockout (Python)

Full rules and talking points: [`../../../challenges/04_login_throttle/README.md`](../../../challenges/04_login_throttle/README.md).

```python
th = LoginThrottle(max_failures, window_s, lockout_s, clock=time.monotonic)
th.allowed(user) -> bool
th.record_failure(user)
th.record_success(user)   # clears failure history
```
Lock once `max_failures` failures fall within the trailing `window_s`; lockout lasts
`lockout_s` from the triggering failure; failures while locked are ignored; fresh start after.
Tests use the shared `fake_clock` fixture from `python/conftest.py`.
