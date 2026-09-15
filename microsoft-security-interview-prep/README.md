# Microsoft Security — Interview Prep

Prep repo for the Microsoft Security Virtual Interview Day on **Wednesday, 2026-09-17**:
one System Design interview + two Coding interviews (60 min each), with behavioral/
collaboration questions woven throughout. Panel said explicitly: **no AI tools during the
actual interview** — so use this repo now, then go in on your own.

## Layout

```
challenges/            16 practice problems, each self-contained
  NN_topic/
    README.md          problem statement, constraints, examples, hints
    solution_*.py       reference implementation
    practice_*.py        stub for YOU to fill in (raises NotImplementedError)
    test_*.py            pytest suite — runs against your practice file by default
conftest.py             shared FakeClock fixture for time-based challenges
system_design/notes.md  security-flavored system design frameworks + practice prompts
  examples/              worked-example walkthroughs, one per practice prompt
behavioral/notes.md     STAR+L framework + the four themes Microsoft actually grades
  examples/              STAR+L templates (one per theme) + a worked technical deep-dive
```

## Challenge index

Two tracks. **Classics** are generic algorithm/data-structure problems — this is the
shape a Microsoft coding round is *most likely* to actually hand you. **Security** are
scenario-flavored problems built around the kind of thing a Security org specifically
cares about — good for the "security-minded engineering" grading criterion and for
system-design talking points, less likely to be the literal prompt verbatim.

| # | Challenge | Pattern | Track |
|---|---|---|---|
| 01 | `rate_limiter` | token bucket, time-windowed state | Security |
| 02 | `lru_cache` | hash map + doubly linked list | Classic |
| 03 | `safe_path_resolver` | string/path normalization | Security |
| 04 | `log_redactor` | regex | Security |
| 05 | `reliable_retry` | backoff, state machine (circuit breaker) | Security/Reliability |
| 06 | `trie_autocomplete` | trie, DFS | Classic |
| 07 | `dependency_cycle_detector` | graph, DFS 3-color, topological sort | Classic/Security |
| 08 | `login_attempt_monitor` | sliding window | Security |
| 09 | `two_sum` | hash map | Classic |
| 10 | `longest_substring_without_repeating` | sliding window, string | Classic |
| 11 | `merge_intervals` | sort + linear sweep | Classic |
| 12 | `number_of_islands` | grid BFS/DFS, connected components | Classic |
| 13 | `linked_list_basics` | pointer manipulation (reverse/cycle/merge) | Classic |
| 14 | `lowest_common_ancestor` | binary tree recursion | Classic |
| 15 | `top_k_frequent_elements` | hash map + heap/bucket sort | Classic |
| 16 | `word_break` | dynamic programming (1D, string) | Classic |

## How the practice/solution toggle works

Every test file imports the implementation like this:

```python
impl = _load_impl("rate_limiter")   # picks practice_rate_limiter or solution_rate_limiter
```

- `pytest` (default) → tests run against **your** `practice_*.py`. Freshly generated,
  those raise `NotImplementedError`, so tests fail until you implement them.
- `PRACTICE=0 pytest` → tests run against the **reference** `solution_*.py`, so you can
  confirm the tests themselves are legit / see them pass, or peek at a working baseline
  when stuck.

Recommended loop per challenge: read the `README.md`, **don't** look at `solution_*.py`,
implement `practice_*.py` against the clock, run `pytest challenges/NN_topic/`, then diff
your approach against the reference solution and talk through tradeoffs out loud (that's
literally what they're grading).

## Setup

```bash
cd microsoft-security-interview-prep
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# run everything against your own in-progress solutions
.venv/bin/pytest

# run everything against the reference solutions (sanity check / see it pass)
PRACTICE=0 .venv/bin/pytest

# work one challenge at a time, verbose
.venv/bin/pytest challenges/09_two_sum -v
```

## Day-by-day plan (today is Wed 9/10; interview is Wed 9/17)

Classics come first each day — they're the more likely shape of the real prompts.
Security-flavored ones are folded in as the secondary problem and as system-design
material.

| Day | Focus | Coding (timed after day 1) | System design |
|---|---|---|---|
| **Wed 9/10 (today)** | Environment + warm-up, untimed | `09_two_sum`, `02_lru_cache`, `01_rate_limiter` — read every solution after, even if you got it right | Skim `system_design/notes.md` framework + STRIDE table |
| **Thu 9/11** | String/array patterns | `10_longest_substring_without_repeating`, `11_merge_intervals` (30–40 min each); skim `03_safe_path_resolver` | Practice prompt: "design a secure file storage / upload service" |
| **Fri 9/12** | Graphs + linked lists | `12_number_of_islands`, `13_linked_list_basics` (40 min each); skim `04_log_redactor`, `05_reliable_retry` | Practice prompt: "design an auth/session service" |
| **Sat 9/13** | Trees + DP + catch-up | `14_lowest_common_ancestor`, `16_word_break`, `15_top_k_frequent_elements`; skim `06_trie_autocomplete`, `07_dependency_cycle_detector`, `08_login_attempt_monitor`; then **redo Day 1's three problems from a blank file**, 20 min each, no peeking | Practice prompt: "design a centralized security log / SIEM ingestion pipeline" |
| **Sun 9/14** | Behavioral + security fundamentals | Light — re-read your two weakest solutions and rewrite the explanation out loud | Review OWASP Top 10, AuthN vs AuthZ, least privilege, threat modeling (STRIDE + DREAD); draft 4–5 **STAR+L** stories from your projects using `behavioral/notes.md`'s four theme templates (dann-of-thursday's MCP integration work is good "designed a system, made a tradeoff" material — see `behavioral/examples/05_technical_deep_dive_worked_example.md`) |
| **Mon 9/15** | Full mock loop | Pick 2 problems at random across *all 16* (aim for one array/string + one graph/tree/DP, mirroring a real 2-problem round), 60 min combined, narrate out loud the whole time | One 45–60 min mock design, cold, on a prompt you haven't seen this week |
| **Tue 9/16** | Taper | Skim all `README.md`s + your notes, no new problems | Re-read your STAR stories once; confirm Teams/mic/camera/quiet room |
| **Wed 9/17 — interview day** | 15 min easy warm-up (e.g. rewrite `09_two_sum` or `02_lru_cache` from memory), review your STAR bullet points, log into Teams 5–10 min early | | |

## Daily checklist

Same plan as the table above, broken into checkable items per day.

### Wed 9/10 — Environment + warm-up, untimed
- [ ] `09_two_sum`
- [ ] `02_lru_cache`
- [ ] `01_rate_limiter`
- [ ] Read every solution above, even the ones you got right
- [ ] Skim `system_design/notes.md` framework + STRIDE table

### Thu 9/11 — String/array patterns
- [ ] `10_longest_substring_without_repeating` (30–40 min, timed)
- [ ] `11_merge_intervals` (30–40 min, timed)
- [ ] Skim `03_safe_path_resolver`
- [ ] System design practice prompt: "design a secure file storage / upload service"

### Fri 9/12 — Graphs + linked lists
- [ ] `12_number_of_islands` (40 min, timed)
- [ ] `13_linked_list_basics` (40 min, timed)
- [ ] Skim `04_log_redactor`
- [ ] Skim `05_reliable_retry`
- [ ] System design practice prompt: "design an auth/session service"

### Sat 9/13 — Trees + DP + catch-up
- [ ] `14_lowest_common_ancestor` (timed)
- [ ] `16_word_break` (timed)
- [ ] `15_top_k_frequent_elements` (timed)
- [ ] Skim `06_trie_autocomplete`
- [ ] Skim `07_dependency_cycle_detector`
- [ ] Skim `08_login_attempt_monitor`
- [ ] Redo Day 1's three problems from a blank file, 20 min each, no peeking
- [ ] System design practice prompt: "design a centralized security log / SIEM ingestion pipeline"

### Sun 9/14 — Behavioral + security fundamentals
- [ ] Re-read your two weakest solutions and rewrite the explanation out loud
- [ ] Review OWASP Top 10
- [ ] Review AuthN vs AuthZ
- [ ] Review least privilege
- [ ] Review threat modeling (STRIDE + DREAD)
- [ ] Draft 4–5 STAR+L stories using `behavioral/notes.md`'s four theme templates (`examples/01`–`04`)
- [ ] Fill in the worked technical deep-dive (`behavioral/examples/05_technical_deep_dive_worked_example.md`, dann-of-thursday's MCP integration work)

### Mon 9/15 — Full mock loop
- [ ] Pick 2 problems at random across all 16 (one array/string + one graph/tree/DP), 60 min combined, narrate out loud
- [ ] One 45–60 min mock system design, cold, on a prompt you haven't seen this week

### Tue 9/16 — Taper
- [ ] Skim all challenge `README.md`s + your notes, no new problems
- [ ] Re-read your STAR stories once
- [ ] Confirm Teams/mic/camera/quiet room

### Wed 9/17 — Interview day
- [ ] 15 min easy warm-up (rewrite `09_two_sum` or `02_lru_cache` from memory)
- [ ] Review your STAR bullet points
- [ ] Log into Teams 5–10 min early

## What each round is actually grading (from the recruiter email)

- **System design**: how you think through ambiguity, tradeoffs, and scale — not just
  the final diagram. Ask clarifying questions before drawing boxes.
- **Coding (x2)**: problem-solving/algorithms, clean & maintainable code, debugging and
  reliability concepts, **security-minded engineering**, and narrating your reasoning.
- **Woven throughout**: be ready to go deep on specific projects from your resume — your
  contributions, decisions, and what you'd do differently.

Talk out loud in every practice rep, even alone — narrating is the actual skill being
tested, not just correctness.

## Field notes: what real candidates report

Researched Sept 2026 across Glassdoor, Blind (teamblind.com), LeetCode Discuss, dev.to,
and LinkedIn — candidate write-ups and a couple of recruiter/interviewer-side posts.
Sources are linked at the bottom of this section. Treat all of this as pattern-matching
across many self-reported, unofficial accounts, not a guarantee of your specific loop —
but the patterns below repeat across enough independent sources to be worth prepping to.

**Format matches the recruiter email closely.** Multiple 2025 write-ups describe
Microsoft's virtual onsite as running 3–4 rounds of ~45–60 minutes each on Microsoft
Teams: 1–2 coding rounds, 1 system design round, 1 behavioral-leaning round — exactly
the shape in your invite (three 60-min rounds: two coding, one system design, behavioral
woven throughout). One recurring detail: **the "resume deep-dive" isn't a separate
round** at Microsoft — it's folded into whichever round you're in, so be ready for a
coding or design interviewer to pause and ask about a specific project at any point, not
just in a dedicated behavioral slot.

**Coding rounds, by reported topic frequency:**
- Heaviest emphasis: **arrays + hash maps** (→ `09_two_sum`, `15_top_k_frequent_elements`)
  and **graph/BFS traversal, often shortest-path or grid-style** (→ `12_number_of_islands`).
- Also commonly reported: **intervals** (→ `11_merge_intervals`), **trees**
  (→ `14_lowest_common_ancestor`), **string/sliding-window**
  (→ `10_longest_substring_without_repeating`), and **DP** (→ `16_word_break`).
- Specific problems named in recent (2025) candidate write-ups: merge intervals,
  trapping rain water, and "anagram-related" problems where you're expected to explain
  your approach *before* coding — don't just start typing.
- **Follow-ups matter as much as the first solution.** Reported follow-up patterns:
  "what if the input is 100x larger," "how would you reduce memory," "how would you
  refactor this for reuse elsewhere." After you get a working solution in any challenge
  here, spend 2 more minutes answering those three questions out loud before moving on
  — that's rehearsing the actual follow-up, not just the base problem.
- **Difficulty is rated moderate, but margin for error is small.** One summary puts it
  well: the problems themselves aren't the hardest LeetCode has to offer, but
  interviewers notice small mistakes (an off-by-one, an unhandled edge case, sloppy
  naming) more than at some other companies — clean code and edge-case coverage are
  graded explicitly, not just "does it run."
- Microsoft's own LeetCode company-tag page lists ~54 tagged problems (roughly 20 easy /
  27 medium / 7 hard), skewed toward Array and Hash Table. If you want extra reps beyond
  this repo's 16 challenges, high-value LeetCode names not built out here: **Group
  Anagrams**, **Trapping Rain Water**, **Maximum Depth of Binary Tree**, **Diameter of
  Binary Tree**, **Binary Tree Right Side View**, **Interval List Intersections**,
  **Course Schedule** (same pattern as `07_dependency_cycle_detector`, worth doing the
  LeetCode version too since it's the most literally-reported one).

**System design** — see `system_design/notes.md`'s "What real candidates report"
section for the full detail. Short version: lighter-weight than a typical FAANG design
round (reported real prompts: a **rate limiter**, a **file sync/storage service** — both
match practice prompts already in this repo), but interviewers ask **"why" repeatedly**
to pressure-test your reasoning, and the **security-org-specific pattern is "design it,
then attack your own design"** — build a self-red-team pass into every mock rep.

**Behavioral** is scored against four recurring themes, not free-form: **growth
mindset** (learning from failure/setbacks — Microsoft's culture is explicitly built
around Carol Dweck's "growth mindset" framing since the Nadella era), **collaboration /
cross-team friction**, **ownership**, and **customer impact**. Reported real prompts
include "tell me about a time you had a conflict with someone — how did you resolve it
and what did you learn" and "describe a time collaborating across teams didn't go well,
and your learnings." The suggested structure candidates report working well is
**STAR+L** — STAR (Situation, Task, Action, Result) plus a fifth beat: **the concrete
behavioral change you made afterward.** That closing sentence — what you'd do
differently, or did differently next time — is reportedly the single most important
line in a Microsoft behavioral answer; don't end on the Result.

**Post-interview timeline — set expectations now so a quiet week doesn't rattle you.**
Glassdoor's aggregate numbers for security-adjacent roles: Cyber Security Analyst
candidates rate the process 4/5 difficulty and 67% positive experience, averaging ~28
days to hire; Security Researcher candidates rate it 3/5 difficulty and only 38%
positive. Independently, a *lot* of Blind threads describe slow or missing follow-up
after final rounds (multi-week silences, occasional recruiter unresponsiveness) as
common, not unusual, across Microsoft generally. None of that is something to fix on
your end — it's just useful to know going in so a week of silence after 9/17 reads as
"normal Microsoft timeline," not as a bad signal about how it went. A polite
check-in with your recruiter (Stephanie) roughly a week out if you haven't heard
anything is a reasonable, well-within-norms thing to send.

Sources:
- [Microsoft Security Engineer Interview Experience & Questions — Glassdoor](https://www.glassdoor.com/Interview/Microsoft-Security-Engineer-Interview-Questions-EI_IE1651.0,9_KO10,27.htm)
- [Microsoft Security Researcher Interview Experience & Questions — Glassdoor](https://www.glassdoor.com/Interview/Microsoft-Security-Researcher-Interview-Questions-EI_IE1651.0,9_KO10,29.htm)
- [Microsoft Cyber Security Analyst Interview Experience & Questions — Glassdoor](https://www.glassdoor.com/Interview/Microsoft-Cyber-Security-Analyst-Interview-Questions-EI_IE1651.0,9_KO10,32.htm)
- [Security Engineer Interview Resources Megathread — Blind](https://www.teamblind.com/post/Security-Engineer-Interview-Resources-Megathread-Fp1izvtL)
- [Microsoft Security Service Engineer Interview — Blind](https://www.teamblind.com/post/Microsoft-Security-Service-Engineer-Interview-XZRpy52C)
- [Microsoft Security Interview — Blind](https://www.teamblind.com/post/Microsoft-Security-Interview-Y3kzeTCV)
- [Ghosted by Microsoft Recruiter after first round Virtual Interview — Blind](https://www.teamblind.com/post/Ghosted-by-Microsoft-Recruiter-after-first-round-Virtual-Interview-a2cCEMH7)
- [Microsoft SDE-2 Recent questions 2025 | Consolidated — LeetCode Discuss](https://leetcode.com/discuss/interview-question/6403987/Microsoft-SDE-2-Recent-questions-2025-or-Consolidated/)
- [Microsoft 2025 virtual onsite interview experience — dev.to](https://dev.to/net_programhelp_e160eef28/microsoft-2025-virtual-onsite-interview-experience-english-version-43fl)
- [Microsoft LeetCode Interview Questions (2025) — hackmnc](https://www.hackmnc.com/companies/microsoft/leetcode-interview-questions)
- [Microsoft Behavioral Interview Questions: What Gets Scored — SpaceComplexity](https://spacecomplexity.ai/blog/microsoft-behavioral-interview-questions)
- [Microsoft System Design Interview (2026 Guide) — Exponent](https://www.tryexponent.com/blog/microsoft-system-design-interview)
- [Experiences Threat Modeling at Microsoft — Adam Shostack](https://shostack.org/files/papers/modsec08/Shostack-ModSec08-Experiences-Threat-Modeling-At-Microsoft.pdf)
