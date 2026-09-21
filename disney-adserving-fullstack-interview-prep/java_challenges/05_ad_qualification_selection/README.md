# 05 — Ad qualification & selection (Streams/Comparator/Optional)

**Theme:** Java 8+ functional style — not concurrency, straight fundamentals. Models the
eligibility-filter-then-rank step from
`../../system_design/examples/01_ad_decisioning_service.md`.

## Problem

```java
record AdCandidate(String id, boolean targetingMatch, boolean entitled,
                    double eCpm, double remainingBudget) {}

// Eligible = targetingMatch && entitled && remainingBudget > 0.
// Among eligible candidates, return the one with the HIGHEST eCPM; ties broken by
// id ascending (lexicographic). Optional.empty() if none are eligible.
Optional<AdCandidate> selectBestAd(List<AdCandidate> candidates) { /* ... */ }

// Same eligibility filter, but return ALL eligible candidates, sorted highest-eCPM
// first, ties broken by id ascending — the ranked-list-for-an-auction case.
List<AdCandidate> rankEligible(List<AdCandidate> candidates) { /* ... */ }
```

## Constraints / edge cases to think about

- A candidate is only eligible if **all three** conditions hold — a common mistake is
  to filter on eCPM before applying targeting/entitlement/budget checks.
- Tie-breaking matters and is checked by the tests: two candidates at the exact same
  eCPM must resolve deterministically (ascending `id`), not by whichever happened to
  come first in iteration order.
- `Comparator.comparingDouble(...).reversed().thenComparing(...)` is the idiomatic way
  to express "descending by X, ascending by Y as tiebreaker" in one line — worth having
  this exact pattern memorized, since "sort by X descending with a tiebreaker" is an
  extremely common phrasing in both take-home and live-coding rounds.
- `selectBestAd` returning `Optional` (rather than `null` or throwing) for the
  "no eligible candidates" case is the idiomatic Java 8+ answer — a senior candidate
  should reach for this without being prompted.

## Why this matters for the role

This is literally "optimizing ad qualification and selection" from the JD's own
description of the Decisioning Fleet's job, reduced to its core algorithm. In a real
system this candidate list would be much larger and this logic would run on the
critical path per `system_design/examples/01` — so beyond correctness, be ready to talk
about it being a single linear pass (`O(n)` filter + `O(n log n)` sort, or `O(n)` if you
only need the single best one via `min`/`max` instead of a full sort).

## Run

```bash
javac Practice.java && java Practice
javac Solution.java && java Solution
```
