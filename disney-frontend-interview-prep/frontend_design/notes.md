# Front-End System Design — prep notes

No confirmed system-design round for this loop specifically (see `../README.md`'s
Field notes — Disney's process isn't standardized), but senior FE loops generally
include *some* architecture-level discussion, even if it's folded into a coding round
rather than a dedicated whiteboard session. This is a framework + practice prompts,
not code — pair it with the live-build practice described in the repo `README.md`.

## Framework (use this shape every time, out loud, in this order)

1. **Clarify requirements before drawing anything.**
   - Functional: what does a user actually do here, end to end? Who is the user —
     a consumer (Disney+/Hulu/ESPN+ viewer) or an internal user (an editor/ops person,
     as in `../espn-conent-dashboard/`)?
   - Non-functional: expected scale (rows in a table, concurrent viewers, update
     frequency), latency/perceived-performance budget, device targets (mobile web?
     smart TV? just desktop?), offline/flaky-network tolerance.
2. **Define the component boundary and data contract** before internals: what props/
   API shape does this component or feature consume, what does it emit (events,
   callbacks), and where does its data come from (REST, GraphQL — see
   `../espn-conent-dashboard/README.md` Module 4 for the real DEEP&T-flavored version
   of this question).
3. **High-level architecture** — component tree + data flow: where does state live
   (local component state vs. a shared store vs. server-cache library like TanStack
   Query/Apollo Client), how does data get from the network to the DOM, what's
   client-rendered vs. server-rendered/streamed if relevant. Narrate one user
   interaction end to end (e.g., "user types in the search box → ...").
4. **Deep dive on 1–2 components** the interviewer steers you toward — same advice as
   any system design round: don't rush past the high-level picture, but don't get
   stuck drawing boxes forever either.
5. **FE review pass** (do this explicitly, even if not asked — see checklist below).
6. **Tradeoffs and scaling** — what breaks first as data/traffic grows (a 200-row table
   vs. a 200,000-row table needs virtualization; a single WebSocket vs. thousands of
   concurrent viewers needs a fan-out layer), and what you'd cut first under a tighter
   timeline.
7. **What you'd do differently with more time** — call out the corners you're
   knowingly cutting, don't cut them silently.

## FE review pass (the "security pass" equivalent for a front-end round)

| Concern | Ask yourself |
|---|---|
| **Performance** | What's the bundle-size/render cost of this? Does a big list need virtualization? Is anything doing unnecessary re-renders (missing `memo`/`useCallback`, an unstable object literal in a dependency array)? |
| **Accessibility** | Can this be operated with a keyboard alone? Does it announce state changes to a screen reader (`aria-live`, focus management on route change)? Sufficient color contrast for status indicators? |
| **Resilience** | What does this look like loading, empty, and errored — not just the happy path? What happens on a flaky/offline network — does a failed mutation roll back cleanly (see `../espn-conent-dashboard/README.md` Module 3's optimistic-update-with-rollback pattern)? |
| **State & data flow** | Where does the source of truth live? How does the cache get invalidated when the underlying data changes (a webhook, a poll, a manual refetch)? Is any state duplicated in two places that can drift out of sync? |
| **Security** | Any user- or CMS-authored content rendered as HTML? Never `dangerouslySetInnerHTML` on unsanitized input — see `../espn-conent-dashboard/README.md`'s `RichTextRenderer` for a real whitelist-based approach to this exact problem with Contentful rich text. |
| **Testability** | Could you unit-test this component's logic without a full browser? Is business logic separated from rendering enough to test it in isolation? |

## Practice prompts (pick one per mock session)

1. **Design a live score ticker / real-time scoreboard widget** — *(this is very close
   to the actual reported real live-coding exercise — see repo `README.md` — practice
   it as a design discussion AND as a timed build).* Cover: polling vs. WebSocket vs.
   Server-Sent Events for "score just changed" updates, what the UI shows while
   waiting/reconnecting, and graceful degradation if the real-time channel drops
   (fall back to polling).
2. **Design the front-end of an internal content-operations dashboard** (search,
   filter, and publish/unpublish a large list of content items) — this is literally
   `../espn-conent-dashboard/`'s UI; use this prompt to practice explaining decisions
   already made there (TanStack Query for server cache, URL as the source of truth for
   filters, `memo`+`useCallback` on table rows) as if you were designing it live.
3. **Design a shared component library/design system** used across multiple web
   properties (Disney+, Hulu, ESPN web). Cover: theming (multiple brands from one
   component set), accessibility as a contract every component must satisfy, versioning
   and how you roll out a breaking change across many consuming teams without breaking
   them all at once.
4. **Design a video player experience** for a streaming product. Cover: you almost
   never hand-roll adaptive bitrate playback — lean on a library (hls.js/shaka-player)
   or native `<video>` — but you do own the surrounding UI: buffering/loading states,
   captions/accessibility, resuming playback position, and instrumentation (QoS/
   analytics events: rebuffer count, time-to-first-frame).
5. **Design client-side caching/state for a data-heavy dashboard.** Cover: cache-key
   design, invalidation strategy (see `09_memoize` in `../challenges/` for the
   mechanism at small scale), optimistic updates with rollback on failure, and
   stale-while-revalidate for perceived performance.

## Worked walkthroughs

Compressed run-throughs of the framework above — this is what "narrate it out loud"
should sound like, not a diagram substitute. Use these to check your own mock reps
against, not to memorize verbatim.

1. [Live score ticker](examples/01_live_score_ticker.md)
2. [Content operations dashboard](examples/02_content_ops_dashboard.md)
3. [Shared design system / component library](examples/03_design_system_component_library.md)
4. [Video player experience](examples/04_video_player.md)

## Day-of reminders

- Ask who the user is and what device/network conditions matter *before* you start
  talking architecture — a smart-TV app and a desktop dashboard have almost nothing in
  common architecturally.
- State assumptions out loud ("I'm assuming this list can grow past a few thousand rows,
  so I'd virtualize it — let me know if that's wrong").
- Do the FE review pass even if not explicitly asked — accessibility and resilience
  (loading/error/empty states) are the two most commonly *skipped* in a rushed answer,
  and skipping them is a bigger signal than not knowing an exotic detail.
- If you don't know a specific library's internals, reason from first principles about
  what problem it solves rather than guessing confidently.
