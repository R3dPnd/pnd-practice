# STAR+L stories — drafted from your resume

Each story is written as a first-person draft for you to say out loud and then rewrite in
your own words. **Anything in `[brackets]` is a detail I couldn't get from the resume.**
Fill it in with the real specifics. Don't invent numbers: interviewers ask "how did you
measure that 40%?" and a vague answer costs more than leaving the number out.

Target length when spoken: **~2 minutes** each. S+T should take about 20 seconds, A
about 60–70% of the time, then R, then L. **Always end on L.**

## Story map

| # | Story | Themes it covers | Why it fits this team |
|---|---|---|---|
| 0 | Tell me about yourself | — | Opener, and it sets up the "returning to Microsoft" thread |
| 1 | Copilot deployment-risk tool (MSFT) | Ownership, collaboration, customer impact, AI tools | Availability/reliability + AI in eng workflows. **Your strongest story.** |
| 2 | On-call DRI → MTTR −35% (Axon) | Ownership, debugging, growth | "Drive improvements in availability, latency, resiliency, observability" |
| 3 | OAuth 2.0 watchlist micro-frontend (Axon) | Customer impact, security | AuthN/authZ and identity, the core of this team |
| 4 | Monolith → SOA migration (JPMC) | Collaboration/conflict, ambiguity | Shared platform services with many consumers |
| 5 | Secure data auditing pipeline (JPMC) | Customer impact, technical deep dive | Data consistency across account/enrollment state |
| 6 | AI-adoption dashboard, 3x (Axon) | Growth mindset, influence without authority | "Leverage AI-powered engineering tools", stated explicitly in the JD |
| 7 | 10k reads/sec ingestion pipeline (Axon) | Technical deep dive, design tradeoffs | Large-scale distributed services |
| 8 | Failure story | Growth mindset | **Needs a real event from you.** Options listed below |

If time is short, polish **0, 1, 2, 3, 4** first. Those five cover every theme.

---

## 0. Tell me about yourself (60–90 seconds)

> I'm a full-stack engineer with about eight years of experience building distributed
> systems, at Boeing, JP Morgan Chase, Microsoft, and now Axon.
>
> At JPMC I worked on payment and account services: event-driven Java/Spring/Kafka
> microservices and a migration from a monolith to independently deployable
> services. At Microsoft, for about three years, I built ASP.NET Core services on
> Cosmos DB, Service Bus and Azure SQL. I also owned our CI/CD pipelines on Azure
> DevOps, and I worked with platform teams on a Copilot-powered deployment-risk tool
> that cut deployment-related outages by 40%. At Axon I build ingestion pipelines that
> handle over 10,000 license-plate reads a second from edge cameras, and I'm a DRI in
> the on-call rotation.
>
> What connects all of it is shared backend services that other teams and customers
> depend on, and making them reliable and secure. That's why this role caught my eye:
> Partner Center's identity, authorization and enrollment services are exactly that
> kind of system, at Microsoft scale, with an AI-first direction I've already been
> working in.

**Be ready for:** "Why did you leave Microsoft, and why come back?" (see the end of
this file).

---

## 1. Copilot-powered deployment risk analysis tool (Microsoft)

**Prompts it answers:** a time you improved reliability · worked across teams · used AI
to solve a real problem · your proudest project · ownership beyond your role

**S:** On my team at Microsoft we deployed Function Apps, AKS workloads and Static Web
Apps through Azure DevOps. A meaningful share of our production incidents were caused
by deployments themselves: `[e.g., config drift, a missing dependency, a bad
manifest]`. We caught them only after rollout.

**T:** I `[proposed / was asked]` to reduce deployment-related outages. The deployment
data and tooling belonged to internal platform teams, not us, so I had to build it
with them.

**A:**
- I went through `[N]` past deployment incidents to find the failure indicators that
  showed up before an outage: `[e.g., resource limit changes, health-probe changes,
  dependency version bumps, unusual diff size]`.
- I partnered with `[platform team]` to get access to deployment metadata and agree
  on where the check would run: `[as a pipeline gate / a PR comment / a pre-deploy
  report]`.
- I built the tool so Copilot `[summarized the diff + config and flagged risk
  factors]`, combined with `[deterministic checks]`. I didn't let the LLM have the final
  say on its own. `[e.g., risk score → required second approver above a threshold]`.
- I rolled it out `[advisory first, then as a gate]` so teams could build trust in it
  before it blocked anyone.

**R:** Deployment-related outages dropped about **40%** `[over what period, measured
how, e.g., incidents tagged "deployment" in the incident tracker, quarter over quarter]`.
`[Adoption: N teams / pipelines used it.]`

**L:** `[Pick the true one:]` I learned to start an AI tool in advisory mode and earn
trust before making it a gate. **or** I learned that the deterministic checks caught
`[X]`, and the model was most valuable for explaining *why* a change was risky, so I
now design AI tools as "explain and flag", not "decide".

**Follow-ups to prepare:**
- How did you handle false positives?
- How did you validate the model's output?
- What would you do differently?
- How would this apply to Partner Center deployments?

---

## 2. On-call DRI, MTTR down 35% (Axon)

**Prompts it answers:** debugging a production issue · ownership · improving
observability · working under pressure

**S:** At Axon I'm a DRI in a formal on-call rotation (one week in eight) for
`[the ingestion pipeline / service]`. Early on, incidents took a long time to resolve
because `[e.g., alerts fired on symptoms with no context; tracing across services
was manual]`.

**T:** I owned resolving incidents on my shifts, and beyond that I wanted to cut the
time each one took.

**A:** Open with **one specific incident**. It makes the story concrete.
- `[Incident: what alerted, what customers saw.]`
- I used Dynatrace PurePath and waterfall views to trace the slow requests to
  `[the bottleneck: e.g., a database query, a downstream call, a retry storm]`.
  I confirmed it in `[Splunk/Datadog]` and mitigated by `[action]`.
- In the root-cause analysis I found `[the underlying cause]`. I then fixed it
  `[change]` and changed the process: `[e.g., runbooks, dashboards in Grafana that
  link alerts to traces, better alert thresholds]`.

**R:** Across the rotation, mean time to resolution dropped about **35%** `[baseline →
after, over what period]`.

**L:** `[e.g.,]` I now write the runbook and the dashboard link *with* the alert,
because the person paged at 3am needs context more than they need another graph.

---

## 3. OAuth 2.0 watchlist micro-frontend (Axon)

**Prompts it answers:** customer impact · security-minded engineering · integrating
messy systems · auth experience (bring this one up yourself, it's this team's domain)

**S:** Customers had license-plate watchlists coming from `[N]` different sources:
`[e.g., state hotlists, agency-internal lists, third-party feeds]`. Each source had its
own interface, so an officer or analyst had to check several places to get an alert.

**T:** I built a single customer-facing alerting interface as a micro-frontend that
pulled these sources together, and it had to authenticate users securely across all of them.

**A:**
- I built it in Angular, deployed on Kubernetes as a micro-frontend inside
  `[the host app]`.
- I implemented the OAuth 2.0 flows: `[authorization code + PKCE? token refresh?
  scopes per source?]`. Be precise about the flow, because this team will dig in.
- I handled `[tenant/agency isolation: a user only sees their agency's lists]`.
  Tokens were `[stored in memory / not in localStorage]`, and I `[validated
  audience/scopes on the backend]`.
- I normalized the different source formats into one alert model.

**R:** `[Customer outcome: one place to check instead of N; time-to-alert; adoption;
fewer support tickets]`.

**L:** `[e.g.,]` I learned that authorization decisions belong on the backend. The UI
hiding things isn't security, so I enforced `[X]` server-side.

**Follow-ups to prepare:**
- Walk me through the OAuth flow you used, and why that one.
- Where did you store tokens?
- How did you prevent one agency from seeing another's data?
- How would you add MFA?

---

## 4. Monolith → SOA migration (JPMC)

**Prompts it answers:** a conflict or disagreement · cross-team collaboration ·
leading through ambiguity · a change that affected other teams' consumers

**S:** At JPMC we had a monolithic batch-job application. Its domain logic was tightly
coupled, so a change for one consuming team meant rebuilding and retesting everything,
and other teams depended on it.

**T:** I led the migration into modular, independently deployable services, without
breaking the teams that consumed it.

**A:**
- I mapped the domain boundaries `[e.g., checkout, payment, account]` and defined
  versioned service contracts *before* moving any code.
- **The conflict:** `[e.g., a consuming team didn't want to change their integration
  timeline / another engineer wanted a big-bang rewrite]`. I `[how you resolved it:
  e.g., ran old and new side by side, shipped an adapter so consumers could migrate on
  their own schedule, agreed on a deprecation date together]`.
- I added test coverage around the contracts so consumers could trust each release.
- I documented integration patterns that the consuming teams then reused.

**R:** Test coverage went up and downstream build times went down `[numbers if you
have them]`. `[N]` consuming teams migrated, and the integration patterns became
reusable `[used by N other teams]`.

**L:** `[e.g.,]` For shared services, I now agree on the contract and the migration
path with consumers before writing code. Most of the conflict came from surprises,
not from the technical choices.

---

## 5. Secure real-time data auditing pipeline (JPMC)

**Prompts it answers:** customer impact · data consistency · technical deep dive ·
design tradeoffs

**S:** Borrowers saw order and account data in the customer portal that didn't always
match the backend records. That caused `[support calls, delayed checkouts, documents
generated from stale data]`.

**T:** I built a real-time pipeline to keep the backend and the portal in sync, and
to audit every discrepancy securely.

**A:**
- `[Architecture: e.g., Kafka events from the backend services → reconciliation
  consumer → audit store → portal updates]`.
- I made consumers idempotent and ordered `[per account key]` so retries didn't create
  new mismatches.
- `[Security: e.g., PII masking in audit logs, access-controlled audit store,
  encryption]`.
- Mismatches that couldn't be reconciled automatically were routed to `[a queue / ops
  dashboard]` instead of being silently overwritten.

**R:** Data discrepancies dropped an estimated **25%**, and borrower turnaround time
improved `[how much]`. Explain how the 25% was estimated before they ask.

**L:** `[e.g.,]` Reconciliation is easiest when the system emits events with stable
keys from the start. I now design for auditability up front instead of adding it later.

**Link to this team:** it's the same problem as keeping partner enrollment state
consistent across Partner Center services (`03_enrollment_workflow`).

---

## 6. AI-assisted development adoption, 3x (Axon)

**Prompts it answers:** growth mindset · influence without authority · using AI to
improve engineering (the JD asks for this directly) · something you started on your own

**S:** Our team had access to AI coding agents, but adoption was uneven. People
`[didn't know what agents were running, lost track of project state, context-switched
a lot]`.

**T:** `[On my own initiative?]` I set out to make AI-assisted development easier to
adopt across the team.

**A:**
- I built an internal React dashboard showing concurrent AI agent utilization and
  project state, so people could see `[what each agent was doing / where work stood]`
  without switching tools.
- `[How you drove adoption: demos, pairing, sharing workflows that worked]`.
- `[How you kept quality up: e.g., agent output still went through code review and
  CI, with nothing merged unreviewed]`. Say this one plainly, because this team builds
  security-critical services.

**R:** AI-assisted development adoption went up **3x** `[measured how: e.g., % of
PRs, active users per week]`. Context-switching overhead went down.

**L:** `[e.g.,]` Adoption didn't come from the tool being available. It came from
making the workflow visible. I now ship internal tools with a demo and a
"here's how I use it" doc.

**The JD's own words:** *"Explore opportunities to apply intelligent automation and
agent-based solutions within engineering workflows."* You've already done exactly that.
Say so.

---

## 7. 10k reads/sec edge-camera ingestion pipeline (Axon)

**Prompts it answers:** most technically complex project · design tradeoffs · scale ·
handling unreliable inputs. Use it when an interviewer says "go deep on a project."

**S:** AI-enabled edge cameras across geographically distributed sites send license
plate reads. The traffic is 10,000+ reads per second, connectivity is intermittent, the
devices have limited compute, and some of the input is malformed.

**T:** I engineered the ingestion and processing pipeline that extracts, normalizes and
spatially indexes that metadata for downstream AI/ML systems.

**A:** Have one or two of these tradeoffs ready in depth:
- **Intermittent connectivity:** `[device-side buffering + replay → duplicates →
  idempotent ingestion keyed on read id]`.
- **Malformed input:** `[validate at the edge of the pipeline, send bad records to a
  dead-letter path, never drop silently]`.
- **Geospatial indexing:** bounding-box queries `[which index and store, why
  bounding boxes rather than radius queries]`.
- **Scale:** `[EC2 vs Lambda split, S3 for raw storage, how you scaled consumers,
  backpressure]`.

**R:** `[Throughput sustained, latency to downstream ML, data quality improvement]`.

**L:** `[e.g., the hardest bugs came from duplicates during reconnect, so I now treat
idempotency as a requirement from the start, not an optimization]`.

---

## 8. Failure story (growth mindset) — you need to supply this one

Microsoft weighs growth mindset heavily, and "tell me about a time you failed" is
almost certain to come up. Pick a **real failure where the fault was yours**, and spend
most of the answer on the L. Candidate sources from your resume:

- **The incidents that led to the deployment-risk tool (Story 1).** Was there a
  deployment *you* shipped that caused an outage? A strong arc: "I caused an outage,
  and it made me build the thing that prevents it."
- **An on-call incident at Axon you handled badly** at first, such as a wrong initial
  diagnosis or escalating too late.
- **Something in the SOA migration** that broke a consumer.
- **The Microsoft Security interview loop itself**, if it didn't go your way. It's
  recent and honest: "my coding round didn't go well, I found I wasn't tracing my code
  by hand, and I changed how I practice." Use this only if you're comfortable bringing
  up another loop, and keep it short.

Template: **what I did → what broke → what I owned → what I changed, with evidence I
actually changed it.**

---

## Questions you'll get because of your timeline

**"You were at Microsoft until September 2025. Why did you leave, and why come back?"**
Keep it positive and short: `[the real reason, framed as a pull toward something,
e.g., wanted to work on high-throughput edge/AI data systems at Axon]`. Then: "I've
grown in `[X]` there, and coming back to work on Partner Center's identity and
platform services brings together that scale/AI work and the Azure platform
experience from before."

**"You've been at Axon about a year. Why move now?"** `[Real reason]`, framed around
this role specifically, never as running away from Axon.

## Leveling note

With 8+ years, 3 of them at Microsoft, aim for **IC4 (Senior)**, or ask whether the
role could go to IC4. That also moves the compensation estimate from before to the
IC4 column. To come across at senior level, your stories should show *you* making the
design decisions and influencing other teams (Stories 1, 4, 6), not just completing
assigned tasks.
