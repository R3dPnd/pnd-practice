# Worked example: video player experience

Practice prompt 4 from `../notes.md` — directly relevant given DEEP&T owns Disney+/
Hulu/ESPN+ playback.

- **Clarify**: Live (a game) or VOD (a show/movie)? Web only, or does the design need
  to translate to smart-TV/mobile-app contexts too? Does this need DRM-protected
  premium content, or is that out of scope for this discussion?
- **Contract**: The player component takes a manifest URL + metadata (title, resume
  position) and emits playback events (`onProgress`, `onBuffering`, `onError`,
  `onQualityChange`) — the surrounding app (recommendations, "next episode" UI) reacts
  to those events; the player itself doesn't know about the rest of the page.
- **Architecture**: Don't hand-roll adaptive bitrate streaming — wrap a proven library
  (hls.js for HLS, shaka-player for DASH, or the browser's native `<video>` HLS support
  on Safari) behind your own component boundary, so the app-facing API stays stable even
  if the underlying playback library is swapped later. Own the chrome around it: play/
  pause/seek controls, captions rendering, buffering spinner, error/retry UI.
- **Deep dive** (likely steered here): buffering and rebuffer-avoidance UX. Show a
  distinct "buffering" state (not just a frozen frame) as soon as the buffer runs low,
  and pre-fetch enough buffer during less-critical moments to avoid a visible stall
  during, e.g., a live sports play. Track and report a rebuffer-count and
  time-to-first-frame metric — these are the actual product-quality metrics a streaming
  team lives or dies by, more than any single UI polish detail.
- **FE review pass**:
  - *Accessibility*: captions/subtitles aren't optional — full keyboard control of all
    playback controls, and captions must render even when a screen reader is active
    without competing with the reader's own audio output.
  - *Resilience*: explicit handling for a manifest fetch failure, a mid-playback
    network drop (retry with backoff before surfacing a hard error), and DRM/license
    failures with a clear, non-cryptic message to the user.
  - *Performance*: lazy-load the player library itself — a video player's JS payload is
    large; don't ship it on pages that don't play video.
  - *Security*: DRM/license-key handling stays server-mediated — the client never holds
    long-lived credentials or a way to bypass content protection; treat this the way
    you'd treat any other secret-handling boundary.
- **Tradeoffs**: wrapping an existing playback library costs you some flexibility
  (you're bound by its API/bugs) but building bitrate-adaptive streaming from scratch
  is a multi-quarter effort with a huge surface area for subtle bugs — not a reasonable
  build-vs-buy call for almost any team.
- **What I'd do differently with more time**: instrument client-side QoS (rebuffer
  ratio, startup time, error rate) per device/network-type from day one, not added
  later — for a streaming product this data usually ends up being the thing leadership
  actually asks about first.
