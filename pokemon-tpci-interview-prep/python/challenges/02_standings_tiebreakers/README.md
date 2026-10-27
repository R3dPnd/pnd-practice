# 02 — Standings with OWP / OOWP tiebreakers (Python)

Full rules and talking points: [`../../../challenges/02_standings_tiebreakers/README.md`](../../../challenges/02_standings_tiebreakers/README.md).

```python
compute(matches: list[Match]) -> list[Standing]
# Match(p1, p2, result) with result in {"P1", "P2", "TIE"}; a bye is Match("X", None, "P1")
# Standing(id, points, wins, losses, ties, owp, oowp)
```
Points W=3/T=1/L=0 (bye = win). Win% over non-bye matches, floored at 0.25.
OWP = mean opponents' win%; OOWP = mean opponents' OWP. Sort points, OWP, OOWP desc, then id asc.
