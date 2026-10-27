package intervals

import (
	"reflect"
	"testing"
)

func TestMerge(t *testing.T) {
	in := []Interval{{8, 10}, {1, 3}, {2, 6}, {15, 18}, {6, 7}}
	want := []Interval{{1, 7}, {8, 10}, {15, 18}}
	if got := Merge(in); !reflect.DeepEqual(got, want) {
		t.Fatalf("got %v want %v", got, want)
	}
	if in[0] != (Interval{8, 10}) {
		t.Fatal("input mutated")
	}
	if got := Merge(nil); len(got) != 0 {
		t.Fatalf("empty: %v", got)
	}
	if got := Merge([]Interval{{1, 10}, {2, 3}}); !reflect.DeepEqual(got, []Interval{{1, 10}}) {
		t.Fatalf("contained: %v", got)
	}
}

func TestHasConflict(t *testing.T) {
	if HasConflict([]Interval{{0, 30}, {30, 60}, {60, 90}}) {
		t.Fatal("back-to-back is not a conflict")
	}
	if !HasConflict([]Interval{{60, 90}, {0, 30}, {20, 40}}) {
		t.Fatal("expected conflict")
	}
}

func TestMinTables(t *testing.T) {
	cases := []struct {
		in   []Interval
		want int
	}{
		{nil, 0},
		{[]Interval{{0, 30}, {5, 10}, {15, 20}}, 2},
		{[]Interval{{0, 10}, {10, 20}}, 1},
		{[]Interval{{1, 5}, {2, 6}, {3, 7}, {6, 8}}, 3},
	}
	for _, c := range cases {
		if got := MinTables(c.in); got != c.want {
			t.Errorf("MinTables(%v) = %d want %d", c.in, got, c.want)
		}
	}
}
