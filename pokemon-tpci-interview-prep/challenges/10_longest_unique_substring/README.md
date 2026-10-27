# 10 — Longest substring without repeating characters

**Pattern:** sliding window + last-seen map · **Classic** (very common in Karat/HackerRank screens)

## Task
`LongestUnique(s string) int` — length of the longest substring with no repeated characters.
Treat the input as **runes**, not bytes (`"ポケモン"` → 4; `"ピカピカ"` → 2).

## Talking points
- O(n) time, O(alphabet) space. Explain why `left = max(left, last[ch]+1)` needs the `max`.
- Go strings are UTF-8 bytes; `range` over a string yields runes and byte offsets — use a
  rune index counter, or convert to `[]rune` first.
