package venue

import "testing"

func TestShortestPath(t *testing.T) {
	cases := []struct {
		name string
		grid []string
		want int
	}{
		{"straight", []string{"S..E"}, 3},
		{"around wall", []string{
			"S.#.",
			"..#E",
			"....",
		}, 6},
		{"blocked", []string{
			"S#.",
			"##E",
		}, -1},
		{"same row detour", []string{
			"S#E",
			"...",
		}, 4},
		{"no exit", []string{"S.."}, -1},
	}
	for _, c := range cases {
		if got := ShortestPath(c.grid); got != c.want {
			t.Errorf("%s: got %d want %d", c.name, got, c.want)
		}
	}
}
