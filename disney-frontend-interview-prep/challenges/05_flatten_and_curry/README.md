# 05 — Flatten & Curry

**Theme:** recursion + function composition. A common JS-fundamentals pairing —
interviewers use these two together to check both "can you recurse correctly" and
"do you understand `arguments`/closures well enough to build `curry`."

## Problem

```js
export function flatten(arr, depth = Infinity) {
  /* like Array.prototype.flat() reimplemented: flattens nested arrays up to `depth`
     levels deep */
}

export function curry(fn) {
  /* returns a curried version of fn: can be called with all args at once, or
     incrementally, one or a few at a time, until fn's declared arity is reached */
}
```

## Constraints / edge cases to think about

- `flatten`: `depth = 0` (or any depth `< 1`) returns a shallow copy, unchanged.
  `depth = Infinity` (the default) fully flattens regardless of nesting.
- `flatten` must not mutate the input array.
- `curry`: use `fn.length` to know how many args are expected — `curried(1)(2)(3)`,
  `curried(1, 2)(3)`, and `curried(1, 2, 3)` must all produce the same result for a
  3-arg function.
- `curry` should work for functions of any arity, not just a hardcoded number of args.

## Why this matters for FE

`flatten` shows up in real data-shaping code (normalizing a tree of nested API
categories into a flat list, for instance) and is a quick way for an interviewer to see
if your recursion is clean. `curry` comes up less in app code directly, but is the
mechanism behind libraries like Redux's `connect()` and Reselect's selector factories
(`makeSelector(a)(b)` style APIs) — knowing how it works under the hood is a good signal
of general JS fluency.

## Run

```bash
node --test challenges/05_flatten_and_curry -v
```
