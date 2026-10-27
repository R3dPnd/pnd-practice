# Microsoft Partner Center (Scale & Partner AI Experiences) — Interview Prep

Software Engineer / Sr. SWE (IC3/IC4) on the team that builds the platform services
behind **Partner Center, CSP, partner onboarding, program enrollment, identity,
authorization and security**. Python coding, ~3 days of prep, starting Mon 2026-10-26.

**The focus this time is coding**, since that was the weak spot in the Security loop.
This folder has only new material. The 23 classics in `../microsoft-security-interview-prep/`
stay where they are and are part of the plan below.

## Layout

```
challenges/                  4 new problems, same practice/solution/test layout as before
  01_nearest_person_distance   your real Security-loop question, done right (multi-source BFS)
  02_delegated_access_resolver role inheritance DFS + tenant tree walk (GDAP-style authZ)
  03_enrollment_workflow       state machine + idempotency keys (onboarding API)
  04_duplicate_partner_merge   union-find (Accounts Merge, framed as duplicate enrollments)
conftest.py                  same FakeClock fixture (used by 02)
system_design/notes.md       Partner Center domain primer + 3 practice prompts with outlines
behavioral/notes.md          what's different from last time: "why this team", AI-tools story
```

Practice/solution toggle works exactly like before: `pytest` runs your `practice_*.py`,
`PRACTICE=0 pytest` runs the reference. The Security folder's venv already has pytest:

```bash
cd microsoft-partner-center-interview-prep
../microsoft-security-interview-prep/.venv/bin/pytest challenges/01_nearest_person_distance -v
PRACTICE=0 ../microsoft-security-interview-prep/.venv/bin/pytest   # 55 tests, all pass
```

## The coding routine (this is the actual fix)

The `q1.py` bugs weren't about knowing the algorithm. It was written top to bottom and
never traced by hand. Every rep below follows these steps, out loud, on a timer:

1. **Restate + clarify (2 min).** Inputs, outputs, edge cases. Ask what happens for an
   empty input, a non-square grid, an unreachable cell. Write down the agreed output format.
2. **Brute force out loud (1 min).** State it and its complexity. Don't code it.
3. **Pattern + complexity (2 min).** "Nearest-to-any-source on an unweighted grid →
   multi-source BFS, O(R·C)." Get a nod before typing.
4. **Code (15–20 min).** Use clear names, small helpers, and no clever one-liners
   until the code works.
5. **Trace a tiny case by hand (3 min).** Pick a *non-square* 2×3 example and walk it
   line by line. This is the step that catches aliased rows, swapped dimensions, and
   an off-by-one in the expand condition. Don't skip it.
6. **Follow-ups (2 min).** Answer "100x bigger?", "less memory?", "how would you test
   this?" before they ask.

Then run pytest. If a test fails that your trace didn't catch, write down *which kind*
of bug it was. That list is what you review on the last day.

## 3-day plan

| Day | Coding (timed, using the routine) | Design / behavioral |
|---|---|---|
| **Mon 10/26** | `01_nearest_person_distance` (30 min, *don't* open the spoiler first). Then, from the Security folder: `02_lru_cache`, `13_linked_list_basics` (30 min each). These are classics you never did. | Read `system_design/notes.md` domain primer (20 min) |
| **Tue 10/27** | `02_delegated_access_resolver` (40 min), `04_duplicate_partner_merge` (30 min). From Security: `16_word_break`, `22_interval_list_intersections` (25 min each). | Practice prompt 1 (enrollment service), 45 min, out loud |
| **Wed 10/28** | `03_enrollment_workflow` (35 min). **Mock:** pick 2 already-done Security classics at random (`10`, `11`, `12`, `14`, `15`, `17`, `18`, `23`), blank file, 25 min each. | Practice prompt 2 (authorization service). Draft "why this team" + AI-tools story (`behavioral/notes.md`). |
| **Interview day** | 15 min warm-up: rewrite `01` from memory. Review your bug-type list. | Re-read STAR bullets. Join Teams 5–10 min early. |

If the interview is sooner than Thursday, drop the Security-folder extras first. Keep
`01`, `02`, `03`, and at least one mock.

### Checklist

- [ ] Mon: `01_nearest_person_distance`
- [ ] Mon: Security `02_lru_cache`
- [ ] Mon: Security `13_linked_list_basics`
- [ ] Mon: domain primer
- [ ] Tue: `02_delegated_access_resolver`
- [ ] Tue: `04_duplicate_partner_merge`
- [ ] Tue: Security `16_word_break`
- [ ] Tue: Security `22_interval_list_intersections`
- [ ] Tue: design prompt 1
- [ ] Wed: `03_enrollment_workflow`
- [ ] Wed: 2-problem mock, blank file, 50 min
- [ ] Wed: design prompt 2
- [ ] Wed: "why this team" + AI-tools story written down
- [ ] Interview day: rewrite `01` from memory, review bug-type list

## Why these four problems

The coding round will most likely be a generic LeetCode-style problem (arrays, hash
maps, grid/graph BFS, trees, intervals), the same as last time. The four new problems
use those same patterns but are framed in this team's domain. That way each rep is
also practice for the "tell me about authZ / onboarding" talking points:

| Problem | Underlying classic | Domain talking point |
|---|---|---|
| 01 | Walls and Gates / 01 Matrix | — (the one that already went wrong) |
| 02 | Course Schedule (cycle DFS) + tree parent walk | GDAP, RBAC, least privilege, fail-closed, revocation latency |
| 03 | Hash-map state machine | idempotency keys, retries, optimistic concurrency, audit log |
| 04 | Accounts Merge (union-find) | onboarding fraud, duplicate enrollments, false-positive cost |

## Bug-type log (fill this in as you go)

| Problem | Bug | Would the hand trace have caught it? |
|---|---|---|
| Security q1 | `[[x]*n]*m` row aliasing | yes, 2×3 grid |
| Security q1 | rows/cols swapped | yes, 2×3 grid |
| Security q1 | expand condition never true from source | yes, any grid |
| | | |
