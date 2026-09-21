# Disney (DEEP&T) Senior Full Stack Engineer — Ad Decisioning — Interview Prep

Prep repo for **Senior Full Stack Engineer - Ad Decisioning** (internal level **P3** =
Senior Software Engineer), on the **Ad Serving Engineering** org within **Disney
Entertainment and ESPN Product & Technology (DEEP&T)**. Confirmed as a real, currently
open req (see Field notes), not a hypothetical — San Francisco / Santa Monica / Glendale /
Seattle, hybrid 4 days/week in office, posted comp range $141.9K–$208.4K depending on
location.

**Scope of this repo:** the JD is React-now-moving-to-Java, on a specific team (the
**Decisioning Fleet**, within Ad Serving) building the service that picks which ad plays
for Video on Demand, Live TV, and interactive ads across Hulu, Disney+, and ESPN+. This
repo covers what's **new** relative to `../disney-frontend-interview-prep/` (already
strong on JS/React fundamentals, live-build practice, and Disney's STAR behavioral
framework — reuse that repo rather than re-deriving it here):

- Java fundamentals + concurrency, in the practice/solution pattern that repo uses
- Spring Boot code-quiz (annotations, DI, REST, validation, exception handling, caching,
  Kafka, resilience) — likely if the technical round is Java-flavored
- Backend/distributed-systems design framework + **ad-tech-specific** worked examples
  (ad decisioning, frequency capping, impression counting, pacing) — this is the part
  most tailored to the actual team, since "qualification, delivery, and tracking of
  ad campaigns," "anti-ad fatigue systems," and "impression counting pipelines" are
  verbatim from this JD
- Behavioral themes specific to *this* JD's language: domain ownership, on-call,
  cross-team/third-party integration, mentoring, and — notably — **responsible AI tool
  use**, which this JD calls out twice (unusual for a JD to name explicitly; treat it as
  a signal they'll actually ask about it)

## Layout

```
behavioral/notes.md         STAR(+L) themes specific to this JD's language
  examples/                 5 fill-in templates, one per theme
system_design/notes.md      backend/distributed-systems framework + review-pass checklist
  examples/                 4 worked ad-tech system design walkthroughs
java_challenges/            5 practice problems, Java, concurrency-and-fundamentals heavy
  NN_topic/README.md        problem statement + why it maps to "high-throughput,
                             low-latency microservices" language in the JD
  Practice.java              stub with TODOs + a main() self-check
  Solution.java               reference implementation
spring_boot/notes.md        annotated code-quiz: DI, REST, validation, caching, Kafka,
                             resilience, observability — fill-in-the-blank, not runnable
react_js/notes.md           React + JS conceptual Q&A, collapsible answers — the recall
                             layer on top of ../disney-frontend-interview-prep/challenges/
react_js/live-build-sandbox/  real Vite+React+TS app for timed spec-to-code practice
                             (LIVE_BUILD_SPEC.md), no AI assistance — see its README.md
ad-decisioning-service/     runnable Maven/Spring Boot project — Parts 1-3 and 9 of
                             spring_boot/notes.md as real, tested, curl-able code
```

## Environment

JDK 21 (Temurin/OpenJDK via Homebrew) and Maven are set up — `java`/`javac`/`mvn` work
in any new terminal (added to `~/.zshrc`). Node was already present. Both runnable
projects below have been built, tested, and smoke-tested end to end as part of setting
this repo up.

```bash
# Java challenges — compile/run any one directly
cd java_challenges/01_thread_safe_frequency_cap
javac Solution.java -d /tmp/out && java -cp /tmp/out Solution

# Spring Boot service — real REST API, in-memory candidates, Micrometer metrics
cd ad-decisioning-service
mvn test              # 5 tests: web-slice (MockMvc) + service (Mockito) — all pass
mvn spring-boot:run    # starts on :8080
curl -X POST localhost:8080/v1/ad-decision -H "Content-Type: application/json" \
  -d '{"sessionId":"s1","contentId":"c1"}'
curl localhost:8080/v1/ad-decision/candidates   # ranked eligible list
curl localhost:8080/actuator/health

# React live-build sandbox — real Vite dev server
cd react_js/live-build-sandbox
npm run dev            # http://localhost:5173
npm run build           # type-checks + production build
```

No JDK/Maven is installed in this environment (checked — `java -version` and `mvn
-version` both fail here), so unlike the JS challenges repo, these Java files aren't
wired to an automated test runner. Use your own IDE (IntelliJ Community is free and has
zero-config JDK download) or paste into an online Java runner to compile/run. Each
`Practice.java` has a `main()` with expected-output comments, same self-check pattern
`costco-booking-platform/practice/java/JavaExercises.java` already uses in this repo.

## What this specific role actually does (from the JD + what "Decisioning Fleet" implies)

- The **Digital Advertising Platform** is a distributed, microservice-based system that
  qualifies, delivers, and tracks ad campaigns (VOD, Live TV, interactive) across
  Hulu/Disney+/ESPN+.
- You're specifically on **Decisioning**: "optimizing ad qualification and selection to
  make sure viewers always see the right ad at the right time," plus tooling that
  "analyzes what ads are competing for slots for ad breaks." This is a real-time
  candidate-filtering-and-ranking problem under a tight latency budget — see
  `system_design/examples/01_ad_decisioning_service.md`.
- Supporting systems explicitly named: **anti-ad-fatigue** (→ frequency capping, see
  `system_design/examples/02_anti_ad_fatigue_frequency_capping.md`), **impression
  counting pipelines** (→ streaming/event-processing, see `examples/03`), and
  integrations with **entitlements, pacing, targeting, ad selection, and third-party
  systems** (→ `examples/04`, plus resilience patterns in `spring_boot/notes.md`).
- Full stack in name, backend-weighted in trajectory: "React or similar" is a basic
  qualification (you already have this — lean on `../disney-frontend-interview-prep/`),
  but Java + Spring Boot + the whole preferred-quals list (DynamoDB, Redis/ValKey, Kafka/
  Kinesis, AWS, Terraform/Docker/Kubernetes) is where the JD's actual depth is. Expect
  the loop to weight backend/systems more than the React side.

## Day-by-day plan

No interview date confirmed yet for this specific role — fill in dates once scheduled.
Suggested order, ~5 sessions:

| Session | Focus | Do |
|---|---|---|
| 1 | Java fundamentals warm-up | `java_challenges/01` and `05` untimed; skim `spring_boot/notes.md` once |
| 2 | Concurrency (the JD's "high-throughput, low-latency" language is really asking about this) | `java_challenges/02`, `03`, `04`, 30–40 min each, timed |
| 3 | Spring Boot code-quiz, timed | `spring_boot/notes.md` exercises from a blank file, no peeking at the annotated answers |
| 4 | Backend system design | `system_design/notes.md` framework once, then mock `examples/01_ad_decisioning_service.md` and `02_anti_ad_fatigue_frequency_capping.md` out loud, 45 min each |
| 5 | Behavioral + remaining system design | All 5 `behavioral/examples/` filled in with real stories; mock `system_design/examples/03` and `04` |
| 6 | React/JS refresh (basic qualification, lower priority than Java) | `react_js/notes.md` Q&A out loud, one blind pass; redo one challenge from `../disney-frontend-interview-prep/challenges/` from a blank file if rusty |
| Day before | Taper | Re-read your 5 behavioral stories out loud once; skim `../disney-frontend-interview-prep/README.md` Field notes for general Disney-loop tone/format expectations, since this role's *format* (not content) likely follows the same non-standardized pattern |

## Field notes: what's actually known about this loop

Researched Sept 2026. Unlike the general "Disney doesn't standardize interviews" caveat
in `../disney-frontend-interview-prep/README.md` (still true — treat format as team-
dependent), a few things are now specifically confirmed for **Disney Streaming /
DEEP&T** engineering loops broadly, which this role likely follows since it's inside
that same org:

- **Process shape**: commonly reported as 3 main stages closing in roughly 4 weeks — a
  20–30 min recruiter screen, then a **90-minute HackerRank online assessment** with
  Java/Spring Boot-flavored live-coding scenarios, then a 45–60 min live round in a
  shared editor (CoderPad/HackerRank) covering system design and behavioral, or
  sometimes a timed take-home instead. Grading emphasis reported as problem
  decomposition, correctness, testing, and code readability — not just "did it pass."
- **Streaming-specific weighting**: Disney Streaming roles are reported to weight
  **performance and concurrency** heavily — thread safety and performance-minded code
  come up specifically, which lines up directly with this JD's "high-throughput,
  low-latency microservices" language and is why `java_challenges/` here is
  concurrency-heavy rather than generic LeetCode.
- **Compensation confirms leveling**: the actual open posting for this exact title lists
  P3 with a hiring range of $141.9K–$190.3K (LA), $148.7K–$199.4K (Seattle), and
  $155.4K–$208.4K (SF) — useful for your own comp-conversation prep, separate from
  interview content.
- **P3 = Senior Software Engineer** in Disney's internal ladder (P1 Associate → P2 SWE →
  P3 Senior SWE → P4 Staff → P5 Principal → P6 Senior Principal), per levels.fyi and
  independent Blind reports; P3→P4 promotion is reported as harder/slower than at
  typical big tech, for context if the "growth/mentoring" behavioral theme comes up.
- **Backend system-design content** for ad serving specifically isn't published by
  Disney, so `system_design/examples/` here is built from general ad-tech system-design
  patterns (frequency capping via Redis/Lua-script atomic counters, real-time bidding's
  ~100ms latency budgets, Netflix's own published post on their ads event-processing
  pipeline decoupling serving from tracking via Kafka) rather than Disney-specific
  leaks — reason from first principles in the room, cite these patterns as "how ad-tech
  systems generally solve this" rather than claiming inside knowledge of Disney's actual
  implementation.

Sources:
- [Senior Full Stack Engineer - Ad Decisioning — Disney Careers](https://www.disneycareers.com/en/job/san-francisco/senior-full-stack-engineer-ad-decisioning/391/95916581952)
- [Same posting — Seattle, WA — Ladders](https://www.theladders.com/job/senior-full-stack-engineer-ad-decisioning-thewaltdisneycompany-seattle-wa_87181092)
- [Same posting — San Francisco — Ladders](https://www.theladders.com/job/sr-product-software-engineer-ad-decisioning-engineering-thewaltdisneycompany-san-francisco-ca_87181078)
- [Walt Disney SWE: 2026 interview questions — Prepfully](https://prepfully.com/interview-questions/walt-disney/software-engineer)
- [Disney Streaming Services Software Engineer Interview Questions — Glassdoor](https://www.glassdoor.ca/Interview/Disney-Streaming-Services-Software-Engineer-Interview-Questions-EI_IE1755978.0,25_KO26,43.htm)
- [Disney Software Engineer Interview: Step-by-Step — Interview Coder](https://www.interviewcoder.co/blog/disney-software-engineer-interview)
- [Disney P3 Senior SWE Offer Evaluation — Blind](https://www.teamblind.com/post/disney-p3-senior-swe-offer-evaluation-jph6apg2)
- [Disney Software Engineer Salary — Levels.fyi](https://www.levels.fyi/companies/disney/salaries/software-engineer)
- [System Design Trackers from Netflix's Ad Tracking Launch — Hello Interview](https://www.hellointerview.com/blog/system-design-trackers-from-netflix-ad-tracking-launch)
- [Behind the Scenes: Building a Robust Ads Event Processing Pipeline — Netflix TechBlog](https://netflixtechblog.com/behind-the-scenes-building-a-robust-ads-event-processing-pipeline-e4e86caf9249)
- [Design an ad frequency capping system — Netflix interview question, via PracHub](https://prachub.com/interview-questions/design-an-ad-frequency-capping-system-4)
