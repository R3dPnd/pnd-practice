import { test } from "node:test";
import assert from "node:assert/strict";
import { loadImpl } from "../_lib/load-impl.mjs";

const { debounce, throttle } = await loadImpl(import.meta.url, "debounce_throttle");

test("debounce only fires once after calls stop, using the latest args", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout"] });
  let calls = 0;
  let lastArg = null;
  const debounced = debounce((arg) => {
    calls += 1;
    lastArg = arg;
  }, 100);

  debounced("a");
  t.mock.timers.tick(50);
  debounced("b"); // resets the timer
  t.mock.timers.tick(50);
  assert.equal(calls, 0, "should not have fired yet - only 50ms since last call");

  t.mock.timers.tick(50);
  assert.equal(calls, 1);
  assert.equal(lastArg, "b");
});

test("debounce preserves `this`", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout"] });
  const obj = {
    value: 42,
    record() {},
  };
  let seenThis = null;
  const debounced = debounce(function () {
    seenThis = this;
  }, 10);
  debounced.call(obj);
  t.mock.timers.tick(10);
  assert.equal(seenThis, obj);
});

test("throttle fires immediately on the leading call", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout", "Date"] });
  let calls = 0;
  const throttled = throttle(() => {
    calls += 1;
  }, 100);

  throttled();
  assert.equal(calls, 1);
});

test("throttle drops calls within the window but fires a trailing call once it ends", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout", "Date"] });
  const seenArgs = [];
  const throttled = throttle((arg) => {
    seenArgs.push(arg);
  }, 100);

  throttled("first");
  throttled("second");
  throttled("third");
  assert.deepEqual(seenArgs, ["first"], "only the leading call should have fired so far");

  t.mock.timers.tick(100);
  assert.deepEqual(
    seenArgs,
    ["first", "third"],
    "trailing call should fire once with the latest args"
  );
});

test("throttle allows a new leading call once the window has fully elapsed", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout", "Date"] });
  let calls = 0;
  const throttled = throttle(() => {
    calls += 1;
  }, 100);

  throttled();
  t.mock.timers.tick(150);
  throttled();
  assert.equal(calls, 2);
});
