# 03 — Event Emitter

**Theme:** pub/sub, closures. A classic "build a mini library" FE question, and the
pattern underneath most component-to-component communication that isn't plain props.

## Problem

```js
export class EventEmitter {
  on(event, handler) { /* subscribe; returns `this` for chaining */ }
  off(event, handler) { /* unsubscribe */ }
  once(event, handler) { /* fires at most once, then auto-unsubscribes */ }
  emit(event, ...args) { /* calls all handlers for `event` with `args`; returns true if
                             there were any listeners, false otherwise */ }
}
```

## Constraints / edge cases to think about

- Multiple listeners on the same event must all fire, in the order they were registered.
- `emit` on an event with no listeners should not throw — just return `false`.
- A handler that calls `off()` on itself (or another handler) *during* an `emit` should
  not crash or skip/duplicate other handlers in that same `emit` call — snapshot the
  listener list before iterating.
- `once` must actually remove itself after firing — don't just track a "fired" flag
  and leave a dead listener registered forever.

## Why this matters for FE

This is the primitive that libraries like Node's own `EventEmitter`, most WebSocket
client wrappers, and plenty of vanilla-JS component architectures (before/around
React's prop-drilling model) are built on. Interviewers use it to check whether you
understand closures and `Map`/`Set` well enough to build a small, correct data
structure from scratch, not whether you know npm's `events` module.

## Run

```bash
node --test challenges/03_event_emitter -v
```
