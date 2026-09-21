# Worked example: ad pacing / budget service with third-party integration

Practice prompt 4 from `../notes.md`. JD names "correct pacing" and "third-party
systems" as integration responsibilities. Pacing means: a campaign has a budget (or a
target impression count) meant to be spent **evenly across its flight**, not burned in
the first hour — and this budget check has to happen under the same tight latency
constraint as everything else in decisioning, while staying accurate under massive
concurrency.

- **Clarify**: Is pacing "smooth" (evenly spread across the day/flight) or does it need
  to respect dayparting (e.g., more budget available during prime-time live sports)?
  Does overspend need to be strictly impossible, or "rare small overspend, corrected
  later" acceptable — same soft-vs-hard question as frequency capping, but pacing
  usually leans a little harder toward "must not meaningfully overspend," since it's
  directly tied to advertiser billing/trust.
- **Contract**: decisioning (`examples/01`) calls this as another eligibility/ranking
  input: `getPacingStatus(campaignId) → {eligible: bool, priorityScore}` — fast, hot-path
  call, same shape as the frequency-cap check.
- **Architecture**: the core hard problem is **distributed budget decrement under high
  concurrency without a single point of contention**. A naive "read remaining budget,
  check if request fits, decrement" from a shared relational row would serialize every
  ad decision globally for that campaign — far too slow at scale, and race-prone
  (two concurrent decisions both read "budget remaining," both proceed, overspend).
  Standard approaches:
  1. **Token-bucket-style local budget allocation**: periodically (e.g., every few
     seconds) allocate each decisioning-service instance/region a *slice* of the
     campaign's remaining budget to spend locally, atomically decremented in-memory or
     in a local Redis (same atomic-INCR-with-Lua pattern as `examples/02`) — no
     cross-instance coordination needed for every single request, only for the periodic
     reallocation.
  2. **Reconciliation**: the durable impression pipeline (`examples/03`) is the actual
     source of truth for spend; a background job periodically reconciles real spend
     against allocated budget and adjusts future allocations — corrects for the
     approximate nature of local token buckets.
  3. **Third-party integration**: if pacing/budget data or spend approval needs to sync
     with an external ad-partner/DSP system, that call must **never** be synchronous on
     the decisioning hot path — pull/cache their state on a schedule, or push updates
     into your own store asynchronously, and apply the same "encapsulation and loose
     coupling" principle: a slow or down third party degrades pacing accuracy, not ad
     serving itself.
- **Deep dive** (likely steered here): what happens when a third-party integration
  (e.g., an external DSP providing bid/eligibility data) is slow or returns errors.
  Apply resilience patterns: a strict timeout, a circuit breaker (stop calling a
  consistently-failing dependency for a cooldown period rather than piling up slow
  calls), and a sane fallback (treat the campaign as paced-normally / skip it from this
  round, rather than blocking the whole decision) — see `../spring_boot/notes.md` for
  the actual Spring/Resilience4j-flavored version of this pattern.
- **Backend review pass**:
  - *Latency*: local/cached budget checks only on the hot path — never a synchronous
    call to a relational DB or a third party per ad decision.
  - *Consistency*: explicitly eventually consistent (local allocation + periodic
    reconciliation), with a stated bound on how wrong it can get before reconciliation
    corrects it (e.g., "at most one reallocation cycle's worth of overspend").
  - *Resilience*: third-party timeouts/circuit breakers, covered above — this is the
    concrete version of "integrations with...third-party systems" from the JD.
  - *Observability*: pacing accuracy (actual spend rate vs. target spend rate over the
    flight), circuit-breaker open/close events per partner integration.
- **Tradeoffs**: local token-bucket allocation trades perfect real-time accuracy for
  throughput and low latency — the right trade here, same reasoning as frequency
  capping, because the reconciliation loop bounds how wrong it can get.
- **What I'd do differently with more time**: make the reallocation cycle
  adaptive — shorter intervals (more coordination overhead, tighter accuracy) for
  small/ending-soon campaigns where overspend risk is higher, longer intervals for
  large steady campaigns where the local approximation error matters less proportionally.
