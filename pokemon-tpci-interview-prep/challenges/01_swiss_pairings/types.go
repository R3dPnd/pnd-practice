package swiss

type Player struct {
	ID     string
	Points int
	HadBye bool
}

type Match struct {
	A, B string
}

type Round struct {
	Pairings []Match
	Bye      string
}
