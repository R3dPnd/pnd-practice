"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution (Kahn's algorithm):
1. Model prerequisites as a directed graph: `prerequisites[i] = [a, b]` becomes an
   edge `b -> a` ("finish b before a"). Track each course's *in-degree* — how many
   unfinished prerequisites are currently blocking it.
2. Any course with in-degree 0 has nothing blocking it right now — seed a queue with
   every such course up front.
3. Repeatedly pop a course from the queue, count it as "finished," and decrement the
   in-degree of everything that listed it as a prerequisite. Any course that drops to
   in-degree 0 as a result just became unblocked — enqueue it too.
4. If every course eventually gets "finished" this way (`finished == num_courses`),
   there's no cycle. If some are left stuck, they (and everything that depends on
   them) never reach in-degree 0 — those are the courses caught in a cycle.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why does 'not all courses finished' prove there's a cycle?" — a course inside a
  cycle is always waiting on another course that's *also* inside that same cycle, so
  none of them can ever be the "first" one processed — none ever reaches in-degree 0,
  so none ever gets enqueued or counted as finished.
- "How does this compare to `07_dependency_cycle_detector`'s approach?" — same
  underlying problem (cycle detection / topological feasibility), solved with the
  opposite traversal strategy: Kahn's BFS via in-degree draining here, versus DFS
  three-color there. Being able to explain both is a stronger signal than knowing
  just one.
- "What's the complexity?" — O(V + E): every course is enqueued/dequeued once, and
  every prerequisite edge is examined exactly once when decrementing in-degrees.
- "How would you return a valid course *order*, not just True/False?" — the order
  courses are dequeued in already **is** a valid topological order — just append
  each to a list instead of only incrementing a counter.
"""
from collections import defaultdict, deque
from typing import List


def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    graph = defaultdict(list)
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque(course for course in range(num_courses) if in_degree[course] == 0)
    finished = 0

    while queue:
        course = queue.popleft()
        finished += 1
        for dependent in graph[course]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    return finished == num_courses
