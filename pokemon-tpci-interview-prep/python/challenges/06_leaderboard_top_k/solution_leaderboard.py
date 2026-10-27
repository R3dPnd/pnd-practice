"""Championship Points leaderboard (top-K) — reference solution.

Big picture:
  - award()/total() are just a dict of running totals: O(1) each.
  - top_k(k) keeps a MIN-heap of size k holding "the best k players seen so far".
    The heap's root (heap[0]) is always the WORST of those k, so each new player only
    has to beat heap[0] to get in. That's O(n log k), versus O(n log n) to sort everyone.

Simpler alternatives worth mentioning in an interview:
  sorted(self._totals.items(), key=lambda kv: (-kv[1], kv[0]))[:k]          # O(n log n)
  heapq.nsmallest(k, self._totals.items(), key=lambda kv: (-kv[1], kv[0]))  # O(n log k)
"""
import heapq
from collections import defaultdict


class _Ranked:
    """One heap entry, ordered so the WORST of the current top-k sits at heap[0].

    heapq is a MIN-heap: the "smallest" item (according to __lt__) is at index 0. We want
    the worst player there, so we define "less than" to mean "ranks worse than".
    """
    __slots__ = ("id", "points")

    def __init__(self, id: str, points: int):
        self.id, self.points = id, points

    def __lt__(self, other: "_Ranked") -> bool:
        # "self ranks worse than other" means:
        #   fewer points, OR the same points and an alphabetically LATER id (ties go to the
        #   earlier id, so the later id is the worse one).
        # Note the deliberate swap: (self.points, other.id) vs (other.points, self.id).
        # Comparing the points normally but the ids in reverse does both in one tuple compare.
        return (self.points, other.id) < (other.points, self.id)


class Leaderboard:
    def __init__(self):
        # Missing players read as 0 points.
        self._totals: dict[str, int] = defaultdict(int)

    def award(self, player_id: str, points: int) -> None:
        # Negative points (penalties, corrections) just subtract.
        self._totals[player_id] += points

    def total(self, player_id: str) -> int:
        # Use .get instead of [] so looking up an unknown player doesn't INSERT them
        # into the defaultdict as a side effect.
        return self._totals.get(player_id, 0)

    def top_k(self, k: int) -> list[tuple[str, int]]:
        if k <= 0:
            return []

        heap: list[_Ranked] = []
        for pid, pts in self._totals.items():
            entry = _Ranked(pid, pts)
            if len(heap) < k:
                # Haven't collected k players yet — everyone gets in.
                heapq.heappush(heap, entry)
            elif heap[0] < entry:
                # The heap is full, and the newcomer ranks better than the current worst.
                # heapreplace pops the root and pushes the newcomer in one O(log k) step.
                heapq.heapreplace(heap, entry)
            # Otherwise the newcomer is worse than all k we're holding → ignore them.

        # The heap is only partially ordered, so sort the k survivors for output.
        # reverse=True because our __lt__ means "worse"; we want best first.
        return [(e.id, e.points) for e in sorted(heap, reverse=True)]
