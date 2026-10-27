# 04 — Login throttle / lockout

**Pattern:** sliding window per key, injected clock · **Domain:** Pokémon Trainer Club login

From AWS's public case study: TPCi moved Pokémon Trainer Club auth onto Aurora PostgreSQL and
used **DynamoDB with TTL** to track login attempts and deny entry past a threshold — cutting
bot login attempts ~90%. Build the in-memory version of that logic.

## Task

```go
th := NewThrottle(maxFailures, window, lockout, now)  // now func() time.Time
th.Allowed(user) bool
th.RecordFailure(user)
th.RecordSuccess(user)   // clears that user's failure history
```

- A user is **locked out** once they have `maxFailures` failures within the trailing `window`.
  The lockout lasts `lockout` from the failure that triggered it.
- While locked, `Allowed` is false. Failures recorded while locked are ignored.
- After the lockout ends, the user starts fresh (old failures don't count).
- Failures older than `window` fall out of the count.

## Talking points
- Map of users grows forever → in prod, that's exactly what DynamoDB TTL solves; in memory,
  prune on access or run a janitor.
- Key by username **and** IP? Credential stuffing uses many usernames per IP; spraying
  uses many IPs per username. Discuss both dimensions.
- COPPA/GDPR: Trainer Club has child accounts — don't log raw usernames/IPs carelessly.
