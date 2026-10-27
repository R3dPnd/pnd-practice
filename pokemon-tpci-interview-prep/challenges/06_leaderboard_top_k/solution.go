//go:build solution

// Championship Points leaderboard (top-K) — reference solution.
//
// Big picture:
//   - Award/Total are a map of running totals: O(1).
//   - TopK keeps a MIN-heap of size k holding the best k players seen so far. The root
//     (index 0) is the WORST of those k, so a newcomer only has to beat the root to get
//     in. That's O(n log k) instead of O(n log n) to sort everyone.
package leaderboard

import (
	"container/heap"
	"slices"
)

type Leaderboard struct {
	totals map[string]int
}

func NewLeaderboard() *Leaderboard { return &Leaderboard{totals: map[string]int{}} }

// A missing key reads as 0, so += works the first time too. Negative points subtract.
func (l *Leaderboard) Award(id string, points int) { l.totals[id] += points }

func (l *Leaderboard) Total(id string) int { return l.totals[id] } // unknown player → 0

// better reports whether a ranks above b: more points, or the same points and an
// alphabetically earlier ID.
func better(a, b Entry) bool {
	if a.Points != b.Points {
		return a.Points > b.Points
	}
	return a.ID < b.ID
}

// minHeap keeps the worst of the current top-k at index 0.
//
// container/heap works on any type that implements heap.Interface:
// Len, Less, Swap (sort.Interface) plus Push and Pop. You implement those five methods,
// then call heap.Push / heap.Pop / heap.Fix, which keep the heap property for you.
type minHeap []Entry

func (h minHeap) Len() int { return len(h) }

// Less(i, j) decides what sits at the root. "i is less than j" here means "i ranks
// WORSE than j", i.e. j is better than i. So the worst entry floats to the top.
func (h minHeap) Less(i, j int) bool { return better(h[j], h[i]) }
func (h minHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

// Push and Pop use POINTER receivers (*minHeap) because they change the slice's length.
// They're called by the heap package; don't call them directly (use heap.Push/heap.Pop).
func (h *minHeap) Push(x any) { *h = append(*h, x.(Entry)) }
func (h *minHeap) Pop() any {
	old := *h
	x := old[len(old)-1]  // heap.Pop has already swapped the root to the end
	*h = old[:len(old)-1] // shrink by one
	return x
}

func (l *Leaderboard) TopK(k int) []Entry {
	if k <= 0 {
		return nil
	}
	h := &minHeap{}
	for id, pts := range l.totals {
		e := Entry{id, pts}
		if h.Len() < k {
			// Fewer than k collected so far: everyone gets in.
			heap.Push(h, e)
		} else if better(e, (*h)[0]) {
			// Full, and the newcomer beats the current worst: overwrite the root, then
			// heap.Fix(h, 0) sifts it down to its correct place. That's O(log k), and
			// cheaper than a Pop followed by a Push.
			(*h)[0] = e
			heap.Fix(h, 0)
		}
		// Otherwise the newcomer can't make the top k; skip them.
	}

	// The heap is only partially ordered, so sort the survivors best-first.
	// []Entry(*h) converts the named type back to a plain slice (same memory).
	out := []Entry(*h)
	// SortFunc's comparator returns negative if a comes before b, positive if after.
	// Two entries are never equal here (IDs are unique), so -1 or 1 is enough.
	slices.SortFunc(out, func(a, b Entry) int {
		if better(a, b) {
			return -1
		}
		return 1
	})
	return out
}
