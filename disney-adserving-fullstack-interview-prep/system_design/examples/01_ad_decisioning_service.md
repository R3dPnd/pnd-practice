# Worked example: ad decisioning / qualification service

Practice prompt 1 from `../notes.md` — this is literally the team's actual system
("optimizing ad qualification and selection to make sure viewers always see the right ad
at the right time"). Use this to practice explaining it live, from scratch, as if
designing it, not reciting it.

- **Clarify**: Given a video-playback session hitting an ad break, return one ad (or an
  ordered list of candidates for a downstream auction) to play. Input context: user/
  device ID, content metadata (what show/event, live vs. VOD), ad-break duration, maybe
  geo. Non-functional: this call sits on the critical path of video playback — assume a
  tight budget, something like **single-digit-to-low-double-digit ms** for the
  decisioning hop itself, inside an overall ad-break-setup budget of maybe 50–200ms
  end-to-end including the network round trip and any real-time auction. Scale: assume
  very high QPS — every ad break, across Hulu+Disney+ESPN+, concurrently, so think in
  terms of tens of thousands of decisions/sec at peak (a live sports event alone could
  spike this).
- **Contract**: `POST /v1/ad-decision` → `{sessionId, contentContext, breakContext}` →
  response `{adId, creativeUrl, trackingUrls}` (or a ranked list if a downstream auction/
  header-bidding layer consumes it). The service doesn't know how the ad was *created*
  (that's a campaign-management system upstream) — it only qualifies and selects from an
  already-ingested candidate pool.
- **Architecture**:
  1. **Candidate retrieval**: pull a small candidate set of campaigns/creatives eligible
     for this content/geo/break-length from a pre-indexed store — not a live scan of all
     campaigns. This index is built/refreshed by an offline or near-real-time process,
     not computed per-request.
  2. **Eligibility filtering** (the hot path): apply hard constraints fast, cheapest
     checks first — targeting match, entitlement check (is this user even eligible for
     ads at all, e.g. ad-supported tier), **frequency cap check** (→ `examples/02`,
     usually a single Redis round trip), budget/pacing check (→ `examples/04`).
  3. **Ranking/selection**: among remaining eligible candidates, rank by whatever the
     business objective is (highest eCPM, pacing priority, fill-rate need) and pick the
     winner (or top-N for an auction).
  4. **Response + async side-effects**: return the decision synchronously; fire the
     "ad was selected" event to Kafka/Kinesis **asynchronously**, off the critical path,
     for downstream impression counting (→ `examples/03`) — decisioning latency must
     never depend on the event pipeline being healthy.
  5. **Fallback path**: if decisioning can't complete in budget (a dependency is slow,
     candidate pool is empty), serve a default "house ad" or slate rather than blocking
     playback — always have a fast, static fallback.
- **Deep dive** (likely steered here): the eligibility filter's performance under load.
  Keep hot-path state (frequency counts, budget remainders) in a fast KV store (Redis/
  ValKey) rather than a relational DB; keep relatively static config (campaign targeting
  rules) in a local in-memory cache refreshed on a short TTL or pushed via a
  config-change event, so the hot path almost never makes a network call for data that
  rarely changes.
- **Backend review pass**:
  - *Latency*: every hop on the synchronous path must have a strict timeout with a
    fallback — a single slow dependency (a partner integration, a cold cache) can't be
    allowed to blow the whole budget; fail fast to the house-ad fallback instead.
  - *Idempotency*: the decision call itself should be safe to retry (client-side retry
    on timeout) without double-counting — usually solved by generating an idempotency/
    request ID the downstream event pipeline dedupes on.
  - *Observability*: p50/p95/p99 decision latency, fallback-ad-serve rate (a rising rate
    is an early warning something upstream is degrading), per-dependency error rate.
  - *Loose coupling*: the event-logging path being down must never affect the decision
    path — this is the JD's "microservice encapsulation" phrase made concrete.
- **Tradeoffs**: keeping campaign config in a local cache trades a bit of staleness
  (a campaign pause takes up to one TTL cycle to propagate) for removing a network hop
  from the hot path — usually the right trade for a latency-critical read-heavy system;
  call this out explicitly as a conscious choice, not an oversight.
- **What I'd do differently with more time**: a shadow-mode ranking model comparison (run
  a new ranking algorithm's output alongside the live one without acting on it) to
  validate changes before they affect real ad delivery.
