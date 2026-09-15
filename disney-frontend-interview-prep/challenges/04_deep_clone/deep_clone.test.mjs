import { test } from "node:test";
import assert from "node:assert/strict";
import { loadImpl } from "../_lib/load-impl.mjs";

const { deepClone } = await loadImpl(import.meta.url, "deep_clone");

test("clones a nested object without sharing references", () => {
  const original = { a: 1, nested: { b: 2, list: [1, 2, { c: 3 }] } };
  const clone = deepClone(original);

  assert.deepEqual(clone, original);
  assert.notEqual(clone, original);
  assert.notEqual(clone.nested, original.nested);
  assert.notEqual(clone.nested.list, original.nested.list);
  assert.notEqual(clone.nested.list[2], original.nested.list[2]);
});

test("mutating the clone does not affect the original", () => {
  const original = { list: [1, 2, 3] };
  const clone = deepClone(original);
  clone.list.push(4);
  assert.deepEqual(original.list, [1, 2, 3]);
});

test("handles circular references without stack overflow", () => {
  const original = { name: "root" };
  original.self = original;

  const clone = deepClone(original);
  assert.equal(clone.self, clone);
  assert.notEqual(clone, original);
});

test("clones a Date as a new Date instance with the same time", () => {
  const original = { when: new Date(2026, 0, 1) };
  const clone = deepClone(original);
  assert.ok(clone.when instanceof Date);
  assert.notEqual(clone.when, original.when);
  assert.equal(clone.when.getTime(), original.when.getTime());
});

test("clones a Map and a Set", () => {
  const original = { m: new Map([["a", 1]]), s: new Set([1, 2, 3]) };
  const clone = deepClone(original);

  assert.ok(clone.m instanceof Map);
  assert.notEqual(clone.m, original.m);
  assert.equal(clone.m.get("a"), 1);

  assert.ok(clone.s instanceof Set);
  assert.notEqual(clone.s, original.s);
  assert.deepEqual([...clone.s], [1, 2, 3]);
});

test("returns primitives as-is", () => {
  assert.equal(deepClone(5), 5);
  assert.equal(deepClone("str"), "str");
  assert.equal(deepClone(null), null);
  assert.equal(deepClone(undefined), undefined);
});
