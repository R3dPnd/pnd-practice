# 09 — Shortest path across the venue floor (Python)

Prompt + follow-ups: [`../../../challenges/09_venue_shortest_path/README.md`](../../../challenges/09_venue_shortest_path/README.md).

`shortest_path(grid: list[str]) -> int` — `.` open, `#` blocked, `S` start, `E` exit,
4-directional moves; `-1` if unreachable or `S`/`E` missing. Use `collections.deque` for BFS.
