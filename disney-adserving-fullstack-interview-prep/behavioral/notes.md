# Behavioral — prep notes (Ad Decisioning, P3)

Use the same **STAR(+Learning)** framework as `../../disney-frontend-interview-prep/behavioral/notes.md`
— Disney's own careers-site guidance (Situation, Task, Action, Result, told in
storytelling language) doesn't change by role. What changes here is the **theme list**:
this JD's "Daily, you should bring" and "Responsibilities" sections name very specific
behaviors, more specific than the general FE loop's themes. Treat each bolded phrase
below as something an interviewer might paraphrase back to you as a question.

## Themes, pulled directly from this JD's language

1. **Ownership of a domain area** — JD: *"Take ownership of one or more of the team's
   domain areas"* and *"an understanding of the importance of project ownership."* Not
   generic "tell me about a project" — they want evidence you can own a *slice* of a
   larger distributed system (one microservice, one pipeline) long-term, not just ship
   a feature once. → `examples/01_domain_ownership.md`
2. **On-call / incident response** — JD: *"Participate in On-Call rotations per team
   escalation policy."* For a system this JD frames as "high-throughput, low-latency"
   and directly responsible for revenue (ad delivery), expect a real incident story:
   what paged, how you triaged, what the actual fix vs. the actual root-cause fix was,
   and — critically for a *senior* role — what you changed afterward so it doesn't
   recur (monitoring, a runbook, an architectural fix). → `examples/02_oncall_incident.md`
3. **Cross-team / third-party integration** — JD: *"a willingness and desire to
   effectively communicate and collaborate across teams and systems"* plus explicit
   responsibilities around integrating with "entitlements," "pacing," "targeting," and
   "third-party systems." This is a distributed-systems-flavored version of teamwork:
   a story about negotiating a contract/API boundary with another team, or debugging
   an issue that spanned a service you don't own. → `examples/03_cross_team_collaboration.md`
4. **Mentoring, learning, and adapting** — JD: *"a passion for mentoring, learning, and
   adapting to a very dynamic and fast-paced environment."* Two angles worth having a
   story for: mentoring someone junior (code review, pairing, unblocking), and your own
   fast pivot (picking up an unfamiliar part of the stack — directly relevant since
   *you* are the one moving from React to Java here, so this can double as your
   "growth/ambiguity" story). → `examples/04_mentoring_growth.md`
5. **Responsible AI tool use** — JD: *"Use AI tools responsibly to improve productivity
   while adhering to company policies"* and, separately, *"Integrate AI-assisted
   development practices into daily workflows."* Two distinct mentions in one JD is
   unusual — treat this as a real signal, not boilerplate. Have a concrete, specific
   story: a tool you use, what you verify before trusting its output (tests, review,
   not blindly merging), and where you draw the line (e.g., not pasting proprietary
   code/credentials into a third-party tool). → `examples/05_ai_tools_responsible_use.md`

## A tone note specific to this JD

The JD's own phrase is *"kindness and pragmatic optimism."* That's an unusually soft,
specific value statement for an ad-tech/infra JD to include — worth mirroring in how you
*tell* your stories, not just what they're about: frame incidents and disagreements in
terms of "here's what we fixed together," not "here's who was wrong." A senior candidate
who narrates a past outage entirely in blame language is a bigger red flag here than at a
company that didn't bother naming this value explicitly.

## Reuse from the sibling repo

`../../disney-frontend-interview-prep/behavioral/notes.md` already has:
- The full STAR(+L) breakdown and why to add the Learning beat
- General Disney themes (storytelling/ownership, collaboration, guest/customer impact,
  growth/ambiguity) that still apply — theme 1 there overlaps with theme 1 here; theme 4
  there overlaps with theme 4 here. Don't write two separate stories for the same
  underlying theme; one strong story usually covers both framings.
- Day-of delivery reminders (lead with Situation, say "I" not "we," don't over-rehearse)
  — identical advice applies here, not repeated.

## Examples

1. [Domain ownership](examples/01_domain_ownership.md)
2. [On-call / incident response](examples/02_oncall_incident.md)
3. [Cross-team / third-party integration](examples/03_cross_team_collaboration.md)
4. [Mentoring / fast learning](examples/04_mentoring_growth.md)
5. [Responsible AI tool use](examples/05_ai_tools_responsible_use.md)
