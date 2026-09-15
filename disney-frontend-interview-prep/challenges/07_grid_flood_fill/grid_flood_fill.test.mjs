import { test } from "node:test";
import assert from "node:assert/strict";
import { loadImpl } from "../_lib/load-impl.mjs";

const { floodFill } = await loadImpl(import.meta.url, "grid_flood_fill");

test("fills the connected region matching the start color", () => {
  const image = [
    [1, 1, 1],
    [1, 1, 0],
    [1, 0, 1],
  ];
  const result = floodFill(image, 1, 1, 2);
  assert.deepEqual(result, [
    [2, 2, 2],
    [2, 2, 0],
    [2, 0, 1],
  ]);
});

test("is a no-op when the new color matches the start color (must not infinite-loop)", () => {
  const image = [
    [0, 0, 0],
    [0, 0, 0],
  ];
  const result = floodFill(image, 0, 0, 0);
  assert.deepEqual(result, [
    [0, 0, 0],
    [0, 0, 0],
  ]);
});

test("does not touch a same-colored region that isn't reachable from the start", () => {
  const image = [
    [1, 0, 1],
    [0, 0, 0],
    [1, 0, 1],
  ];
  // top-left 1 and bottom-right 1 are not 4-directionally connected to each other
  const result = floodFill(image, 0, 0, 9);
  assert.deepEqual(result, [
    [9, 0, 1],
    [0, 0, 0],
    [1, 0, 1],
  ]);
});

test("respects grid boundaries", () => {
  const image = [[5]];
  const result = floodFill(image, 0, 0, 7);
  assert.deepEqual(result, [[7]]);
});

test("fills an irregular connected shape correctly", () => {
  const image = [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0],
  ];
  const result = floodFill(image, 0, 0, 3);
  assert.deepEqual(result, [
    [3, 3, 0, 0],
    [0, 3, 3, 0],
    [0, 0, 3, 0],
    [0, 0, 0, 0],
  ]);
});
