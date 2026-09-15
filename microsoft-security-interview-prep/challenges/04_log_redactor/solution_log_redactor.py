"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Break the problem into known secret "shapes" rather than trying to write one
   giant catch-all regex: explicit key=value pairs (`password=...`, `api_key: ...`),
   well-known token formats (`Bearer <token>`, AWS access key IDs), and other
   fixed-format sensitive data (credit card numbers).
2. Write one compiled regex per shape, each independently reviewable and testable,
   instead of one unreadable monolith.
3. Apply the patterns in a fixed pipeline order, substituting a constant
   `[REDACTED]` placeholder — for key=value pairs, keep the key name and separator
   intact so the log's *structure* stays useful for debugging even though the
   *value* is gone.
4. Match key names case-insensitively (`re.IGNORECASE`) since real logs are
   inconsistent about casing (`Password`, `PASSWORD`, `password`).

COMMON INTERVIEWER FOLLOW-UPS:
- "Why not just try to detect any base64/high-entropy string?" — far too many false
  positives (session IDs, hashes you don't care about) and false negatives (a plain
  password isn't high-entropy). Matching known formats and known key names is the
  practical, auditable middle ground actually used in production log scrubbers.
- "How would you add a new secret type?" — add one more compiled pattern and fold it
  into the substitution pipeline; flag that this doesn't scale well as a hand-maintained
  list and should ideally be centralized in one shared library, not copy-pasted
  per service.
- "What about secrets split across multiple log lines or streamed in chunks?" — this
  operates on one complete string; a real streaming log pipeline needs to buffer and
  reassemble lines (or accept the limitation) before this kind of pattern match works.
- "What's the fundamental risk of a regex-based approach?" — false negatives: a
  secret shape you didn't anticipate slips through. The real defense in depth is
  making sure secrets are never logged at the source in the first place — this
  redactor is a safety net, not the primary control.
"""
import re

_KV_KEYS = r"(?:password|passwd|pwd|api_key|apikey|secret|token|access_key)"
_KV_PATTERN = re.compile(
    rf'\b({_KV_KEYS})\b(\s*[:=]\s*)("[^"]*"|\S+)',
    re.IGNORECASE,
)
_BEARER_PATTERN = re.compile(r"\bBearer\s+\S+")
_AWS_KEY_PATTERN = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
_CREDIT_CARD_PATTERN = re.compile(r"\b(?:\d{4}[- ]){3}\d{4}\b|\b\d{16}\b")


def redact(text: str) -> str:
    if not text:
        return text

    result = _BEARER_PATTERN.sub("Bearer [REDACTED]", text)
    result = _AWS_KEY_PATTERN.sub("[REDACTED]", result)
    result = _CREDIT_CARD_PATTERN.sub("[REDACTED]", result)
    result = _KV_PATTERN.sub(lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]", result)
    return result
