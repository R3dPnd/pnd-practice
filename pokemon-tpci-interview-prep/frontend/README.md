# Frontend — React + TypeScript live build

One Glassdoor report for a TPCi SWE loop mentions **"2 interviews on design and React."**
Expect either a live build ("render this list from an API, add filter/search/loading states")
or a React concepts discussion. Practice the prompt below in a fresh Vite app, timed (45 min).

```bash
npm create vite@latest event-finder -- --template react-ts
cd event-finder && npm install
cp ../reference/mockApi.ts src/    # gives you the fake API; write EventFinder.tsx yourself
npm run dev
```

## Prompt: "Find an Event" page

`fetchEvents({ region, text, signal })` (in `reference/mockApi.ts`) returns
`Promise<PlayEvent[]>` after a random 200–800ms delay and fails ~15% of the time.

Build `<EventFinder />`:

1. Region `<select>` (All / NA / EU / LATAM / OCE) and a text search box.
2. Text search is **debounced** (300ms). Changing region refetches immediately.
3. Show **loading**, **error with a Retry button**, **empty** ("No events found"), and the list.
4. **No stale results**: if request A is slower than request B, A's response must not overwrite
   B's. (Use `AbortController` in the effect cleanup.)
5. Each row: name, city, date (formatted), and a type badge. Clicking a row toggles a
   "★ Saved" state (kept in memory, survives refetches — key by `id`).
6. Accessible: labelled inputs, list semantics, the saved toggle is a `<button aria-pressed>`.

Stretch: persist saved IDs to `localStorage`; extract a `useDebouncedValue` hook and a
`useEvents` hook; virtualize the list if there are 5,000 events.

Reference solution: `reference/EventFinder.tsx` — don't open it until you've tried.

## React/TS concepts to be able to explain out loud
- Why the effect cleanup + `AbortController` fixes the race (and why `ignore` flags also work).
- `useEffect` dependency arrays; why objects/functions in deps cause refetch loops.
- `useMemo` / `useCallback` — when they actually help vs. noise. React 19 compiler.
- Controlled vs uncontrolled inputs. Lifting state up vs. context vs. a store.
- Keys in lists — why not array index.
- Server state vs client state — TanStack Query (caching, dedupe, retries) vs hand-rolled.
- Next.js: SSR/SSG/ISR — pokemon.com and Pokémon Center are SEO-heavy public sites.
- Testing: React Testing Library (query by role), Jest/Vitest, Playwright E2E
  (TPCi's London frontend JD lists Jest + Playwright).
- TS: discriminated unions for request state:
  `type State = {status:"idle"} | {status:"loading"} | {status:"error", error:string} | {status:"success", data:PlayEvent[]}`
