# STAR template: on-call / incident response

Example prompt shape: "tell me about a production incident you handled" / "walk me
through a time something broke in production" / "how do you approach being on-call."

JD language this maps to: *"Participate in On-Call rotations per team escalation
policy"* plus the general seniority expectation that a P3 owns incidents, not just
follows a runbook someone else wrote. For a system explicitly framed as
"high-throughput, low-latency" and revenue-adjacent (ad delivery), expect this
question directly, possibly early.

- **Situation**: _(what paged, what was the blast radius — was ad delivery actually
  degraded, or was it caught before customer impact?)_
- **Task**: _(what were you specifically responsible for in the response — incident
  commander, the person who found the root cause, the person who wrote the fix?)_
- **Action**: _(your triage sequence — what did you check first and why; how did you
  distinguish "mitigate now" from "fix root cause"; did you loop in other teams if the
  issue crossed a service boundary you don't own?)_
- **Result**: _(time to mitigate, time to full root-cause fix, and — the senior-level
  differentiator — what changed afterward: a new alert, a runbook, a circuit breaker
  added, a postmortem action item you personally drove to completion, not just filed.)_
- **Learning**: _(what you do differently now because of this incident specifically.)_

## A structural point worth stating explicitly if asked to go deeper

If you don't have a live-service incident story (e.g., your prior work wasn't on-call
for a production system), don't force one — pick the closest analog (a batch job that
silently corrupted data, a deploy that broke a downstream consumer) and be upfront: "I
haven't carried a pager before, but here's the closest thing, and here's how I'd apply
the same triage discipline to an on-call rotation." Honesty about a gap, paired with a
credible plan, reads better than a stretched analogy presented as equivalent.

## Common failure mode to avoid

Don't tell an incident story that's 90% "here's the outage" and 10% "here's what I did"
— the interviewer already knows outages happen; they're grading your *judgment* under
pressure (what you checked first, what you ruled out, who you looped in) and your
follow-through afterward (did the fix actually stick, or did it recur). Also avoid blame
language about other teams/people — see the "kindness and pragmatic optimism" tone note
in `../notes.md`.

## Answer

_(fill in)_
