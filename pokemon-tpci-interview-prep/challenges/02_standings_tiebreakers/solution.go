//go:build solution

// Standings with OWP / OOWP tiebreakers — reference solution.
//
// Big picture (layered passes, because each tiebreaker depends on the one before):
//  1. Walk every match once and tally each player's record + list of opponents.
//  2. win% per player (with the 25% floor) → OWP = average of opponents' win%.
//  3. OOWP = average of opponents' OWP. Build the rows and sort.
package standings

import "sort"

// record is the per-player tally. Two kinds of counts are kept:
//   - wins/losses/ties include byes (byes are worth points)
//   - played/won exclude byes (byes don't count toward win%)
type record struct {
	wins, losses, ties int // all matches, byes included in wins
	played, won        int // non-bye matches only, for win%
	opponents          []string
}

func Compute(matches []Match) []Standing {
	// Map of player ID → *record. Storing POINTERS means get(id).wins++ updates the
	// record in the map. With map[string]record (values) you'd get a copy and have to
	// write it back yourself.
	recs := map[string]*record{}

	// get is a closure: a function literal that can see `recs`. It returns the
	// player's record, creating an empty one the first time we see that ID.
	get := func(id string) *record {
		if recs[id] == nil { // a missing key reads as the zero value; for pointers that's nil
			recs[id] = &record{}
		}
		return recs[id]
	}

	// ---- Pass 1: tally ----
	for _, m := range matches {
		p1 := get(m.P1)

		// A bye has an empty P2. It counts as a win for points only: no opponent and
		// no effect on win%. (Calling get(m.P1) above already registered the player.)
		if m.P2 == "" {
			p1.wins++
			continue
		}

		p2 := get(m.P2)
		p1.played++
		p2.played++
		p1.opponents = append(p1.opponents, m.P2)
		p2.opponents = append(p2.opponents, m.P1)

		// Go's switch has no fall-through by default, so no `break` is needed.
		switch m.Result {
		case P1Win:
			p1.wins++
			p1.won++
			p2.losses++
		case P2Win:
			p2.wins++
			p2.won++
			p1.losses++
		case Tie:
			p1.ties++
			p2.ties++
		}
	}

	// ---- Pass 2a: win% with the 25% floor ----
	winPct := map[string]float64{}
	for id, r := range recs {
		pct := 0.0
		if r.played > 0 { // avoid dividing by zero for bye-only players
			// Go never converts int to float implicitly. You must write float64(...).
			// (int/int would also do INTEGER division: 1/2 == 0.)
			pct = float64(r.won) / float64(r.played)
		}
		winPct[id] = max(pct, 0.25) // built-in max (Go 1.21+)
	}

	// mean averages vals[id] over the given IDs, or returns 0 for an empty list.
	// It's reused for both OWP (over win%) and OOWP (over OWP).
	mean := func(ids []string, vals map[string]float64) float64 {
		if len(ids) == 0 {
			return 0
		}
		sum := 0.0
		for _, id := range ids {
			sum += vals[id]
		}
		return sum / float64(len(ids))
	}

	// ---- Pass 2b: OWP ----
	owp := map[string]float64{}
	for id, r := range recs {
		owp[id] = mean(r.opponents, winPct)
	}

	// ---- Pass 3: rows + OOWP ----
	// make(type, length 0, capacity n) pre-allocates room so append doesn't have to
	// grow the slice repeatedly.
	out := make([]Standing, 0, len(recs))
	for id, r := range recs {
		out = append(out, Standing{
			ID:     id,
			Points: 3*r.wins + r.ties, // win = 3, tie = 1, loss = 0
			Wins:   r.wins, Losses: r.losses, Ties: r.ties,
			OWP:  owp[id],
			OOWP: mean(r.opponents, owp), // same shape as OWP, one level deeper
		})
	}

	// Map iteration order is RANDOM in Go, so this sort is what makes the output
	// deterministic. Compare points, then OWP, then OOWP, then ID.
	sort.Slice(out, func(i, j int) bool {
		a, b := out[i], out[j]
		// A tagless `switch {}` is a tidy if/else-if chain: the first true case wins.
		switch {
		case a.Points != b.Points:
			return a.Points > b.Points
		case a.OWP != b.OWP:
			return a.OWP > b.OWP
		case a.OOWP != b.OOWP:
			return a.OOWP > b.OOWP
		}
		return a.ID < b.ID
	})
	return out
}
