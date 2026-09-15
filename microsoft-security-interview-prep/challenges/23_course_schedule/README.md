# 23 — Course Schedule

**Theme:** graph, topological sort. Same underlying pattern as
`07_dependency_cycle_detector`, but the top-level `README.md`'s Field notes flag this
exact LeetCode phrasing as **the most literally-reported Microsoft coding question**
among the "extra reps" — worth doing both, since the input shape differs (adjacency
dict vs. an edge list over integer course IDs) and this version is solved here with
**Kahn's BFS-based topological sort** instead of `07`'s DFS three-color approach, for
pattern variety.

## Problem

```python
def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """There are num_courses labeled 0..num_courses-1. prerequisites[i] = [a, b]
    means you must take course b before course a. Return True if it's possible
    to finish all courses (i.e. there is no cyclic dependency), False otherwise."""
```

## Examples

```
can_finish(2, [[1, 0]])                 -> True   (take 0, then 1)
can_finish(2, [[1, 0], [0, 1]])         -> False  (0 needs 1, 1 needs 0 — cycle)
can_finish(3, [])                       -> True   (no prerequisites at all)
can_finish(1, [[0, 0]])                 -> False  (a self-loop is a cycle)
```

## Constraints

- `num_courses` may be 0 (trivially finishable) or courses may have no prerequisites
  at all (also trivially finishable).
- Courses with no dependency relationship to each other (disconnected components) are
  fine — every course still needs to end up "finished."

## Hints

- **Kahn's algorithm**: build an adjacency list (`b -> a` for each `[a, b]`) and an
  in-degree count per course. Start a queue with every course that has in-degree 0
  (nothing blocking it). Repeatedly pop a course, "finish" it, and decrement the
  in-degree of everything that depended on it — if any of those drop to 0, they're now
  unblocked, enqueue them. If you finish fewer courses than `num_courses` total, the
  remainder are stuck in a cycle.
- This is a **breadth-first** topological sort — contrast with `07`'s depth-first,
  three-color approach. Both are valid; be ready to explain either, since an
  interviewer may ask "is there another way to do this."

## Run

```bash
pytest challenges/23_course_schedule -v
```
