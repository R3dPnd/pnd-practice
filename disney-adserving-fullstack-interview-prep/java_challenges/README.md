# Java challenges

Five practice problems, plain Java (no build tool required beyond a JDK — no JDK is
installed in this environment, use your own IDE or an online runner). Picked to match
this JD's specific language — *"high-throughput, low-latency microservices"* is really
asking about **concurrency correctness and performance**, not algorithmic cleverness, so
4 of the 5 are concurrency problems modeled directly on the ad-serving systems in
`../system_design/examples/`, not generic LeetCode.

## Pattern (same idea as `../../disney-frontend-interview-prep/challenges/`, Java-flavored)

Each `NN_topic/` has:
- `README.md` — problem statement, constraints, and which real ad-serving system it
  models
- `Practice.java` — stub class with `// TODO` method bodies and a `main()` self-check
  with expected-output comments (same self-check pattern as
  `../../costco-booking-platform/practice/java/JavaExercises.java` already in this repo)
- `Solution.java` — reference implementation, same class name (`Solution`) so it drops
  in as a like-for-like replacement once you rename the class in `Practice.java` to
  compare

Recommended loop: read the `README.md`, implement `Practice.java` against the clock
(30–40 min), run it (`javac Practice.java && java Practice`), then diff against
`Solution.java` and say out loud what you'd do differently — same rehearsal habit the
JS challenges repo recommends.

## Index

| # | Challenge | Concurrency primitive | Models |
|---|---|---|---|
| 01 | `01_thread_safe_frequency_cap` | `synchronized` + `LinkedHashMap` LRU eviction, correctness under concurrent access | `system_design/examples/02` — frequency-cap counter |
| 02 | `02_token_bucket_pacer` | `ReentrantLock`/atomic refill math, scheduled-refill correctness | `system_design/examples/04` — pacing/budget token bucket |
| 03 | `03_concurrent_impression_counter` | `ConcurrentHashMap` + `AtomicLong`, idempotent dedupe | `system_design/examples/03` — impression counting, at-least-once redelivery |
| 04 | `04_producer_consumer_ad_queue` | `BlockingQueue`, producer/consumer, graceful shutdown | `system_design/examples/01`/`03` — decoupling ingestion from processing |
| 05 | `05_ad_qualification_selection` | Java Streams, `Comparator`, `Optional` (not concurrency — fundamentals/functional-style) | `system_design/examples/01` — eligibility filter + ranking |

## Why concurrency, specifically

Reported field notes (see `../README.md`) say Disney Streaming loops weight
**performance and concurrency** heavily, and this JD's own language ("high-throughput,
low-latency microservices") backs that up directly. If the technical round is a live
Java exercise, thread-safety bugs (missing synchronization, non-atomic
check-then-act races, forgetting `volatile`/atomics) are exactly the kind of subtle
mistake a senior candidate is expected to catch in their own code without being told to
look for it — practice writing these correctly the first time, not just fixing them
after a hint.
