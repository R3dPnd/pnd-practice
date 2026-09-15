"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. The risk: `user_path` might contain `../` sequences designed to escape `base_dir`
   (classic path traversal, CWE-22).
2. Naive (and wrong) fix: blocklist the substring `".."`. Reject this approach out
   loud — encodings, redundant separators, and platform-specific quirks can bypass a
   textual check, and it doesn't handle the "absolute path" footgun below at all.
3. Robust approach: canonicalize first, then check containment structurally.
   `os.path.abspath` resolves both `base_dir` and the joined candidate path into
   absolute, normalized form (collapsing any `..`/`.`/redundant separators) — then
   `os.path.commonpath` tells you whether the candidate is actually still inside the
   base directory, as a path-structure fact rather than a string pattern.
4. Reject absolute `user_path` values outright *before* joining — `os.path.join`
   silently discards the first argument when the second is absolute
   (`os.path.join("/base", "/etc/passwd") == "/etc/passwd"`), which would otherwise
   let an absolute path bypass containment checking entirely.
5. Reject embedded NUL bytes — some lower-level (C-based) file APIs historically
   truncate a path at the first NUL, which can be used to smuggle a shorter,
   different path than the one that was validated.

COMMON INTERVIEWER FOLLOW-UPS:
- "Why not just check for `..` in the string?" — canonicalize-then-compare handles
  every encoding of "escape the base directory" structurally; a substring check only
  catches the literal pattern you thought to block.
- "What about symlinks that point outside `base_dir`?" — this solution doesn't
  resolve symlinks, and that's a real, known gap. `os.path.realpath` (which follows
  symlinks) would close it — mention this proactively as a limitation.
- "Why explicitly reject absolute paths instead of just letting `abspath`/`commonpath`
  catch it?" — because `os.path.join` drops the base entirely for an absolute second
  argument, so the escape happens *before* the containment check ever runs; you have
  to catch it earlier, not rely on the later check to save you.
- "What's the actual security impact if this check is missing or wrong?" — arbitrary
  file read (or write, if this guards a write path) outside the intended directory —
  a directory-traversal vulnerability, CWE-22.
"""
import os


class PathTraversalError(ValueError):
    pass


def safe_resolve(base_dir: str, user_path: str) -> str:
    if not user_path:
        raise PathTraversalError("user_path must be a non-empty string")
    if "\x00" in user_path:
        raise PathTraversalError("embedded NUL byte in user_path")
    if os.path.isabs(user_path):
        raise PathTraversalError("absolute paths are not allowed")

    base_abs = os.path.abspath(base_dir)
    candidate = os.path.abspath(os.path.join(base_abs, user_path))

    try:
        common = os.path.commonpath([base_abs, candidate])
    except ValueError:
        # e.g. different drives on Windows -> definitely not contained
        raise PathTraversalError("resolved path escapes base_dir")

    if common != base_abs:
        raise PathTraversalError("resolved path escapes base_dir")

    return candidate
