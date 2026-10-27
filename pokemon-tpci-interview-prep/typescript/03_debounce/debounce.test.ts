import { test, mock } from "node:test";
import assert from "node:assert/strict";
import { load } from "../impl.ts";
import type * as M from "./solution.ts";

const { debounce } = await load<typeof M>("03_debounce");

test("calls once with last args after quiet period", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout"] });
  const fn = mock.fn((_q: string) => {});
  const d = debounce(fn, 300);
  d("p"); t.mock.timers.tick(100);
  d("pi"); t.mock.timers.tick(100);
  d("pik");
  t.mock.timers.tick(299);
  assert.equal(fn.mock.callCount(), 0);
  t.mock.timers.tick(1);
  assert.equal(fn.mock.callCount(), 1);
  assert.deepEqual(fn.mock.calls[0].arguments, ["pik"]);
});

test("cancel drops the pending call", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout"] });
  const fn = mock.fn(() => {});
  const d = debounce(fn, 100);
  d();
  d.cancel();
  t.mock.timers.tick(200);
  assert.equal(fn.mock.callCount(), 0);
});

test("flush runs immediately, once", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout"] });
  const fn = mock.fn((_n: number) => {});
  const d = debounce(fn, 100);
  d(7);
  d.flush();
  assert.deepEqual(fn.mock.calls.map((c) => c.arguments), [[7]]);
  t.mock.timers.tick(200);
  d.flush();
  assert.equal(fn.mock.callCount(), 1);
});
