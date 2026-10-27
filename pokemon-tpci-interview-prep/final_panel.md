# TPCi final-stage panel — what to expect & how to prep

This builds on what the folder already has (`README.md`, `behavioral/notes.md`,
`system_design/notes.md`, `frontend/`, `challenges/`). It adds only what's specific to
the **final panel stage**, plus your resume stories mapped to TPCi's values.

## What the final stage looks like (public reports, Oct 2026)

There isn't much public detail, and the reports are anonymous, self-reported, and
sometimes years old. Treat these as patterns, not a promise.

- **The most detailed recent report** (Senior SWE, Bellevue, accepted the offer)
  describes a **7-round onsite loop**:
  1 coding · 1 low-level design (LLD) · **1 DevOps** · **1 testing** · 1 behavioral ·
  a final round with the hiring manager. That candidate rated the coding round hard.
- **A 2021 Senior SWE report:** a **~6-hour (virtual) onsite** made of back-to-back
  30–60 min sessions with **groups of mixed backgrounds**: producers, engineers, HR, and
  studio heads. A recruiter **prep call** came before the onsite. That candidate said
  questions centered on tech design/architecture, working with production, and
  **conflict resolution**, with "no typical in-depth engineering questions, because they
  care about who you are and how you'll work with the team."
- **Your folder's earlier research:** about 7 interviews over ~14 days, with **two on
  design and React** and the rest behavioral.
- **Timing:** Glassdoor's average is about 34 days end to end, and some candidates
  reported much longer. A quiet week after the panel is normal.

**What this means for you:** expect several sessions in a row, and some of them with
more than one interviewer, some of them non-engineers (product/production, HR,
leadership). The technical rounds are probably **practical** (design, React, DevOps/IaC,
testing), not LeetCode-hard. **Culture fit and collaboration carry real weight.** A
product manager or producer on the panel is grading how you communicate, not how well
you know Go.

## Ask your recruiter (send this today)

You've reached the final stage, so recruiters will usually share the schedule. Ask:

1. The **agenda**: how many sessions, how long each, and **who is on each one**
   (names/roles, so you can look them up on LinkedIn).
2. Which sessions are **technical**, and in what format: live coding (which language,
   which tool), whiteboard design, React build, or discussion only?
3. Is there a **DevOps/infrastructure** or **testing** session? (One recent loop had both.)
4. Onsite in Bellevue or virtual? If onsite: where to go, parking, and whether lunch is
   part of the interview.
5. "Is there anything the team would like me to prepare or read beforehand?"
6. Whether there's a prep call, like some past candidates had. Take it if offered.

## Round-by-round prep

### 1. Coding (probably 1 round)

Use what you already have: the Go challenges `01`–`10` (or the `python/` copies), with
the timed routine from `../microsoft-partner-center-interview-prep/README.md` (clarify →
brute force → pattern → code → **hand-trace a small case** → follow-ups). Rotate through
the domain problems first (`01_swiss_pairings`, `02_standings_tiebreakers`,
`03_event_registration`), because those are also talking points with a Pokémon panel.

### 2. Design / LLD

`system_design/notes.md` prompts 1–5. "LLD" (low-level design) usually means **classes
or modules, interfaces, and data model** for one component, not a whole-system diagram.
For each prompt, practice going one level lower: Go structs and interfaces, Postgres
tables + indexes, and the REST endpoints with their status codes. Prompt 1 (sell-out
registration) and prompt 2 (tournament management) are the most likely shapes.

**Your experience to bring in:**
- The **10k reads/sec ingestion** at Axon maps to "Worlds-day traffic spike."
- The **JPMC checkout/payment consistency** work maps to "two people grab the last
  registration seat."

### 3. DevOps / infrastructure — new, not in the folder before

The JD says **AWS CDK, IaC, containers + serverless**. You've done this on Azure
(Azure DevOps, Bicep, Terraform, AKS, Function Apps) and on AWS (EC2, Lambda, S3).
CDK itself isn't on your resume. Don't hide that. Bridge from what you know:

> "My IaC experience is Terraform and Bicep. I authored the pipelines that cut our
> release cycle time 30% at Microsoft. CDK is the same model, desired-state infra
> reviewed in PRs, but in real TypeScript, with constructs and `grant*` helpers for
> least-privilege IAM. I'd expect to be productive in it quickly. I've read through
> [whatever you actually try before the panel]."

**Before the panel, actually do this (about 1 hour):** `npx cdk init app --language
typescript`, define a Lambda (Go, `provided.al2023`) + API Gateway + DynamoDB table,
then run `cdk synth` and read the generated CloudFormation. Now "I've written CDK" is
true. The sketch in `system_design/notes.md` shows the shape.

Questions to be ready for:
- **Walk through a CI/CD pipeline you built.** Use the Microsoft story: stages,
  approvals, how tests gate a deploy, how you roll back.
- **How do you deploy safely?** Blue/green or canary, feature flags, automated rollback
  on alarms, and database migrations that are backwards compatible (expand → migrate →
  contract).
- **Lambda vs Fargate vs EKS?** Use the existing notes. Add "I ran AKS in production,
  so I know the operational cost of Kubernetes. For a small team I'd default to
  Lambda/Fargate unless there's a reason not to."
- **Observability:** what you alert on (golden signals, SLOs) and how you trace a slow
  request. That's your Axon DRI story: Dynatrace PurePath/waterfall, Grafana, Datadog,
  MTTR −35%.
- **Secrets & IAM:** Secrets Manager/SSM, least-privilege roles per function, no
  long-lived keys in CI (OIDC federation from GitHub/GitLab to AWS).
- **Event-day readiness:** "Worlds is in 2 weeks. What do you do?" Load test at 3–5x
  expected traffic, pre-warm or provisioned concurrency, a freeze on risky deploys,
  runbooks, an on-call roster, and dashboards built before the event, not during it.

### 4. Testing — new

TPCi's values include **"Dedicated to Quality"**, and one recent loop had a whole
testing round. Your resume lists **Jest, Puppeteer, JUnit, Mockito**. Have answers for:

- **Your testing pyramid.** Many fast unit tests, fewer integration tests (a real
  Postgres in a container, not mocks of SQL), and a thin layer of end-to-end tests
  (Puppeteer/Playwright) for the critical flows only: registration, results upload.
- **What you mock and what you don't.** Mock things across a network boundary or that
  are slow or nondeterministic (clock, payment provider). Don't mock your own database
  queries, because that hides the bugs you care about. Mention injected clocks; your
  challenges do this (`04_login_throttle`).
- **Testing concurrency.** `go test -race`, plus a test that starts N goroutines to
  register for M < N seats and asserts that exactly M succeed (`03_event_registration`).
- **Flaky tests.** Quarantine the test, find the nondeterminism (time, ordering, shared
  state), and fix it or delete it. Never just retry until it passes.
- **Infra tests.** CDK assertions: `Template.fromStack(...).hasResourceProperties(...)`.
- **"How would you test Swiss pairings?"** Property tests: no rematches, everyone paired
  or exactly one bye, and the bye goes to the lowest-ranked player without a previous
  bye. Plus fixed examples taken from the Tournament Rules Handbook.
- **A story:** a bug that tests caught, or one that escaped and the test you added
  afterward. JPMC's monolith → SOA work improved test coverage, so use that.

### 5. React / frontend (if included)

`frontend/README.md` has the "Find an Event" live build. Do it once, timed. You've
built Angular micro-frontends with OAuth (Axon) and React dashboards, so mention both.

### 6. Behavioral + hiring manager

See the mapping below. For the hiring-manager round, also prepare:
- **Why Pokémon, why this team, why now** (≤60 seconds, specific, genuine).
- **The 24-month fixed term.** Your existing note in `behavioral/notes.md` covers it.
- **Seniority fit.** The JD says 5–7 YOE and you have 8+. Present that as a strength,
  mentoring in particular: "the JD asks for proven mentoring, and here's my example."
  Don't sound overqualified or like you're passing through.
- **"Why leave Axon after a year?"** Real reason, framed around this role. Short, and
  never negative about Axon.

## Your resume → TPCi's six values

The full STAR+L drafts are in
`../microsoft-partner-center-interview-prep/behavioral/star_stories.md`. **Same stories,
different emphasis:** for TPCi, lean into the community/customer and quality angles,
and talk less about scale.

| TPCi value | Story | Angle for this panel |
|---|---|---|
| **Passion for Pokémon** | — (personal) | `behavioral/notes.md` "prepare honestly" section. Do the 30-min homework in `company/notes.md` first. |
| **Challenging the Expected** | #1 Copilot deployment-risk tool (MSFT, −40% outages) **or** #6 AI-adoption dashboard (Axon, 3x) | You tried a new approach and introduced it carefully. |
| **Integrity and Respect** | #4 Monolith → SOA migration (JPMC), the conflict | Disagree with data, listen, commit, no villains. Expect this one: **conflict questions come up repeatedly at TPCi.** |
| **Dedicated to Quality** | #2 On-call DRI, MTTR −35% (Axon) + the testing answers above | Root cause, not just patching. |
| **Building Relationships** | #1 (partnering with platform teams) + **a mentoring example** | Every story needs this. Microsoft design docs that sped up onboarding, Boeing docs that cut onboarding ~20%, scrum facilitation at Boeing and JPMC. **Pick one named person you mentored.** |
| **Delighting Customers** | #3 OAuth watchlist micro-frontend (Axon) **or** #5 JPMC auditing pipeline (borrower turnaround) | Tell it from the end user's experience. Connect it to organizers and parents of Junior players. |

**Fill the gaps in `star_stories.md` before the panel:** the bracketed details, a real
**failure** story (#8), and a real **mentoring** story. Those two are the most likely to
come up and the least prepared right now.

## Panel tactics (several interviewers, mixed backgrounds)

- **Make eye contact with everyone**, not just whoever asked. When someone new asks a
  question, answer them directly.
- **Adjust to the audience.** For a producer or PM, give the outcome first and skip the
  jargon ("players got their pairings 5 minutes faster"). For engineers, go deep when
  they ask. Ask the panel "how deep do you want me to go?"
- **Short answers, then offer more.** About 2 minutes per STAR story, then: "happy to
  go deeper on the technical side." Panels have several people's questions to get through.
- **Write down names** at the start of each session. Use them in your questions, and in
  thank-you notes afterward.
- **Have 2 questions ready for each session**, and pick them based on the interviewer's
  role (questions are in `behavioral/notes.md`). Don't repeat the same question to
  every group.
- **Ask for a short break between sessions if you need one.** If there's a lunch
  session, treat it as part of the interview.
- **Thank-you note within 24 hours** to the recruiter, who can forward it, with one
  specific thing from your conversations.

## Prep plan (adjust once you have the date)

| When | Do |
|---|---|
| **Today** | Email the recruiter the questions above. Fill in `star_stories.md` gaps: failure + mentoring stories first. |
| **Day 1** | Company homework (`company/notes.md`, 30 min). One-hour CDK hands-on. Testing answers out loud. |
| **Day 2** | System design prompts 1–2 at LLD depth (Go structs, SQL tables, endpoints). One timed Go challenge (`03_event_registration`). |
| **Day 3** | React live build, timed. Mock behavioral: say all six values' stories out loud, ~2 min each. |
| **Day before** | Look up the panelists on LinkedIn. Re-read stories. Pick per-interviewer questions. Rest. |

**Balancing two loops:** you're also preparing for the Microsoft Partner Center loop.
The behavioral stories are shared, so polishing them helps both. The coding and design
prep is different for each: Python/BFS for Microsoft, Go/domain/practical for TPCi.
Whichever interview comes first gets that day's coding slot.

## Sources

- [Glassdoor — TPCi Senior Software Engineer interviews](https://www.glassdoor.com/Interview/The-Pok%C3%A9mon-Company-International-Senior-Software-Engineer-Interview-Questions-EI_IE447167.0,33_KO34,58.htm) (7-round loop; 2021 6-hour onsite)
- [Glassdoor — TPCi Software Engineer interviews](https://www.glassdoor.com/Interview/The-Pok%C3%A9mon-Company-International-Software-Engineer-Interview-Questions-EI_IE447167.0,33_KO34,51.htm)
- [Glassdoor — TPCi Bellevue interviews](https://www.glassdoor.com/Interview/The-Pok%C3%A9mon-Company-International-Bellevue-Interview-Questions-EI_IE447167.0,33_IL.34,42_IC1150442.htm)
- [Glassdoor — TPCi all interviews (ratings, ~34-day average)](https://www.glassdoor.com/Interview/The-Pok%C3%A9mon-Company-International-Interview-Questions-E447167.htm)
- [Interview Query — TPCi SWE guide](https://www.interviewquery.com/interview-guides/pokemon-software-engineer) (aggregator; lower confidence)
- [Scoutify — TPCi interview overview](https://scoutify.com/companies/the-pokmon-company-international/interview/) (aggregator; lower confidence)
- Earlier sources in `README.md` (Blind, AWS case study, Play! Pokémon docs)
