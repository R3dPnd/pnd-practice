# 01 — Thread-safe frequency cap

**Theme:** `synchronized` + bounded LRU eviction. Models the Redis-backed frequency-cap
counter from `../../system_design/examples/02_anti_ad_fatigue_frequency_capping.md`, but
as an in-process cache instead of a Redis round trip.

## Problem

```java
class FrequencyCap {
    FrequencyCap(int maxEntries) { /* ... */ }

    // Atomically checks whether `key` is under capPerWindow and, if so, increments
    // its count and returns true. If key is already at/over capPerWindow, returns
    // false WITHOUT incrementing.
    boolean tryRecord(String key, int capPerWindow) { /* ... */ }

    int currentCount(String key) { /* ... */ }
}
```

## Constraints / edge cases to think about

- **The check-then-increment must be atomic.** Two threads racing `tryRecord` on the
  same key must never both succeed past the cap — this is the exact race condition the
  real Redis version avoids with a Lua script (`INCR` + compare, evaluated atomically
  server-side). Here, a single lock around the whole check-and-increment is the
  in-process equivalent.
- **Bounded size with LRU eviction.** Once a new key would push the cache past
  `maxEntries`, evict the *least recently used* key — not the oldest inserted. Both
  `tryRecord` and `currentCount` count as "used" and should refresh a key's recency.
  `LinkedHashMap`'s access-order mode (`new LinkedHashMap<>(16, 0.75f, true)` +
  overriding `removeEldestEntry`) does this in a few lines — no hand-rolled doubly
  linked list needed, same trick as `../../../disney-frontend-interview-prep/challenges/09_memoize/`.
- Gotcha if you reach for `LinkedHashMap`: `Map.getOrDefault` does **not** refresh access
  order in `HashMap`/`LinkedHashMap` (it bypasses `get()` internally) — use `get()`
  explicitly and handle the `null` case yourself if you want reads to count as "used."

## Why this matters for the role

This is the actual shape of the hot-path eligibility check described in
`system_design/examples/01_ad_decisioning_service.md` — a single ad-decision request
racing thousands of others per second, all hitting the same shared counter for a popular
campaign. Getting the atomicity right here is exactly the kind of thing a live Java round
would be checking for, per this repo's field notes on Disney Streaming loops weighting
concurrency correctness.

## Run

```bash
javac Practice.java && java Practice
# then compare:
javac Solution.java && java Solution
```
