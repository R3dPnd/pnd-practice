import { test } from "node:test";
import assert from "node:assert/strict";
import { load } from "../impl.ts";
import type * as M from "./solution.ts";

const { retry } = await load<typeof M>("01_retry_with_backoff");

test("succeeds after transient failures with exponential delays", async () => {
  const delays: number[] = [];
  const result = await retry(
    async (attempt) => {
      if (attempt < 3) throw new Error(`fail ${attempt}`);
      return "ok";
    },
    { retries: 5, baseMs: 100, sleep: async (ms) => void delays.push(ms) },
  );
  assert.equal(result, "ok");
  assert.deepEqual(delays, [100, 200]);
});

test("rethrows last error when retries exhausted", async () => {
  let calls = 0;
  await assert.rejects(
    retry(async (a) => { calls++; throw new Error(`fail ${a}`); }, { retries: 2, baseMs: 1, sleep: async () => {} }),
    /fail 3/,
  );
  assert.equal(calls, 3);
});

test("does not retry when shouldRetry is false", async () => {
  let calls = 0;
  const err = Object.assign(new Error("bad request"), { status: 400 });
  await assert.rejects(
    retry(async () => { calls++; throw err; }, {
      retries: 5, baseMs: 1, sleep: async () => {},
      shouldRetry: (e) => (e as { status?: number }).status !== 400,
    }),
    /bad request/,
  );
  assert.equal(calls, 1);
});
