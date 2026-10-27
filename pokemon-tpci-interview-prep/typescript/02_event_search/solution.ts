// Event search: filter, sort, paginate — reference solution.
//
// Big picture: filter → sort → slice out one page. In a real service this logic is pushed
// down into SQL (WHERE / ORDER BY / LIMIT OFFSET) so the database does the work. Writing it
// in memory shows you understand what that SQL means.

// `import type` imports only types. It's erased at runtime, so there's no runtime import.
import type { Page, PlayEvent, Query } from "./types.ts";

export function searchEvents(events: PlayEvent[], q: Query): Page<PlayEvent> {
  // Lower-case the search text ONCE, not on every event.
  // `?.` (optional chaining): if q.text is undefined, the whole expression is undefined
  // instead of throwing "cannot read property of undefined".
  const text = q.text?.toLowerCase();

  const matches = events
    // .filter keeps the events where the callback returns true. Every filter follows the
    // same pattern, (!filter || matchesFilter): if the filter wasn't given, `!filter` is
    // true and the event passes. All the conditions are joined with && (AND).
    .filter((e) =>
      (!q.region || e.region === q.region) &&
      // `!q.types?.length` is true for both undefined and an empty array, so either
      // one means "no type filter".
      (!q.types?.length || q.types.includes(e.type)) &&
      // Dates are "YYYY-MM-DD" strings. That format sorts and compares correctly as
      // plain strings, so no Date parsing is needed. from/to are inclusive.
      (!q.from || e.date >= q.from) &&
      (!q.to || e.date <= q.to) &&
      (!text || e.name.toLowerCase().includes(text) || e.city.toLowerCase().includes(text)))
    // .sort's comparator returns negative / 0 / positive. localeCompare does exactly that
    // for strings. `||` chains the tiebreakers: if the dates are equal (0, which is falsy),
    // fall through to comparing names.
    // Note: .sort mutates in place, but .filter already made a new array, so the
    // caller's `events` is never reordered.
    .sort((a, b) => a.date.localeCompare(b.date) || a.name.localeCompare(b.name));

  // Clamp pageSize into [1, 100]. `??` (nullish coalescing) uses 20 only when pageSize is
  // null/undefined. `||` would ALSO replace 0, and then the clamp would never see it.
  const pageSize = Math.min(100, Math.max(1, q.pageSize ?? 20));
  const page = Math.max(1, q.page ?? 1); // pages are 1-based; don't allow 0 or negatives

  // Page 1 starts at index 0, page 2 at pageSize, and so on.
  const start = (page - 1) * pageSize;

  return {
    // slice(start, end) excludes `end` and is safe past the end of the array
    // (it just returns fewer items, or []).
    items: matches.slice(start, start + pageSize),
    page,      // shorthand for `page: page`
    pageSize,
    total: matches.length,
    // Round up: 5 items at 2 per page is 3 pages. 0 matches gives 0 pages.
    totalPages: Math.ceil(matches.length / pageSize),
  };
}
