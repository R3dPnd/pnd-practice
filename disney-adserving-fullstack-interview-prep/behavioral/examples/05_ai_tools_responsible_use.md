# STAR-ish template: responsible use of AI tools

Example prompt shape: "how do you use AI tools in your development workflow" / "tell me
about a time an AI tool's output was wrong and how you caught it" / "what's your policy
for what you will and won't hand to an AI tool."

JD language this maps to two separate lines: *"Use AI tools responsibly to improve
productivity while adhering to company policies"* (under "Daily, you should bring") and
*"Integrate AI-assisted development practices into daily workflows"* (under
"Responsibilities"). Two independent mentions in one JD is a real signal — prepare this
as its own answer, not an aside inside a different story. Notably, this is close to home:
you're likely using an AI coding assistant (this repo is proof) — the honest answer is
probably strong here if you can be specific rather than generic.

This is less classic-STAR and more "here's my working policy, illustrated with one
concrete example" — structure it that way:

- **Your policy, stated plainly**: _(what do you use AI tools for day-to-day —
  boilerplate, test scaffolding, exploring an unfamiliar API, first-draft code review
  comments — and what do you deliberately NOT hand to them — e.g., anything touching
  auth/credentials, proprietary business logic you can't paste into a third-party tool,
  or a final decision on an architecture tradeoff.)_
- **How you verify output before it ships**: _(be concrete: do you always run the tests
  it wrote, read every line of generated code before committing, treat its suggestions
  as a first draft you're accountable for rather than a final answer? "I always review
  and test AI-generated code the same as I would a junior engineer's PR" is a strong,
  specific answer.)_
- **One concrete example where an AI tool got something wrong**, and how you caught it:
  _(a hallucinated API, a subtly wrong edge case, an insecure pattern it suggested —
  having a real "and here's where it failed and I caught it" example is far more
  convincing than "I always double-check everything" as an abstract claim.)_
- **Where you draw a hard line**: _(company policy/data-handling boundary — not pasting
  proprietary code, customer data, or credentials into a tool that isn't sanctioned by
  the company; being upfront with your team about what's AI-assisted if it matters for
  review context.)_

## Common failure mode to avoid

Don't answer with either extreme: "I don't really use AI tools" (reads as behind, given
the JD explicitly wants this) or "I just trust whatever it outputs" (reads as exactly the
irresponsibility the JD is trying to screen for by using the word "responsibly" twice).
The strong answer is specific and calibrated: real tools you use, a real boundary you
hold, a real time it was wrong and you caught it.

## Answer

_(fill in)_
