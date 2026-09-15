# Worked example: live score ticker / real-time scoreboard widget

Practice prompt 1 from `../notes.md`. This is the design-discussion version of the
same shape as the reported real live-coding exercise (build a scoreboard component
against an API in ~1 hour) — see repo `README.md`'s Field notes.

- **Clarify**: How "live" does live need to be (sub-second for an in-progress play, or
  is a 10–15s lag acceptable)? One scoreboard on a page, or many (a full slate of
  games)? Any device constraints (this needs to work on a smart-TV browser too, not
  just desktop Chrome)?
- **Contract**: The component takes a `gameId` (or list of IDs) and renders scores +
  game state (`scheduled`/`live`/`final`). It doesn't know or care *how* data arrives —
  that's a hook's job (`useLiveScore(gameId)`), keeping the component itself dumb and
  testable.
- **Architecture**: Client subscribes via WebSocket (or SSE) to a per-game or per-slate
  channel for near-real-time updates; falls back to short-interval polling (e.g. every
  10s) if the real-time channel is unavailable or the browser doesn't support it. A
  small reducer/state machine per game tracks `connecting → live → stale → reconnecting`
  so the UI can show a "reconnecting…" indicator instead of silently freezing on stale
  data.
- **Deep dive** (likely steered here): reconnection strategy. On a dropped WebSocket:
  exponential backoff with jitter for reconnect attempts, and while disconnected, fall
  back to polling so the score doesn't just go stale and silent — the user should never
  see a "final" score that's actually 3 plays behind reality without some visual signal
  that it might be stale.
- **FE review pass**:
  - *Performance*: for a full-slate page (dozens of live games), batch updates into one
    WebSocket message/topic rather than one connection per game — one connection
    fanning out to many component subscribers via a shared context/store.
  - *Accessibility*: score changes should be announced via an `aria-live="polite"`
    region, not just a silent DOM update — a screen-reader user following a game needs
    the same "it just changed" signal a sighted user gets from a flash/animation.
  - *Resilience*: explicit `stale`/`reconnecting` visual state, never a UI that looks
    fully live while quietly not receiving updates.
  - *Security*: score/game data from the API — validate shape, don't trust the socket
    payload blindly if there's any team-name/text field going into the DOM.
- **Tradeoffs**: WebSocket gives lower latency but adds real infrastructure complexity
  (fan-out, connection scaling); polling is simpler and more robust across flaky
  networks/proxies but has a latency floor set by the poll interval. For a smart-TV
  target specifically, I'd lean more heavily on the polling fallback being solid, since
  TV browsers are the least predictable WebSocket environment.
- **What I'd do differently with more time**: server-sent events (SSE) instead of raw
  WebSockets for this specific use case — it's one-directional (server → client only,
  which is all a scoreboard needs), and gets you automatic reconnection semantics from
  the browser's `EventSource` API for free, instead of hand-rolling reconnect/backoff.
