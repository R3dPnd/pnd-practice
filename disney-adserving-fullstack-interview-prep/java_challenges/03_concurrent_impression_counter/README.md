# 03 — Concurrent impression counter (idempotent dedupe)

**Theme:** `ConcurrentHashMap` + atomic dedupe. Models the durable impression-counting
pipeline from `../../system_design/examples/03_impression_counting_pipeline.md` — Kafka/
Kinesis deliver **at-least-once**, so the same impression event can arrive twice, and the
consumer must not double-count it.

## Problem

```java
class ImpressionCounter {
    // Records one impression for campaignId, deduped by impressionId. Returns true
    // if this was a NEW impression (and the campaign's count was incremented), false
    // if impressionId was already seen (no increment — a safe no-op replay).
    boolean record(String campaignId, String impressionId) { /* ... */ }

    long getCount(String campaignId) { /* ... */ }
}
```

## Constraints / edge cases to think about

- **The dedupe check and the increment must not race.** If 100 threads all call
  `record("campaignB", "dup-imp")` concurrently (simulating a redelivery storm), exactly
  **one** of them may count it — not zero, not more than one. A naive
  "if (!seen.contains(id)) { seen.add(id); count++ }" has a check-then-act race between
  two threads that both pass the `contains` check before either calls `add`.
  `Set<String>` backed by `ConcurrentHashMap.newKeySet()` has an atomic `add()` that
  returns whether the element was newly added — use that return value as your
  single source of truth, don't check-then-add separately.
- Distinct impression IDs submitted concurrently must **all** be counted — don't
  over-correct into a design that also drops legitimately-new events.
- `getCount` for a campaign with zero recorded impressions should return `0`, not throw.

## Why this matters for the role

This is the single most-cited correctness property in Netflix's own published post on
their ads event pipeline (see `../../README.md` sources) and is exactly what "impression
counting pipelines" in the JD is asking you to be able to reason about: at-least-once
delivery is a given at this scale, so idempotent consumption is not optional.

## Run

```bash
javac Practice.java && java Practice
javac Solution.java && java Solution
```
