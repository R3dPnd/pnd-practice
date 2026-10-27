"""Schedule intervals — reference solution.

All three problems share one trick: SORT BY START TIME FIRST. Once intervals are sorted,
anything that overlaps the current interval must be right next to it, so a single
left-to-right sweep is enough.

Intervals are half-open [start, end): (0, 30) and (30, 60) touch but don't overlap.
"""
import heapq

Interval = tuple[int, int]


def merge(intervals: list[Interval]) -> list[Interval]:
    # Use lists (not tuples) internally because we need to update the end in place.
    out: list[list[int]] = []

    # sorted() returns a new list (the input is untouched). Tuples sort by start first,
    # then by end.
    for start, end in sorted(intervals):
        # out[-1] is the last merged interval so far. If the current one starts at or
        # before that interval ends, they overlap or touch → extend instead of appending.
        # `<=` (not `<`) is what makes touching intervals merge: (1, 3) + (3, 5) → (1, 5).
        if out and start <= out[-1][1]:
            # max() handles intervals fully contained in the previous one:
            # (1, 10) then (2, 3) must stay (1, 10), not shrink to (1, 3).
            out[-1][1] = max(out[-1][1], end)
        else:
            # No overlap: start a new merged interval.
            out.append([start, end])

    # Convert back to tuples for the return type.
    return [(s, e) for s, e in out]


def has_conflict(intervals: list[Interval]) -> bool:
    s = sorted(intervals)
    # After sorting, you only need to compare NEIGHBORS: if interval i doesn't overlap
    # interval i-1, it can't overlap anything earlier either (those started even earlier).
    # Strict `<` here, because touching (start == previous end) is NOT a conflict.
    # any() stops at the first True.
    return any(s[i][0] < s[i - 1][1] for i in range(1, len(s)))


def min_tables(intervals: list[Interval]) -> int:
    # Picture the matches in start order. `ends` is a min-heap holding the end times of
    # matches currently using a table. Its size = tables in use right now.
    ends: list[int] = []
    best = 0   # the most tables in use at any one moment = the answer

    for start, end in sorted(intervals):
        # Free every table whose match has finished by the time this one starts.
        # ends[0] is the EARLIEST end time (min-heap root), so check it first.
        # `<=` because a table freed at 10 can be reused by a match starting at 10.
        while ends and ends[0] <= start:
            heapq.heappop(ends)

        # This match takes a table.
        heapq.heappush(ends, end)

        # Track the peak.
        best = max(best, len(ends))

    return best
