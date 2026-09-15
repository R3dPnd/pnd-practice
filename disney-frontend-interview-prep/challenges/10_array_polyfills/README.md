# 10 — Array Method Polyfills

**Theme:** reimplement `map`/`filter`/`reduce`. Extremely common "prove you actually
understand JS" trivia-round question — almost guaranteed in some form for a front-end
role, regardless of which of Disney's reported interview shapes you get.

## Problem

Implement standalone versions (don't monkey-patch `Array.prototype` — operate on an
array argument instead, so these are trivially testable in isolation):

```js
export function myMap(arr, callback) { /* callback(element, index, array) */ }
export function myFilter(arr, predicate) { /* predicate(element, index, array) */ }
export function myReduce(arr, reducer, initialValue) {
  /* reducer(accumulator, element, index, array); initialValue is OPTIONAL,
     matching real Array.prototype.reduce semantics */
}
```

## Constraints / edge cases to think about

- All three callbacks receive `(element, index, array)` (reducer additionally gets the
  accumulator first) — matching the real methods lets you reuse the same callbacks you'd
  pass to native `map`/`filter`/`reduce`.
- `myReduce` **without** an `initialValue`: use the first element as the initial
  accumulator and start iterating from index 1. Calling it on an **empty array with no
  initial value** must throw a `TypeError` — this is the edge case people forget, and
  it's exactly the kind of detail an interviewer will probe for.
- Don't just call the real `Array.prototype.map`/etc. internally — the point is
  demonstrating you understand the loop underneath.

## Why this matters for FE

This is a direct fluency check: if you can't reimplement these three from memory, it
suggests you've only ever used them, not understood them — and `reduce`'s optional-
initial-value behavior in particular trips up a lot of candidates who "know" the method
but have never hit that edge case in real code.

## Run

```bash
node --test challenges/10_array_polyfills -v
```
