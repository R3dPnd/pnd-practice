# System design — prep notes

The JD says "contribute to architectural discussions," "system design fundamentals," and
lists **Go, TypeScript/React, REST, AWS CDK / IaC, Postgres, NoSQL, containers + serverless**.
Design answers should land on *that* stack — it's literally the team's toolbox.

The team "builds the technology that enables our communities, from small gatherings to our
largest events." That is Play! Pokémon: League Challenges / Cups at local game stores,
Regionals, Internationals, Worlds. Expect prompts in that space.

## Framework (45 min)

1. **Clarify (5 min)** — users (players, parents, Tournament Organizers/Professors, judges,
   staff), core flows, scale, read/write ratio, latency, consistency needs. Ask about **kids**:
   COPPA/GDPR-K shape everything at Pokémon (Trainer Club accounts are often child accounts
   managed by parents).
2. **Numbers (3 min)** — order-of-magnitude only. Event traffic is **spiky**: quiet all week,
   then a registration drop or Worlds day.
3. **API (5 min)** — REST resources + verbs + status codes. Idempotency keys on POSTs.
4. **Data model (5 min)** — Postgres tables with keys/indexes; call out what goes to DynamoDB.
5. **High-level architecture (10 min)** — draw it. Name the AWS services.
6. **Deep dive (10 min)** — the hard part (concurrency, spikes, offline, consistency).
7. **Operations (5 min)** — observability, failure modes, deploys, cost, how you'd CDK it.

## Postgres vs DynamoDB — have a crisp answer

| | Aurora Postgres | DynamoDB |
|---|---|---|
| Use when | relational data, joins, ad-hoc queries, transactions across entities, reporting | known access patterns, key-value at huge/spiky scale, TTL data, single-digit-ms |
| At TPCi (public AWS case study) | Pokémon Trainer Club **auth** moved here (encryption, multi-region reliability) | **global config + TTL data** (e.g. login attempt counters → ~90% fewer bot logins) |
| Gotchas | connection limits (use RDS Proxy from Lambda), vacuum, migrations | design for access patterns up front, hot partitions, 400KB items, GSIs are eventually consistent |

Line to use: *"Default to Postgres for the domain model — tournaments, players, results are
relational and organizers want reporting. Put high-volume, TTL'd, or key-lookup data in
DynamoDB."*

## Containers vs serverless

- **Lambda**: spiky/event-driven work (results uploaded → award points → notify), cron jobs,
  low-traffic APIs. Watch cold starts (Go has fast cold starts — a reason they use Go), 15-min
  limit, DB connection fan-out (RDS Proxy).
- **ECS Fargate**: steady APIs, long-lived connections (WebSockets for live pairings), anything
  needing warm caches or >15 min.
- Both behind **API Gateway / ALB**, static React on **S3 + CloudFront**.

## AWS CDK sketch (TypeScript) — be able to talk through this

```ts
const table = new dynamodb.Table(this, "Attempts", {
  partitionKey: { name: "pk", type: dynamodb.AttributeType.STRING },
  billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
  timeToLiveAttribute: "expiresAt",
});

const db = new rds.DatabaseCluster(this, "Db", {
  engine: rds.DatabaseClusterEngine.auroraPostgres({ version: rds.AuroraPostgresEngineVersion.VER_16_4 }),
  writer: rds.ClusterInstance.serverlessV2("writer"),
  vpc,
});

const registerFn = new lambda.Function(this, "Register", {
  runtime: lambda.Runtime.PROVIDED_AL2023,      // Go compiled to a `bootstrap` binary
  architecture: lambda.Architecture.ARM_64,
  handler: "bootstrap",
  code: lambda.Code.fromAsset("dist/register"),
  environment: { TABLE: table.tableName },
});
table.grantReadWriteData(registerFn);           // least-privilege IAM generated for you

new apigw.LambdaRestApi(this, "Api", { handler: registerFn });
```

Talking points: constructs (L1/L2/L3), `cdk diff` in PR review, separate stacks per
env/stage, `grant*` methods for least privilege, snapshot tests of synthesized templates,
CDK Pipelines or GitLab CI deploying to dev → staging → prod.

---

## Practice prompts

### 1. Event registration for a sell-out event (Regionals / Worlds side events)
- 10k+ players hit "Register" the second it opens; capacity 2,000; waitlist; must never oversell.
- Key ideas: virtual waiting room / SQS buffer in front of the write path; **conditional
  write** for the capacity check (`UPDATE ... WHERE taken < capacity` or DynamoDB
  `ConditionExpression`); **idempotency key** per player+event so retries don't double-book;
  holds with expiry if payment is involved; waitlist promotion on cancel (event-driven).
- Verify eligibility (age division, Play! Pokémon ID, not banned) *before* the hot path.
- Ties to: `challenges/03_event_registration`.

### 2. Tournament management (the "TOM / Pokémon Event Manager" problem)
- Organizers run events at a store with flaky Wi-Fi; players need pairings on their phones;
  results upload to award Championship Points.
- Key ideas: **offline-first** client (local DB, sync later — the old TOM was a desktop app
  for this reason); server is source of truth after upload; round state machine
  (`pairing → in_progress → results_entered → finalized`); idempotent result upload; audit
  log for judge corrections; Swiss pairing + OWP/OOWP standings
  (`challenges/01`, `challenges/02`).
- Live pairings for big events: publish round → push via WebSocket/SSE (API Gateway WebSocket
  or AppSync) + a cached read model on CloudFront for the stampede of refreshes.

### 3. Championship Points ledger & leaderboard
- Points from thousands of events; corrections; qualification thresholds for Worlds.
- Key ideas: **append-only ledger** (`point_awards(event_id, player_id, points, reason)` with
  unique `(event_id, player_id, reason)` for idempotency); totals are a projection
  (materialized view / Redis ZSET); recompute on correction; season boundaries.
- Ties to: `challenges/06_leaderboard_top_k`.

### 4. Event Locator (find a League near me)
- Read-heavy, public, SEO-relevant. Search by location radius, type, date.
- Key ideas: PostGIS or geohash; CDN caching of search results by rounded lat/lng; Next.js
  SSR/ISR for SEO; pagination (`typescript/02_event_search`).

### 5. Login / account protection (Pokémon Trainer Club)
- Credential stuffing at scale, child accounts, parental consent.
- Key ideas: rate limiting per user + per IP (DynamoDB TTL counters), WAF, CAPTCHA step-up,
  breached-password checks, COPPA consent flows, PII minimization in logs.
- Ties to: `challenges/04_login_throttle`.

## Production troubleshooting (JD: "troubleshoot production issues, identify root causes")

Have one real story, and a generic approach:
1. Mitigate first (rollback / feature flag / scale out), communicate in the incident channel.
2. Scope: when did it start, what changed (deploys, config, traffic), who's affected.
3. Signals: dashboards (latency/error/saturation), logs with correlation IDs, traces (X-Ray /
   Datadog), DB metrics (connections, slow queries, locks).
4. Root cause → sustainable fix → test that reproduces it → blameless postmortem with
   action items (alerts, runbooks, guardrails).

Common culprits to name: Lambda→Postgres connection exhaustion (fix: RDS Proxy), N+1
queries, missing index after data growth, DynamoDB hot partition, retry storms (fix: backoff
+ jitter, circuit breaker), cache stampede at event start.
