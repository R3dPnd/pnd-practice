import { test } from "node:test";
import assert from "node:assert/strict";
import { loadImpl } from "../_lib/load-impl.mjs";

const { flatten, curry } = await loadImpl(import.meta.url, "flatten_and_curry");

test("flatten fully flattens arbitrarily nested arrays by default", () => {
  assert.deepEqual(flatten([1, [2, [3, [4, [5]]]]]), [1, 2, 3, 4, 5]);
});

test("flatten respects an explicit depth", () => {
  assert.deepEqual(flatten([1, [2, [3, [4]]]], 1), [1, 2, [3, [4]]]);
  assert.deepEqual(flatten([1, [2, [3, [4]]]], 2), [1, 2, 3, [4]]);
});

test("flatten with depth 0 returns a shallow copy, unchanged", () => {
  const input = [1, [2, 3]];
  const result = flatten(input, 0);
  assert.deepEqual(result, input);
  assert.notEqual(result, input);
});

test("flatten does not mutate the input", () => {
  const input = [1, [2, 3]];
  flatten(input);
  assert.deepEqual(input, [1, [2, 3]]);
});

test("curry allows calling with all args at once", () => {
  const add3 = (a, b, c) => a + b + c;
  const curried = curry(add3);
  assert.equal(curried(1, 2, 3), 6);
});

test("curry allows calling one argument at a time", () => {
  const add3 = (a, b, c) => a + b + c;
  const curried = curry(add3);
  assert.equal(curried(1)(2)(3), 6);
});

test("curry allows calling with a mix of grouped arguments", () => {
  const add3 = (a, b, c) => a + b + c;
  const curried = curry(add3);
  assert.equal(curried(1, 2)(3), 6);
  assert.equal(curried(1)(2, 3), 6);
});

test("curry works for a different arity", () => {
  const add4 = (a, b, c, d) => a + b + c + d;
  const curried = curry(add4);
  assert.equal(curried(1)(2)(3)(4), 10);
  assert.equal(curried(1, 2, 3, 4), 10);
});
