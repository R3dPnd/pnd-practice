# System Design — Security-flavored prep notes

One interview is System Design. There's no test harness for this one — it's a
whiteboard/talk-through round — so this is a framework + a set of practice prompts, not
code.

## What real candidates report

Researched Sept 2026 from Glassdoor, Blind, LeetCode Discuss, and dev.to — see
`../README.md`'s "Field notes" section for the coding-round version of this plus full
source links.

- **Microsoft's system design bar is "lighter than FAANG's, but very detail-oriented."**
  Multiple 2025 candidate write-ups describe the design itself as less exotic
  (rate limiters, file sync services, not "design Netflix at global scale") but note
  interviewers ask **"why" repeatedly** to test whether your reasoning actually holds
  up, not just whether you can draw the right boxes. Treat every design choice as
  something you need a one-sentence justification for, ready before they ask.
- **A specific pattern reported for Microsoft's security-org design rounds:
  design something, then the interviewer (or you, proactively) pivots into
  "now how would you attack your own design."** Build this into your own practice —
  after you finish a design, spend 2–3 minutes doing a self red-team pass out loud
  before moving on, whether or not you're asked. This is exactly what the
  **STRIDE pass in step 5 below** is for — just be ready to go a level deeper than
  "here's the checklist" into "here's specifically how I'd try to break this."
- Real reported example prompts that match this repo's practice list almost exactly:
  a **rate limiter** and a **file sync/storage service** — see practice prompts 1 and
  5 below, and coding challenge `01_rate_limiter`.

## Framework (use this shape every time, out loud, in this order)

1. **Clarify requirements before drawing anything.**
   - Functional: what does this system actually do, end to end?
   - Non-functional: scale (requests/sec, data volume, users), latency budget,
     consistency needs, availability target.
   - **Security-specific, always ask these** (this is the differentiator for this
     panel): who are the trust boundaries / actors (end user, internal service,
     admin)? What's the sensitivity of the data (PII, secrets, auth tokens)? What's
     the threat model — external attacker, malicious insider, compromised dependency?
2. **Define the API / interfaces** at a high level (what a client calls, request/response
   shape) before internals.
3. **High-level architecture diagram** — boxes and arrows: clients, load balancer,
   services, datastore(s), cache, queue, external dependencies. Narrate data flow for
   one request end to end.
4. **Deep dive on 1–2 components** the interviewer steers you toward — this is usually
   where most of the signal comes from, don't rush past the high-level diagram to get
   here, but don't get stuck drawing boxes forever either.
5. **Security review pass** (do this explicitly, even if not asked):
   - AuthN (who are you) vs AuthZ (what are you allowed to do) at each boundary.
   - Data in transit (TLS) and at rest (encryption, key management/rotation).
   - Least privilege between services (a compromised component shouldn't have blanket
     access to everything).
   - Input validation at every trust boundary — never trust a client-supplied value,
     including ones that already passed through another internal service.
   - Auditability — can you answer "who did what, when" after the fact? (This one
     specifically resonates with a Security org — logging/audit trails are often the
     actual product, not an afterthought.)
   - Rate limiting / abuse prevention (see `01_rate_limiter` and
     `08_login_attempt_monitor` in `../challenges/` — this is where those two coding
     patterns show up again at the architecture level).
6. **Tradeoffs and scaling** — bottlenecks, single points of failure, how you'd shard/
   cache/replicate, and what you'd cut first under a tighter timeline (shows judgment,
   not just knowledge).
7. **Explicitly call out what you'd do differently with more time/scale** — interviewers
   like seeing you know the corners you're cutting, not just cutting them silently.

## STRIDE (quick mental checklist during the security pass)

| Letter | Threat | Ask yourself |
|---|---|---|
| S | Spoofing | Can someone pretend to be a legitimate user/service? |
| T | Tampering | Can data be modified in transit or at rest without detection? |
| R | Repudiation | Can an actor deny having done something? (→ audit logging) |
| I | Information disclosure | Can sensitive data leak to someone who shouldn't see it? |
| D | Denial of service | Can the system be overwhelmed / made unavailable? |
| E | Elevation of privilege | Can a low-privilege actor gain higher privilege? |

STRIDE (also a Microsoft-originated framework — Adam Shostack et al., used internally
for years) tells you *what kinds* of threats to look for. If you finish STRIDE early
and the interviewer wants more depth, **DREAD** gives you a way to prioritize the ones
you found instead of just listing them flat:

| Letter | Question |
|---|---|
| D | Damage — how bad is it if this is exploited? |
| R | Reproducibility — how easy is it to reproduce? |
| E | Exploitability — how much skill/effort does it take to exploit? |
| A | Affected users — how many users/systems does it hit? |
| D | Discoverability — how easy is it for an attacker to find? |

## Practice prompts (security-flavored — pick one per mock session)

1. **Design a secure file upload/storage service** (users upload attachments, other
   users download them by link). Cover: virus/malware scanning, access control on the
   download link, preventing the path-traversal class of bug from `03_safe_path_resolver`,
   storage encryption, and how you'd stop it being used to host/distribute malware.
   *(A file-sync/storage-service design is one of the specific prompts reported by 2025
   Microsoft candidates — see field notes above.)*
2. **Design an authentication/session service** for a suite of internal apps (think
   SSO). Cover: password storage (hashing/salting, never plaintext/reversible), MFA,
   session token design and revocation, refresh-token rotation, and what happens when a
   token leaks (how fast can you invalidate it, blast radius).
3. **Design a centralized security log ingestion pipeline** (a mini SIEM) — services
   ship logs, the system needs to detect suspicious patterns (e.g. the brute-force
   pattern from `08_login_attempt_monitor`, at fleet scale) and alert. Cover: ingestion
   scale, the redaction problem from `04_log_redactor` (secrets must never reach
   long-term storage unmasked), retention/compliance, and real-time vs batch detection
   tradeoffs.
4. **Design a secrets management service** (like a mini Vault/Key Vault) — services
   fetch DB credentials/API keys at runtime instead of them being baked into config.
   Cover: how a service authenticates *to* the secrets service in the first place
   (bootstrapping trust), key rotation, audit trail of who fetched what, and short-lived
   vs long-lived credentials.
5. **Design a rate-limited public API gateway** in front of several internal services.
   Cover: per-client vs per-IP limiting (`01_rate_limiter`'s tradeoff discussion, now at
   scale — shared state across many gateway instances, e.g. Redis), authentication at
   the edge, and what a client sees when throttled. *(A rate limiter is another
   specific prompt reported by 2025 Microsoft candidates — do this one for sure.)*

## Worked walkthroughs

Full run through the framework above for each practice prompt, compressed to the key
beats — this is what "narrate it out loud" should actually sound like, not a diagram
substitute. Use these to check your own mock reps against, not to memorize verbatim.
Each one lives in its own file under `examples/`:

1. [Secure file upload/storage service](examples/01_secure_file_storage.md)
2. [Authentication/session service (SSO)](examples/02_auth_session_service.md)
3. [Centralized security log ingestion pipeline (mini SIEM)](examples/03_siem_log_pipeline.md)
4. [Secrets management service (mini Vault/Key Vault)](examples/04_secrets_management.md)
5. [Rate-limited public API gateway](examples/05_rate_limited_gateway.md)

## Day-of reminders

- Ask clarifying questions before you start drawing — silence while thinking is fine,
  but jumping straight to a diagram without scoping reads as not handling ambiguity well.
- State assumptions out loud when you make them ("I'm assuming reads vastly outnumber
  writes here — let me know if that's wrong").
- If you don't know a specific technology's internals, say what you know and reason
  from first principles rather than guessing confidently — that's the "communicate your
  reasoning" grading criterion from the recruiter email in action.
- Expect to be asked "why" more than once on the same decision — that's reported as a
  normal, not adversarial, part of Microsoft's style. Don't second-guess and change your
  answer just because they asked again; hold your position if you still believe it, or
  say explicitly what new information would change your mind.
- Finish with a deliberate self-attack pass even if not asked (see "What real candidates
  report" above) — say out loud "if I were attacking this system, I'd go after X."
