# 02 — Standings with OWP / OOWP tiebreakers

**Pattern:** aggregation over a graph of results, multi-key sort · **Domain:** live standings

Play! Pokémon ranks Swiss standings by match points, then **Opponents' Win Percentage
(OWP)**, then **Opponents' Opponents' Win Percentage (OOWP)**. This is a simplified model of
that — check the official Play! Pokémon Tournament Rules Handbook for the exact rules if
you want to talk about them in the interview.

## Task

Implement `Compute(matches []Match) []Standing`.

- `Match{P1, P2 string, Result Result}` with `Result` one of `P1Win`, `P2Win`, `Tie`.
- A **bye** is `Match{P1: "X", P2: "", Result: P1Win}`.

Definitions:
- Points: win = 3, tie = 1, loss = 0. A bye is a win (3 points, counts in `Wins`).
- **Win%** of a player = wins / (wins + losses + ties) **over non-bye matches only**,
  floored at **0.25**. A player with no non-bye matches has win% 0.25.
- **OWP** = mean win% of the player's opponents (byes are not opponents). 0 if no opponents.
- **OOWP** = mean OWP of the player's opponents. 0 if no opponents.
- Sort by Points desc, OWP desc, OOWP desc, ID asc.

## Example

```
R1: A beat B, C beat D
R2: A beat C, D beat B
→ A 6pts (OWP .375), C 3pts (OWP .75), D 3pts (OWP .375), B 0pts
   C beats D on OWP: C lost to the undefeated player, D lost to nobody strong.
```

## Talking points
- Why the 25% floor exists (stop players who drop early from tanking their opponents).
- Live standings at scale: recompute after each round is O(players × rounds) — cheap. Where
  does this run? (Lambda on "round results submitted" event → write to a read model.)
- Floating point: compare with an epsilon or store as rationals if exact ties matter.
