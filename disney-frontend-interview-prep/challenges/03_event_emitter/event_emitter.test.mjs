import { test } from "node:test";
import assert from "node:assert/strict";
import { loadImpl } from "../_lib/load-impl.mjs";

const { EventEmitter } = await loadImpl(import.meta.url, "event_emitter");

test("emit calls the handler with the given args", () => {
  const emitter = new EventEmitter();
  let received = null;
  emitter.on("greet", (name) => {
    received = name;
  });
  emitter.emit("greet", "world");
  assert.equal(received, "world");
});

test("multiple listeners on the same event all fire, in registration order", () => {
  const emitter = new EventEmitter();
  const order = [];
  emitter.on("tick", () => order.push("a"));
  emitter.on("tick", () => order.push("b"));
  emitter.emit("tick");
  assert.deepEqual(order, ["a", "b"]);
});

test("off removes a handler so it no longer fires", () => {
  const emitter = new EventEmitter();
  let calls = 0;
  const handler = () => {
    calls += 1;
  };
  emitter.on("x", handler);
  emitter.off("x", handler);
  emitter.emit("x");
  assert.equal(calls, 0);
});

test("once fires exactly one time then unsubscribes", () => {
  const emitter = new EventEmitter();
  let calls = 0;
  emitter.once("x", () => {
    calls += 1;
  });
  emitter.emit("x");
  emitter.emit("x");
  emitter.emit("x");
  assert.equal(calls, 1);
});

test("emit returns false for an event with no listeners, true otherwise", () => {
  const emitter = new EventEmitter();
  assert.equal(emitter.emit("nothing"), false);
  emitter.on("something", () => {});
  assert.equal(emitter.emit("something"), true);
});

test("a handler unsubscribing itself mid-emit doesn't break other handlers", () => {
  const emitter = new EventEmitter();
  const order = [];
  const first = () => {
    order.push("first");
    emitter.off("x", first);
  };
  const second = () => order.push("second");
  emitter.on("x", first);
  emitter.on("x", second);

  emitter.emit("x");
  assert.deepEqual(order, ["first", "second"]);

  order.length = 0;
  emitter.emit("x");
  assert.deepEqual(order, ["second"], "first should have stayed unsubscribed");
});
