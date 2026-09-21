# 04 — Producer/consumer ad-event pipeline

**Theme:** `BlockingQueue`, graceful shutdown. Models the "decouple ingestion from
processing" pattern from `../../system_design/examples/01_ad_decisioning_service.md`
(fire the decision event async, off the critical path) and
`../../system_design/examples/03_impression_counting_pipeline.md` (ingestion writes to a
durable log; a separate consumer processes it).

## Problem

```java
class EventPipeline {
    EventPipeline(int capacity) { /* starts a background consumer */ }

    // Producer side: enqueue an event. Blocks (backpressure) if the internal queue
    // is at capacity — never silently drops an event.
    void submit(String event) throws InterruptedException { /* ... */ }

    // Signals no more events are coming, waits for the consumer to finish processing
    // every already-submitted event (in submission order), then returns them.
    List<String> shutdownAndDrain() throws InterruptedException { /* ... */ }
}
```

## Constraints / edge cases to think about

- **Never drop an event.** `submit` must block, not fail or silently discard, when the
  queue is full — this is what "ingestion is protected, but never lossy" means in
  practice. `BlockingQueue.put()` gives you this for free; don't reach for a
  non-blocking `offer()` and swallow the false return.
- **Ordering.** Events must be processed in the order they were submitted — a single
  consumer thread draining a FIFO queue (`ArrayBlockingQueue`) gives you this trivially;
  a thread *pool* of consumers would not, without extra work, so keep it to one consumer
  thread for this exercise.
- **Graceful shutdown, not abrupt.** `shutdownAndDrain` must wait for every
  already-queued event to actually finish processing before returning — a "poison pill"
  sentinel value pushed onto the same queue (so it's processed strictly after every real
  event ahead of it) is the standard pattern; the consumer loop exits when it sees the
  sentinel, and the caller `Thread.join()`s the consumer to know it's actually done.

## Why this matters for the role

This is the shape of "enhance observability with metrics" and "high-throughput
microservices" put together: real systems fire events onto a queue/log rather than
processing synchronously, specifically so a slow or failing consumer never blocks the
producer (the ad-serving critical path). Getting shutdown semantics right (not losing
in-flight work when a service restarts/deploys) is a very real operational concern, not
just an interview exercise.

## Run

```bash
javac Practice.java && java Practice
javac Solution.java && java Solution
```
