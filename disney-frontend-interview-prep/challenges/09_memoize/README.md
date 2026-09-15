# 09 — Memoize (with bounded LRU eviction)

**Theme:** closures + caching. Common FE performance question, and sets up the caching
tradeoffs discussed in `../../frontend_design/notes.md`.

## Problem

```js
export function memoize(fn, { resolver, maxSize = Infinity } = {}) {
  /* returns a memoized wrapper around fn.
     - resolver(...args) => cache key; defaults to JSON.stringify(args)
     - maxSize: once the cache would exceed maxSize entries, evict the LEAST
       RECENTLY USED entry (not just the oldest inserted) before adding the new one */
}
```

## Constraints / edge cases to think about

- A cache hit must return the cached value **without calling `fn` again** — tests check
  this via a call counter, not just return-value correctness.
- Accessing an existing cached key (a hit) should count as "recently used" and protect
  it from eviction — this is what makes it LRU rather than plain FIFO. `Map` preserves
  insertion order, and deleting + re-inserting a key moves it to the end — that's the
  whole trick, no separate linked list needed for this scope.
- `resolver` lets the caller define what "same arguments" means (e.g., only the first
  argument matters, or args need normalizing) — don't hardcode `JSON.stringify`.
- Preserve `this` when calling the wrapped `fn`.

## Why this matters for FE

Memoization is one of the few interview-y patterns that shows up verbatim in real FE
code: `React.memo`, `useMemo`/`useCallback`, and Reselect's memoized selectors are all
variations on exactly this idea, just applied to renders/values instead of arbitrary
function calls. Interviewers ask this to see if you understand the actual mechanism
`useMemo` is built on, not just that you know to call it.

## Run

```bash
node --test challenges/09_memoize -v
```
