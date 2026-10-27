"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Recognize the shape: "same group if linked, transitively" is connected components.
   Say that out loud. Naming the pattern is half the signal.
2. Brute force compares every pair of records for a shared identifier: O(n^2 * k).
   Improve it with a hash map from identifier to the first record that had it, so
   each identifier needs one union instead of comparisons against every record.
3. Union-find: `parent[i]` points toward the group's root. Path compression in
   `find` plus union by size gives near-O(1) amortized operations (inverse Ackermann).
4. Make `find` iterative. Recursion depth on a chain input is O(n) before compression
   kicks in, and Python's default recursion limit is 1000.
5. Collect the groups by root, sort inside each group, then sort the groups.

COMMON INTERVIEWER FOLLOW-UPS:
- "Complexity?" — O(N*K * α(N)) for the unions, where N*K is the total number of
  identifiers. The final sorts add O(N log N). Space is O(N + distinct identifiers).
- "Records stream in continuously?" — union-find is incremental, so keep it in memory
  and union each new record as it arrives. *Splitting* a group (when an identifier was
  wrong and gets removed) is the hard part. Union-find can't undo a union, so you'd
  rebuild that component.
- "One shared identifier like `domain:gmail.com` merges everyone." — real dedupe
  ignores high-cardinality identifiers (an identifier on more than N records isn't
  a signal), or weights identifiers by how strong they are (tax ID > domain). That's a
  product and security judgment call, so raise it unprompted.
- "Is this the fraud decision?" — no. It produces *candidates* for a reviewer or a
  risk model. Auto-blocking on a false merge locks a legitimate partner out of onboarding.
"""
from typing import Dict, List, Tuple


def merge_partner_records(records: List[Tuple[str, List[str]]]) -> List[List[str]]:
    parent = list(range(len(records)))
    size = [1] * len(records)

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    owner: Dict[str, int] = {}
    for i, (_, identifiers) in enumerate(records):
        for raw in identifiers:
            ident = raw.strip().lower()
            if not ident:
                continue
            if ident in owner:
                union(i, owner[ident])
            else:
                owner[ident] = i

    groups: Dict[int, List[str]] = {}
    for i, (record_id, _) in enumerate(records):
        groups.setdefault(find(i), []).append(record_id)

    return sorted(sorted(group) for group in groups.values())
