//go:build solution

// The line above is a BUILD TAG: this file is only compiled when you run
// `go test -tags solution`. practice.go has the opposite tag (!solution), so exactly one
// of the two Pair functions exists in any given build.

// Swiss pairings — reference solution.
//
// Big picture:
//  1. Sort players into standings order (most points first).
//  2. If the player count is odd, hand out a bye and remove that player.
//  3. Pair top-down, never pairing two players who already played each other. If a greedy
//     choice paints us into a corner, BACKTRACK and try the next opponent.
//  4. If no rematch-free round exists, give up on that rule and pair top-down.
package swiss

import "sort"

func Pair(players []Player, history []Match) Round {
	// Copy the input before sorting. append([]Player(nil), players...) builds a NEW
	// slice with the same elements. sort.Slice sorts in place, and without the copy we
	// would reorder the caller's slice (a test checks that we don't).
	ranked := append([]Player(nil), players...)

	// sort.Slice takes a "less" function: return true if element i should come BEFORE
	// element j. More points first, then ID alphabetically for a deterministic order.
	sort.Slice(ranked, func(i, j int) bool {
		if ranked[i].Points != ranked[j].Points {
			return ranked[i].Points > ranked[j].Points
		}
		return ranked[i].ID < ranked[j].ID
	})

	// The zero value of a struct is ready to use: empty Pairings (nil slice) and Bye "".
	var round Round

	// ---- Step 2: the bye ----
	if len(ranked)%2 == 1 {
		// Default: the lowest-ranked player (used if everyone has already had a bye).
		byeIdx := len(ranked) - 1
		// Walk upward from the bottom and stop at the first player without a bye.
		for i := len(ranked) - 1; i >= 0; i-- {
			if !ranked[i].HadBye {
				byeIdx = i
				break
			}
		}
		round.Bye = ranked[byeIdx].ID
		// Remove index byeIdx: glue the part before it to the part after it.
		// This is safe because `ranked` is our own copy.
		ranked = append(ranked[:byeIdx], ranked[byeIdx+1:]...)
	}

	// ---- A fast "have these two played?" lookup ----
	// Go has no built-in set type, so a map[K]bool is the usual stand-in. The key is a
	// fixed-size ARRAY [2]string (arrays are comparable, so they can be map keys; slices
	// can't). Insert both orders so the lookup works whichever way round we ask.
	played := map[[2]string]bool{}
	for _, m := range history {
		played[[2]string{m.A, m.B}] = true
		played[[2]string{m.B, m.A}] = true
	}

	// From here on we only need the IDs, already in ranked order.
	ids := make([]string, len(ranked))
	for i, p := range ranked {
		ids[i] = p.ID
	}

	// Try for a rematch-free round.
	if pairs, ok := backtrack(ids, played); ok {
		round.Pairings = pairs
		return round
	}

	// ---- Step 4: fallback ----
	// Impossible without rematches: pair neighbors (0 vs 1, 2 vs 3, ...).
	for i := 0; i+1 < len(ids); i += 2 {
		round.Pairings = append(round.Pairings, Match{ids[i], ids[i+1]})
	}
	return round
}

// backtrack pairs ids[0] with the best-ranked legal opponent, recursing on the rest.
// It returns (pairings, true) on success, or (nil, false) if no rematch-free pairing of
// `ids` exists. Returning (value, ok) is the idiomatic Go way to signal "might fail".
func backtrack(ids []string, played map[[2]string]bool) ([]Match, bool) {
	// Base case: nobody left to pair. That's success, with zero more pairings.
	if len(ids) == 0 {
		return nil, true
	}

	// The highest-ranked unpaired player always gets paired next.
	top := ids[0]

	// Try opponents in ranked order, best candidate first.
	for j := 1; j < len(ids); j++ {
		if played[[2]string{top, ids[j]}] {
			continue // already played each other; try the next candidate
		}

		// Build the list of everyone still unpaired: ids[1:j] (between top and the
		// opponent) plus ids[j+1:] (after the opponent).
		// Use a FRESH slice. Appending to ids[1:j] directly could overwrite ids[j] in
		// the shared backing array, which would corrupt this loop's later iterations.
		rest := make([]string, 0, len(ids)-2)
		rest = append(rest, ids[1:j]...)
		rest = append(rest, ids[j+1:]...)

		// If the rest of the round works out, this choice is good: prepend it.
		if tail, ok := backtrack(rest, played); ok {
			return append([]Match{{top, ids[j]}}, tail...), true
		}
		// Otherwise fall through and try the next opponent. That's the "backtrack".
	}

	// No opponent for `top` leads to a complete round.
	return nil, false
}
