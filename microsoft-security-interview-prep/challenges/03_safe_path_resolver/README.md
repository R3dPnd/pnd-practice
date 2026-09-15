# 03 — Safe Path Resolver (Path Traversal Prevention)

**Theme:** security-minded engineering. This is the exact class of bug behind real CVEs
(e.g. path traversal in file-serving/upload endpoints) — very on-theme for a Security
org coding interview.

## Problem

You're implementing the file-lookup for a service that serves files from a single base
directory (think: a static file server, or "fetch attachment by name"). Write:

```python
def safe_resolve(base_dir: str, user_path: str) -> str:
    """Resolve `user_path` (untrusted, attacker-controlled) relative to `base_dir`
    and return the absolute, normalized path — but ONLY if that path is still
    inside `base_dir`.

    Raises PathTraversalError if the resolved path would escape base_dir, or if
    user_path is otherwise malformed/unsafe.
    """
```

A custom exception is provided for you to raise:

```python
class PathTraversalError(ValueError):
    ...
```

## Cases your resolver must reject

- `../` sequences that climb above `base_dir` (`"../../etc/passwd"`, nested combos like
  `"a/../../b"` that still net-escape).
- An **absolute path** supplied as `user_path` (e.g. `"/etc/passwd"`) — must not be
  allowed to replace `base_dir` entirely (this is the classic bug: naive
  `os.path.join(base_dir, user_path)` lets an absolute `user_path` win outright).
- Embedded NUL bytes (`"file\x00.txt"`) — a classic string-truncation attack against
  C-based filesystem APIs.
- Empty string / `None`.

## Cases that must succeed

- A simple filename: `"report.pdf"`.
- A nested-but-contained relative path: `"subdir/report.pdf"`.
- A path that uses `..` internally but nets out *still inside* `base_dir`, e.g.
  `"subdir/../report.pdf"` (this should resolve to `base_dir/report.pdf`, not be
  rejected just for containing `..`) — reject based on the *final resolved location*,
  not on the mere presence of `..` in the string.

## Hints

- `os.path.normpath` / `pathlib` can normalize `..` sequences without touching the
  filesystem.
- After resolving, compare against `base_dir` using something like
  `os.path.commonpath` (careful with trailing slashes / exact-prefix bugs — e.g.
  `"/base"` is *not* a safe prefix check against `"/basement/evil"`).
- You do not need to handle symlink escapes for this exercise (that requires
  `os.path.realpath` + filesystem access) — normalization-based traversal is the focus.

## Run

```bash
pytest challenges/03_safe_path_resolver -v
```
