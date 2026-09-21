# Spring Boot code quiz

Annotated code-writing exercises, same `<details>` collapsible-answer pattern as
`../../costco-booking-platform/practice/rest/rest-quiz.md`. Not runnable/tested here (no
JDK/Maven in this environment — see repo `README.md`) — for live-coding or whiteboard
rehearsal, and to refresh Spring idioms if you've been React-only for a while. Covers the
JD's "preferred qualifications" list directly: SpringBoot, DynamoDB, Redis/ValKey, Kafka/
Kinesis, plus the "microservice encapsulation and loose coupling" and "observability"
language from the "Daily, you should bring"/"Responsibilities" sections.

Try writing each exercise from a blank file before expanding the answer.

---

## Part 1 — Dependency injection & layering

**Exercise:** Wire a `AdDecisionController` → `AdDecisionService` → `AdCandidateRepository`
chain using constructor injection (not field injection — know *why* constructor
injection is preferred: it makes dependencies explicit/final, and makes the class
trivially testable without Spring's container via `new AdDecisionService(mockRepo)`).

<details>
<summary>Answer</summary>

```java
@RestController
@RequestMapping("/v1/ad-decision")
public class AdDecisionController {
    private final AdDecisionService adDecisionService;

    public AdDecisionController(AdDecisionService adDecisionService) {
        this.adDecisionService = adDecisionService;
    }
    // endpoints below in Part 2
}

@Service
public class AdDecisionService {
    private final AdCandidateRepository adCandidateRepository;

    public AdDecisionService(AdCandidateRepository adCandidateRepository) {
        this.adCandidateRepository = adCandidateRepository;
    }
}

@Repository
public interface AdCandidateRepository extends CrudRepository<AdCandidate, String> {
    List<AdCandidate> findByCampaignActiveTrue();
}
```

With a single constructor, `@Autowired` on it is optional (Spring 4.3+ infers it) — but
some teams still require it explicitly for clarity/consistency; know both are correct.
`@RestController` = `@Controller` + `@ResponseBody` (every method's return value is
serialized straight to the response body, no view resolution). This wiring is also the
concrete version of the JD's "microservice encapsulation" language: the controller
never talks to the repository directly, so the persistence layer can change without
touching the API layer.

</details>

---

## Part 2 — REST endpoint with validation

**Exercise:** Add a `POST /v1/ad-decision` endpoint taking a validated request body
(`sessionId` and `contentId` required, non-blank) and returning `200` with a decision,
or a `400` with a clear error body if validation fails.

<details>
<summary>Answer</summary>

```java
public record AdDecisionRequest(
    @NotBlank String sessionId,
    @NotBlank String contentId
) {}

public record AdDecisionResponse(String adId, String creativeUrl) {}

@PostMapping
public ResponseEntity<AdDecisionResponse> decide(@Valid @RequestBody AdDecisionRequest request) {
    AdDecisionResponse response = adDecisionService.decide(request);
    return ResponseEntity.ok(response);
}
```

`@Valid` triggers Jakarta Bean Validation on the incoming body; a failed
`@NotBlank`/etc. throws `MethodArgumentNotValidException` — which by default Spring
already turns into a `400` with a field-error body, but see Part 3 for shaping that
response yourself instead of relying on the default. Records (Java 16+) are a natural
fit for immutable DTOs — no boilerplate getters/equals/hashCode.

</details>

---

## Part 3 — Centralized exception handling

**Exercise:** Instead of letting Spring's default error body leak through, write a
`@ControllerAdvice` that turns `MethodArgumentNotValidException` into a clean `400` JSON
body, and a custom `AdNotEligibleException` into a `404`.

<details>
<summary>Answer</summary>

```java
public class AdNotEligibleException extends RuntimeException {
    public AdNotEligibleException(String message) { super(message); }
}

public record ErrorResponse(String error, String message) {}

@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        String message = ex.getBindingResult().getFieldErrors().stream()
                .map(f -> f.getField() + ": " + f.getDefaultMessage())
                .collect(Collectors.joining(", "));
        return ResponseEntity.badRequest().body(new ErrorResponse("VALIDATION_FAILED", message));
    }

    @ExceptionHandler(AdNotEligibleException.class)
    public ResponseEntity<ErrorResponse> handleNotEligible(AdNotEligibleException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ErrorResponse("NO_ELIGIBLE_AD", ex.getMessage()));
    }
}
```

`@RestControllerAdvice` = `@ControllerAdvice` + `@ResponseBody`, applies globally across
every `@RestController` — this is what keeps error handling out of every individual
endpoint method (loose coupling again: controllers stay focused on the happy path).

</details>

---

## Part 4 — DynamoDB repository pattern

**Exercise:** Using the AWS SDK v2 **Enhanced Client** (the modern, idiomatic way — not
the low-level `DynamoDbClient` with manual `AttributeValue` maps), write a repository
method that fetches frequency-cap state for a `(userId, campaignId)` key.

<details>
<summary>Answer</summary>

```java
@DynamoDbBean
public class FrequencyCapRecord {
    private String userId;      // partition key
    private String campaignId;  // sort key
    private int count;
    private long ttlEpochSeconds;

    @DynamoDbPartitionKey
    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }

    @DynamoDbSortKey
    public String getCampaignId() { return campaignId; }
    public void setCampaignId(String campaignId) { this.campaignId = campaignId; }

    public int getCount() { return count; }
    public void setCount(int count) { this.count = count; }

    public long getTtlEpochSeconds() { return ttlEpochSeconds; }
    public void setTtlEpochSeconds(long ttlEpochSeconds) { this.ttlEpochSeconds = ttlEpochSeconds; }
}

@Repository
public class FrequencyCapDynamoRepository {
    private final DynamoDbTable<FrequencyCapRecord> table;

    public FrequencyCapDynamoRepository(DynamoDbEnhancedClient enhancedClient) {
        this.table = enhancedClient.table(
                "frequency_caps", TableSchema.fromBean(FrequencyCapRecord.class));
    }

    public Optional<FrequencyCapRecord> find(String userId, String campaignId) {
        Key key = Key.builder().partitionValue(userId).sortValue(campaignId).build();
        return Optional.ofNullable(table.getItem(key));
    }

    public void save(FrequencyCapRecord record) {
        table.putItem(record);
    }
}
```

Composite key (`userId` partition + `campaignId` sort) is the standard DynamoDB pattern
for "give me this user's data for this campaign" access — matches the access pattern in
`../system_design/examples/02_anti_ad_fatigue_frequency_capping.md` exactly. Note real
frequency-cap hot-path reads would more likely hit Redis (sub-ms) with DynamoDB as the
durable backing store reconciled periodically, not DynamoDB directly on every ad
decision — see Part 5 for the caching layer in front of this.

</details>

---

## Part 5 — Redis/ValKey caching

**Exercise:** Add a caching layer in front of a slow campaign-config lookup, using
Spring's `@Cacheable`, and make sure a config update evicts the stale entry.

<details>
<summary>Answer</summary>

```java
@Service
public class CampaignConfigService {
    private final CampaignConfigRepository repository;

    public CampaignConfigService(CampaignConfigRepository repository) {
        this.repository = repository;
    }

    @Cacheable(cacheNames = "campaignConfig", key = "#campaignId")
    public CampaignConfig getConfig(String campaignId) {
        return repository.findById(campaignId)
                .orElseThrow(() -> new AdNotEligibleException("No such campaign: " + campaignId));
    }

    @CacheEvict(cacheNames = "campaignConfig", key = "#campaignId")
    public void invalidate(String campaignId) {
        // no body needed — the annotation does the eviction; call this from
        // whatever handles a campaign-update event/webhook
    }
}
```

```yaml
spring:
  cache:
    type: redis
  data:
    redis:
      host: ${REDIS_HOST}
      port: 6379
```

`@Cacheable` short-circuits the method body entirely on a cache hit — the repository
call never happens. `key = "#campaignId"` uses SpEL to key the cache entry off the
method argument. In `../system_design/examples/01_ad_decisioning_service.md`'s terms,
this is exactly "keep relatively static config in a fast cache so the hot path almost
never makes a network call for data that rarely changes" — and `@CacheEvict` is how a
config-change event keeps that cache from serving stale data indefinitely.

</details>

---

## Part 6 — Kafka producer + consumer

**Exercise:** Publish an ad-decision event asynchronously (never blocking the response),
and write the consumer that processes it idempotently.

<details>
<summary>Answer</summary>

```java
@Service
public class AdEventPublisher {
    private final KafkaTemplate<String, AdDecisionEvent> kafkaTemplate;

    public AdEventPublisher(KafkaTemplate<String, AdDecisionEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void publishAsync(AdDecisionEvent event) {
        // fire-and-forget from the caller's perspective — decisioning latency must
        // never depend on Kafka being healthy; a failed send is logged, not thrown
        kafkaTemplate.send("ad-decisions", event.impressionId(), event)
                .whenComplete((result, ex) -> {
                    if (ex != null) {
                        log.warn("Failed to publish ad decision event {}", event.impressionId(), ex);
                    }
                });
    }
}

@Component
public class ImpressionEventConsumer {
    private final ImpressionCounterService impressionCounterService;

    public ImpressionEventConsumer(ImpressionCounterService impressionCounterService) {
        this.impressionCounterService = impressionCounterService;
    }

    @KafkaListener(topics = "ad-decisions", groupId = "impression-counter")
    public void onMessage(AdDecisionEvent event) {
        // idempotent: record() itself dedupes by impressionId, so redelivery
        // (Kafka is at-least-once) is a safe no-op — see java_challenges/03
        impressionCounterService.record(event.campaignId(), event.impressionId());
    }
}
```

Note the `key` passed to `kafkaTemplate.send` (`event.impressionId()`) — Kafka
guarantees ordering only *within* a partition, and keying by impression ID (or user ID,
depending on what ordering actually matters for) determines which partition an event
lands in.

</details>

---

## Part 7 — Resilience: timeouts + circuit breaker on a third-party call

**Exercise:** The JD calls out integrations with "third-party systems." Wrap a call to
an external ad-partner API with a timeout, a circuit breaker, and a sane fallback — using
Resilience4j, the standard Spring Boot resilience library.

<details>
<summary>Answer</summary>

```yaml
resilience4j:
  circuitbreaker:
    instances:
      adPartnerApi:
        sliding-window-size: 20
        failure-rate-threshold: 50
        wait-duration-in-open-state: 30s
  timelimiter:
    instances:
      adPartnerApi:
        timeout-duration: 200ms
```

```java
@Service
public class AdPartnerClient {
    private final RestClient restClient;

    public AdPartnerClient(RestClient restClient) {
        this.restClient = restClient;
    }

    @CircuitBreaker(name = "adPartnerApi", fallbackMethod = "fallback")
    @TimeLimiter(name = "adPartnerApi")
    public CompletableFuture<PartnerBidResponse> getBid(BidRequest request) {
        return CompletableFuture.supplyAsync(() ->
                restClient.post().uri("/bid").body(request).retrieve().body(PartnerBidResponse.class));
    }

    // Fallback signature must match the original + a Throwable param.
    private CompletableFuture<PartnerBidResponse> fallback(BidRequest request, Throwable t) {
        log.warn("Ad partner call failed/timed out, skipping this partner", t);
        return CompletableFuture.completedFuture(PartnerBidResponse.none());
    }
}
```

This is the concrete version of "microservice encapsulation and loose coupling" applied
to an external dependency: a slow/down third party degrades gracefully (skip that one
partner) instead of taking down ad decisioning. Once `failure-rate-threshold` is
crossed, the breaker opens and stops even *attempting* calls for `wait-duration-in-
open-state`, protecting your own service from piling up threads waiting on a dependency
that's already known to be unhealthy.

</details>

---

## Part 8 — Observability

**Exercise:** The JD explicitly asks for "metrics, monitoring, and alerting." Add a
custom timer and counter around the ad-decision path using Micrometer (Spring Boot
Actuator's metrics facade, vendor-neutral — works with Prometheus, CloudWatch, Datadog,
etc. underneath).

<details>
<summary>Answer</summary>

```java
@Service
public class AdDecisionService {
    private final AdCandidateRepository adCandidateRepository;
    private final Timer decisionTimer;
    private final Counter fallbackServedCounter;

    public AdDecisionService(AdCandidateRepository adCandidateRepository, MeterRegistry registry) {
        this.adCandidateRepository = adCandidateRepository;
        this.decisionTimer = Timer.builder("ad.decision.latency")
                .publishPercentiles(0.5, 0.95, 0.99)
                .register(registry);
        this.fallbackServedCounter = Counter.builder("ad.decision.fallback_served")
                .register(registry);
    }

    public AdDecisionResponse decide(AdDecisionRequest request) {
        return decisionTimer.record(() -> {
            try {
                return selectBestCandidate(request);
            } catch (NoEligibleCandidateException e) {
                fallbackServedCounter.increment();
                return AdDecisionResponse.houseAd();
            }
        });
    }
}
```

`publishPercentiles(0.5, 0.95, 0.99)` is what gets you the p50/p95/p99 latency numbers
this repo's `system_design/notes.md` review-pass checklist asks for. A rising
`fallback_served` rate is exactly the kind of thing that should back a real alert — it
means the primary decisioning path is degrading even though the *response* to the
client still looks fine (a house ad, not an error).

</details>

---

## Part 9 — Testing

**Exercise:** Write a slice test for the controller (`@WebMvcTest`, mocking the service
layer) and a plain unit test for the service (Mockito, no Spring context at all).

<details>
<summary>Answer</summary>

```java
@WebMvcTest(AdDecisionController.class)
class AdDecisionControllerTest {
    @Autowired MockMvc mockMvc;
    @MockBean AdDecisionService adDecisionService;

    @Test
    void returns400WhenSessionIdMissing() throws Exception {
        mockMvc.perform(post("/v1/ad-decision")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"contentId\":\"abc\"}"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void returns200WithDecision() throws Exception {
        when(adDecisionService.decide(any()))
                .thenReturn(new AdDecisionResponse("ad-1", "https://example.com/creative"));

        mockMvc.perform(post("/v1/ad-decision")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"sessionId\":\"s1\",\"contentId\":\"c1\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.adId").value("ad-1"));
    }
}

@ExtendWith(MockitoExtension.class)
class AdDecisionServiceTest {
    @Mock AdCandidateRepository repository;
    @InjectMocks AdDecisionService service;

    @Test
    void selectsHighestECpmEligibleCandidate() {
        when(repository.findByCampaignActiveTrue()).thenReturn(List.of(/* ... */));
        AdDecisionResponse result = service.decide(new AdDecisionRequest("s1", "c1"));
        assertThat(result.adId()).isEqualTo("expected-id");
    }
}
```

`@WebMvcTest` boots only the web layer (fast — no real DB/Redis/Kafka), `@MockBean`
replaces the service with a mock in Spring's context. The service-level test uses plain
Mockito with zero Spring context — much faster, and the right default for pure business
logic (this is the selection algorithm from `java_challenges/05`, now under a Spring
service).

</details>
