# Backend / Distributed Systems Design — prep notes

Companion to `../../disney-frontend-interview-prep/frontend_design/notes.md`'s
framework, but for the backend-weighted round this JD's stack (microservices, Spring
Boot, Kafka/Kinesis, DynamoDB, Redis/ValKey, AWS) implies. Same discipline as the FE
version: clarify out loud, state assumptions, do the review pass explicitly even if not
asked.

## Framework

1. **Clarify functional + non-functional requirements before drawing anything.**
   - Functional: what's the actual request/response? For ad decisioning specifically —
     given a user + ad-break context, return one ad (or ranked candidates) from a pool.
   - Non-functional, and get numbers, don't assume: **QPS** (how many ad decisions/sec
     across Hulu+Disney+ESPN+ combined — think large, this is a top-5 streaming
     footprint), **latency budget** (ad decisioning is on the critical path of video
     playback — a slow decision either delays the stream or forces a fallback ad,
     so this is a tight, single-digit-to-low-double-digit-ms-per-hop budget, not a
     "returns in under a second" budget), **consistency requirements** (is slightly
     stale frequency-cap data acceptable, or must it be exact — usually acceptable,
     see `examples/02`), **availability target** (an ad *must* play even if decisioning
     fails — what's the fallback?).
2. **Back-of-envelope capacity math.** Even rough numbers signal seniority: pick a QPS,
   multiply out storage/throughput, sanity-check against a single Redis/DynamoDB
   instance's known limits, decide if you need sharding/partitioning. Say the numbers
   out loud — the interviewer is grading that you reach for this, not that you get an
   exactly correct answer.
3. **Data model + API contract.** What's the request/response shape for the core
   endpoint? What does the data model look like for the entities involved (campaign,
   creative, targeting rule, user/session, impression event)? Which store fits which
   entity — this is where DynamoDB (high-throughput key-value, e.g. per-user frequency
   state) vs. a relational store (campaign config, low write volume, needs joins) vs.
   Redis/ValKey (hot-path cache, sub-ms reads) actually differ, and you should justify
   the choice, not just name-drop the JD's preferred-quals list.
4. **High-level architecture.** Draw the request path end to end: client/player →
   API gateway → decisioning service → [candidate retrieval, eligibility filtering,
   ranking] → response, plus the async side paths (impression/event logging to Kafka/
   Kinesis, downstream aggregation). Call out where a call is synchronous-on-the-critical-
   path vs. fire-and-forget-async — this distinction is the single biggest "do they
   actually understand latency budgets" signal in an ad-serving design.
5. **Deep dive** wherever steered — likely one of: the eligibility/ranking algorithm,
   the frequency-cap check, the event pipeline, or a failure-mode question ("what
   happens if Redis is down / a third-party ad partner times out").
6. **Backend review pass** (below) — do this even unprompted.
7. **Tradeoffs and what breaks first at 10x scale.** What's the first bottleneck as QPS
   grows — usually the hot-path cache tier or a single-partition hotspot (e.g. one
   viral live event driving all traffic to one ad-break config).
8. **What you'd cut/defer with less time**, stated explicitly.

## Backend review pass

| Concern | Ask yourself |
|---|---|
| **Latency** | What's on the synchronous critical path vs. async? Where's the p99 budget spent — is any hop a cache-or-die (e.g., "if this Redis lookup misses, do we serve a fallback ad or block")? |
| **Idempotency & exactly-once-ish delivery** | Ad events (impressions, clicks) travel over at-least-once messaging (Kafka/Kinesis) — is the consumer-side aggregation idempotent (dedupe by an event ID), or will a redelivered message double-count an impression/overspend a budget? |
| **Consistency model** | Which reads need to be strongly consistent (a budget check before spending money) vs. which can be eventually consistent (a frequency-cap count that's "close enough")? Naming this distinction explicitly is a strong signal. |
| **Failure isolation / loose coupling** | If a third-party ad partner or a downstream analytics pipeline is slow or down, does that ever block ad decisioning itself? (JD explicitly names "micro-service encapsulation and loose coupling" — this is the concrete version of that phrase: a slow non-critical dependency must never take down the critical path. Timeouts + circuit breakers, see `../spring_boot/notes.md`.) |
| **Observability** | JD explicitly asks for this: what metrics would page someone (ad-decision latency p50/p95/p99, fallback-ad-serve rate, error rate per partner integration), and what's a dashboard vs. an alert vs. just a log line? |
| **Scalability / hotspots** | Any single partition key (a campaign ID, a user ID) that could get hot under a viral event or a whale advertiser? How would you shard/cache around it? |
| **Security/compliance** | Frequency-cap and targeting data is tied to user identifiers — what's PII here, and does it need to be pseudonymized/short-TTL'd rather than stored indefinitely? |

## Practice prompts

1. **Ad decisioning / qualification service** — the actual team's core system.
   → `examples/01_ad_decisioning_service.md`
2. **Anti-ad-fatigue / frequency capping** — explicitly named in the JD as a supporting
   component this team builds. → `examples/02_anti_ad_fatigue_frequency_capping.md`
3. **Impression counting pipeline** — explicitly named in the JD.
   → `examples/03_impression_counting_pipeline.md`
4. **Ad pacing / budget service with third-party integration** — JD names "correct
   pacing" and "third-party systems" as integration points. → `examples/04_ad_pacing_budget_service.md`

## Worked walkthroughs

1. [Ad decisioning service](examples/01_ad_decisioning_service.md)
2. [Anti-ad-fatigue / frequency capping](examples/02_anti_ad_fatigue_frequency_capping.md)
3. [Impression counting pipeline](examples/03_impression_counting_pipeline.md)
4. [Ad pacing / budget service](examples/04_ad_pacing_budget_service.md)

## Day-of reminders

- Get a number before you architect anything — QPS, latency budget, data size. An
  ad-decisioning system designed for 100 req/s looks nothing like one designed for
  100K req/s, and guessing wrong signals you don't think about scale by default.
- State the sync/async boundary explicitly and early — it's the single most
  ad-serving-specific piece of judgment this round can test.
- If you don't know a specific AWS service's exact limits, reason from the general
  shape (key-value vs. relational vs. streaming) rather than guessing a number
  confidently — same advice as the FE repo's design notes.
- These worked examples reason from general ad-tech system-design patterns (Netflix's
  published ads pipeline post, standard RTB-style latency budgets), not Disney-specific
  internals — say so if asked, don't imply inside knowledge you don't have.
