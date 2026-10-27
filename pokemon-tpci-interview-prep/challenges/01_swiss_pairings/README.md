# 01 — Swiss pairings

**Pattern:** sort + backtracking · **Domain:** Play! Pokémon tournaments (TOM / Pokémon Event Manager)

Every Play! Pokémon TCG/VGC event runs Swiss rounds before top cut. Each round, players
are paired against others with the same (or nearest) record, nobody plays the same
opponent twice, and with an odd player count someone gets a bye.

## Task

Implement `Pair(players []Player, history []Match) Round`.

- `Player{ID string, Points int, HadBye bool}` — match points so far (win=3, tie=1, loss=0).
- `history` — every pairing already played (order of `A`/`B` doesn't matter).
- Return `Round{Pairings []Match, Bye string}`.

Rules:

1. Rank players by `Points` desc, then `ID` asc (deterministic).
2. If the count is odd, the bye goes to the **lowest-ranked player who has not had a bye**
   (if everyone has, the lowest-ranked player). Remove them before pairing.
3. Pair top-down: the highest remaining player is paired with the highest-ranked remaining
   player they **have not played**. If that choice makes the rest of the round impossible
   without a rematch, backtrack and try the next candidate.
4. If no rematch-free round exists at all, fall back to plain top-down pairing (rematches
   allowed) — a round must always be produced.
5. In each `Match`, `A` is the higher-ranked player. Pairings are listed in pairing order.

## Examples

```
players A(6) B(3) C(3) D(0), no history      → A-B, C-D
same players, A already played B             → A-C, B-D
same players, C already played D             → A-C, B-D   (A-B would force C-D rematch → backtrack)
```

## Talking points

- Complexity: backtracking is exponential worst case; real tools bound it (pair within
  point brackets, "float" players down). Mention that if asked to scale to 2,000-player Worlds.
- Why deterministic ordering matters: reproducibility, judge appeals, testability.
- Follow-up they might ask: avoid pairing players from the same store/family early rounds.
