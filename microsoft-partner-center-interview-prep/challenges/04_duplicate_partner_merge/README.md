# 04 — Duplicate Partner Merge (Union-Find)

**Theme:** onboarding integrity. If one organization enrolls several times under
different accounts, it can stack program incentives or slip past a previous
rejection. To catch this, enrollment records that share *any* identifier (domain,
tax ID, verified email) are grouped as the same organization. The link is transitive:
if A shares a domain with B, and B shares a tax ID with C, then A, B and C are one
org. This is LeetCode 721 *Accounts Merge*, which is on Microsoft's company tag.

## Problem

```python
def merge_partner_records(records: List[Tuple[str, List[str]]]) -> List[List[str]]:
    ...
```

Each record is `(record_id, identifiers)`, for example
`("rec-1", ["domain:contoso.com", "tax:US-123"])`.

Return the groups of `record_id`s that belong to the same organization:

- Sort the ids inside each group.
- Sort the groups by their first id.
- A record that shares nothing with any other record is a group of one.

## Constraints

- **Normalize identifiers** before comparing them: strip surrounding whitespace and
  compare case-insensitively. `"Domain:Contoso.com "` and `"domain:contoso.com"` are
  the same identifier.
- Ignore identifiers that are empty after stripping. An empty string doesn't link
  anything.
- `record_id`s are unique.
- Up to 50k records. The tests include a **chain of 20,000 records** where each record
  links only to the next. A recursive DFS or recursive `find` will hit Python's
  recursion limit (1,000) on that input.

## Hints

- Union-find (disjoint set union) over record indices. Map each normalized identifier
  to the first record that had it. When a later record has the same identifier,
  `union` the two records.
- Write `find` **iteratively**, with path compression. Use union by size so the
  trees stay shallow.
- You can do it with BFS over an identifier ↔ record graph instead. Mention it, but
  union-find is the cleaner answer here and it's what interviewers expect.

## Run

```bash
pytest challenges/04_duplicate_partner_merge -v
```
