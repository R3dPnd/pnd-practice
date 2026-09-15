import { test } from "node:test";
import assert from "node:assert/strict";
import { loadImpl } from "../_lib/load-impl.mjs";

const { memoize } = await loadImpl(import.meta.url, "memoize");

test("caches the result and does not call fn again for the same args", () => {
  let calls = 0;
  const slowSquare = (n) => {
    calls += 1;
    return n * n;
  };
  const memoized = memoize(slowSquare);

  assert.equal(memoized(5), 25);
  assert.equal(memoized(5), 25);
  assert.equal(memoized(5), 25);
  assert.equal(calls, 1);
});

test("treats different arguments as different cache entries", () => {
  let calls = 0;
  const memoized = memoize((n) => {
    calls += 1;
    return n * 2;
  });

  memoized(1);
  memoized(2);
  memoized(1);
  assert.equal(calls, 2);
});

test("supports a custom resolver for the cache key", () => {
  let calls = 0;
  const memoized = memoize(
    (user) => {
      calls += 1;
      return user.name.toUpperCase();
    },
    { resolver: (user) => user.id }
  );

  memoized({ id: 1, name: "alice" });
  memoized({ id: 1, name: "ignored-different-object-same-id" });
  assert.equal(calls, 1);
});

test("preserves `this` when calling the wrapped function", () => {
  const obj = {
    factor: 10,
    scale: memoize(function (n) {
      return n * this.factor;
    }),
  };
  assert.equal(obj.scale(5), 50);
});

test("evicts the least-recently-used entry once maxSize is exceeded", () => {
  const calls = [];
  const memoized = memoize(
    (n) => {
      calls.push(n);
      return n;
    },
    { maxSize: 2 }
  );

  memoized(1);
  memoized(2);
  memoized(1); // touches 1 again - now 2 is the least recently used
  memoized(3); // should evict 2, not 1

  memoized(1); // still cached - should not add a new call
  memoized(2); // was evicted - should re-compute

  assert.deepEqual(calls, [1, 2, 3, 2]);
});
