import { test } from "node:test";
import assert from "node:assert/strict";
import { loadImpl } from "../_lib/load-impl.mjs";

const { fromArray, toArray, reverseKGroup } = await loadImpl(
  import.meta.url,
  "reverse_linked_list_in_k_groups"
);

test("reverses every 2 nodes (the specific reported variant)", () => {
  const head = fromArray([1, 2, 3, 4]);
  const result = reverseKGroup(head, 2);
  assert.deepEqual(toArray(result), [2, 1, 4, 3]);
});

test("reverses every 3 nodes, leaving a shorter final group unreversed", () => {
  const head = fromArray([1, 2, 3, 4, 5]);
  const result = reverseKGroup(head, 3);
  assert.deepEqual(toArray(result), [3, 2, 1, 4, 5]);
});

test("k = 1 is a no-op", () => {
  const head = fromArray([1, 2, 3]);
  const result = reverseKGroup(head, 1);
  assert.deepEqual(toArray(result), [1, 2, 3]);
});

test("an empty list returns null", () => {
  assert.equal(reverseKGroup(null, 2), null);
});

test("a list shorter than k is left entirely unreversed", () => {
  const head = fromArray([1, 2]);
  const result = reverseKGroup(head, 5);
  assert.deepEqual(toArray(result), [1, 2]);
});

test("a list that's an exact multiple of k is fully reversed in groups", () => {
  const head = fromArray([1, 2, 3, 4, 5, 6]);
  const result = reverseKGroup(head, 3);
  assert.deepEqual(toArray(result), [3, 2, 1, 6, 5, 4]);
});
