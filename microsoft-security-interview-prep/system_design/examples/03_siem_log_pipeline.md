# Worked example: centralized security log ingestion pipeline (mini SIEM)

Practice prompt 3 from `../notes.md`: services ship logs, the system needs to detect
suspicious patterns and alert. Full run through the framework in `../notes.md`,
compressed to the key beats — this is what "narrate it out loud" should actually
sound like, not a diagram substitute. Use it to check your own mock reps against, not
to memorize verbatim.

- **Clarify**: What ships logs (assume: hundreds of internal services, fairly high
  volume — say 1M events/sec at fleet scale), what's the detection latency requirement
  (assume near-real-time for a subset of high-value rules like brute-force login
  patterns, batch/nightly acceptable for broader analytics), retention requirement
  (assume compliance-driven, e.g. 1 year).
- **API**: services push via a lightweight SDK/sidecar to `POST /ingest` (or more
  realistically, write to a local agent that batches to a streaming pipeline) —
  no synchronous per-event HTTP call from a hot path in a real design.
- **Architecture**: service → local log agent → stream (Kafka-equivalent) → a
  redaction/normalization stage (this is `04_log_redactor`'s job at fleet scale —
  strip secrets/PII *before* anything hits durable storage, not after) → fan-out to
  (a) a real-time rules engine for alerting (the `08_login_attempt_monitor`
  sliding-window pattern, running per-account/per-IP over the stream) and (b) a
  cold-storage/data-warehouse sink for retention and batch analytics.
- **Deep dive** (likely steered here): the redaction stage — it must run before the
  fan-out, be fail-closed (if redaction can't confidently parse a log line, drop or
  quarantine it rather than pass it through unmasked), and be versioned/testable
  against known secret-shaped patterns (API keys, tokens, connection strings).
- **Security pass**:
  - Redaction before durable storage, always — the log pipeline itself is a huge
    target if it accumulates unmasked secrets at rest.
  - Access control on query/read access to the log store — logs about production
    systems are themselves sensitive; not every engineer should be able to query
    everything.
  - Auditability of *who queried what* in the SIEM itself (audit-the-audit-log).
  - Self-attack pass: "I'd target the redaction stage — craft a secret in a format the
    redactor's regex doesn't recognize, or split it across two log fields to evade a
    single-field pattern match." → argue for defense in depth (multiple detection
    patterns, periodic re-scans of stored logs as detection rules improve).
- **Tradeoffs / scale**: real-time path only carries high-value rules to keep it cheap
  and fast; everything else goes through cheaper batch processing — explicitly cutting
  "real-time for everything" as a scope/cost tradeoff.
- **What I'd do differently**: a feedback loop where confirmed incidents retroactively
  tune the real-time rule set, and anomaly-detection (not just fixed-threshold rules)
  for patterns that don't fit a simple sliding-window count.
