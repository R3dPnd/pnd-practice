# React / JavaScript conceptual quiz

Same `<details>` collapsible-answer pattern as `../spring_boot/notes.md` and
`../../costco-booking-platform/practice/rest/rest-quiz.md`, but for **React fundamentals
and JS conceptual trivia** — the recall/explain-it-out-loud questions that come up
alongside or instead of live coding. The JD lists ReactJS as a **basic qualification**
("proficiency... with the ability to quickly pick up new technologies"), which for a
role that's *moving toward* Java reads as: they'll sanity-check your React depth is real
and move on, not drill it as hard as the Java/Spring Boot side. This is that
sanity-check layer.

For **hands-on coding practice** (not just recall), use
`../../disney-frontend-interview-prep/challenges/` — that repo already has 10
practice/solution/test problems (debounce, promise polyfill, event emitter, etc.) and a
front-end system-design framework. This file is the piece neither of those covers: fast
"explain the concept" answers.

Answer each out loud before expanding.

---

## Part 1 — React rendering & hooks

**Q1:** Why does this component re-render every keystroke even though `formatted`
doesn't change until `count` hits a multiple of 10?

```jsx
function Counter({ count }) {
  const formatted = count % 10 === 0 ? `Milestone: ${count}` : `${count}`;
  return <div>{formatted}</div>;
}
```

<details>
<summary>Answer</summary>

It's not actually a bug — this is correct, expected React behavior, and the question is
really testing whether you understand *why*. A component re-renders whenever its parent
re-renders (unless wrapped in `memo` and props are shallowly equal) or its own state/
props change — React doesn't skip a render just because the *computed output* happens to
be the same string as last time. `formatted` is recomputed every render regardless;
what would actually be wasteful is if this were an *expensive* computation — that's what
`useMemo` is for, not this. The real fix for unnecessary re-renders here would be
`React.memo(Counter)` on the component itself, if the parent re-renders for unrelated
reasons and `count` hasn't changed.

</details>

---

**Q2:** What's wrong with this, and how would you fix it?

```jsx
function SearchBox({ onSearch }) {
  const [query, setQuery] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => onSearch(query), 300);
  }, [query]);

  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

<details>
<summary>Answer</summary>

Missing the cleanup function — every keystroke schedules a new `setTimeout`, but the
previous one is never cancelled, so `onSearch` fires once per keystroke after 300ms each
(not debounced at all), not once 300ms after the user stops typing. Fix:

```jsx
useEffect(() => {
  const timer = setTimeout(() => onSearch(query), 300);
  return () => clearTimeout(timer); // cleanup: cancels the stale timer on the next render/unmount
}, [query]);
```

This is the exact mechanism `../../disney-frontend-interview-prep/challenges/01_debounce_throttle/`
implements from scratch — worth doing that challenge if this one felt shaky, since
"debounce via useEffect cleanup" is one of the most common real React interview
questions.

</details>

---

**Q3:** `useMemo` vs `useCallback` — what's the actual difference, and when does neither
one matter?

<details>
<summary>Answer</summary>

- `useMemo(fn, deps)` memoizes a **value** — the return of calling `fn()`.
- `useCallback(fn, deps)` memoizes a **function reference** itself — it's actually
  just `useMemo(() => fn, deps)` under the hood.

Neither matters for a component that isn't wrapped in `memo` and has no expensive
child re-render or expensive computation to avoid — a very common interview follow-up is
"would this actually help here?" and the correct senior answer is often "no, this is
premature — without a `memo`'d child or genuinely expensive computation, this just adds
overhead for no benefit." Reach for these specifically when: (1) passing a callback to a
`memo`'d child (an unstable new function reference every render would defeat the memo),
or (2) the computation itself is measurably expensive.

</details>

---

**Q4:** Why do keys matter in a list, and what's wrong with using the array index as a
key when the list can be reordered or filtered?

<details>
<summary>Answer</summary>

React uses `key` to match elements between renders during reconciliation — it's how
React decides "this is the same logical item, just re-render it with new props" vs. "this
is a new item, mount it fresh" vs. "this item is gone, unmount it." Using the array
index as a key works fine for a static list that never reorders/filters, but breaks once
items can move: if item 3 is deleted, item 4 becomes index 3 and React thinks the
*original* item 3 changed rather than being removed — this can cause wrong data to show
in inputs/component state that got left behind on the "same" key, and defeats any
`memo` optimization on the list items. Use a stable, unique ID from the data itself.

</details>

---

**Q5:** What's a controlled vs. uncontrolled input, and when would you actually choose
uncontrolled?

<details>
<summary>Answer</summary>

Controlled: the input's `value` is driven by React state (`value={query}` +
`onChange`) — React is the single source of truth, every keystroke is a state update
and a re-render. Uncontrolled: the DOM itself holds the value (`defaultValue` +
reading via a `ref` when needed), React doesn't re-render on every keystroke.
Uncontrolled is the right choice for large forms where per-keystroke re-renders are a
real perf cost and you only need the value on submit (e.g., a file input, which can't
be controlled at all in the value sense) — otherwise default to controlled since it's
easier to validate/derive UI from as the user types.

</details>

---

**Q6:** How does `useEffect`'s dependency array actually decide when to re-run, and
what's the classic "stale closure" bug?

<details>
<summary>Answer</summary>

React does a shallow (`Object.is`) comparison of each dependency against its value from
the previous render; if any changed, the effect re-runs (cleanup from the last run
fires first). The stale-closure bug: an effect with an empty `[]` dependency array
captures the *initial* values of any variables it references from the render, forever —
e.g., an interval reading `count` from state will always see `count`'s value from the
very first render, not the current one, because the closure was created once and never
recreated. Fix: either add the real dependency (and accept the effect re-running), or
use the functional updater form (`setCount(c => c + 1)`) which doesn't need to read the
current value from the closure at all.

</details>

---

## Part 2 — React architecture

**Q7:** When do you reach for Context vs. prop drilling vs. a state management library?

<details>
<summary>Answer</summary>

Prop drilling is fine (and often *clearer*, since data flow is explicit and traceable)
for 1-2 levels. Context solves the "many levels deep, would otherwise thread props
through components that don't care about them" problem, but every consumer of a Context
re-renders on *any* change to that context's value — fine for rarely-changing global
data (theme, auth user, feature flags), a poor fit for high-frequency state (Context
isn't a replacement for a proper state manager or server-cache library). A dedicated
library (Redux, Zustand, or a server-cache tool like TanStack Query for server state
specifically) earns its complexity when you need selective re-rendering, devtools/time-
travel debugging, or you're managing genuinely complex client state — not by default.

</details>

---

**Q8:** What's an Error Boundary, and why can't you write one as a function component?

<details>
<summary>Answer</summary>

An Error Boundary catches JS errors thrown during rendering in its child tree and
renders a fallback UI instead of unmounting the whole app. It must be a class component
because it relies on the lifecycle methods `static getDerivedStateFromError` (to render
the fallback) and `componentDidCatch` (to log the error) — there's no hook equivalent
as of the current React APIs. It only catches errors during rendering/lifecycle
methods/constructors of its children — not errors in event handlers (those need a plain
try/catch), not async errors, not errors in the boundary itself.

</details>

---

**Q9:** What actually happens, step by step, when `setState`/a state setter is called
inside a React event handler vs. inside a `setTimeout`?

<details>
<summary>Answer</summary>

Modern React (18+) batches state updates in both cases by default — multiple setter
calls in the same tick (event handler, `setTimeout` callback, promise callback, or
anywhere else) are grouped into a single re-render, not one re-render per call. This
changed from React 17 and earlier, where only updates inside React-managed event
handlers were batched, and anything in a `setTimeout`/promise callback triggered a
separate synchronous re-render per call. If asked to force multiple renders instead of
batching, `flushSync` from `react-dom` opts out explicitly — worth knowing this exists
even if you'd rarely reach for it.

</details>

---

## Part 3 — JS fundamentals

**Q10:** Explain closures with a concrete example — what does this print, and why?

```js
function makeCounters() {
  const counters = [];
  for (var i = 0; i < 3; i++) {
    counters.push(() => console.log(i));
  }
  return counters;
}
makeCounters().forEach(fn => fn());
```

<details>
<summary>Answer</summary>

Prints `3, 3, 3` — not `0, 1, 2`. `var` is function-scoped, not block-scoped, so all
three closures capture the *same* `i` binding, and by the time any of them run, the loop
has already finished with `i === 3`. Swapping `var` for `let` fixes it (`let` creates a
**new binding per iteration**, so each closure captures its own `i`) — this exact
mechanism (each closure capturing its own snapshot) is what
`../../disney-frontend-interview-prep/challenges/09_memoize/` and `03_event_emitter/`
rely on for correctness. Good follow-up to ask yourself: how would you fix it *without*
changing `var` to `let`? (Wrap the closure body in an IIFE that takes `i` as a parameter,
creating a new scope per iteration manually — this is literally what transpilers did
before `let` existed.)

</details>

---

**Q11:** What's the actual difference between the microtask queue and the macrotask
(task) queue, and what does this log?

```js
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
console.log("4");
```

<details>
<summary>Answer</summary>

Logs `1, 4, 3, 2`. Synchronous code runs first (`1`, `4`). Then, before the event loop
picks up the *next* macrotask, it fully drains the **microtask queue** (Promise
callbacks, `queueMicrotask`) — so `3` logs before `2`, even though both were scheduled
with a 0ms/immediate delay, because `setTimeout` callbacks are macrotasks and only run
after all currently-queued microtasks are exhausted. This distinction is the whole
reason `async/await` "feels synchronous" — an `await` is sugar over a `.then()`, so
control returns to it as a microtask, generally before the next macrotask (a render,
a timer, an I/O callback) runs.

</details>

---

**Q12:** What does `this` refer to in each of these, and why?

```js
const obj = {
  name: "campaign",
  regular: function () { return this.name; },
  arrow: () => { return this.name; },
};
const { regular, arrow } = obj;
```

<details>
<summary>Answer</summary>

`obj.regular()` → `"campaign"` — called as a method, so `this` is `obj`.
`regular()` (destructured, called standalone) → `undefined` (or throws in strict mode/
modules) — `this` is determined by *how a regular function is called*, not where it was
defined; called standalone, `this` is `undefined` in strict mode (modules are always
strict). `obj.arrow()` → `undefined` too (or the outer scope's `this.name`, likely
`undefined` at module top level) — arrow functions don't have their own `this` at all;
they lexically capture `this` from the enclosing scope at definition time, which for a
top-level object literal is whatever `this` is outside the object, not the object
itself. This is exactly why class methods passed as callbacks (`<button
onClick={this.handleClick}>` in old-style class components) need `.bind(this)` or to be
defined as arrow-function class fields — a plain method loses its `this` once detached
from the object it was called on.

</details>

---

**Q13:** `==` vs `===`, and name one case where `==` is arguably fine to use
intentionally.

<details>
<summary>Answer</summary>

`===` compares value and type with no coercion. `==` coerces operands to a common type
first, following a specific (and famously confusing) set of rules — `'' == 0` is `true`,
`null == undefined` is `true` but `null == 0` is `false`. Default to `===` always;
the one commonly-cited intentional use of `==` is `value == null`, which is `true` for
both `null` and `undefined` and nothing else — a deliberate, narrow use of coercion
instead of writing `value === null || value === undefined`. Outside that one idiom,
using `==` is a code smell an interviewer will likely flag.

</details>

---

**Q14:** Shallow copy vs. deep copy — what does `{ ...original }` actually copy, and
where does that bite you?

<details>
<summary>Answer</summary>

Spread (`{ ...original }`) creates a new top-level object, but any nested
object/array **values** are copied by reference, not cloned — mutating
`copy.nested.field` also mutates `original.nested.field`, since both point at the same
inner object. This matters constantly in React: `setState({ ...state, nested:
{...state.nested, field: newValue} })` needs the spread at *every* level you're
changing, not just the top, or you'll mutate state in place (breaking React's
reference-equality-based re-render detection) while believing you made an immutable
update. `../../disney-frontend-interview-prep/challenges/04_deep_clone/` covers writing
an actual recursive deep clone (including cycle handling) if this needs more practice.

</details>

---

## Day-of reminders

- These are meant to be answered **out loud, fast** — if an answer takes you more than
  ~30–45 seconds to get to the core point, that's a signal to drill it more, not just
  read the answer once.
- Given this JD's basic-qualification framing ("ReactJS or similar... ability to
  quickly pick up new technologies"), a plausible round shape is a handful of these
  conceptual questions folded into a broader conversation, rather than a dedicated
  React deep-dive — don't over-invest time here relative to `../java_challenges/` and
  `../spring_boot/notes.md`, which map to where this JD's actual depth is.
