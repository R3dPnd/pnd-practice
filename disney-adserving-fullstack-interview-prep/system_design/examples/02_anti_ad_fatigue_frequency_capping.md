# Worked example: anti-ad-fatigue / frequency capping

Practice prompt 2 from `../notes.md`. JD names "anti-ad fatigue systems" explicitly as a
supporting component this team builds — this is the classic **frequency capping**
problem: don't show the same viewer the same ad (or the same campaign) more than N times
per some window (per break, per day, per campaign lifetime).

- **Clarify**: What's the cap granularity — per creative, per campaign, or both? What's
  the window — per session, rolling 24h, campaign lifetime? Does it need to be *exact*
  (never one impression over) or is "close enough, rare small overage acceptable" fine?
  For ad fatigue specifically, the answer is almost always **soft/approximate is fine** —
  the goal is a better viewer experience, not a hard business-critical guarantee like
  billing, and that relaxation is exactly what makes the fast-path design below work.
- **Contract**: the decisioning service (`examples/01`) calls this as one of its
  eligibility filters: `checkAndIncrement(userId, campaignId, window) → boolean eligible`.
  Called on the synchronous hot path, so it needs to be a single fast round trip, not a
  multi-step transaction.
- **Architecture**: a Redis/ValKey-backed counter, keyed by `{userId}:{campaignId}:{window}`,
  with the window's TTL set on the key so old windows expire automatically instead of
  needing a cleanup job. The check-and-increment needs to be **atomic** to avoid a
  race where two concurrent requests both read "count=2, cap=3" and both increment,
  overshooting the cap — solved with a Redis Lua script (`INCR` + compare, evaluated
  atomically server-side) or Redis's native `INCR` + a second pass, not a
  read-then-write from the application.
- **Deep dive** (likely steered here): multi-region consistency. If Redis is deployed
  per-region for latency (a US-East viewer's frequency check shouldn't cross-region), a
  user's counts can diverge slightly across regions — accept this explicitly as the
  tradeoff for the "approximate is fine" requirement above, rather than trying to build
  cross-region strong consistency for a soft cap. If asked "what if this absolutely must
  be exact," the honest answer is: it gets much more expensive (a single consistent
  source of truth, likely DynamoDB global tables with conditional writes, at higher
  latency) — and push back on whether ad fatigue actually needs that guarantee.
- **Backend review pass**:
  - *Latency*: single Redis round trip, sub-millisecond typically — this is exactly the
    kind of check that must stay off any path that would call a relational DB.
  - *Consistency*: explicitly eventually-consistent across regions, by design (see
    above) — state this instead of letting it be an unstated gap.
  - *Failure mode*: if Redis is unreachable, **fail open** (let the ad show) rather than
    fail closed (block all ads) — a missed cap is a minor UX annoyance; blocking all ad
    delivery because a cache is down is a revenue-impacting outage. This fail-open-vs-
    fail-closed decision, stated explicitly, is a strong signal in this kind of round.
  - *Observability*: cap-hit rate per campaign (an unusually high hit rate might mean
    too small a candidate pool for that targeting segment, a business signal, not just
    an engineering one).
- **Tradeoffs**: per-region Redis (fast, eventually consistent) vs. a single global
  strongly-consistent store (slow, always correct) — for ad fatigue, per-region wins;
  for a hard business rule like total ad slots sold, it wouldn't.
- **What I'd do differently with more time**: a periodic reconciliation job that
  aggregates true impression counts (from the durable event pipeline in `examples/03`)
  back into the cache, so any drift from the approximate hot-path counting
  self-corrects rather than accumulating indefinitely.
