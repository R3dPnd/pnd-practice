# TS 02 — event search: filter, sort, paginate

The kind of data-shaping function behind an "Event Locator" REST endpoint
(`GET /events?region=NA&type=league_cup&from=2026-11-01&page=2&pageSize=20`).

```ts
searchEvents(events: PlayEvent[], q: Query): Page<PlayEvent>
```
- Filters (all optional, AND-ed): `region`, `types` (any of), `from`/`to` (ISO dates,
  inclusive, compare on `date`), `text` (case-insensitive substring of `name` or `city`).
- Sort by `date` asc, then `name` asc.
- `page` is 1-based, default 1; `pageSize` default 20, clamp to 1..100.
- Return `{ items, page, pageSize, total, totalPages }`. `totalPages` is 0 when nothing matches.
- Talking points: why you'd push this into Postgres (`WHERE ... ORDER BY ... LIMIT/OFFSET`,
  indexes on `(region, date)`), offset vs cursor pagination, validating query params at the edge.
