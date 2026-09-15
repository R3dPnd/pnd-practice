# Worked example: rate-limited public API gateway

Practice prompt 5 from `../notes.md`: a rate-limited public API gateway in front of
several internal services. Full run through the framework in `../notes.md`,
compressed to the key beats — this is what "narrate it out loud" should actually
sound like, not a diagram substitute. Use it to check your own mock reps against, not
to memorize verbatim.

- **Clarify**: Per-client (API key) or per-IP limiting, or both (assume both — IP as a
  cheap first line, API key/account as the real limit); what happens on throttle
  (assume `429` + `Retry-After` header, not a silent drop); is this in front of one
  service or many (assume many internal services behind one gateway).
- **API**: gateway is transparent to callers — same paths as the backing services —
  but every response can carry `X-RateLimit-Remaining` / `Retry-After` headers.
- **Architecture**: client → edge/gateway (authN + rate limiting happens here, before
  any request reaches an internal service) → the `01_rate_limiter` token-bucket logic,
  but the bucket state has to live somewhere *shared* across many gateway instances —
  a fast shared store (Redis-equivalent) holding per-client bucket state, checked with
  an atomic increment-and-check op to avoid a race between concurrent gateway nodes.
- **Deep dive** (likely steered here): making the shared counter fast and correct
  under concurrency — atomic ops (e.g. a Lua script / `INCR`+`EXPIRE` combo) so two
  gateway nodes handling the same client's requests at the same instant can't both
  read stale state and let a burst through past the limit.
- **Security pass**:
  - AuthN at the edge, before rate limiting is even applied per-account (an
    unauthenticated request still gets the cheaper per-IP limit as a DoS backstop).
  - Distinguish abusive traffic from a legitimate retry storm — a client that respects
    `Retry-After` shouldn't be penalized further; one that ignores it can be
    escalated to a temporary hard block.
  - Self-attack pass: "I'd target the shared limiter store itself — if Redis is a
    single point of failure, an attacker who can degrade it removes rate limiting
    fleet-wide." → mitigate with a fail-safe default (fail *closed*, i.e. apply a
    conservative fallback limit, not fail-open/unlimited, if the shared store is
    unreachable).
  - Also: distributed clients rotating IPs/API keys to evade per-identity limits —
    layer in anomaly detection (the `08_login_attempt_monitor` pattern) on top of
    hard limits, not as a replacement for them.
- **Tradeoffs / scale**: a shared store adds a network hop to every request but is
  necessary for correctness across multiple gateway instances; a purely local
  (per-instance) bucket would be faster but let a client get N-times the intended
  limit by spreading requests across N gateway nodes — explicitly not acceptable here.
- **What I'd do differently**: tiered limits (burst allowance + sustained rate, like
  a real token bucket's burst capacity) instead of a flat cap, and per-endpoint limits
  since a cheap `GET` and an expensive `POST` shouldn't share one budget.
