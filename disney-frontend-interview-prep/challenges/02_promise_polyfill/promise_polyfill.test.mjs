import { test } from "node:test";
import assert from "node:assert/strict";
import { loadImpl } from "../_lib/load-impl.mjs";

const { MyPromise } = await loadImpl(import.meta.url, "promise_polyfill");

test("resolves a value to .then", async () => {
  const value = await new MyPromise((resolve) => resolve(42));
  assert.equal(value, 42);
});

test("rejects a reason to .catch", async () => {
  let caught = null;
  await new MyPromise((_resolve, reject) => reject("boom")).catch((reason) => {
    caught = reason;
  });
  assert.equal(caught, "boom");
});

test("chains .then calls, transforming the value each time", async () => {
  const result = await new MyPromise((resolve) => resolve(1))
    .then((v) => v + 1)
    .then((v) => v * 10);
  assert.equal(result, 20);
});

test("flattens when a handler returns another MyPromise", async () => {
  const result = await new MyPromise((resolve) => resolve(1)).then(
    (v) => new MyPromise((resolve) => resolve(v + 100))
  );
  assert.equal(result, 101);
});

test("a throw inside a handler rejects the returned promise", async () => {
  let caught = null;
  await new MyPromise((resolve) => resolve(1))
    .then(() => {
      throw new Error("nope");
    })
    .catch((err) => {
      caught = err;
    });
  assert.equal(caught.message, "nope");
});

test(".finally runs regardless of outcome and doesn't change the resolved value", async () => {
  let finallyRan = false;
  const value = await new MyPromise((resolve) => resolve("ok")).finally(() => {
    finallyRan = true;
  });
  assert.equal(finallyRan, true);
  assert.equal(value, "ok");
});

test("handlers run asynchronously, never synchronously", () => {
  let ran = false;
  MyPromise.resolve(1).then(() => {
    ran = true;
  });
  assert.equal(ran, false, "handler should not have run synchronously");
});

test("MyPromise.all resolves to an array of values, in order", async () => {
  const result = await MyPromise.all([
    MyPromise.resolve(1),
    2,
    new MyPromise((resolve) => resolve(3)),
  ]);
  assert.deepEqual(result, [1, 2, 3]);
});

test("MyPromise.all rejects as soon as any input rejects", async () => {
  let caught = null;
  await MyPromise.all([MyPromise.resolve(1), MyPromise.reject("bad")]).catch((reason) => {
    caught = reason;
  });
  assert.equal(caught, "bad");
});

test("MyPromise.all([]) resolves immediately with []", async () => {
  const result = await MyPromise.all([]);
  assert.deepEqual(result, []);
});
