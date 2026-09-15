import { test } from "node:test";
import assert from "node:assert/strict";
import { loadImpl } from "../_lib/load-impl.mjs";

const { myMap, myFilter, myReduce } = await loadImpl(import.meta.url, "array_polyfills");

test("myMap matches native map, including index and array args", () => {
  const arr = [1, 2, 3];
  const result = myMap(arr, (n, i, a) => n * 2 + i + a.length);
  assert.deepEqual(result, arr.map((n, i, a) => n * 2 + i + a.length));
});

test("myFilter matches native filter, including index and array args", () => {
  const arr = [1, 2, 3, 4, 5, 6];
  const result = myFilter(arr, (n, i) => n % 2 === 0 && i > 0);
  assert.deepEqual(result, arr.filter((n, i) => n % 2 === 0 && i > 0));
});

test("myReduce with an initial value matches native reduce", () => {
  const arr = [1, 2, 3, 4];
  const result = myReduce(arr, (acc, n) => acc + n, 100);
  assert.equal(result, arr.reduce((acc, n) => acc + n, 100));
});

test("myReduce without an initial value uses the first element and starts at index 1", () => {
  const arr = [1, 2, 3, 4];
  const result = myReduce(arr, (acc, n) => acc + n);
  assert.equal(result, arr.reduce((acc, n) => acc + n));
});

test("myReduce on an empty array with no initial value throws a TypeError", () => {
  assert.throws(() => myReduce([], (acc, n) => acc + n), TypeError);
});

test("myReduce on an empty array WITH an initial value returns the initial value", () => {
  assert.equal(
    myReduce([], (acc, n) => acc + n, 42),
    42
  );
});
