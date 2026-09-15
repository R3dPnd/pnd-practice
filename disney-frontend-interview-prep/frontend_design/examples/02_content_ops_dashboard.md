# Worked example: content operations dashboard front-end

Practice prompt 2 from `../notes.md`. This is literally the UI built in
`../../espn-conent-dashboard/README.md` Module 3 — use this to practice explaining
those decisions live, as if designing it from scratch, not just describing what's
already built.

- **Clarify**: Who's the user (an editor managing dozens to low-thousands of content
  items, not millions)? What actions matter most — search/filter, or bulk publish/
  unpublish? Is this single-editor or does it need to handle concurrent edits from
  multiple editors on the same item?
- **Contract**: A `ContentTable` component takes `items`, `total`, and an
  `onStatusChange` callback — it doesn't know where `items` came from. A
  `useContentItems(filters)` hook owns fetching/caching; the table is purely
  presentational and testable with plain props.
- **Architecture**: URL query params are the source of truth for filters (search text,
  sport, status, page) — not component state — so filters survive a page refresh and
  are shareable/bookmarkable. A server-cache library (TanStack Query) owns the actual
  data fetching, caching, and background refetch, keyed by the filter object, instead
  of hand-rolled `useEffect` + `useState` (see `../../espn-conent-dashboard/README.md`
  Module 3's interview-question answer on exactly this point).
- **Deep dive** (likely steered here): the publish-button optimistic update. Clicking
  "Publish" updates the row's status in the local cache immediately (before the network
  call resolves), and rolls back to the previous cached value if the mutation fails —
  so the UI feels instant instead of waiting on a round trip, without lying to the user
  if it actually fails.
- **FE review pass**:
  - *Performance*: `memo` on table rows + `useCallback` on the status-change handler,
    so updating one row's status doesn't re-render all 200 rows — cheap here, but
    exactly the kind of thing that becomes a real problem if this table grows.
  - *Accessibility*: filter dropdowns and the publish button need real focus/keyboard
    support, and a status change should be announced, not just visually indicated by a
    color chip (color alone isn't accessible).
  - *Resilience*: explicit loading state, an empty state ("No content found"), and a
    visible error state if the fetch fails — not just a blank table.
  - *Security*: if any field renders CMS-authored rich text (an article body preview),
    it must go through a sanitizing renderer, never `dangerouslySetInnerHTML` directly —
    see the actual `RichTextRenderer` in `../../espn-conent-dashboard/README.md` Module 5
    for the real whitelist-based approach.
- **Tradeoffs**: URL-as-state is slightly more code than component state, but the
  "shareable/bookmarkable/refresh-safe filters" property is worth it for an internal
  tool editors live in all day. `useDeferredValue` on the search input keeps typing
  responsive without a manual debounce, at the cost of being slightly less precise about
  exactly when a request fires than an explicit debounce would be.
- **What I'd do differently with more time**: virtualize the table once item counts
  grow past a couple hundred rows (react-window/TanStack Virtual) instead of rendering
  every row — not needed at current scale, but the first thing that breaks as content
  volume grows.
