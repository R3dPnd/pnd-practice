# Behavioral — what's different for this loop

The structure (STAR+L) and the four themes (growth mindset, collaboration, ownership,
customer impact) are the same as last time. Reuse
`../../microsoft-security-interview-prep/behavioral/notes.md` and its `examples/`
directly. This file adds only what this team specifically asks for.

## 1. "Why this team?" — have a 45-second answer written down

Cover three things. Use your own words, but keep them specific:

- **The problem**: Partner Center's identity and authZ sits in front of a huge
  ecosystem. A bug in one shared service affects every partner and every one of
  their customers. That combination of scale and security is what you want to work on.
- **The link to your experience**: the Security-org prep and whatever authN/authZ,
  API, or distributed-systems work is on your resume. Name one concrete thing.
- **The AI-first angle**: the JD says the team wants AI-enabled partner experiences
  and AI tools in engineering workflows. You already work that way (next section).

Since you interviewed with Microsoft Security recently, expect "what happened with
the other team?" Answer briefly and positively, then move on: "It was a great loop.
I learned a lot about how Microsoft interviews, and this team's mix of platform,
identity, and AI is an even closer fit."

## 2. AI-tools story (the JD asks for this explicitly)

> "Experience leveraging AI tools to improve engineering productivity" and "agent-based
> solutions within engineering workflows."

Prepare one STAR+L story about using AI tooling in real engineering work. The
dann-of-thursday MCP integration work from the Security prep
(`examples/05_technical_deep_dive_worked_example.md`) is a natural fit, because it
*is* agent tooling. What makes it land with this team:

- **A specific productivity result**, not "it made me faster." Say what got
  automated, how much time it saved, or what quality issue it caught.
- **How you checked the AI's output.** This team builds security-critical services.
  They want to hear that you review generated code, have tests gate it, and don't
  hand authZ logic to an LLM without checking it.
- **The Learning beat**: where it *didn't* help, and what you changed.

The last panel said no AI tools *during* the interview. Assume the same here unless
the recruiter says otherwise.

## 3. Likely technical-behavioral prompts for this team

- "Tell me about a time you made a system more reliable or observable." (Matches the
  JD's availability, latency, resiliency, and observability line.)
- "Describe a security tradeoff you made, such as convenience vs safety." Prompt 3 in
  `system_design/notes.md` (MFA rollout) is the shape of a good answer.
- "Tell me about a change that could have broken other teams' consumers. How did you
  roll it out?" (Shared platform services have many consumers.)
- "A time you debugged a production issue end to end."

## 4. Questions to ask them (pick 2–3)

- What's the split between shared platform services (identity, authZ, enrollment) and
  product surfaces on this team? Which would I start on?
- How are the "AI-enabled partner experiences" being built? Agents calling Partner
  Center APIs on a partner's behalf, or internal tooling first? How does authZ work
  when an agent is the caller?
- What does on-call look like, and what was the last incident that changed how the
  team builds things?
- How do you roll out a breaking security requirement, like MFA enforcement, across
  partners who automate against your APIs?
