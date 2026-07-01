# Java Interview Prep — Costco Travel Booking Engineer

A practical, hands-on prep guide built around building a real travel booking microservice that mirrors Costco's stack (Java, Spring MVC, JSP, SQL/DB2, REST, React). Work through each phase, answer the question bank out loud, and you'll walk into that interview with muscle memory — not just notes.

---

## 1. Project Overview

You will build **TravelDesk**, a Spring Boot microservice that handles:

- **Booking creation** — REST API to create/read/cancel travel bookings
- **Account management** — User entity with basic auth context
- **Payment stub** — A fake payment service to practice interface + mocking patterns
- **JSP front-end** — A minimal booking form rendered server-side via Spring MVC + JSP
- **SQL schema** — Tables and queries that mirror a relational booking DB (close to DB2 syntax)

Each phase is deliberately small. The point is repetition on the patterns Costco cares about, not a production-grade system.

---

## 2. Prerequisites & Setup

| Tool | Version | Verify |
|------|---------|--------|
| Java JDK | 17+ | `java -version` |
| Maven | 3.8+ | `mvn -version` |
| IntelliJ IDEA | Community (free) | Launch, open any Maven project |
| H2 (embedded) | via Maven dep | No install needed |
| Git | Any | `git --version` |

### Quick scaffold

```bash 
# Generate the project skeleton via Spring Initializr CLI or browser
# https://start.spring.io → Group: com.costco.travel, Artifact: traveldesk
# Dependencies: Spring Web, Spring Data JPA, H2, Thymeleaf (swap for JSP in Phase 4)

mvn archetype:generate \
  -DgroupId=com.costco.travel \
  -DartifactId=traveldesk \
  -DarchetypeArtifactId=maven-archetype-quickstart \
  -DinteractiveMode=false
```

Then open `pom.xml` and add the Spring Boot parent + starter dependencies (shown in Phase 1).

---

## 3. Step-by-Step Build Guide

### Phase 1 — Project Scaffolding

**What you build:** A runnable Spring Boot app with an `/health` endpoint.

**Concepts:** Spring Boot auto-configuration, Maven project structure, `@SpringBootApplication`, `@RestController`.

**Task — `pom.xml` essentials:**

```xml
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.2.5</version>
</parent>
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
  </dependency>
  <dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
  </dependency>
</dependencies>
```

**Task — `HealthController.java`:**

```java
@RestController
public class HealthController {
    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "UP", "service", "traveldesk");
    }
}
```

**Checkpoint:** `mvn spring-boot:run` → `curl localhost:8080/health` returns JSON.

---

### Phase 2 — Domain Model & OOP Design

**What you build:** `Booking`, `Traveler`, and `Trip` entity classes with proper OOP structure.

**Concepts:** Encapsulation, inheritance, composition vs. inheritance, `@Entity`, JPA annotations, builder pattern.

**Key OOP decision to practice explaining:** Why `Trip` is a separate entity composed into `Booking` rather than flattened columns — normalization + single-responsibility.

```java
@Entity
@Table(name = "bookings")
public class Booking {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "traveler_id", nullable = false)
    private Traveler traveler;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "trip_id")
    private Trip trip;

    @Enumerated(EnumType.STRING)
    private BookingStatus status;   // PENDING, CONFIRMED, CANCELLED

    private LocalDateTime createdAt;

    // No public setters on id/createdAt — enforce invariants
    @PrePersist
    void onCreate() { this.createdAt = LocalDateTime.now(); }
}
```

**Checkpoint:** `mvn spring-boot:run` with `spring.jpa.hibernate.ddl-auto=create-drop` → H2 console at `/h2-console` shows `BOOKINGS`, `TRAVELERS`, `TRIPS` tables.

---

### Phase 3 — REST API Layer

**What you build:** `BookingController` with CRUD endpoints.

**Concepts:** `@RestController`, `@RequestBody`, `@PathVariable`, `ResponseEntity`, HTTP status codes, DTO pattern (never expose entities directly).

```java
@RestController
@RequestMapping("/api/v1/bookings")
public class BookingController {

    private final BookingService bookingService;

    public BookingController(BookingService bookingService) {
        this.bookingService = bookingService;  // constructor injection, not @Autowired field
    }

    @PostMapping
    public ResponseEntity<BookingDto> create(@RequestBody @Valid CreateBookingRequest req) {
        BookingDto booking = bookingService.create(req);
        URI location = URI.create("/api/v1/bookings/" + booking.getId());
        return ResponseEntity.created(location).body(booking);
    }

    @GetMapping("/{id}")
    public ResponseEntity<BookingDto> getById(@PathVariable Long id) {
        return ResponseEntity.ok(bookingService.findById(id));
    }

    @PatchMapping("/{id}/cancel")
    public ResponseEntity<Void> cancel(@PathVariable Long id) {
        bookingService.cancel(id);
        return ResponseEntity.noContent().build();
    }
}
```

**Why DTOs?** Entities are JPA-managed objects — exposing them leaks DB structure, causes lazy-load issues in JSON serialization, and couples API to schema. DTOs decouple the two.

**Checkpoint:** Postman or `curl -X POST localhost:8080/api/v1/bookings -H 'Content-Type: application/json' -d '{...}'` returns `201 Created` with a `Location` header.

---

### Phase 4 — JSP Front-End via Spring MVC

**What you build:** A booking form at `/bookings/new` rendered by a JSP template.

**Concepts:** Spring MVC `@Controller` (not `@RestController`), `Model`, `ModelAndView`, JSP + JSTL, view resolver config. This is the server-side rendering pattern Costco still uses.

**`pom.xml` — add JSP support:**

```xml
<dependency>
  <groupId>org.apache.tomcat.embed</groupId>
  <artifactId>tomcat-embed-jasper</artifactId>
</dependency>
<dependency>
  <groupId>jakarta.servlet.jsp.jstl</groupId>
  <artifactId>jakarta.servlet.jsp.jstl-api</artifactId>
</dependency>
```

**`application.properties`:**

```properties
spring.mvc.view.prefix=/WEB-INF/views/
spring.mvc.view.suffix=.jsp
```

**`BookingViewController.java`:**

```java
@Controller
@RequestMapping("/bookings")
public class BookingViewController {

    @GetMapping("/new")
    public String newBookingForm(Model model) {
        model.addAttribute("booking", new CreateBookingRequest());
        return "booking-form";   // resolves to /WEB-INF/views/booking-form.jsp
    }

    @PostMapping
    public String submitBooking(@ModelAttribute CreateBookingRequest req,
                                 RedirectAttributes attrs) {
        bookingService.create(req);
        attrs.addFlashAttribute("message", "Booking confirmed!");
        return "redirect:/bookings/new";
    }
}
```

**`booking-form.jsp` (minimal):**

```jsp
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html><body>
  <c:if test="${not empty message}"><p>${message}</p></c:if>
  <form method="post" action="/bookings">
    <input name="destination" placeholder="Destination" required />
    <input name="travelerId" placeholder="Traveler ID" required />
    <button type="submit">Book</button>
  </form>
</body></html>
```

**Checkpoint:** Navigate to `localhost:8080/bookings/new` in browser — form renders and submits.

---

### Phase 5 — Service & Repository Layer

**What you build:** `BookingService` (business logic) and `BookingRepository` (data access), cleanly separated.

**Concepts:** `@Service`, `@Repository`, Spring Data JPA, `@Transactional`, custom JPQL queries, exception handling (`@ControllerAdvice`).

```java
public interface BookingRepository extends JpaRepository<Booking, Long> {

    List<Booking> findByTravelerId(Long travelerId);

    @Query("SELECT b FROM Booking b WHERE b.status = :status AND b.createdAt > :since")
    List<Booking> findRecentByStatus(@Param("status") BookingStatus status,
                                      @Param("since") LocalDateTime since);
}
```

```java
@Service
@Transactional
public class BookingService {

    private final BookingRepository repo;
    private final PaymentService paymentService;  // injected interface, not impl

    public BookingDto create(CreateBookingRequest req) {
        Booking booking = BookingMapper.toEntity(req);
        booking.setStatus(BookingStatus.PENDING);
        Booking saved = repo.save(booking);

        paymentService.charge(saved.getId(), req.getAmount());  // stub call
        saved.setStatus(BookingStatus.CONFIRMED);

        return BookingMapper.toDto(saved);
    }

    public void cancel(Long id) {
        Booking booking = repo.findById(id)
            .orElseThrow(() -> new BookingNotFoundException(id));
        if (booking.getStatus() == BookingStatus.CANCELLED) {
            throw new IllegalStateException("Already cancelled");
        }
        booking.setStatus(BookingStatus.CANCELLED);
        // no explicit save — @Transactional flushes dirty entity automatically
    }
}
```

**Checkpoint:** Unit test `BookingService` with a mocked repo — service logic runs without a DB.

---

### Phase 6 — SQL Schema & Queries

**What you build:** `schema.sql` and `data.sql` files + practice raw SQL queries.

**Concepts:** DDL vs DML, foreign keys, indexes, JOIN types, `GROUP BY`, DB2-compatible syntax.

**`src/main/resources/schema.sql`:**

```sql
CREATE TABLE travelers (
    id      BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name    VARCHAR(100) NOT NULL,
    email   VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE trips (
    id          BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    destination VARCHAR(200) NOT NULL,
    depart_date DATE NOT NULL,
    return_date DATE NOT NULL
);

CREATE TABLE bookings (
    id          BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    traveler_id BIGINT NOT NULL REFERENCES travelers(id),
    trip_id     BIGINT NOT NULL REFERENCES trips(id),
    status      VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for the most common query pattern: bookings by traveler
CREATE INDEX idx_bookings_traveler ON bookings(traveler_id);
```

**Practice queries (run in H2 console):**

```sql
-- All confirmed bookings with traveler names
SELECT b.id, t.name, tr.destination, b.status
FROM bookings b
JOIN travelers t  ON b.traveler_id = t.id
JOIN trips tr     ON b.trip_id     = tr.id
WHERE b.status = 'CONFIRMED';

-- Booking count per traveler (aggregate)
SELECT t.name, COUNT(b.id) AS total_bookings
FROM travelers t
LEFT JOIN bookings b ON b.traveler_id = t.id
GROUP BY t.name
ORDER BY total_bookings DESC;

-- Bookings in the last 30 days
SELECT * FROM bookings
WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '30' DAY;
```

**Checkpoint:** All queries return expected results in H2 console. Explain the LEFT JOIN — why it includes travelers with zero bookings.

---

### Phase 7 — Unit Tests with JUnit 5

**What you build:** Tests for `BookingService` and `BookingController`.

**Concepts:** JUnit 5 (`@Test`, `@BeforeEach`, `@ExtendWith`), Mockito (`@Mock`, `when/thenReturn`, `verify`), `@WebMvcTest` for controller slice tests.

```java
@ExtendWith(MockitoExtension.class)
class BookingServiceTest {

    @Mock BookingRepository repo;
    @Mock PaymentService paymentService;
    @InjectMocks BookingService service;

    @Test
    void cancel_alreadyCancelled_throws() {
        Booking cancelled = new Booking();
        cancelled.setStatus(BookingStatus.CANCELLED);
        when(repo.findById(1L)).thenReturn(Optional.of(cancelled));

        assertThrows(IllegalStateException.class, () -> service.cancel(1L));
        verify(repo, never()).save(any());  // no save should happen
    }
}
```

```java
@WebMvcTest(BookingController.class)
class BookingControllerTest {

    @Autowired MockMvc mockMvc;
    @MockBean BookingService bookingService;

    @Test
    void getById_notFound_returns404() throws Exception {
        when(bookingService.findById(99L)).thenThrow(new BookingNotFoundException(99L));

        mockMvc.perform(get("/api/v1/bookings/99"))
               .andExpect(status().isNotFound());
    }
}
```

**Checkpoint:** `mvn test` passes with zero failures.

---

### Phase 8 — Logging & Observability Basics

**What you build:** Structured logging with SLF4J and a basic `@ControllerAdvice` for global error handling.

**Concepts:** SLF4J + Logback, log levels, MDC (correlation IDs), `@ControllerAdvice`, `@ExceptionHandler`.

```java
@Slf4j  // Lombok — generates: private static final Logger log = LoggerFactory.getLogger(...)
@Service
public class BookingService {
    public BookingDto create(CreateBookingRequest req) {
        log.info("Creating booking for traveler={} destination={}",
                  req.getTravelerId(), req.getDestination());
        // ...
        log.debug("Booking persisted id={}", saved.getId());
        return BookingMapper.toDto(saved);
    }
}
```

```java
@ControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(BookingNotFoundException.class)
    public ResponseEntity<Map<String, String>> handleNotFound(BookingNotFoundException ex) {
        log.warn("Booking not found: {}", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                             .body(Map.of("error", ex.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, String>> handleGeneric(Exception ex) {
        log.error("Unhandled exception", ex);
        return ResponseEntity.internalServerError()
                             .body(Map.of("error", "Internal server error"));
    }
}
```

**Checkpoint:** Hit a missing booking ID — response is a clean JSON error body, and the log shows the `WARN` line with the ID.

---

## 4. Key Concepts Cheat Sheet

### OOP Pillars (with Java examples)

| Pillar | One-line definition | Java example |
|--------|-------------------|--------------|
| **Encapsulation** | Hide internals, expose behavior | Private fields + getters; `Booking.cancel()` instead of `setStatus(CANCELLED)` |
| **Inheritance** | Reuse via `extends` | `AdminTraveler extends Traveler` adds permissions |
| **Polymorphism** | Same interface, different behavior | `PaymentService` interface → `StripePaymentService`, `StubPaymentService` |
| **Abstraction** | Expose what, hide how | `BookingRepository` interface — callers don't know if it's JPA, JDBC, or in-memory |

### REST API Design Principles

- **Resources are nouns, verbs are HTTP methods** — `POST /bookings`, not `POST /createBooking`
- **Use proper status codes** — `201 Created` with `Location` header on POST; `204 No Content` on DELETE/cancel; `404` when entity doesn't exist
- **DTOs at the boundary** — never serialize JPA entities directly
- **Stateless** — no server-side session; each request carries all context (auth token, IDs)
- **Versioning** — `/api/v1/` prefix isolates breaking changes

### Spring MVC Request Lifecycle

```
HTTP Request
  → DispatcherServlet (front controller)
    → HandlerMapping (finds @Controller method)
      → HandlerInterceptor.preHandle() (auth, logging)
        → Controller method executes
          → ViewResolver (for JSP) or MessageConverter (for JSON)
            → HTTP Response
```

Key: `DispatcherServlet` is the single entry point. Spring MVC is a front-controller pattern.

### SQL Joins & Indexing

```sql
INNER JOIN  -- only rows with matches on both sides
LEFT JOIN   -- all left rows, NULL for unmatched right (use for "find travelers with no bookings")
RIGHT JOIN  -- opposite (rarely needed; rewrite as LEFT JOIN)
```

**Index rule of thumb:**
- Index foreign keys (`traveler_id`, `trip_id`) — they're used in JOINs and WHERE clauses constantly
- Index columns in `WHERE` and `ORDER BY` for high-traffic queries
- Avoid indexing columns with low cardinality (e.g., `status` with 3 values) unless combined with high-selectivity columns
- Every index speeds reads but slows writes — don't over-index

### Microservice vs. Monolith Tradeoffs

| | Monolith | Microservices |
|--|---------|--------------|
| **Deploy** | One artifact | Per-service CI/CD |
| **Data** | Shared DB | Each service owns its DB |
| **Calls** | In-process method call | Network call (latency, failure modes) |
| **Good for** | Early product, small team | Independent scaling, team autonomy |
| **Hard part** | Scaling specific components | Distributed tracing, data consistency |

**SOA migration context (Costco angle):** Legacy SOA means services that share a common ESB/message bus. Microservices cut that shared bus — each service communicates directly via REST or async messaging (Kafka/JMS). The risk is distributed transactions; the pattern is eventual consistency + saga.

---

## 5. Interview Question Bank

### Java & OOP

**Q1: What's the difference between an abstract class and an interface in Java?**
> Abstract class can have state (fields) and constructor logic; use it when subclasses share implementation. Interface is a pure contract; use it when unrelated classes need the same capability (e.g., `Chargeable`). In Java 8+, interfaces can have `default` methods, blurring the line — but if you need fields or constructor injection, use abstract class.

**Q2: Explain method overloading vs. overriding.**
> Overloading: same method name, different parameter signature, resolved at compile time. Overriding: subclass replaces parent's method at runtime — that's runtime polymorphism. Common interview trip-up: overloading is NOT polymorphism.

**Q3: What does `final` mean in Java?**
> On a variable: can't reassign the reference. On a method: can't override. On a class: can't extend. `String` is `final` — immutable and non-extendable.

**Q4: How does `HashMap` work internally?**
> Array of buckets. `hashCode()` picks the bucket; `equals()` resolves collisions within a bucket (linked list → tree if bucket size > 8, Java 8+). Key contract: if two objects are `equals()`, they must have the same `hashCode()`. Breaking this makes `HashMap` lose entries silently.

### REST & Spring

**Q5: Walk me through the lifecycle of a POST request in Spring MVC.**
> `DispatcherServlet` receives the request → `HandlerMapping` finds the `@PostMapping` method → interceptors run (auth, logging) → Jackson deserializes the body via `@RequestBody` → controller calls service → service returns DTO → Jackson serializes to JSON response. For JSP: the controller returns a view name, `ViewResolver` maps it to a `.jsp` file.

**Q6: What's the difference between `@Controller` and `@RestController`?**
> `@RestController = @Controller + @ResponseBody`. Every method return value is serialized to the response body directly. `@Controller` alone expects you to return view names for server-side rendering (JSP, Thymeleaf).

**Q7: What is `@Transactional` and when does it matter?**
> Tells Spring to wrap the method in a DB transaction — commit on success, rollback on unchecked exception. Matters any time you do multiple DB writes that must succeed or fail together. Gotcha: `@Transactional` only works on Spring-managed beans, and only on public methods (proxy limitation).

### Database

**Q8: How would you find slow queries in production?**
> Enable slow query logging (DB-level), then look at `EXPLAIN`/`EXPLAIN ANALYZE` on the offenders. Common culprits: full table scan (missing index), N+1 queries (Hibernate fetching children one by one), or joining without indexes on the join columns.

**Q9: What is an N+1 query problem and how do you fix it?**
> You load 100 bookings, then Hibernate fires 100 separate queries to load each booking's traveler. Fix: `JOIN FETCH` in JPQL, or `@EntityGraph`, or switch the association to `EAGER` loading only when you always need it. In practice, `JOIN FETCH` in a specific query is cleanest.

**Q10: Explain INNER JOIN vs. LEFT JOIN with an example.**
> `INNER JOIN` returns only rows with matches in both tables. `LEFT JOIN` returns all rows from the left table, with NULLs on the right where there's no match. Example: "find all travelers even if they have no bookings" → `LEFT JOIN bookings b ON b.traveler_id = t.id`.

### Debugging & Incidents

**Q11: A booking endpoint returns 500 errors intermittently in production. Walk me through how you'd debug it.**
> 1. Check logs for stack traces around the 500 time window. 2. Correlate with deployment — did it start after a release? 3. Check DB connection pool metrics — pool exhaustion causes timeouts. 4. Reproduce locally with a specific payload if you can isolate one from logs. 5. Add more targeted logging, deploy, observe. 6. If DB-related, check slow query log and active connections.

**Q12: How do you approach a production incident where users can't complete bookings?**
> Communicate status first (status page, Slack). Triage severity — is it total outage or partial? Check health endpoints, logs, DB connections, downstream dependencies (payment service). Identify rollback option if recent deploy. Mitigate first (restart, rollback, feature flag), then do RCA after. Document the timeline and fix in a postmortem.

### Agile

**Q13: Describe how you've worked in Agile sprints.**
> Two-week sprints with planning at the start (break epics into stories with acceptance criteria), daily standups (what I did, what I'm doing, blockers), sprint review (demo to stakeholders), and retrospective (process improvements). Key: stories should be shippable increments, not task lists.

**Q14: How do you handle a story that turns out to be bigger than estimated mid-sprint?**
> Flag it in standup immediately — don't wait until the end. Work with the team to split the story: deliver the core acceptance criteria this sprint, carry the rest to next sprint as a new story. Scope creep mid-sprint is the enemy; transparent communication is the fix.

### Architecture

**Q15: When would you choose a microservice over keeping something in a monolith?**
> When the component needs to scale independently (e.g., a pricing engine hit 100x more than booking creation), when separate teams own it, or when it has significantly different deployment cadence. Don't microservice prematurely — the operational overhead (networking, distributed tracing, data consistency) is real. Costco's context: migrating from SOA means you already have service boundaries; the question is whether to cut the shared bus dependency.

---

## 6. Five-Day Study Schedule

**Goal:** 2-3 hours/day, code every session — reading without coding doesn't build muscle memory.

### Day 1 — Foundation & OOP
- **Hour 1:** Set up project, complete Phase 1 (scaffolding). Run it. Understand `pom.xml` structure.
- **Hour 2:** Phase 2 — build `Booking`, `Traveler`, `Trip` entities. Explain each JPA annotation out loud.
- **Review:** OOP cheat sheet. Practice explaining encapsulation and polymorphism with your own code.

### Day 2 — REST & Spring MVC
- **Hour 1:** Phase 3 — `BookingController` with CRUD. Test with Postman.
- **Hour 2:** Phase 4 — JSP form. Walk through the Spring MVC request lifecycle on paper.
- **Review:** Questions 5 & 6. Know the difference between `@Controller` and `@RestController` cold.

### Day 3 — Service Layer & SQL
- **Hour 1:** Phase 5 — `BookingService` and `BookingRepository`. Practice explaining `@Transactional`.
- **Hour 2:** Phase 6 — SQL schema + run the practice queries in H2 console. Explain each JOIN.
- **Review:** Questions 7, 8, 9, 10. Write the N+1 fix from memory.

### Day 4 — Testing & Error Handling
- **Hour 1:** Phase 7 — write unit tests. Make one test fail intentionally, then fix it.
- **Hour 2:** Phase 8 — add logging and `@ControllerAdvice`. Trigger an error and trace it through the logs.
- **Review:** Questions 11 & 12. Practice the production incident response out loud — timing matters in interviews.

### Day 5 — Full Review & Mock Interview
- **Hour 1:** Walk through the whole codebase from scratch. Can you explain every file's purpose in one sentence?
- **Hour 2:** Answer all 15 questions out loud, timed. Stumble on one? Add 30 minutes to that topic.
- **Buffer:** If you have a third hour, focus on microservice vs. monolith tradeoffs and Agile questions — those tend to be easy points that candidates skip.

---

## Quick Reference: Command Cheatsheet

```bash
# Run the app
mvn spring-boot:run

# Run tests only
mvn test

# Package as JAR
mvn package -DskipTests

# H2 console (while app is running)
open http://localhost:8080/h2-console
# JDBC URL: jdbc:h2:mem:testdb  User: sa  Password: (empty)

# Hit the API
curl -X POST http://localhost:8080/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{"travelerId": 1, "destination": "Cancun", "departDate": "2026-08-01", "returnDate": "2026-08-08"}'
```

---

Good luck. The Costco interview will lean heavily on "explain how this works" over "write code from scratch" — so practice talking through your code as much as writing it.
