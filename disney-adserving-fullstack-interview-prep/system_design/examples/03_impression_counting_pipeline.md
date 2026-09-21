# Worked example: impression counting pipeline

Practice prompt 3 from `../notes.md`. JD names "impression counting pipelines"
explicitly. This is the durable, source-of-truth counting system — distinct from the
fast/approximate frequency-cap counter in `examples/02`, which is a hot-path cache, not
the ledger. Netflix has published real detail on this exact problem for their own ads
launch (see README sources) — draw on that shape rather than guessing from scratch.

- **Clarify**: What counts as an "impression" — ad-served (decisioning returned an ad)
  or ad-actually-viewed (player fired a beacon confirming playback started/completed)?
  Almost always the latter is what actually matters for billing/reporting — decisioning
  returning an ad doesn't guarantee the viewer's player actually rendered it (they could
  have closed the app, hit a playback error, etc.). Who consumes these counts — billing/
  reconciliation (needs to be *exact*), real-time pacing (`examples/04`, needs to be
  *fast*), and reporting dashboards (needs to be *eventually complete*)? Different
  consumers, different consistency/latency needs off the same event stream.
- **Contract**: the video player fires a beacon (`POST /v1/impression-event` or a
  client-side event SDK call) when an ad actually plays, containing an idempotency key
  (a unique impression/request ID generated at decision time) plus campaign/creative/
  user context.
- **Architecture**: this is the classic **decouple ingestion from processing** pattern —
  1. **Ingestion**: a lightweight, highly available endpoint that does minimal
     validation and immediately writes the raw event to a durable log
     (**Kafka/Kinesis**) — this is the JD's "impression counting pipelines" literally.
     Ingestion must be fast and durable, never doing heavy processing inline.
  2. **Stream processing**: a consumer (Kafka Streams/Flink/a Lambda-per-Kinesis-shard)
     aggregates events — rolling counts per campaign/creative/time-bucket — and this is
     where **idempotency matters most**: Kafka/Kinesis are at-least-once, so a
     redelivered event must not double-count. Dedupe by the impression's unique ID
     (e.g., a bounded-time dedupe set, or a conditional/upsert write keyed by that ID
     so a replay is a no-op).
  3. **Durable storage**: aggregated counts land in DynamoDB (high write throughput,
     simple key-value access pattern: campaign+time-bucket → count) for anything that
     needs fast lookups (pacing, reporting APIs); raw events can also land in a
     data-lake/warehouse (S3 + Athena/Redshift-style) for offline analytics/billing
     reconciliation that doesn't need to be real-time.
  4. **Backpressure isolation**: this is the specific lesson from Netflix's published
     post — the ingestion/serving path must be protected from the processing path's
     failures. If the stream processor falls behind or the analytics store is down,
     Kafka/Kinesis buffers the backlog; ad *serving* (a completely separate system,
     `examples/01`) is never blocked by this, because it never talks to this pipeline
     synchronously.
- **Deep dive** (likely steered here): exactly-once-ish counting under redelivery. Walk
  through: consumer crashes after writing to DynamoDB but before committing its Kafka
  offset → on restart, re-processes the same event → the DynamoDB write must be an
  idempotent upsert (conditional on "have I seen this impression ID," or an additive
  counter keyed such that reprocessing the same ID is a no-op) rather than a blind
  increment, or you double-count.
- **Backend review pass**:
  - *Idempotency*: covered above — the single most important property of this pipeline.
  - *Backpressure/isolation*: covered above — never let this pipeline's health affect
    ad serving.
  - *Observability*: consumer lag (how far behind is processing — directly answers "how
    stale are pacing decisions right now"), dedupe-hit rate (an unexpectedly high rate
    might mean a client-side retry bug over-firing beacons).
  - *Consistency*: real-time counts (used by pacing) are explicitly eventually
    consistent and approximate; the offline data-lake path is the actual source of
    truth for billing reconciliation — say this distinction out loud.
- **Tradeoffs**: a single unified pipeline (real-time + billing from the same path) is
  simpler to build but couples a hard-consistency requirement (billing) to a
  low-latency one (pacing) — splitting them (real-time aggregate for pacing, batch
  reconciliation for billing) is more moving parts but lets each side optimize for what
  it actually needs.
- **What I'd do differently with more time**: a daily reconciliation job comparing
  real-time aggregated counts against the offline/batch source of truth, alerting on
  drift past a threshold — catches silent bugs in the streaming path before they become
  a billing dispute.
