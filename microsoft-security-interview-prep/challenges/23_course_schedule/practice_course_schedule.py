"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/23_course_schedule -v` to check yourself, or
`PRACTICE=0 pytest challenges/23_course_schedule -v` to see the reference
solution's tests pass instead.
"""
from collections import defaultdict, deque
from typing import List


def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    graph = defaultdict(list)
    schedule = [0]*num_courses

    for a, b in prerequisites:
        graph[b].append(a)
        schedule[a] += 1
    print(graph)

    queue = deque(course for course in range(num_courses) if schedule[course] == 0)
    finished = 0

    while queue:
        course = queue.pop()
        finished += 1
        for dependent in graph[course]:
            schedule[dependent] -=1
            if schedule[dependent] == 0:
                queue.append(dependent)
    return finished == num_courses
