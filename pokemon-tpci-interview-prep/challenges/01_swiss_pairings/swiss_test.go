package swiss

import (
	"reflect"
	"testing"
)

func four() []Player {
	// Deliberately unsorted input.
	return []Player{{ID: "D", Points: 0}, {ID: "B", Points: 3}, {ID: "A", Points: 6}, {ID: "C", Points: 3}}
}

func TestNoHistoryPairsTopDown(t *testing.T) {
	got := Pair(four(), nil)
	want := Round{Pairings: []Match{{"A", "B"}, {"C", "D"}}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %+v want %+v", got, want)
	}
}

func TestAvoidsRematch(t *testing.T) {
	got := Pair(four(), []Match{{"B", "A"}})
	want := Round{Pairings: []Match{{"A", "C"}, {"B", "D"}}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %+v want %+v", got, want)
	}
}

func TestBacktracksWhenGreedyForcesRematch(t *testing.T) {
	got := Pair(four(), []Match{{"C", "D"}})
	want := Round{Pairings: []Match{{"A", "C"}, {"B", "D"}}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %+v want %+v", got, want)
	}
}

func TestOddCountByeGoesToLowestWithoutBye(t *testing.T) {
	players := []Player{
		{ID: "A", Points: 6}, {ID: "B", Points: 3}, {ID: "C", Points: 3},
		{ID: "D", Points: 0}, {ID: "E", Points: 0, HadBye: true},
	}
	got := Pair(players, nil)
	if got.Bye != "D" {
		t.Fatalf("bye = %q, want D (E already had one)", got.Bye)
	}
	want := []Match{{"A", "B"}, {"C", "E"}}
	if !reflect.DeepEqual(got.Pairings, want) {
		t.Fatalf("pairings %+v want %+v", got.Pairings, want)
	}
}

func TestEveryoneHadByeFallsBackToLowest(t *testing.T) {
	players := []Player{{ID: "A", Points: 3, HadBye: true}, {ID: "B", HadBye: true}, {ID: "C", HadBye: true}}
	if got := Pair(players, nil); got.Bye != "C" {
		t.Fatalf("bye = %q, want C", got.Bye)
	}
}

func TestImpossibleRoundStillPairsEveryone(t *testing.T) {
	all := []Match{{"A", "B"}, {"A", "C"}, {"A", "D"}, {"B", "C"}, {"B", "D"}, {"C", "D"}}
	got := Pair(four(), all)
	want := Round{Pairings: []Match{{"A", "B"}, {"C", "D"}}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %+v want %+v", got, want)
	}
}

func TestDoesNotMutateInput(t *testing.T) {
	in := four()
	Pair(in, nil)
	if in[0].ID != "D" {
		t.Fatal("Pair must not reorder the caller's slice")
	}
}
