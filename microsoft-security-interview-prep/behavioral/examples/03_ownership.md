# STAR+L template: ownership

Example prompt shape: "tell me about a time you took ownership of something that
wasn't officially your responsibility" / "describe a project you saw through end to
end with minimal oversight."

This theme is about whether you drove something to completion — including the
unglamorous parts — without being told to, and whether you took responsibility when
something under your remit broke.

Fill this in with a real story — don't fabricate one. Good candidates: a piece of
tech debt or a gap nobody assigned you that you fixed anyway, an incident you were
on-call for and drove to resolution, a project that lost its original owner and you
picked it up, a decision to do the less exciting but more correct thing (writing
tests, documenting a setup process, fixing a flaky pipeline) when nobody would have
noticed if you skipped it.

- **Situation**: _(1–2 sentences — what was the gap, risk, or incident?)_
- **Task**: _(was this explicitly your job, or did you take it on? Be honest either
  way — "nobody owned this and I decided it needed an owner" is a strong answer.)_
- **Action**: _(what did you specifically do, start to finish — including the parts
  that weren't interesting: the follow-through, the documentation, the handoff.)_
- **Result**: _(concrete outcome — ideally something measurable: an incident that
  stopped recurring, a process that got adopted by others, a system that's still
  running the way you left it.)_
- **Learning**: _(what you now do differently as a result — e.g. "I now write a
  short runbook the moment I fix an on-call issue, because the fix itself wasn't the
  hard part next time — rediscovering it was.")_

## Common failure mode to avoid

Don't describe ownership as "I did all the work myself" if the real story involves
delegating, asking for help, or looping in the right people at the right time —
ownership isn't solo heroics, it's making sure the outcome happened, which sometimes
means recognizing you needed someone else's expertise and going and getting it.

## Answer

### Situation

At JP Morgan Chase, we had a monolithic batch-job application with checkout,
payment, and account-management domain logic all tightly coupled together. It
technically worked, so nobody had prioritized decomposing it — but it was becoming
a growing drag on build times and a growing risk for every team that depended on it.

### Task

This wasn't formally assigned to me. I noticed the coupling was quietly getting
worse with every change, and decided the migration needed an owner before it became
a much bigger, riskier problem.

### Action

I led the migration into a modular SOA architecture — decomposing the tightly
coupled logic into independently deployable services with clear contracts. That
meant the interesting design work, but also the unglamorous parts: mapping every
existing consumer's dependency on the monolith, staging the cutover so nothing broke
in production, backfilling test coverage for the pieces I was extracting, and
documenting the new service contracts for the teams that would consume them.

### Result

Build time for downstream consumers dropped, test coverage improved, and the
service-contract pattern I established got reused by other teams doing similar
decompositions afterward — [fill in: real number if you have one, e.g. build time
reduction %, or number of teams that adopted the pattern].

### Learning

I learned that ownership often starts with noticing a problem nobody has explicitly
assigned and deciding to be its owner — including the unglamorous mapping and
documentation work, not just the architecture decisions. I now flag coupling like
this earlier, before it turns into a migration this large.
