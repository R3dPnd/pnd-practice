# 07 — Schedule intervals (merge / conflicts / tables needed)

**Pattern:** sort + sweep, min-heap · **Classic trio** (Merge Intervals, Meeting Rooms I & II)

An event venue schedules side events and matches. Intervals are half-open `[Start, End)`
in minutes — an event ending at 10 and one starting at 10 do **not** overlap.

## Task
1. `Merge(iv []Interval) []Interval` — merge overlapping (touching ones too — `[1,3)`+`[3,5)` → `[1,5)`), sorted by start.
2. `HasConflict(iv []Interval) bool` — does any pair overlap (touching is not a conflict)?
3. `MinTables(iv []Interval) int` — min number of tables so every match gets one (Meeting Rooms II).

Don't mutate the input slice.

## Talking points
- `MinTables`: either a min-heap of end times, or split starts/ends into two sorted arrays
  and sweep with two pointers. Both O(n log n).
- Why half-open intervals avoid off-by-one bugs.
