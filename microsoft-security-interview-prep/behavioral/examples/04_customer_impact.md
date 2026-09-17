# STAR+L template: customer impact

Example prompt shape: "tell me about a time you went above and beyond for a customer
or user" / "describe a time you made a tradeoff between what was easier to build and
what was better for the user" / "how have you incorporated customer feedback into
your work?"

This theme checks whether your work connects to an actual user/customer outcome, not
just an internal technical win — even in a Security org, where "customer" is often
another internal team, an end user's data safety, or a compliance/trust outcome
rather than a literal paying customer.

Fill this in with a real story — don't fabricate one. Good candidates: a change you
made because of user-reported pain (a bug, a confusing flow, a performance issue), a
security or reliability fix that protected users even though they never saw it, a
tradeoff you made in favor of the user experience over what was technically simpler
for you, a time you talked to (or read feedback from) actual users before building
something.

- **Situation**: _(1–2 sentences — who was affected, and how did you find out?)_
- **Task**: _(what was the user-facing problem you were specifically trying to solve
  — described in terms of impact on them, not just the technical symptom?)_
- **Action**: _(what did you actually build/change/fix — and where did you make a
  choice that favored the user's experience over what was easiest for you to ship?)_
- **Result**: _(the outcome from the user's side — fewer complaints, faster flow,
  data that stayed safe, trust preserved — plus any number you have.)_
- **Learning**: _(what you now do differently — e.g. "I now try to reproduce a
  reported issue exactly as the user experienced it before touching code, because
  this taught me the symptom I assumed wasn't actually what they were hitting.")_

## Common failure mode to avoid

Don't substitute "shipped a feature on time" for customer impact — the interviewer is
listening for evidence you understood the *user's* problem, not just that you
executed. If your best material is internal/infra work, frame it through who it
protected or unblocked downstream, even if that's other engineers rather than
external customers — that's a legitimate customer-impact story in a Security context.

## Answer

### Situation

At Microsoft, my team was integrating Copilot into the intake form release managers
use to submit releases. The PM raised concerns about the proposed changes — large
edits to the form, including moving questions around, that risked confusing release
managers who already knew the existing flow by heart.

### Task

I needed to design the Copilot integration in a way that actually addressed the
PM's concern: any change to the form had to earn its place by clearly benefiting
release managers, weighed against the real cost of disrupting a flow they already
relied on — not just add the feature and hope the disruption was acceptable.

### Action

I worked extra hours to turn this around quickly and built a functional mockup that
made the Copilot call asynchronous instead of blocking the release manager's flow.
Rather than reordering or inserting new required questions into the existing form,
I designed it so Copilot's involvement would either actively accelerate the release
manager's work or simply stay out of the way — it was never allowed to add friction,
waiting, or confusion to the path they already knew.

### Result

The PM was grateful for the approach and it was adopted as the direction for the
integration — the async, non-blocking design became the pattern we shipped, instead
of the more disruptive version originally proposed.

### Learning

I now weigh any change to an existing user flow against the disruption it causes to
users who already know that flow, not just the benefit the change is meant to add —
because a feature that's valuable in isolation can still be a net loss if it
confuses or slows down people who relied on the flow staying familiar.
