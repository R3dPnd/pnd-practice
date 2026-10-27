package leaderboard

import (
	"reflect"
	"testing"
)

func seeded() *Leaderboard {
	lb := NewLeaderboard()
	lb.Award("ash", 200)
	lb.Award("misty", 350)
	lb.Award("brock", 200)
	lb.Award("gary", 500)
	lb.Award("gary", -100) // penalty
	return lb
}

func TestTopK(t *testing.T) {
	got := seeded().TopK(3)
	want := []Entry{{"gary", 400}, {"misty", 350}, {"ash", 200}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %v want %v", got, want)
	}
}

func TestKLargerThanN(t *testing.T) {
	got := seeded().TopK(10)
	if len(got) != 4 || got[3] != (Entry{"brock", 200}) {
		t.Fatalf("got %v", got)
	}
}

func TestTotalsAndEmpty(t *testing.T) {
	lb := seeded()
	if lb.Total("gary") != 400 || lb.Total("nobody") != 0 {
		t.Fatal("bad totals")
	}
	if len(lb.TopK(0)) != 0 || len(NewLeaderboard().TopK(3)) != 0 {
		t.Fatal("expected empty")
	}
}
