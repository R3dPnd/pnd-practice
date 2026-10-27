# 01 — Swiss pairings (Python)

Full rules, examples, and talking points: [`../../../challenges/01_swiss_pairings/README.md`](../../../challenges/01_swiss_pairings/README.md).

```python
pair(players: list[Player], history: list[tuple[str, str]]) -> Round
# Player(id, points, had_bye=False); Round(pairings: list[tuple[str, str]], bye: str | None)
```
Rank by points desc then id asc; odd count → bye to lowest-ranked player without one;
pair top-down avoiding rematches with backtracking; fall back to plain top-down if impossible.
