# Behavioral — prep notes

Glassdoor reports for TPCi say behavioral rounds "focus on who you are and how well you'll
work with the team," with conflict-resolution questions (disagreeing with a coworker or
manager) coming up repeatedly. TPCi publishes six "How you'll be successful" values in the JD
— treat those as the rubric.

Use STAR+L (Situation, Task, Action, Result, **Learning**), same as
`../../microsoft-security-interview-prep/behavioral/notes.md`. Your existing stories there
(growth mindset, cross-team collaboration, ownership, customer impact, and the
dann-of-thursday technical deep dive) map onto the TPCi values below — reuse them.

## The six TPCi values → likely questions → which story

| Value (from the JD) | Likely question | Story to use |
|---|---|---|
| **Passion for Pokémon** | "Why Pokémon?" "What's your relationship with the brand?" "Which product of ours do you use?" | Be genuine and specific (see below). |
| **Challenging the Expected** | "Tell me about a time you tried something new that failed." "A creative solution to a hard problem?" | growth mindset story |
| **Integrity and Respect** | "Tell me about a disagreement with a coworker/manager." "A time you made a mistake and owned it." | collaboration / conflict story |
| **Dedicated to Quality** | "How do you approach code reviews?" "Time you raised the quality bar?" "Feedback you received and acted on?" | ownership story + code review philosophy |
| **Building Relationships** | "Working with product/design who disagreed with you?" "Helping a struggling teammate?" | cross-team story + a mentoring example |
| **Delighting Customers** | "A time you advocated for the user?" "Tradeoff between shipping fast and doing it right?" | customer impact story |

## JD-driven questions (prep an answer for each)

- **Lead a complex feature design → production.** Walk through scoping, design doc, tradeoffs,
  rollout, what broke. (Use the dann-of-thursday MCP deep dive or a work equivalent.)
- **Troubleshoot a production issue.** Detection → mitigation → root cause → sustainable fix →
  what you changed afterward. Have numbers (duration, users affected).
- **Mentoring.** JD explicitly wants "proven ability to mentor." One concrete example: who,
  what they were stuck on, what you did (pairing? review comments? a doc?), outcome.
- **Break down ambiguous business requirements.** Product asks for X; how you clarified,
  sliced into milestones, and pushed back on scope.
- **Evaluating a technical solution / architecture decision.** A time you compared options
  (e.g. Postgres vs DynamoDB, Lambda vs containers) — criteria, decision, what you'd revisit.
- **Process / tooling improvement.** Something you changed that made the team faster (CI,
  test infra, templates, scripts).
- **Learning a new technology quickly.** Especially relevant if Go or CDK is newer to you —
  have the honest version ready ("I've used X in Y; here's how I ramp").
- **Fast-paced priorities.** Two urgent things at once; how you chose and communicated.

## Role-specific questions to expect

- **"This is a 24-month fixed-term role — how do you feel about that?"** Have a calm,
  positive answer: the scope/impact interests you, you'd treat it like any role (ship,
  document, leave things better), and you're open to what comes after. Ask what's typically
  happened at the end of past fixed-term roles (conversions? extensions?) — in your questions,
  not defensively.
- **Hybrid in Bellevue** — confirm you're comfortable with the in-office cadence.
- **Comp** — posted new-hire range is $117,485–$156,318 (full range to $211,605). Know your
  number; let them name theirs first if possible.

## "Passion for Pokémon" — prepare honestly

This is a stated value, and interviewers will probe it. Don't fake it; be specific about
whatever your real connection is:
- What you played/collected/watched, and when. A favorite generation/Pokémon and *why*.
- Have you used their products recently? Before the interview, actually try:
  pokemon.com Event Locator, the Pokémon TCG Live app, a Play! Pokémon event page, rk9.gg
  registration flow, the Pokémon Trainer Club login. Note **one thing you'd improve** — it's
  a great answer to "what would you change?"
- Watch a bit of the most recent World Championships stream — know Worlds exists, there
  are TCG / VGC / Pokémon GO / Pokémon UNITE divisions, and Juniors/Seniors/Masters age divisions.
- Connect it to the role: "Organized play is how a 9-year-old and their parent end up at a
  local game store every Saturday — the software for that has to work for organizers who
  aren't technical and for kids."

## Your questions for them (pick 3–4)

1. Which products does this team own today — Play! Pokémon tools (event management, Event
   Locator, registration, Championship Points), or something else? What's the biggest
   technical challenge on the roadmap for the next 12 months?
2. Where is the team in moving to Go/CDK/serverless — greenfield, or migrating existing
   systems (e.g. Java services)?
3. What does on-call / production support look like around big events like Worlds?
4. How do engineers work with product and design — who writes the tech design docs?
5. What would success look like for this role at 6 months? At 24 months?
6. What has typically happened at the end of fixed-term engineering roles here?
7. How does the team handle the extra requirements of serving kids (COPPA/GDPR-K) in practice?

## Day-of reminders

- 4–5 stories, each mapped to ≥2 values. End every story with the **Learning**.
- First person ("I decided…"), numbers where you have them.
- For conflict stories: show you listened, disagreed with data, committed once decided, and
  kept the relationship intact. No villains.
