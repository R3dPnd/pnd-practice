# Disney (DEEP&T) Senior Front-End — Interview Prep

Prep repo for a Senior Front-End Engineer loop at Disney, most likely landing in **Disney
Entertainment & ESPN Product & Technology (DEEP&T)** — the org behind Disney+, Hulu, and
ESPN+ (see `../espn-conent-dashboard/` for the deep hands-on stack project: TypeScript,
Node.js, React, GraphQL, OpenSearch, Contentful, Docker — that's the actual DEEP&T job
description stack, and it's a separate build-along resource this repo doesn't duplicate).

**First interview: Friday, 2026-09-18.** Hopefully a fuller loop the week of 2026-09-21,
format TBD.

## The single most important thing to know going in

**Disney does not run a standardized interview loop.** A recurring, independently-reported
theme across candidates (see Field notes below): format, difficulty, and even whether
there's live coding at all varies **by team and by interviewer**, not by a fixed company
process. One reported quote: *"There is zero standardized interview process at Disney.
It's entirely up to the team to decide how they interview."* Reported first-technical-round
shapes range from a friendly FizzBuzz, to a DFS graph problem, to a scope/closures trick-
question code review of a mock PR, to a **live "build this React component to a spec"
exercise** (see below) — with no way to predict which one you'll get. This repo preps you
broadly across all of them rather than betting on one shape.

## Layout

```
challenges/              10 practice problems, JS/TS, each self-contained
  NN_topic/
    README.md            problem statement, constraints, why it's FE-relevant
    solution_*.mjs        reference implementation
    practice_*.mjs        stub for YOU to fill in (throws "not implemented")
    *.test.mjs            node:test suite — runs against your practice file by default
  _lib/load-impl.mjs      shared PRACTICE/solution toggle loader
frontend_design/notes.md  FE-architecture-flavored system design framework + prompts
  examples/               worked-example walkthroughs, one per practice prompt
behavioral/notes.md       STAR framework (Disney's own recommended shape) + themes
  examples/               STAR templates, one per theme
```

## How the practice/solution toggle works

Every test file loads the implementation like this:

```js
const { debounce } = await loadImpl(import.meta.url, "debounce");
```

- `npm test` (default) → tests run against **your** `practice_*.mjs`. Freshly written,
  those throw `Error("not implemented")`, so tests fail until you implement them.
- `npm run test:solutions` (`PRACTICE=0`) → tests run against the **reference**
  `solution_*.mjs`, so you can confirm the tests are legit or peek at a working baseline.

Recommended loop per challenge: read the `README.md`, **don't** look at `solution_*.mjs`,
implement `practice_*.mjs` against the clock (most FE take-homes/live rounds are
30–60 min), run the tests, then diff against the reference and say out loud what you'd do
differently with more time — that's rehearsing the actual "explain your tradeoffs" skill
Disney's own interview page says it's grading for (see Field notes).

## Setup

```bash
cd disney-frontend-interview-prep
npm test                    # run everything against your in-progress practice files
npm run test:solutions      # sanity-check: run everything against the reference solutions
node --test challenges/06_binary_tree_bfs -v   # work one challenge at a time
```

Requires Node 20+ (this repo uses `node:test` and `node --test`'s built-in timer mocking —
no external test framework needed, nothing to `npm install`).

## Challenge index

Picked to match what real 2025–2026 candidates report being asked (see Field notes) —
skewed toward the JS-fundamentals questions FE rounds actually ask (debounce, promises,
closures) plus the specific LeetCode-style patterns Disney's own tagged problem list
repeats (grid BFS/flood-fill, tree BFS, linked lists).

| # | Challenge | Pattern | Why it's here |
|---|---|---|---|
| 01 | `debounce_throttle` | closures, timers | The single most commonly reported FE trivia/coding question everywhere, incl. Disney threads |
| 02 | `promise_polyfill` | async, Promise internals | Reported real question: "write a Promise" |
| 03 | `event_emitter` | pub/sub, closures | Classic FE "build a mini library" question; underlies most component communication |
| 04 | `deep_clone` | recursion, object graphs | Common FE fundamentals question (handles cycles, nested structures) |
| 05 | `flatten_and_curry` | recursion, function composition | Common JS-fundamentals pairing question |
| 06 | `binary_tree_bfs` | tree, level-order/BFS | Reported real question: "BFS of a binary tree"; matches Disney's tagged "Populating Next Right Pointers" |
| 07 | `grid_flood_fill` | grid BFS/DFS | Matches Disney's tagged "Flood Fill" and "Walls and Gates" problems directly |
| 08 | `reverse_linked_list_in_k_groups` | linked list, pointers | Reported real question: "linked list flip every two nodes" |
| 09 | `memoize` | closures, caching | Common FE performance question; ties into `frontend_design`'s caching discussions |
| 10 | `array_polyfills` | reimplement `map`/`filter`/`reduce` | Extremely common "prove you understand JS" trivia round question |

## The live-coding wildcard: "build this component to a spec"

At least one 2025 candidate reported the *entire* technical round was: build a React
scoreboard/banner component against a provided API spec, in ~1 hour, 5 implementation
steps, **Google allowed, AI tools not allowed** (see Field notes — this is a separate
policy note from the interviewer, confirm your own panel's rules, but plan to practice
without AI regardless). This is a fundamentally different skill from the algorithmic
challenges above — it's "can you turn a spec into working, reasonably clean React under
time pressure," not "do you know a clever algorithm." Practice this shape directly:

- Use the existing `../espn-conent-dashboard/` project's `ContentTable`/`ContentRow`
  pattern (`README.md` Module 3) as a template for what "clean, senior-level React under
  time pressure" looks like: typed props, `memo`/`useCallback` where it actually matters,
  clear loading/empty states.
- Time-box yourself: pick any small, spec-able UI piece (a live score ticker, a paginated
  list, a filter bar) and build it from a written spec in under an hour, without AI
  assistance, out loud, narrating decisions the way you would in the room.
- If given an ambiguous API, ask clarifying questions before writing code — same "handle
  ambiguity out loud" signal every round below is grading for.

## Day-by-day plan (today is Mon 2026-09-14; first interview Fri 2026-09-18)

Format is unknown (see above), so the plan covers behavioral, JS-fundamentals coding, and
a live-build rep — not a bet on one shape.

| Day | Focus | Coding | Other |
|---|---|---|---|
| **Mon 9/14 (today)** | Warm up, untimed | `01_debounce_throttle`, `02_promise_polyfill` | Skim `behavioral/notes.md`; draft your 4 STAR stories' Situation/Task bullets only |
| **Tue 9/15** | JS fundamentals | `03_event_emitter`, `10_array_polyfills` (30–40 min each, timed) | Skim `frontend_design/notes.md`; do one live-build rep (see above), 45–60 min, no AI |
| **Wed 9/16** | Trees/grids/lists | `06_binary_tree_bfs`, `07_grid_flood_fill`, `08_reverse_linked_list_in_k_groups` (30–40 min each) | Finish all 4 STAR stories fully (Action/Result/Learning beats); read `../espn-conent-dashboard/README.md` Module 3 (React patterns) once if rusty on hooks/memo |
| **Thu 9/17** | Taper + mixed review | Redo `01` and `02` from a blank file, 15 min each, no peeking; skim `04`, `05`, `09` | Re-read your STAR stories out loud once; re-read Field notes below; confirm camera/mic/quiet room |
| **Fri 9/18 — interview day** | 15 min easy warm-up (`01_debounce_throttle` from memory) | | Review STAR bullet points; log in 5–10 min early |
| **Week of 9/21 (if a fuller loop follows)** | Assume it may include: a deeper live-coding/system-design/behavioral panel per Field notes below | Full mock: one algorithmic problem + one live-build rep, 90 min combined | One 45–60 min mock FE system design cold, using `frontend_design/notes.md`; re-confirm format with your recruiter as soon as it's scheduled — worth explicitly asking what to expect, since there's no company-wide standard to assume from |

## What each round is probably grading (best-guess — no recruiter email to go on)

Unlike a company with a published rubric, Disney's own careers-site interview-prep page
and independent reports converge on a few consistent signals rather than a formal scorecard:

- **Can you explain your reasoning and tradeoffs clearly**, not just produce a correct
  answer — reported tone is "conversational," valuing clear explanation over
  performing-under-pressure.
- **Can you turn ambiguity into a plan** — ask clarifying questions before coding or
  designing, whether the prompt is an algorithm, a component spec, or a design question.
- **Storytelling** — Disney's own interview-prep material frames your career narrative
  explicitly in storytelling terms ("what role did you play, how did you drive the plot")
  — see `behavioral/notes.md`.
- **JS/React fundamentals depth** over exotic algorithms — closures, `this`, async/
  Promises, and React rendering behavior (memoization, hooks) are reported far more than
  hard LeetCode.

## Field notes: what real candidates report

Researched Sept 2026 across Glassdoor, Blind (teamblind.com), LeetCode's Disney company
tag, Exponent, Prepfully, JoinTaro, and Disney's own careers site. Treat this as
pattern-matching across independent, self-reported accounts for a company with an
explicitly *non*-standardized loop — more so than usual, don't assume your loop matches
any single account below.

**Round structure, roughly:** 3–5 rounds over 2–6 weeks is the commonly reported range: a
~20–30 min recruiter screen (background, interest, comp, work authorization), then either
a live technical assessment (sometimes HackerRank-hosted) or a hiring-manager
deep-dive conversation, then a final panel/set of virtual meetings with senior engineers,
tech leads, and PMs covering system design, deeper coding, and behavioral — though, per the
Blind quote above, *whether* you get all of these stages, and in what order, is
team-dependent, not guaranteed.

**Technical round — reported shapes, in no particular order:**
- Straightforward DSA: arrays, strings, linked lists, trees with BFS/DFS — "most commonly
  reported" per multiple 2025–2026 write-ups.
- A live React build exercise against a provided spec/API — one detailed 2025 report
  (Software Engineer II, Frontend) describes building a scoreboard/banner component in
  ~1 hour across 5 steps, Google allowed, AI tools explicitly not allowed.
- A **code-review exercise** — reviewing a mock PR, with "scope-related trick questions,"
  no live coding at all.
- A plain **FizzBuzz** for one candidate vs. a **DFS graph problem** for another candidate
  interviewing for the same role, per one Blind thread — underscores the "ask your
  recruiter what to expect" advice above.
- Specific reported questions: "write a Promise" (→ `02_promise_polyfill`), BFS of a
  binary tree (→ `06_binary_tree_bfs`), reverse/flip a linked list two nodes at a time
  (→ `08_reverse_linked_list_in_k_groups`), and a "tell me about a production incident/
  regret" question (behavioral, woven into a technical round — same pattern as
  Microsoft's "resume deep-dive isn't separate" behavior, if you've prepped that repo).
- Disney's LeetCode company tag lists ~32 tagged problems (9 easy / 17 medium / 6 hard),
  skewed toward **Array** and **Binary Search**, with **Walls and Gates**, **Populating
  Next Right Pointers in Each Node**, and **Flood Fill** specifically named in candidate
  write-ups (→ `07_grid_flood_fill`, `06_binary_tree_bfs` cover these patterns).
- One broader note on Disney Streaming Technology specifically (DEEP&T's consumer
  products — Disney+/Hulu/ESPN+): hiring bar is reported as "closer to Netflix than
  typical enterprise media," and SQL comes up in roughly half of reported Disney Streaming
  SWE interviews — worth a refresher on basic joins/aggregations even for a front-end
  title, in case the loop leans full-stack.

**Behavioral — Disney's own guidance (from disneycareers.com/interview-prep), not just
inferred:** Disney explicitly recommends the **STAR** framework — Situation, Task,
Action, Result — and frames it in storytelling language: *"Set the stage for your
interviewer,"* describe *"the creativity you brought, and how you collaborated with
others,"* and share *"the outcome and impact of your efforts."* Independent write-ups
describe candidates preparing 5–7 stories (some call it the "SOAR" method) covering
customer service, teamwork, problem-solving, and "going above and beyond," plus explicit
questions about alignment with Disney's stated values (Creativity, Quality, Community/
inclusivity) and the "cast member" mindset. Unlike Microsoft's explicit "+L" learning
beat, nothing in Disney's own material asks for a closing "what I changed" line — but
`behavioral/notes.md` still recommends including one anyway, since it's a strictly
stronger answer and no interviewer will penalize you for a beat they didn't ask for.

**Tone:** repeatedly described as conversational and low-pressure relative to reputation —
interviewers reportedly care more about whether you can explain your experience and
tradeoffs clearly than whether you can perform flawlessly under a countdown clock.

Sources:
- [Disney Software Engineer Interview Questions + Guide — InterviewQuery](https://www.interviewquery.com/interview-guides/disney-software-engineer)
- [Walt Disney Company Senior Software Engineer Interview Experience & Questions — Glassdoor](https://www.glassdoor.com/Interview/Walt-Disney-Company-Senior-Software-Engineer-Interview-Questions-EI_IE717.0,19_KO20,44.htm)
- [Walt Disney Company Software Engineer Interview Experience & Questions — Glassdoor](https://www.glassdoor.com/Interview/Walt-Disney-Company-Software-Engineer-Interview-Questions-EI_IE717.0,19_KO20,37.htm)
- [Disney's Interview Process (2026) — TechPrep](https://www.techprep.app/blog/disney-interview-process)
- [Disney Software Engineer Interview: Step-by-Step — Interview Coder](https://www.interviewcoder.co/blog/disney-software-engineer-interview)
- [Disney Frontend Engineer Interview Questions (Updated 2026) — Exponent](https://www.tryexponent.com/questions?company=disney&role=frontend-engineer)
- [Disney Frontend Engineer: 2025 interview question bank — Prepfully](https://prepfully.com/interview-questions/disney/frontend-engineer)
- [Disney LeetCode & Coding Interview Questions — LeetCode company tag](https://leetcode.com/company/disney/)
- [Disney Software Engineer II - Frontend Interview Experience — JoinTaro](https://www.jointaro.com/interviews/companies/disney/experiences/software-engineer-ii-frontend-bergen-op-zoom-may-1-2025-no-offer-positive-1707e185/)
- [Disney Front End Interview — Blind](https://www.teamblind.com/post/Disney-Front-End-Interview-xps3iWeG)
- [Behavioral Interview Questions — Disney Careers](https://www.disneycareers.com/en/interview-prep)
- [How to Ace the Disney Interview: Insights from an Ex-Disney Recruiter — Medium](https://medium.com/interview-guide/how-to-ace-the-disney-interview-insights-from-an-ex-disney-recruiter-1dbd7e4444f8)
