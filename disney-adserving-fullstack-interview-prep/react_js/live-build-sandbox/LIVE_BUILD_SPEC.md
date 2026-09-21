# Live-build spec: live ad-break / score ticker banner

Modeled on the reported real Disney exercise shape (a scoreboard/banner component to a
spec, ~1 hour) crossed with this repo's actual domain (ad breaks during live sports).
Read this once, then build against it from memory/notes — don't keep it open while
coding, same as a real interview.

## The ask

Build a `<LiveEventBanner />` component that shows the current state of a live sporting
event and, when an ad break starts, swaps to an ad-break countdown.

### Data shape (assume this comes from a hook you don't need to implement — mock it)

```ts
type EventState =
  | { phase: "live"; homeTeam: string; awayTeam: string; homeScore: number; awayScore: number; clock: string }
  | { phase: "ad-break"; secondsRemaining: number; nextEventLabel: string };

// Provided for you — DO implement a fake version that cycles through states on a
// timer, so you have something to visually verify against:
declare function useEventState(): EventState;
```

### Requirements

1. **Live phase**: show `"{homeTeam} {homeScore} — {awayScore} {awayTeam}"` and the
   game clock.
2. **Ad-break phase**: show a countdown ("Back in {secondsRemaining}s") that ticks down
   once per second, and the `nextEventLabel` (e.g., "Returning to 4th quarter").
3. **Transition**: when `phase` flips from `"live"` to `"ad-break"` (or back), the
   banner should visually distinguish the two states clearly (not just swap text) —
   your call on exact styling, but justify the choice out loud.
4. **Resilience**: what does the banner show if `useEventState()` hasn't returned data
   yet (loading), or if it's `undefined`/malformed? Don't let this crash the component.
5. **Bonus, if time allows**: the countdown shouldn't drift — verify your `setInterval`/
   timer approach stays accurate over a full countdown rather than losing time.

## Self-check after building

- Did you write a real (if simplified) implementation of `useEventState` so you could
  actually see both phases render, not just guess at the JSX?
- Did you handle the timer's cleanup (no leaked interval on unmount / on phase change)?
  This is the exact mechanism `../notes.md` Q2 and
  `../../../disney-frontend-interview-prep/challenges/01_debounce_throttle/` cover.
- Would this re-render efficiently if the parent re-rendered every second for an
  unrelated reason (e.g., a global clock elsewhere on the page)? Would `memo` help here,
  or is that premature — see `../notes.md` Q3.
- Compare against the worked walkthrough:
  `../../../disney-frontend-interview-prep/frontend_design/examples/01_live_score_ticker.md`
  (polling vs. WebSocket, graceful degradation on a dropped real-time channel) — this
  spec is a scoped-down, buildable version of that same design discussion.
