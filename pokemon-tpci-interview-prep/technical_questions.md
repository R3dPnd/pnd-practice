# Technical concept questions — by JD bullet

Short answers you should be able to say out loud in under a minute each. The JD's stack:
**Go, TypeScript, React, REST, AWS CDK / IaC, Postgres, NoSQL, containers, serverless**
(+ some Python/JS).

## Go
- **Goroutines vs threads?** Goroutines are cheap (KB stacks), multiplexed onto OS threads by
  the runtime scheduler (M:N). Start thousands; bound them anyway (`challenges/08`).
- **Channels vs mutex?** Channels to pass ownership / coordinate stages; mutex to protect
  shared state. "Share memory by communicating" is a guideline, not a law — the registration
  challenge is cleaner with a mutex.
- **`context.Context`** — cancellation, deadlines, request-scoped values. First param, never
  stored in structs, always propagate to DB/HTTP calls.
- **Error handling** — errors are values; wrap with `fmt.Errorf("register: %w", err)`, check
  with `errors.Is/As`; sentinel errors (`ErrNotRegistered`) for expected cases.
- **Interfaces** — implicit satisfaction; "accept interfaces, return structs"; define small
  interfaces at the consumer (great for test fakes, e.g. an injected clock).
- **Slices** — header (ptr, len, cap); `append` may or may not reallocate → aliasing bugs;
  `slices.Clone` before returning internal state.
- **Maps** — not safe for concurrent writes (runtime panics); iteration order is random.
- **Generics** — type params with constraints (`comparable`, `cmp.Ordered`); used in
  `challenges/05_lru_cache` and `08_worker_pool`.
- **Race detector** — `go test -race`. **defer** runs LIFO at function return.
- **HTTP service shape** — `net/http` (Go 1.22+ has method+path patterns:
  `mux.HandleFunc("POST /events/{id}/registrations", h)`), middleware for logging/auth,
  graceful shutdown with `http.Server.Shutdown(ctx)`.
- **Why Go on Lambda?** Single static binary, fast cold starts, low memory, `provided.al2023`.

## TypeScript / JavaScript
- `type` vs `interface`; discriminated unions + exhaustive `switch` with `never`.
- `unknown` vs `any`; narrowing; type guards; `satisfies`.
- Utility types: `Partial`, `Pick`, `Omit`, `Record`, `ReturnType`.
- Event loop: call stack, microtasks (promises) before macrotasks (timers).
- `Promise.all` vs `allSettled` vs `race` vs `any`.
- Runtime validation at the edge (zod) — types vanish at runtime.

## React
See `frontend/README.md` for the full list. Biggest hits: effect races + `AbortController`,
dependency arrays, keys, server vs client state, memoization, testing by role.

## REST API design
- Resources as nouns: `POST /events/{id}/registrations`, `DELETE /events/{id}/registrations/{playerId}`.
- Status codes: 200/201 (+`Location`)/204, 400 validation, 401 vs 403, 404, **409 conflict**
  (already registered / event full), 422, 429 (+`Retry-After`), 5xx.
- Idempotency: GET/PUT/DELETE idempotent by definition; POST via `Idempotency-Key` header.
- Pagination: offset (simple, drifts) vs cursor (stable, scales). Filtering via query params.
- Versioning (`/v1`, or header), consistent error body, ETags for caching / optimistic
  concurrency (`If-Match`).
- REST vs GraphQL (Pokémon Center uses both per their JD): GraphQL for many client shapes,
  REST for simple cacheable resources.

## Postgres
- Indexes: B-tree default; composite index column order matters (`(region, date)` serves
  `WHERE region=? ORDER BY date`); `EXPLAIN ANALYZE`.
- Transactions & isolation (Read Committed default; Repeatable Read; Serializable).
  `SELECT ... FOR UPDATE` vs conditional `UPDATE ... WHERE taken < capacity`.
- Lost updates → optimistic locking with a `version` column.
- N+1 queries; connection pooling (pgx pool, RDS Proxy for Lambda).
- Migrations that don't lock big tables (add nullable column, backfill, then constrain;
  `CREATE INDEX CONCURRENTLY`).
- JSONB when the shape varies, but don't use it to dodge modeling.

## NoSQL (DynamoDB)
- Partition key + sort key; design from access patterns; single-table design tradeoffs.
- GSIs (eventually consistent), LSIs; conditional writes; transactions (`TransactWriteItems`).
- TTL for expiring data (sessions, rate-limit counters — TPCi does this).
- Hot partitions; on-demand vs provisioned capacity; Streams → Lambda for projections.

## Infrastructure as code / AWS CDK
- Why IaC: reviewable, repeatable envs, drift detection, rollback.
- CDK vs CloudFormation vs Terraform: CDK synthesizes CloudFormation from real code (loops,
  types, constructs, `grant*` least-privilege helpers); Terraform is multi-cloud with state files.
- Constructs L1 (`Cfn*`) / L2 (opinionated) / L3 (patterns). Stacks, stages, `cdk diff`, `cdk deploy`.
- Testing: `Template.fromStack(stack).hasResourceProperties(...)`, snapshot tests.
- Secrets: Secrets Manager / SSM, never in env literals in code.

## Containers & serverless
- Docker image layers, multi-stage builds (Go → `FROM scratch`/distroless, tiny images).
- ECS Fargate vs EKS vs Lambda; when each.
- Lambda: cold starts, concurrency limits, reserved concurrency to protect the DB, DLQs,
  idempotent handlers (at-least-once delivery from SQS).
- Event-driven: SQS (queue, retries, DLQ), SNS (fan-out), EventBridge (routing/bus).

## Engineering practices (JD: "advance engineering best practices")
- Code review: what you look for (correctness, tests, naming, failure modes, security), how
  you give feedback (questions, not commands; nit vs blocking).
- Testing pyramid; contract tests between services; testing time with an injected clock.
- CI/CD (TPCi uses GitLab per other JDs), trunk-based dev, feature flags, canary/blue-green.
- Observability: structured logs, metrics, traces; SLOs and alerting on symptoms.
- Security: OWASP top 10, least-privilege IAM, PII handling — **kids' data (COPPA)** is
  a big deal here.
