# STAR+L template: collaboration / cross-team friction

Example prompt shape: "describe a time collaborating across teams didn't go well, and
your learnings" / "tell me about a time you had a conflict with someone — how did you
resolve it and what did you learn" / "tell me about a time you disagreed with a
teammate's technical decision."

Fill this in with a real story — don't fabricate one. Good candidates: a dependency
another team owned that blocked you, a disagreement over an API contract or shared
interface, competing priorities between your team and a partner team, a time you had
to push back on a decision (or someone pushed back on yours) and you had to actually
resolve it rather than escalate.

- **Situation**: _(1–2 sentences — which teams, what was the shared goal or shared
  dependency?)_
- **Task**: _(what did you specifically need from the other team, or they from you?)_
- **Action**: _(what actually went wrong first — miscommunication, misaligned
  priorities, a technical disagreement? Then: what did *you* specifically do to
  resolve it — a conversation you initiated, a compromise you proposed, a document
  you wrote to align on scope?)_
- **Result**: _(how did it actually get resolved — and be honest if the resolution
  was imperfect; a believable partial win beats a suspiciously clean one.)_
- **Learning**: _(the concrete change: e.g. "I now loop in the owning team before I
  design around their API, not after," or "I start cross-team asks with the
  constraint I'm under, not just the request, because that's what unblocked this.")_

## Common failure mode to avoid

Don't tell a story where the other team was simply wrong and you were simply right —
even if that's true, it reads as one-sided and doesn't show what *you* learned about
collaborating. The interviewer is listening for your role in either causing or
resolving the friction, not for a case you're relitigating.

## Answer

### Situation

While at Microsoft, the project I was working on was sunset. My manager split our team into two groups to support other projects within the org. I was placed on a team working on an application designed to reduce downtime during outages.

### Task

I needed the owning team to review and approve our PRs promptly so we could ship functionality and reduce the latency our users were experiencing. That wasn't happening — their team already had a full plate, and reviewing our PRs on top of it wasn't their priority, so approvals were taking over a week in some cases. Their concerns were legitimate, but we still had commitments to meet.

### Action

To build trust and reduce the friction, I started joining their standups, asking clarifying questions, and surfacing our blockers early so they knew who we were and what we needed from them. I also consolidated our questions into fewer, scheduled syncs instead of ad hoc pings, to make more efficient use of their time. Finally, I blocked off time on my own calendar each week specifically to review their PRs, so I was giving back time rather than only asking for theirs.

### Result

PR turnaround time dropped from over a week to [fill in: real number, e.g. "2-3 days"] within [fill in: timeframe], team morale improved, and we were able to ship [fill in: specific feature/functionality] and hit our latency and downtime targets.

### Learning

I learned to invest in a relationship with an owning team — understanding their priorities, showing up to their standups, giving back time — *before* asking for their bandwidth, not after friction has already built up. Now I build that relationship-building step into any new cross-team dependency from day one, instead of waiting for a bottleneck to force it.