//go:build solution

// Schedule intervals — reference solution.
//
// The shared trick: SORT BY START TIME. After that, anything overlapping the current
// interval must be right next to it, so a single left-to-right sweep is enough.
// Intervals are half-open [Start, End): [0,30) and [30,60) touch but don't overlap.
package intervals

import (
	"cmp"
	"slices"
)

// sorted returns a sorted COPY, so callers' slices are never reordered.
func sorted(iv []Interval) []Interval {
	s := slices.Clone(iv)
	// cmp.Compare returns -1, 0 or +1: exactly the shape SortFunc's comparator wants.
	slices.SortFunc(s, func(a, b Interval) int { return cmp.Compare(a.Start, b.Start) })
	return s
}

func Merge(iv []Interval) []Interval {
	var out []Interval // nil slice; append works on it
	for _, cur := range sorted(iv) {
		// `if n := len(out); n > 0 && ...` declares n scoped to this if statement.
		// out[n-1] is the last merged interval. If cur starts at or before it ends
		// (`<=`, so touching intervals merge too), extend it instead of appending.
		if n := len(out); n > 0 && cur.Start <= out[n-1].End {
			// max handles containment: [1,10) then [2,3) must stay [1,10).
			// out[n-1].End = ... writes into the slice element itself. That works because
			// indexing a slice gives you an addressable element, not a copy.
			out[n-1].End = max(out[n-1].End, cur.End)
			continue
		}
		out = append(out, cur) // no overlap: start a new merged interval
	}
	return out
}

func HasConflict(iv []Interval) bool {
	s := sorted(iv)
	// Once sorted, only NEIGHBORS need comparing: if i doesn't overlap i-1, it can't
	// overlap anything earlier. Strict `<` because touching isn't a conflict.
	for i := 1; i < len(s); i++ {
		if s[i].Start < s[i-1].End {
			return true
		}
	}
	return false
}

// MinTables uses the "two sorted arrays" sweep (an alternative to a heap of end times):
// walk the start times in order. Before seating each new match, free every table whose
// match has already ended. The peak number of tables in use is the answer.
func MinTables(iv []Interval) int {
	starts := make([]int, len(iv))
	ends := make([]int, len(iv))
	for i, x := range iv {
		starts[i], ends[i] = x.Start, x.End // multiple assignment in one line
	}
	slices.Sort(starts)
	slices.Sort(ends)

	// inUse: tables busy right now. best: the peak. e: index of the next end to process.
	inUse, best, e := 0, 0, 0
	for _, s := range starts {
		// Free tables for every match that ended at or before this start.
		// `<=` lets a table freed at 10 be reused by a match starting at 10.
		for e < len(ends) && ends[e] <= s {
			inUse--
			e++
		}
		inUse++ // seat this match
		best = max(best, inUse)
	}
	return best
}
