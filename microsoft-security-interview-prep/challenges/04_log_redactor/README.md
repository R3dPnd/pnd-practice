# 04 — Secret Redactor for Logs

**Theme:** security-minded engineering. Secrets leaking into logs (then into a log
aggregator, then into who-knows-how-many engineers' search results) is a very real,
very common incident class — squarely in scope for a Security org.

## Problem

```python
def redact(text: str) -> str:
    """Return `text` with sensitive values replaced by "[REDACTED]".
    Must NOT alter any part of the string that isn't sensitive."""
```

Redact these patterns (case-insensitive on keywords):

1. **Key/value secrets** in the common `key=value`, `key: value`, or `key="value"`
   forms, for keys: `password`, `passwd`, `pwd`, `api_key`, `apikey`, `secret`,
   `token`, `access_key`. Replace only the *value*, keep `key=` intact, e.g.
   `password=hunter2` → `password=[REDACTED]`.
2. **Bearer tokens** in `Authorization: Bearer <token>` headers — redact the token,
   keep `Bearer` in place.
3. **AWS access key IDs** — pattern `AKIA` followed by 16 uppercase letters/digits,
   redact the whole thing regardless of context (no keyword needed).
4. **Credit-card-shaped numbers** — 16 digits, optionally grouped in 4s with spaces or
   dashes (`4111-1111-1111-1111`, `4111 1111 1111 1111`, `4111111111111111`) — redact
   the whole number.

Everything else in the string must pass through **unchanged**, including things that
merely *look* key-shaped but aren't secrets (e.g. `username=alice` must stay untouched).

## Examples

```
redact('user login: username=alice password=hunter2')
  -> 'user login: username=alice password=[REDACTED]'

redact('Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.abc.def')
  -> 'Authorization: Bearer [REDACTED]'

redact('leaked key AKIAABCDEFGHIJKLMNOP in config dump')
  -> 'leaked key [REDACTED] in config dump'

redact('card on file: 4111-1111-1111-1111')
  -> 'card on file: [REDACTED]'

redact('nothing sensitive here, just a normal_key=normal_value')
  -> 'nothing sensitive here, just a normal_key=normal_value'
```

## Hints

- Build this with `re` and a handful of named patterns, applied in sequence (or one
  combined alternation) — don't try to write one giant unreadable regex.
- Watch out for **greedy value matching**: `password=hunter2 next_field=x` should only
  redact `hunter2`, not swallow the rest of the line. Values typically stop at
  whitespace or a matching quote.
- Be ready to talk about what this *can't* catch (secrets not matching a known shape,
  secrets split across log lines, base64-blob secrets with no keyword) and what a more
  robust real-world approach looks like (structured logging + an explicit allowlist of
  loggable fields, rather than a denylist regex on free text).

## Run

```bash
pytest challenges/04_log_redactor -v
```
