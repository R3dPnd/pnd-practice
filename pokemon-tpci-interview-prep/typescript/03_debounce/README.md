# TS 03 — debounce (with cancel/flush)

The search box on an event locator shouldn't fire a request per keystroke.

```ts
const d = debounce(fn, waitMs);
d(...args);   // (re)starts the timer; fn runs once with the LAST args after waitMs of quiet
d.cancel();   // drop any pending call
d.flush();    // run the pending call now (no-op if none)
```
Keep the generic types tight: `debounce<A extends unknown[]>(fn: (...args: A) => void, ms)`.

Talking points: debounce vs throttle; in React, wrap with `useMemo`/`useRef` so the debounced
function is stable across renders and `cancel` on unmount; `AbortController` to cancel the
in-flight fetch too.
