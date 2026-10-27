package standings

type Result int

const (
	P1Win Result = iota
	P2Win
	Tie
)

type Match struct {
	P1, P2 string
	Result Result
}

type Standing struct {
	ID                 string
	Points             int
	Wins, Losses, Ties int
	OWP, OOWP          float64
}
