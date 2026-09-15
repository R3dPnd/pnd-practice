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

At Boeing, a customer had placed an order for access to a specific set of
schematics. A salesperson had entered the order incorrectly, and the access that
was actually provisioned didn't match what the customer had purchased — they were
either missing documents they were entitled to or seeing access that didn't belong
to their order.

### Task

I needed to correct the customer's access so it matched exactly what they had
ordered — no less than they'd paid for, and no extra/unnecessary document access
left over from the incorrect entry.

### Action

I wrote a SQL script to directly revert the bad order entry and re-grant access
based on the correct schematics the customer had actually purchased, then cleaned
up the leftover/unnecessary access records the mistaken order had created. I chose
to fix the underlying data directly rather than just patching the customer's
account from the front end, because a surface-level fix would have left stale
incorrect access records in the backend that could cause the same confusion again.

### Result

The customer received the correct schematic access without further delay, and the
incorrect access created by the original order was fully cleaned up rather than
lingering as a discrepancy.

### Learning

I now treat a "wrong access granted" ticket as a data-integrity issue, not just a
one-off account fix — because correcting only what the customer sees on their end
can leave incorrect grants behind that surface again later.
