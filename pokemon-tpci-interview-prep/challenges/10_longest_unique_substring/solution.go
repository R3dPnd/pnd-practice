//go:build solution

// Longest substring without repeating characters — reference solution (sliding window).
//
// Keep a window [left, i] with no duplicates. Advance i one character at a time. If the
// new character already appears INSIDE the window, jump left to just past its earlier
// occurrence. Track the widest window seen. O(n) time.
package unique

func LongestUnique(s string) int {
	// rune → index where we LAST saw it.
	last := map[rune]int{}
	best, left := 0, 0

	// Why []rune(s)? Go strings are UTF-8 BYTES. "ポケモン" is 12 bytes but 4 characters.
	// Converting to []rune gives one element per character, so i counts characters.
	// (Ranging over the string directly would also yield runes, but i would be a BYTE
	// offset, which gives wrong lengths for multi-byte text.)
	for i, ch := range []rune(s) {
		if j, ok := last[ch]; ok {
			// Seen before. Move left past that occurrence, but never BACKWARDS: if the
			// old occurrence is already left of the window, max keeps left where it is.
			// Example: "abba". At the final 'a', left is 2 and last['a'] is 0, so
			// left = max(2, 1) = 2.
			left = max(left, j+1)
		}
		last[ch] = i
		best = max(best, i-left+1) // current window length
	}
	return best
}
