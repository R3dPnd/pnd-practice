# 01 — Debounce & Throttle

**Theme:** closures + timers. The single most commonly reported FE interview
question, full stop — expect it in some form even if the rest of the round is
unpredictable (see repo `README.md`'s Field notes).

## Problem

```js
export function debounce(fn, wait) {
  /* returns a debounced wrapper around fn: only invokes fn after `wait` ms
     have elapsed since the LAST call to the wrapper (each call resets the timer) */
}

export function throttle(fn, wait) {
  /* returns a throttled wrapper around fn: invokes fn immediately on the first
     call (leading edge), then at most once every `wait` ms while calls keep
     coming; the last call within a throttled window should still fire once
     the window ends (trailing edge) */
}
```

## Constraints / edge cases to think about

- Both wrappers must preserve `this` and forward all arguments to `fn`.
- `debounce`: calling the wrapper again before `wait` elapses must reset the timer,
  not queue a second call.
- `throttle`: don't just drop trailing calls — a call that arrives mid-window should
  still fire once, after the window closes, with its (latest) arguments.
- Don't call `Date.now()`/`setTimeout` directly in a way that resists testing — the
  tests here use `node:test`'s built-in timer mocking (`t.mock.timers`), so as long as
  you use the real global `setTimeout`/`Date`, mocking works transparently.

## Why this matters for FE

This is the shape behind every "don't fire a network request on every keystroke"
search box, every scroll/resize handler, and every button that shouldn't double-submit.
Be ready to explain when you'd reach for one vs. the other: debounce for "wait until
the user stops" (search-as-you-type), throttle for "cap the rate but keep responding"
(scroll position tracking, drag handlers).

## Run

```bash
node --test challenges/01_debounce_throttle -v
```
