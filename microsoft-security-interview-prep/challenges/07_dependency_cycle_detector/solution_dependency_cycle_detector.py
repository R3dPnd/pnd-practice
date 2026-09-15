"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. The graph may reference nodes only as *values* (a leaf dependency that's never a
   top-level key) — `_all_nodes` collects the full node set from both keys and
   values first, so those leaves aren't silently skipped.
2. Cycle detection needs to distinguish "fully explored, definitely safe" from
   "currently being explored on *this* DFS path" — a single visited set can't make
   that distinction, which is why this uses three colors: white (untouched), gray
   (on the current recursion stack), black (fully done, safe).
3. Hitting a **gray** node during DFS means you've looped back onto your own current
   path — that's exactly what a cycle (a back-edge) looks like. Hitting a **black**
   node just means "already verified fine elsewhere," not a cycle.
4. `topological_order` reuses the identical DFS, appending each node to the output
   only *after* all of its dependencies have been recursed into (post-order) — that
   ordering guarantees every dependency appears before the thing that depends on it.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why not just use one visited set instead of three colors?" — one set can tell you
  "have I ever seen this node," but not "is it currently in-progress on my current
  path" — and that second fact is the entire definition of a cycle. Two colors
  (visited / not) cannot distinguish a safe re-visit from a cycle; three can.
- "Is there another way to detect a cycle / do a topological sort?" — yes, Kahn's
  algorithm (BFS via in-degree counting) — see `23_course_schedule` for the same
  underlying problem solved that way. Be ready to explain both.
- "What's the real-world tie-in for a Security org specifically?" — this is exactly
  the shape of validating a software dependency graph / bill of materials — a cycle
  usually signals a broken or even maliciously crafted manifest that can never
  actually resolve/build.
- "What's the time complexity?" — O(V + E): every node and every edge is visited
  exactly once across the whole DFS.
"""
from typing import Dict, List


class CycleError(ValueError):
    pass


_WHITE, _GRAY, _BLACK = 0, 1, 2


def _all_nodes(graph: Dict[str, List[str]]):
    nodes = set(graph.keys())
    for deps in graph.values():
        nodes.update(deps)
    return nodes


def has_cycle(graph: Dict[str, List[str]]) -> bool:
    color = {node: _WHITE for node in _all_nodes(graph)}

    def visit(node: str) -> bool:
        color[node] = _GRAY
        for dep in graph.get(node, []):
            if color[dep] == _GRAY:
                return True
            if color[dep] == _WHITE and visit(dep):
                return True
        color[node] = _BLACK
        return False

    for node in list(color):
        if color[node] == _WHITE:
            if visit(node):
                return True
    return False


def topological_order(graph: Dict[str, List[str]]) -> List[str]:
    color = {node: _WHITE for node in _all_nodes(graph)}
    order: List[str] = []

    def visit(node: str) -> None:
        color[node] = _GRAY
        for dep in graph.get(node, []):
            if color[dep] == _GRAY:
                raise CycleError(f"cycle detected involving {node!r} -> {dep!r}")
            if color[dep] == _WHITE:
                visit(dep)
        color[node] = _BLACK
        order.append(node)  # dependencies are already appended before node

    for node in list(color):
        if color[node] == _WHITE:
            visit(node)

    return order
