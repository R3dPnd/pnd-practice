# 02 — Promise Polyfill

**Theme:** async internals. Directly reported real question: **"write a Promise."**

## Problem

Implement a `MyPromise` class matching the core of the real `Promise` API:

```js
export class MyPromise {
  constructor(executor) { /* executor(resolve, reject) */ }
  then(onFulfilled, onRejected) { /* returns a new MyPromise */ }
  catch(onRejected) { /* sugar for .then(undefined, onRejected) */ }
  finally(onFinally) { /* runs regardless of outcome, doesn't change the value */ }
  static resolve(value) {}
  static reject(reason) {}
  static all(iterable) { /* resolves to an array of values, in order; rejects on first rejection */ }
}
```

## Constraints / edge cases to think about

- A promise has three states (pending, fulfilled, rejected) and settles exactly once.
- `.then()` must return a **new** promise so calls can chain: `p.then(f1).then(f2)`.
- If `onFulfilled`/`onRejected` throws, the returned promise must reject with that error.
- If a handler returns another `MyPromise`, the outer promise should wait on it
  ("flattening" — this is the trickiest part of a real `Promise` implementation).
- Callbacks must run asynchronously (use `queueMicrotask`), even if the promise is
  already settled when `.then()` is called — real `Promise`s never call handlers
  synchronously, and interviewers do check for this.
- `MyPromise.all([])` should resolve immediately with `[]`.

## Why this matters for FE

Nobody hand-writes their own Promise in production, but being asked to build one is a
direct test of whether you actually understand microtasks, chaining, and error
propagation — not just whether you can call `.then()`. It's also one specific question
reported by real Disney candidates (see repo `README.md` Field notes).

## Run

```bash
node --test challenges/02_promise_polyfill -v
```
