"""Standings with OWP / OOWP tiebreakers — reference solution.

Big picture (three passes):
  1. Walk every match once and tally each player's record + list of opponents.
  2. Compute each player's win% (with the 25% floor), then each player's OWP
     (average of their opponents' win%).
  3. Compute OOWP (average of their opponents' OWP), build Standing rows, and sort.

OOWP depends on OWP, which depends on win% — that's why it has to be layered passes
rather than one loop.
"""
from collections import defaultdict
from statistics import fmean

from models_standings import Match, Standing


def compute(matches: list[Match]) -> list[Standing]:
    # defaultdict(int) returns 0 for a missing key, so `wins[p] += 1` works even the
    # first time we see p — no "if p not in wins" boilerplate needed.
    wins: dict[str, int] = defaultdict(int)     # all wins, INCLUDING byes (for points)
    losses: dict[str, int] = defaultdict(int)
    ties: dict[str, int] = defaultdict(int)
    won: dict[str, int] = defaultdict(int)      # wins EXCLUDING byes (for win%)
    played: dict[str, int] = defaultdict(int)   # matches EXCLUDING byes (for win%)
    # defaultdict(list) gives an empty list for a missing key.
    opponents: dict[str, list[str]] = defaultdict(list)

    # ---- Pass 1: tally records ----
    for m in matches:
        # A bye is represented as p2 = None. It counts as a win for points, but it is
        # NOT a real opponent and does NOT count toward win%.
        if m.p2 is None:
            wins[m.p1] += 1
            # Just touching opponents[m.p1] creates an empty list for them. That matters
            # because we use `opponents` as our master list of players below — without
            # this line, a player whose only match was a bye would vanish.
            opponents[m.p1]
            continue

        # A real match: both players get a match played and each other as an opponent.
        played[m.p1] += 1
        played[m.p2] += 1
        opponents[m.p1].append(m.p2)
        opponents[m.p2].append(m.p1)

        # Credit the result. `won` mirrors `wins` but only for real (non-bye) matches.
        if m.result == "P1":
            wins[m.p1] += 1
            won[m.p1] += 1
            losses[m.p2] += 1
        elif m.result == "P2":
            wins[m.p2] += 1
            won[m.p2] += 1
            losses[m.p1] += 1
        else:  # "TIE"
            ties[m.p1] += 1
            ties[m.p2] += 1

    # Every player appears as a key in `opponents` (see the bye note above).
    players = list(opponents)

    # ---- Pass 2a: win% per player ----
    # won / played, or 0.0 if they never played a real match (avoids dividing by zero).
    # Then max(..., 0.25) applies the floor: nobody's win% counts as lower than 25%.
    win_pct = {p: max(won[p] / played[p] if played[p] else 0.0, 0.25) for p in players}

    # ---- Pass 2b: OWP = average of opponents' win% ----
    # fmean() is a fast float mean. It raises on an empty input, so guard with
    # `if opponents[p] else 0.0` for players who only had a bye.
    owp = {p: fmean(win_pct[o] for o in opponents[p]) if opponents[p] else 0.0 for p in players}

    # ---- Pass 3: build the rows (OOWP computed inline) ----
    out = [
        Standing(
            id=p,
            points=3 * wins[p] + ties[p],   # win = 3, tie = 1, loss = 0
            wins=wins[p], losses=losses[p], ties=ties[p],
            owp=owp[p],
            # OOWP = average of my opponents' OWP — same shape as OWP, one level deeper.
            oowp=fmean(owp[o] for o in opponents[p]) if opponents[p] else 0.0,
        )
        for p in players
    ]

    # Sort in place. Negate the numbers we want DESCENDING; leave id ascending as the
    # final deterministic tiebreak. Tuples compare left to right, so this is exactly
    # "points, then OWP, then OOWP, then id".
    out.sort(key=lambda s: (-s.points, -s.owp, -s.oowp, s.id))
    return out
