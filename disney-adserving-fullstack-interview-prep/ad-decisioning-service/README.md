# ad-decisioning-service

A real, runnable Spring Boot project — Parts 1 (DI/layering), 2 (REST + validation), 3
(centralized exception handling), and 9 (testing) of `../spring_boot/notes.md`, wired
together into one small service instead of isolated snippets. It's the eligibility-
filter-then-rank algorithm from `../java_challenges/05_ad_qualification_selection/`
sitting behind a real `POST /v1/ad-decision` endpoint, matching
`../system_design/examples/01_ad_decisioning_service.md`.

**In-memory only** — no real DynamoDB/Redis/Kafka wired up (would need running
infrastructure this environment doesn't have). `spring_boot/notes.md` Parts 4-8 (the
DynamoDB repository, Redis `@Cacheable`, Kafka producer/consumer, Resilience4j circuit
breaker, and the same Micrometer approach used here) stay as annotated reference code
there — read this project alongside those to see where each would plug in:
`AdCandidateRepository` is the seam where a real DynamoDB-backed repository would drop
in without `AdDecisionService` changing at all.

## Structure

```
controller/   AdDecisionController + request/response DTOs (spring_boot/notes.md Part 2)
service/      AdDecisionService — the actual selection algorithm + Micrometer metrics
              (Part 8's Timer/Counter pattern, applied for real here)
repository/   AdCandidateRepository — in-memory now, the seam for a real DynamoDB
              repository later (Part 4)
model/        AdCandidate record
exception/    AdNotEligibleException + @RestControllerAdvice (Part 3)
```

## Run it

```bash
mvn test              # 5 tests, all passing: 2 web-slice (MockMvc) + 3 service (Mockito)
mvn spring-boot:run    # starts on :8080
```

```bash
# Highest-eCPM eligible candidate wins; ties broken by id ascending
curl -X POST localhost:8080/v1/ad-decision -H "Content-Type: application/json" \
  -d '{"sessionId":"s1","contentId":"c1"}'
# → {"adId":"ad-2","campaignId":"campaignB","creativeUrl":"https://example.com/creative/b"}

curl localhost:8080/v1/ad-decision/candidates    # full ranked eligible list

# Validation failure → 400 with a clean error body (Part 3)
curl -X POST localhost:8080/v1/ad-decision -H "Content-Type: application/json" -d '{}'

curl localhost:8080/actuator/health
curl localhost:8080/actuator/metrics/ad.decision.latency   # the Part 8 Timer, live
```

## Extending it (good next reps)

- Swap `AdCandidateRepository`'s in-memory list for the DynamoDB-backed version in
  `../spring_boot/notes.md` Part 4 (needs a local DynamoDB — `docker run -p 8000:8000
  amazon/dynamodb-local` — or point at a real table).
- Add the frequency-cap check from `../java_challenges/01_thread_safe_frequency_cap/`
  as a filter in `AdDecisionService.decide()`, backed by Redis instead of the in-process
  version, using Part 5's `@Cacheable`-style setup as a starting point (frequency
  capping itself isn't cache-shaped, so it'd be a direct `RedisTemplate` call, not
  `@Cacheable` — good exercise in knowing when each fits).
- Publish an event on every decision using Part 6's Kafka producer, then write a
  consumer using the idempotent-counter logic from
  `../java_challenges/03_concurrent_impression_counter/`.
