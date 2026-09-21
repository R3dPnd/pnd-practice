# Live-build sandbox

A real Vite + React + TypeScript dev environment (not a mock) for the timed
"build this component to a spec" exercise described in
`../../../disney-frontend-interview-prep/README.md`'s "The live-coding wildcard"
section — one 2025 Disney candidate reported the *entire* technical round being exactly
this shape (build a scoreboard/banner component to a spec in ~1 hour, Google allowed, AI
tools not allowed).

## Setup (already done once, for reference)

```bash
npm create vite@latest . -- --template react-ts
npm install
```

## Run

```bash
npm run dev      # starts a real dev server with HMR, default http://localhost:5173
npm run build    # type-checks (tsc -b) + production build — good final check after a timed build
```

## How to practice with this

1. Open `LIVE_BUILD_SPEC.md` — a spec in the same shape as the reported real exercise
   (a live score ticker, matching `../../system_design/examples/` and
   `../../../disney-frontend-interview-prep/frontend_design/examples/01_live_score_ticker.md`).
2. Set a real timer (45–60 min).
3. **No AI assistance** — this is the one reported explicit constraint from the actual
   candidate account. Google is fine.
4. Build directly in `src/App.tsx` (or break it into components under `src/`, your
   call — that's part of what's being evaluated).
5. When time's up (or you finish early), run `npm run build` as a final sanity check,
   then diff your approach against the worked walkthrough in
   `../../../disney-frontend-interview-prep/frontend_design/examples/01_live_score_ticker.md`
   and narrate out loud what you'd do differently — same rehearsal habit the rest of
   this prep repo recommends.
6. Reset for another rep: `git checkout -- src/App.tsx` (from the repo root) or just
   overwrite it — this sandbox is meant to be built-and-reset repeatedly, not preserved.

## Why a real dev server instead of just reading code

The actual reported exercise is scored partly on "can you turn a spec into working code
under time pressure" — that's a different skill from reading a finished example, and it
only transfers if you rehearse it under the same conditions (a blank file, a running
browser, a clock).
