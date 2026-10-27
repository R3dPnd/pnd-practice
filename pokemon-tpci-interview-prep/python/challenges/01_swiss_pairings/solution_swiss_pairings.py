"""Swiss pairings — reference solution.

Big picture:
  1. Sort players into "standings order" (most points first).
  2. If there's an odd number of players, hand out a bye and remove that player.
  3. Pair the rest top-down, never pairing two players who already played each other.
     If a greedy choice paints us into a corner, BACKTRACK and try the next opponent.
  4. If no rematch-free round exists at all, give up on that rule and pair top-down.

Complexity: sorting is O(n log n). Backtracking is exponential in the worst case, but in
practice it almost always succeeds on the first or second candidate.
"""
from models_swiss import Player, Round


def pair(players: list[Player], history: list[tuple[str, str]]) -> Round:
    # sorted() returns a NEW list, so we never reorder the caller's list (a test checks this).
    # The key is a tuple: Python compares tuples element by element.
    #   -p.points → negate so MORE points sorts FIRST (sorted() is ascending by default)
    #   p.id      → tiebreak alphabetically so the output is deterministic
    ranked = sorted(players, key=lambda p: (-p.points, p.id))

    # Start with an empty round: no pairings yet, no bye.
    rnd = Round()

    # ---- Step 2: the bye (only needed when the player count is odd) ----
    if len(ranked) % 2 == 1:
        # Walk from the BOTTOM of the standings upward (indexes n-1, n-2, ..., 0)
        # and find the first player who hasn't already had a bye.
        #   next(generator, default) returns the first value the generator yields,
        #   or `default` if it yields nothing (i.e. everyone has had a bye) — in that
        #   case we fall back to the lowest-ranked player, index len(ranked) - 1.
        bye_idx = next(
            (i for i in range(len(ranked) - 1, -1, -1) if not ranked[i].had_bye),
            len(ranked) - 1,
        )
        # pop() removes that player from `ranked` AND returns them, so they won't be paired.
        rnd.bye = ranked.pop(bye_idx).id

    # ---- Build a fast "have these two played?" lookup ----
    # frozenset({"A", "B"}) == frozenset({"B", "A"}), so the order inside each historical
    # match doesn't matter. frozensets are hashable (regular sets aren't), so they can live
    # inside a set. Lookups are O(1).
    played = {frozenset(m) for m in history}

    # We only need IDs from here on, already in ranked order.
    ids = [p.id for p in ranked]

    # ---- Step 3: recursive backtracking ----
    # Given the players still unpaired (in ranked order), return a full list of pairings
    # with no rematches, or None if that's impossible.
    def backtrack(remaining: list[str]) -> list[tuple[str, str]] | None:
        # Base case: everyone is paired — success with zero more pairings.
        if not remaining:
            return []

        # The highest-ranked unpaired player always gets paired next.
        top = remaining[0]

        # Try opponents in ranked order: best-ranked candidate first.
        for j in range(1, len(remaining)):
            # Skip anyone `top` has already played.
            if frozenset((top, remaining[j])) in played:
                continue

            # Tentatively pair top with remaining[j]. Everyone else still needs pairing:
            #   remaining[1:j]   → players between top and the chosen opponent
            #   remaining[j+1:]  → players after the chosen opponent
            # (We build a new list instead of mutating, so "undoing" a choice is free.)
            tail = backtrack(remaining[1:j] + remaining[j + 1:])

            # If the rest of the round worked out, this choice is good — prepend it.
            if tail is not None:
                return [(top, remaining[j])] + tail
            # Otherwise loop on and try the next opponent (this is the "backtrack").

        # No opponent for `top` leads to a complete, rematch-free round.
        return None

    pairs = backtrack(ids)

    # ---- Step 4: fallback ----
    # If backtracking found a valid round, use it. Otherwise pair neighbors top-down:
    # range(0, len(ids), 2) gives 0, 2, 4, ... so we pair (ids[0], ids[1]), (ids[2], ids[3]), ...
    rnd.pairings = pairs if pairs is not None else [(ids[i], ids[i + 1]) for i in range(0, len(ids), 2)]
    return rnd
