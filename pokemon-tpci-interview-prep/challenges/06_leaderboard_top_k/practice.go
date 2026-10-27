//go:build !solution

package leaderboard

type Leaderboard struct {
	// TODO
}

func NewLeaderboard() *Leaderboard { panic("not implemented") }

func (l *Leaderboard) Award(id string, points int) { panic("not implemented") }

func (l *Leaderboard) Total(id string) int { panic("not implemented") }

func (l *Leaderboard) TopK(k int) []Entry { panic("not implemented") }
