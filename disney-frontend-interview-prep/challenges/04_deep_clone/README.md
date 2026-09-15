# 04 — Deep Clone

**Theme:** recursion over object graphs. Common FE fundamentals question — tests
whether you actually understand reference vs. value semantics, not just `structuredClone`.

## Problem

```js
export function deepClone(value) {
  /* returns a deep copy of value: nested objects/arrays are copied recursively,
     not shared by reference with the original */
}
```

## Constraints / edge cases to think about

- Primitives (numbers, strings, booleans, `null`, `undefined`) return as-is.
- Arrays and plain objects must be recursively cloned — mutating the clone must never
  affect the original, at any depth.
- Handle **circular references** without a stack overflow (an object that contains a
  reference to itself, directly or indirectly) — track already-cloned objects.
- Bonus types worth handling explicitly: `Date`, `Map`, `Set` (a naive `{...spread}`
  approach silently breaks on all three).

## Why this matters for FE

This comes up constantly in real code, not just interviews: cloning Redux/Zustand
state before mutating it, deep-copying a form's default values before editing, cloning
API responses before local edits. `structuredClone()` exists natively now, but
interviewers ask this to see if you understand *why* it's needed and what a shallow
`{...spread}` or `JSON.parse(JSON.stringify(x))` silently gets wrong (loses `Date`
objects, `undefined` values, functions, and breaks entirely on circular references).

## Run

```bash
node --test challenges/04_deep_clone -v
```
