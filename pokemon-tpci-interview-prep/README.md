# The Pokémon Company International — SDE (24-month fixed term) interview prep

**Role:** Software Development Engineer, Bellevue WA, hybrid. Builds "the technology that
enables our communities, from small gatherings to our largest events" — almost certainly
**Play! Pokémon** organized play (leagues → Regionals → Worlds). See `company/notes.md`.

**Stack from the JD:** Go · TypeScript · React · REST · AWS CDK / IaC · Postgres · NoSQL ·
containers + serverless (some Python/JS a plus). 5–7 YOE, mentoring expected.

## What we know about the interview process (public reports — verify with your recruiter)

TPCi's process varies a lot by team. What people have reported:

- **Recruiter screen → hiring manager call** (background + high-level technical questions
  about the role) → recruiter feedback/prep call → **loop** of several 30–60 min interviews
  with engineers, managers, and HR. One SWE report: ~7 interviews over 14 days, **two on
  design and React**, the rest behavioral.
- **Coding screens vary by team**: reports mention **Karat** (third-party live coding,
  usually LeetCode-easy/medium), a **HackerRank** online test (one 2026 candidate called the
  time limit "extremely unrealistic"), and a 1-hour/2-question online assessment for an SDET
  role. Older Bellevue reports for game-dev roles were Unity/C# — not relevant here.
- **Behavioral** rounds focus on "who you are and how you'll work with the team";
  **conflict resolution** (disagreeing with a coworker/manager) comes up repeatedly.
- One candidate called their first interview "by far the most challenging first interview"
  they'd had — don't under-prepare the screen.

**Ask your recruiter:** which coding platform (Karat? HackerRank? live in an IDE?), which
language you may use (Go vs TS), whether there's a system design round, and whether a React
live build is included.

> **Final panel stage reached (Oct 2026):** start with `final_panel.md`. It covers the
> panel format, recruiter questions, DevOps/testing round prep, and your resume mapped
> to TPCi's values.

## Layout

```
challenges/            10 Go problems (the JD's primary backend language)
  NN_topic/
    README.md          prompt, rules, examples, talking points
    practice.go        stub for YOU (panics until implemented)   — build tag !solution
    solution.go        reference implementation                   — build tag solution
    *_test.go          tests (shared by both)
python/                the same 10 problems in Python (pytest), same layout as the
                       Microsoft prep: practice_*.py / solution_*.py / test_*.py
typescript/            3 TS problems, Node's built-in test runner (no npm install)
frontend/              React + TS live-build prompt, mock API, reference component
system_design/notes.md framework, Postgres vs DynamoDB, Lambda vs Fargate, CDK sketch,
                       5 Play!-Pokémon-flavored design prompts, prod troubleshooting
technical_questions.md one-minute answers for every tech in the JD
behavioral/notes.md    TPCi's six values → questions → your stories; fixed-term & "why Pokémon"
company/notes.md       TPCi, Play! Pokémon domain (TOM/PEM/RK9/CP/OWP), public AWS facts
```

## Challenge index

| # | Challenge | Pattern | Track |
|---|---|---|---|
| 01 | `swiss_pairings` | sort + backtracking | Domain (tournaments) |
| 02 | `standings_tiebreakers` | aggregation, OWP/OOWP, multi-key sort | Domain (tournaments) |
| 03 | `event_registration` | mutex, FIFO waitlist, concurrency (`-race`) | Domain (registration) |
| 04 | `login_throttle` | sliding window per key, injected clock | Domain (Trainer Club, from AWS case study) |
| 05 | `lru_cache` | map + doubly linked list, generics | Classic |
| 06 | `leaderboard_top_k` | map + min-heap | Domain (Championship Points) |
| 07 | `schedule_intervals` | merge / conflict / min rooms | Classic |
| 08 | `worker_pool` | goroutines, semaphore, context cancellation | Go idioms |
| 09 | `venue_shortest_path` | grid BFS | Classic |
| 10 | `longest_unique_substring` | sliding window, runes | Classic (Karat/HackerRank staple) |
| TS 01 | `retry_with_backoff` | async, exponential backoff | TypeScript |
| TS 02 | `event_search` | filter/sort/paginate, typed query | TypeScript (REST endpoint logic) |
| TS 03 | `debounce` | closures, timers, generics | TypeScript (React search box) |

**Which language?** Unconfirmed — ask the recruiter. Karat and HackerRank both allow Python,
so practice the screen in whichever language you're fastest in (`python/` mirrors all 10
problems; 08 becomes `08_bounded_concurrency` with asyncio). Keep the Go versions for
Go-specific discussion (goroutines, channels, `context`, errors-as-values).

Domain problems are your talking-point fuel ("I practiced Swiss pairing since that's what
your tools do"). Classics are what a Karat/HackerRank screen will most likely hand you —
if the screen is generic DSA, also run through the 16 classics in
`../microsoft-security-interview-prep/challenges/` (Python).

## Running

```bash
# Go (brew install go)
cd challenges
go test ./...                          # against YOUR practice.go files (fail until implemented)
go test ./03_event_registration/ -race # one challenge
go test -tags solution -race ./...     # against reference solutions (all pass)

# Python (same problems; 08 is asyncio instead of goroutines)
cd python
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/pytest                       # against practice_*.py
PRACTICE=0 .venv/bin/pytest            # against solution_*.py
.venv/bin/pytest challenges/03_event_registration -v

# TypeScript (Node 22.18+ runs .ts directly)
cd typescript
node --test                            # against practice.ts
PRACTICE=0 node --test                 # against solution.ts

# React live build
see frontend/README.md
```

Loop per challenge: read the README → set a 25-min timer → implement `practice.*` **while
talking out loud** → run tests → compare with the reference → rehearse the "Talking points."

## Suggested plan (adjust to your interview date)

| Day | Focus |
|---|---|
| 1 | `company/notes.md` homework list; draft 5 STAR+L stories against `behavioral/notes.md` |
| 2 | Go 01–04 (domain); `technical_questions.md` Go + REST sections |
| 3 | Go 05–10 (classics); TS 01–03 |
| 4 | React live build, timed; React/TS concepts out loud |
| 5 | System design prompts 1–2 on paper/whiteboard, 45 min each; Postgres/DynamoDB/CDK sections |
| 6 | System design 3–5; mock behavioral out loud; prepare your questions |
| Day before | Redo whichever two challenges felt shakiest; re-read stories; rest |

## Sources

- Glassdoor — TPCi [Software Engineer](https://www.glassdoor.com/Interview/The-Pok%C3%A9mon-Company-International-Software-Engineer-Interview-Questions-EI_IE447167.0,33_KO34,51.htm),
  [Senior SWE](https://www.glassdoor.com/Interview/The-Pok%C3%A9mon-Company-International-Senior-Software-Engineer-Interview-Questions-EI_IE447167.0,33_KO34,58.htm),
  [Software Developer](https://www.glassdoor.com/Interview/The-Pok%C3%A9mon-Company-International-Software-Developer-Interview-Questions-EI_IE447167.0,33_KO34,52.htm),
  [SDET](https://www.glassdoor.com/Interview/The-Pok%C3%A9mon-Company-International-Software-Engineer-In-Test-Interview-Questions-EI_IE447167.0,33_KO34,59.htm),
  [Bellevue](https://www.glassdoor.com/Interview/The-Pok%C3%A9mon-Company-International-Bellevue-Interview-Questions-EI_IE447167.0,33_IL.34,42_IC1150442.htm)
  (summarized via search snippets; pages are login-walled)
- Blind — [Upcoming coding interview for TPCi (Karat)](https://www.teamblind.com/post/Upcoming-Coding-Interview-for-Pokemon-Company-International-FMrMG8cO),
  [TPCi discussions](https://www.teamblind.com/company/Pokmon-Company-International/posts)
- AWS — [TPCi Aurora/DynamoDB/ElastiCache case study (PDF)](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/product-categories/databases/case-studies/gaming/the-pokemon-company-aurora-dynamodb-elasticache-performance-cost-optimization-case-study.html.pdf),
  [re:Invent 2019 GAM304 slides](https://d1.awsstatic.com/events/reinvent/2019/Migrating_the_live_Pok%C3%A9mon_database_to_Aurora_PostgreSQL_GAM304.pdf)
- TPCi London JDs (stack reference): [Frontend SDE](https://builtin.com/job/frontend-software-development-engineer/7925589),
  [Backend SDE](https://builtinlondon.uk/job/backend-software-development-engineer/7925587)
- Play! Pokémon — [Host events](https://www.pokemon.com/us/play-pokemon/organize/host-play-pokemon-events),
  [TOM FAQ](https://support.play.pokemon.com/hc/en-us/articles/27119497000724-Tournament-Operations-Manager-TOM-FAQ),
  [Tournament Rules Handbook (PDF)](https://www.pokemon.com/static-assets/content-assets/cms2/pdf/play-pokemon/rules/play-pokemon-tournament-rules-handbook-en.pdf),
  [Play! Tools guide](https://play-tools.pokemon.com/guide),
  [Pokémon Event Manager announcement](https://pocketmonsters.net/news/4458),
  [RK9](https://rk9.gg)
- [Palo Alto Networks — TPCi Cortex XSOAR case study](https://www.paloaltonetworks.com/customers/pokemon-company-international-xsoar)
