# 07 — Dependency Graph Cycle Detector (Topological Sort)

**Theme:** graphs — and a real security use case: build/dependency graphs (think a
software bill of materials, or a package manager's install graph) should never contain
a cycle; a cycle usually means a broken/malicious manifest or a build that can never
resolve.

## Problem

The graph is given as an adjacency dict: `graph[node] = [nodes that `node` depends on]`
(a directed edge `node -> dep` means "node depends on dep, so dep must come first").

```python
def has_cycle(graph: Dict[str, List[str]]) -> bool:
    """True if the dependency graph contains a cycle."""

def topological_order(graph: Dict[str, List[str]]) -> List[str]:
    """Return a valid build order (dependencies before dependents).
    Raise CycleError if the graph has a cycle."""
```

`CycleError` is provided:

```python
class CycleError(ValueError):
    ...
```

## Constraints

- The graph may reference nodes only as values (a dependency that's never a top-level
  key) — treat those as leaf nodes with no further dependencies.
- Disconnected components are fine — must all appear in the output.
- A **self-loop** (`graph["a"] = ["a"]`) counts as a cycle.
- `topological_order`'s output need not be unique, but for every edge `node -> dep`,
  `dep` must appear **before** `node` in the result. Tests will check this property
  (and full coverage of nodes), not an exact ordering.

## Hints

- DFS with a three-color (white/gray/black) visited state is the classic approach for
  cycle detection — gray = "currently on the recursion stack", revisiting a gray node
  means you found a back-edge (a cycle). Don't just use a single visited-set; that only
  detects "already fully processed," not "currently in progress" (which is what a cycle
  actually looks like).

## Run

```bash
pytest challenges/07_dependency_cycle_detector -v
```
