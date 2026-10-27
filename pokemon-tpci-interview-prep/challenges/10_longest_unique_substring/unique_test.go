package unique

import "testing"

func TestLongestUnique(t *testing.T) {
	cases := map[string]int{
		"":         0,
		"abcabcbb": 3,
		"bbbbb":    1,
		"pwwkew":   3,
		"abba":     2,
		"ポケモン":     4,
		"ピカピカ":     2,
	}
	for in, want := range cases {
		if got := LongestUnique(in); got != want {
			t.Errorf("LongestUnique(%q) = %d want %d", in, got, want)
		}
	}
}
