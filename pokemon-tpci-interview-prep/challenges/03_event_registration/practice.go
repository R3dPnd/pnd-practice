//go:build !solution

package registration

type Event struct {
	// TODO
}

func NewEvent(capacity int) *Event {
	panic("not implemented")
}

func (e *Event) Register(playerID string) (Status, error) {
	panic("not implemented")
}

func (e *Event) Cancel(playerID string) (promoted string, err error) {
	panic("not implemented")
}

func (e *Event) Confirmed() []string {
	panic("not implemented")
}

func (e *Event) Waitlist() []string {
	panic("not implemented")
}
