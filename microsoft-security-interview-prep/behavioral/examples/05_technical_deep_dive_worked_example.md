# Worked example: technical project deep-dive (dann-of-thursday MCP integration)

Microsoft doesn't run a separate "resume deep-dive" round — a coding or system-design
interviewer can pause mid-round and ask about a specific project, so you need at
least one story that demonstrates "designed a system, made a tradeoff" on demand,
not just the four behavioral themes. This one is grounded in a real technical
decision from `dann-of-thursday` (your local voice AI agent project) so the
*technical* details below are concrete — fill in the bracketed human details
(who you discussed it with, exact numbers) with what actually happened, since an
interviewer will ask "why" repeatedly and dig for specifics only you would know.

## The technical decision, as design material

`dann-of-thursday` connects an LLM to a set of tool-providing MCP server processes
(project discovery, calendar, notes, gardening log, BJJ log, background dev
pipelines, system control). Two separate consumers need these tools: the voice
pipeline (`voice/orchestrator.py`) and the text-chat backend
(`app/services/chat_service.py`).

**The naive design**: each consumer starts and owns its own MCP server processes.
Simple, isolated, no shared state to worry about.

**The tradeoff that mattered**: as more tool modules got added, that naive design
would double the process count (once per consumer) and double the tool schema sent
to the LLM on every turn — most modules aren't needed most of the time (calendar
tools aren't relevant to a gardening question), so a growing, mostly-irrelevant tool
schema both wastes context and gives the model more chances to pick the wrong tool.

**The actual design**: a single process-wide `MCPManager` (`get_shared_manager()`)
shared by both the voice orchestrator and chat service — one set of server
processes, not one per consumer. Most modules default to `enabled: false`
(registered but not started), and the manager exposes three meta-tools
(`list_modules`, `enable_module`, `disable_module`) so the LLM itself starts a
module's process only when a turn actually needs it. `always_on: true` stays the
escape hatch for a module (like project discovery) that should just always be
connected.

## STAR+L

- **Situation**: `dann-of-thursday` had two separate consumers of the same tool
  integrations (voice and chat), and the module list was growing — each new
  integration (gardening, BJJ, devteam) added more surface area.
- **Task**: _(what were you specifically trying to solve — was this your own
  initiative, or in response to something concrete like a noticeably slower/worse
  tool-selection turn?)_
- **Action**: I chose a shared, process-wide manager instance over one-per-consumer,
  and lazy module activation over always-on, specifically to keep both the process
  count and the tool schema small as the module list grows — the meta-tool pattern
  (`list_modules`/`enable_module`/`disable_module`) lets the LLM opt into a module's
  tools only for turns that need them, rather than the schema growing unboundedly
  with every new integration. _(Fill in: did you consider or try the naive
  per-consumer design first? Did you discuss this tradeoff with anyone, or find it
  through testing/observation?)_
- **Result**: _(what did you actually observe — e.g. tool-selection accuracy, schema
  size, process count before/after, or just "this is the current architecture and
  it's held up as N more modules got added.")_
- **Learning**: _(the concrete thing you'd do differently or now do differently on a
  similar design — e.g. "I now default new capabilities to opt-in/lazy rather than
  always-on from the start, because retrofitting that after modules accumulate is
  more disruptive than designing for it up front.")_

## Follow-ups to be ready for

- **"Why not just give each consumer its own manager?"** — isolation is simpler, but
  duplicates process count and (more importantly) duplicates the tool schema
  overhead per consumer for no benefit, since both consumers want the same tools.
- **"What's the security angle?"** (a Security-org interviewer may pivot here) — a
  shared manager also means a single place to reason about which processes are
  running and what they can access, rather than two divergent sets of running tool
  servers to audit.
- **"What would you do differently at 10x the module count?"** — _(have a real
  answer ready: e.g. grouping related modules so `enable_module` activates a
  category rather than one at a time, or caching which modules a given session
  historically needs.)_

---

# Alternate worked example: resume-grounded (Axon license-plate-read ingestion pipeline)

Use this one if the interviewer's follow-up questions push toward production-scale
distributed systems, throughput, or a security/data-integrity angle rather than an
LLM-tooling angle — it's grounded in the Axon bullet: "high-throughput distributed
ingestion and processing pipelines handling 10,000+ license plate reads per second
from AI-enabled edge cameras on AWS (EC2, Lambda, S3) — extracting, normalizing, and
spatially indexing metadata using bounding-box geospatial queries... while handling
intermittent connectivity, on-device processing constraints, and malformed inputs
across geographically distributed sites." Fill in the bracketed specifics (exact
AWS services wired together, real numbers, who you discussed the design with) —
an interviewer will ask "why" repeatedly and dig for details only you would know.

## The technical decision, as design material

Edge cameras at geographically distributed sites produce license-plate reads —
10,000+ per second in aggregate — that need to be extracted, normalized, and
spatially indexed (via bounding-box geospatial queries) before downstream AI/ML
systems can consume them. Two constraints make this harder than a typical ingestion
pipeline: edge sites have **intermittent connectivity** (a site can drop offline and
later reconnect with a backlog of reads to send), and camera output is not fully
trusted — it can arrive **malformed**.

**The naive design**: process and geospatially index each read synchronously, inline
in the request path, as it arrives from a camera — extract, normalize, index, done,
one read at a time.

**The tradeoff that mattered**: at this throughput, and with edge sites that
periodically reconnect and replay a backlog, synchronous inline processing means a
burst of replayed reads from one reconnecting site competes directly with live
reads from every other site for the same processing path — a backlog replay (or any
slowdown in the normalization/indexing step) risks creating backpressure that delays
or drops *new* incoming reads, not just the backlog. It also means a single
malformed read can stall or crash the same code path that's supposed to be handling
9,999 other reads that second.

**The actual design**: decouple ingestion from processing. Incoming reads land
first (via [fill in: e.g. S3 + event-driven Lambda triggers]), get validated at that
boundary — malformed reads are rejected/quarantined rather than allowed to propagate
— and only then move into normalization and spatial indexing as a separate,
independently-scalable stage. That separation means a reconnecting site's backlog
replay competes for capacity in the processing stage, not the ingestion path
itself, so live reads from other sites keep flowing. [Fill in: how you actually
implemented the decoupling — e.g. Lambda concurrency/queueing behavior, any
batching you did before writing to the spatial index.]

## STAR+L

- **Situation**: Axon's edge cameras generate 10,000+ license-plate reads per
  second across geographically distributed sites, several of which have
  intermittent connectivity, and the reads need to be normalized and spatially
  indexed for downstream AI/ML systems.
- **Task**: _(was this greenfield work you designed from scratch, or did you
  inherit a version of this pipeline and redesign a piece of it? What specifically
  triggered the decoupled design — an incident, a load test, or a design review
  before anything shipped?)_
- **Action**: I chose to decouple ingestion from processing rather than handling
  reads synchronously and inline, specifically so that a reconnecting site's backlog
  replay, or a slow/failing normalization step, couldn't create backpressure on live
  reads from other sites. I also pushed input validation to the ingestion boundary
  so a malformed read from a camera gets rejected there instead of propagating into
  the geospatial indexing logic or downstream ML systems. _(Fill in: did you
  prototype the synchronous version first and hit a real bottleneck, or design this
  way from the start? Who reviewed this design with you?)_
- **Result**: _(what did you actually observe — throughput sustained during a
  reconnect/backlog event, reduction in malformed-data incidents downstream, or
  simply "this is the architecture and it's held up under N sites' worth of
  intermittent connectivity.")_
- **Learning**: _(the concrete thing you do differently now — e.g. "I now assume
  any edge/IoT-sourced input is intermittent and adversarial-shaped by default, and
  design the ingestion boundary around that from day one, rather than treating
  connectivity gaps and malformed input as edge cases to patch in later.")_

## Follow-ups to be ready for

- **"Why not just add more compute to the synchronous path instead of decoupling
  it?"** — more compute helps raw throughput, but doesn't fix the coupling problem:
  a reconnecting site's backlog would still compete directly with live traffic for
  the same path, and a malformed read could still stall processing for everyone
  sharing that path at that instant.
- **"What's the security angle?"** (a Security-org interviewer will likely ask this
  directly) — edge cameras are a class of input you don't fully trust: they can be
  compromised, misconfigured, or simply buggy, so validating and quarantining
  malformed input at the ingestion boundary — before it reaches normalization,
  spatial indexing, or downstream ML systems — is a data-integrity control, not
  just robustness. It also bounds the blast radius of a bad/compromised camera to
  the ingestion stage instead of letting it corrupt indexed data.
- **"What would you do differently at 10x the read volume?"** — _(have a real
  answer ready: e.g. partitioning the spatial index by geographic region so a hot
  region doesn't bottleneck the whole index, or tuning batching/concurrency limits
  per ingestion source so one site's backlog can't starve others.)_
