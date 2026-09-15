# STAR+L template: growth mindset

Reported real prompt shape: "tell me about a time you failed / something didn't go
as planned — what did you learn?" Microsoft's culture is explicitly built around
Carol Dweck's "growth mindset" framing, so the bar here is specifically **what you
changed afterward**, not just that you can admit a mistake.

Fill this in with a real story — don't fabricate one. Good candidates: a design you
had to redo, a bug you shipped that you later fixed the *process* around (not just
the code), a technology bet that didn't pay off, a code review comment that changed
how you approach a whole class of problem.

- **Situation**: _(1–2 sentences — what was the project/context?)_
- **Task**: _(what were you specifically responsible for?)_
- **Action**: _(what did you actually do — and where, specifically, did it go wrong?
  Own the mistake plainly; don't hedge or blame the team.)_
- **Result**: _(what was the actual outcome — the fallout, and how it got resolved?)_
- **Learning**: _(the single concrete thing you do differently now because of this.
  Not "I communicate more" — something specific: "I now write a one-paragraph design
  doc before touching shared infrastructure, because this bug came from an assumption
  a 10-minute doc would have surfaced.")_

## Common failure mode to avoid

Don't pick a story where the "failure" was actually someone else's fault and your
role was minor — that reads as deflection, not growth mindset. Pick something where
your own decision was the direct cause, even if the story is less flattering. The
Learning beat is what makes it a strength, not the absence of a real mistake.

## Answer

### Situation

At Axon, I was building the asynchronous data integration pipeline that ingests
records from hundreds of diverse legacy agency data sources into our
PostgreSQL-backed services.

### Task

I was responsible for writing the ingestion and normalization logic across a large,
growing number of agency schemas — each one slightly different from the last.

### Action

Early on, I assumed new agencies' data would roughly match the shape of the first
few reference sources I'd built against, so I didn't put strict validation at the
ingestion boundary before writing to the database. When we onboarded [fill in: a
specific new agency], its data included [fill in: malformed/mistyped/unexpected
fields], and my ingestion job wrote a batch of corrupted or partially-normalized
records into several tables before anyone caught it.

### Result

We caught the discrepancy [fill in: how — a downstream consumer noticed bad data /
a monitoring alert] about [fill in: timeframe] later, had to write backfill/cleanup
scripts to fix the affected records, and it delayed that agency's onboarding by
[fill in: X days/weeks].

### Learning

I learned to treat every new external data source as untrusted until proven
otherwise, rather than assuming it matches prior sources. Now I write schema
validation and defensive checks at the ingestion boundary *before* writing anything
downstream — malformed-input handling is a first-class part of how I design
ingestion pipelines now, not something I add after the first incident.
