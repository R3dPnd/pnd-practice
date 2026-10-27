import { test } from "node:test";
import assert from "node:assert/strict";
import { load } from "../impl.ts";
import type * as M from "./solution.ts";
import type { PlayEvent } from "./types.ts";

const { searchEvents } = await load<typeof M>("02_event_search");

const events: PlayEvent[] = [
  { id: "1", name: "Portland Regional", city: "Portland", region: "NA", type: "regional", date: "2026-11-14" },
  { id: "2", name: "Seattle League Cup", city: "Seattle", region: "NA", type: "league_cup", date: "2026-11-01" },
  { id: "3", name: "Bellevue League Challenge", city: "Bellevue", region: "NA", type: "league_challenge", date: "2026-11-01" },
  { id: "4", name: "London International", city: "London", region: "EU", type: "international", date: "2027-04-10" },
  { id: "5", name: "Worlds", city: "San Francisco", region: "NA", type: "worlds", date: "2027-08-20" },
];

test("sorts by date then name with defaults", () => {
  const r = searchEvents(events, {});
  assert.deepEqual(r.items.map((e) => e.id), ["3", "2", "1", "4", "5"]);
  assert.equal(r.page, 1);
  assert.equal(r.pageSize, 20);
  assert.equal(r.total, 5);
  assert.equal(r.totalPages, 1);
});

test("filters combine with AND", () => {
  const r = searchEvents(events, { region: "NA", types: ["league_cup", "regional"], from: "2026-11-01", to: "2026-11-14" });
  assert.deepEqual(r.items.map((e) => e.id), ["2", "1"]);
});

test("text search is case-insensitive over name and city", () => {
  assert.deepEqual(searchEvents(events, { text: "SEATTLE" }).items.map((e) => e.id), ["2"]);
  assert.deepEqual(searchEvents(events, { text: "francisco" }).items.map((e) => e.id), ["5"]);
});

test("paginates and clamps page size", () => {
  const p2 = searchEvents(events, { page: 2, pageSize: 2 });
  assert.deepEqual(p2.items.map((e) => e.id), ["1", "4"]);
  assert.equal(p2.totalPages, 3);
  assert.equal(searchEvents(events, { pageSize: 0 }).pageSize, 1);
  assert.equal(searchEvents(events, { pageSize: 500 }).pageSize, 100);
});

test("empty result", () => {
  const r = searchEvents(events, { region: "OCE" });
  assert.deepEqual(r, { items: [], page: 1, pageSize: 20, total: 0, totalPages: 0 });
});
