package standings

import (
	"math"
	"testing"
)

func near(a, b float64) bool { return math.Abs(a-b) < 1e-9 }

func TestOWPBreaksPointTie(t *testing.T) {
	got := Compute([]Match{
		{"A", "B", P1Win}, {"C", "D", P1Win},
		{"A", "C", P1Win}, {"D", "B", P1Win},
	})
	order := []string{"A", "C", "D", "B"}
	if len(got) != 4 {
		t.Fatalf("got %d standings", len(got))
	}
	for i, id := range order {
		if got[i].ID != id {
			t.Fatalf("position %d = %s, want %s (full: %+v)", i, got[i].ID, id, got)
		}
	}
	want := map[string][2]float64{
		"A": {0.375, 0.75}, "B": {0.75, 0.375},
		"C": {0.75, 0.375}, "D": {0.375, 0.75},
	}
	for _, s := range got {
		w := want[s.ID]
		if !near(s.OWP, w[0]) || !near(s.OOWP, w[1]) {
			t.Errorf("%s OWP/OOWP = %v/%v, want %v/%v", s.ID, s.OWP, s.OOWP, w[0], w[1])
		}
	}
	if got[0].Points != 6 || got[0].Wins != 2 || got[3].Losses != 2 {
		t.Errorf("bad records: %+v", got)
	}
}

func TestByeIsWinButNotOpponent(t *testing.T) {
	got := Compute([]Match{{"A", "", P1Win}})
	if len(got) != 1 {
		t.Fatalf("bye must not create a player for the empty ID: %+v", got)
	}
	s := got[0]
	if s.Points != 3 || s.Wins != 1 || s.OWP != 0 || s.OOWP != 0 {
		t.Fatalf("got %+v", s)
	}
}

func TestTiesAndFloor(t *testing.T) {
	// A ties B. B loses to C. A's only opponent B has 0 wins in 2 → floored to 0.25.
	got := Compute([]Match{{"A", "B", Tie}, {"C", "B", P1Win}})
	byID := map[string]Standing{}
	for _, s := range got {
		byID[s.ID] = s
	}
	if byID["A"].Points != 1 || byID["B"].Points != 1 || byID["C"].Points != 3 {
		t.Fatalf("points wrong: %+v", got)
	}
	if !near(byID["A"].OWP, 0.25) {
		t.Errorf("A OWP = %v, want 0.25 (floor)", byID["A"].OWP)
	}
	// B's opponents: A (0 wins/1 → .25), C (1/1 → 1.0) → .625
	if !near(byID["B"].OWP, 0.625) {
		t.Errorf("B OWP = %v, want 0.625", byID["B"].OWP)
	}
	// A and B both 1pt; B has higher OWP so ranks above A.
	if got[1].ID != "B" || got[2].ID != "A" {
		t.Errorf("order = %s,%s,%s want C,B,A", got[0].ID, got[1].ID, got[2].ID)
	}
}
