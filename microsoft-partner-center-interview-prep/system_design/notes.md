# System Design — Partner Center prep notes

Use the same 5-step framework as `../../microsoft-security-interview-prep/system_design/notes.md`:
clarify → API → high-level diagram → deep dive → security pass. Last time, interviewers
kept asking "why?" and expected you to attack your own design, and that still applies.
This file adds only the **domain knowledge** for this team and three prompts shaped
like its work.

## Domain primer (enough to sound like you've read the docs)

From public Microsoft Learn docs. Product names change often, so if the interviewer
uses a different name, follow their lead.

- **Partner Center**: the portal *and* REST APIs/SDKs that Microsoft partners use to
  enroll in programs, manage customers, buy and manage subscriptions, see billing, and
  claim incentives. "Platform services" means the shared backends behind all of that:
  enrollment, identity, authZ, and account/profile.
- **CSP (Cloud Solution Provider)**: how partners resell Microsoft cloud (M365, Azure,
  Dynamics). There are two models:
  - **Direct-bill**: the partner buys from Microsoft directly.
  - **Indirect (two-tier)**: an **indirect provider** (distributor) works with many
    **indirect resellers**, and each reseller serves many customers.
  That's a *hierarchy of tenants*, which is why `02_delegated_access_resolver` walks a tree.
- **Microsoft AI Cloud Partner Program**: the partner program, formerly *Microsoft
  Partner Network (MPN)*. "Program enrollment" means a partner org signs up for this
  and its sub-programs, gets verified, and earns designations.
- **Partner onboarding/verification**: legal entity, tax ID, domain, and contact
  verification before an account becomes active. Some checks are automated and some
  are manual review, so the workflow is asynchronous (`03_enrollment_workflow`).
- **GDAP (Granular Delegated Admin Privileges)**: replaced **DAP**, which gave partners
  broad standing Global Admin on customer tenants. GDAP is **least privilege**:
  specific Entra roles, granted to partner security groups, **time-bound** (it
  expires), and approved by the customer. This is the best example to use for
  "security-first authorization." It shows the shift from standing broad access to
  scoped, expiring, auditable access.
- **Partner security requirements**: Microsoft made **MFA mandatory** for Partner
  Center access, *including API calls*. Automation that used app-only or
  password-based auth broke and had to move to the **Secure Application Model**
  (app + user consent, refresh tokens stored in Key Vault). The JD mentions "MFA
  enforcement" for this reason.
- **Identity stack**: **Microsoft Entra ID** (formerly Azure AD), with OAuth 2.0 /
  OpenID Connect. Be able to explain:
  - multi-tenant app registrations
  - access tokens and the claims that matter (`tid` tenant, `oid` user, `scp`
    delegated scopes vs `roles` app roles)
  - Conditional Access
  - **managed identities** for service-to-service calls, so there are no secrets in config
- **Azure building blocks to name in designs**:
  - Front Door (global entry + WAF)
  - API Management (quotas, keys, versioning)
  - AKS or App Service (compute)
  - Cosmos DB (globally distributed, tunable consistency, partition key matters) or
    Azure SQL (relational, transactions)
  - Service Bus (queues and topics with sessions and dead-lettering) vs Event Hubs
    (high-throughput streams)
  - Key Vault (secrets and keys)
  - Azure Monitor / Application Insights (telemetry)
- **How Microsoft ships**: **safe deployment** in rings (canary → small region → broad),
  feature flags, and fast automated rollback. It's a good answer to "how would you
  roll this out?"

## Clarifying questions specific to this domain

Ask 3–4 of these before you draw anything:

- Who are the callers: partner users in the portal, partner automation via API, or
  internal Microsoft services? Each one authenticates differently.
- Is the system tenant-scoped? Can one partner *ever* see another partner's data?
  (The answer is no. Say "tenant isolation" early.)
- Scale: number of partner orgs (hundreds of thousands) vs customers under them
  (millions) vs API calls per second. Reads usually far outnumber writes.
- What has to be strongly consistent? Usually authorization changes (revocation) and
  billing. Profile and catalog data can be eventually consistent.
- Compliance: audit retention, data residency (EU data boundary), and what counts as PII.

## Practice prompt 1 — Partner enrollment & onboarding service

*"Design the service a new partner org uses to sign up for the partner program and get
verified."*

Outline to compare against after you try it cold:

- **API**:
  - `POST /enrollments` (with an `Idempotency-Key` header)
  - `GET /enrollments/{id}`
  - `POST /enrollments/{id}:submit`
  - webhooks or polling for status
- **State machine** like `03_enrollment_workflow`. Store state + version in the DB
  and update it with **optimistic concurrency** (ETag / version compare-and-swap).
- **Verification is async.** On submit, move to PENDING and publish a
  `VerificationRequested` message to Service Bus. Separate workers handle tax ID,
  domain (DNS TXT record), and sanctions screening, and some cases go to manual
  review. Each worker reports back with its own idempotency key. Use a **saga** or
  orchestrator (e.g. Durable Functions) for the multi-step flow, not a distributed
  transaction.
- **Data**: the enrollment record is partitioned by partner id. Keep documents (tax
  forms) in Blob storage, encrypted, with short-lived SAS links for access.
- **Reliability**:
  - retries with exponential backoff + jitter
  - dead-letter queue + alerting for poison messages
  - **outbox pattern**, so the state change and the event publish can't diverge
- **Security**:
  - authN via Entra
  - the creator becomes the first admin
  - rate-limit sign-ups per IP and per domain (abuse)
  - duplicate-org detection (`04_duplicate_partner_merge`) produces review
    *candidates*, not auto-blocks
  - PII minimization and audit log
- **Observability**:
  - funnel metrics (started → submitted → approved, time-in-state)
  - alert on queue age, not just error rate
- **Attack your own design**:
  - replayed submit → idempotency key
  - forged verification callback → the worker authenticates with a managed identity,
    and the callback is checked against the pending job
  - someone enrolling with a domain they don't own → DNS proof

## Practice prompt 2 — Authorization service for Partner Center APIs

*"Every Partner Center API call has to answer: can this user, acting for this partner,
do this action on this customer tenant?"*

- **PEP/PDP split**: each API has a *policy enforcement point* (middleware) that calls
  a central *policy decision point* (this service). The decision logic is what
  `02_delegated_access_resolver` implements.
- **Inputs**: the token (`tid`, `oid`, group claims) + action + resource tenant.
  Relationship and role data come from the GDAP store.
- **Hot-path latency** (p99 in single-digit ms):
  - cache decisions per (principal, tenant) close to the caller, either in-process
    or in a regional Redis
  - **The key tradeoff is cache TTL vs revocation latency.** Say a number, e.g.
    "revocation takes effect within 60s", and add push invalidation via an event for
    high-risk revocations.
- **Fail closed** if the PDP is unreachable. Then discuss the availability cost:
  - multi-region active-active
  - a local read replica of the policy data
  - a short stale-cache grace period *only* for read actions, never for writes or
    admin actions
- **Data model**:
  - relationships (partner ↔ customer, with expiry)
  - role assignments (relationship + security group + role)
  - role definitions (versioned)
  - Writes are rare and reads are huge, so use a strongly consistent store for
    writes with read replicas in each region.
- **Audit**: every grant/revoke event, plus sampled or full decision logs. Be able to
  answer "why was this allowed?" by returning the grant chain.
- **Attack your own design**:
  - token replay → short-lived tokens, audience check
  - confused deputy (an internal service calls on the user's behalf with its own
    stronger identity) → pass the user context through, and authorize the user, not
    the service
  - stale cache after revoke → TTL bound + push invalidation
  - tenant ID taken from the URL instead of the token → validate both, and reject if
    they don't match

## Practice prompt 3 — Roll out MFA enforcement across all Partner Center APIs

*"Leadership says MFA is now required for every partner API call. How do you ship it
without breaking thousands of partners' automation?"*

This one is mostly about operations and rollout judgment, not boxes and arrows.

- **Measure first.** Add telemetry for how each call authenticates (MFA claim present?
  app-only? which app id?). Then you know *who* would break before enforcing anything.
- **Phases**:
  1. audit only (log would-be failures)
  2. warn (response header / partner notification + docs on the Secure Application Model)
  3. enforce in **rings** (internal → small % of partners → all), with a feature flag
     per ring and a fast rollback
- **Exceptions**: a time-boxed, audited exemption list for partners with a migration
  plan. Every exemption has an owner and an expiry date.
- **Where to check**: the `amr` claim in the token, at the gateway or the shared
  middleware, *not* in each API separately. One place to enforce, one place to audit.
- **Success metrics**: % of calls with MFA, number of partners still on legacy auth,
  support ticket volume, and error rate per ring.
- **Behavioral tie-in**: this prompt is also a "customer impact" story. You're
  protecting partners' customers while breaking some partners' scripts, and the
  answer should take both seriously.

## Reliability vocabulary to use naturally

- SLO vs SLA. Availability math: 99.9% ≈ 43 min/month, 99.99% ≈ 4.3 min/month.
  Serial dependencies multiply their availabilities.
- Retries with backoff + jitter, plus a **retry budget** so retries don't amplify an
  outage. Circuit breakers (Security folder `05_reliable_retry`). Timeouts on every call.
- Idempotency, at-least-once delivery + idempotent consumers, the outbox pattern.
- Bulkheads and per-partner quotas, so one noisy partner can't take down everyone else
  (Security folder `01_rate_limiter`).
- Golden signals: latency, traffic, errors, saturation. Alert on symptoms, not causes.
