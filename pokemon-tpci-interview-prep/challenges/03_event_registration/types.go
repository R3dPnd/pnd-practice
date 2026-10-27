package registration

import "errors"

type Status int

const (
	Confirmed Status = iota
	Waitlisted
)

var (
	ErrAlreadyRegistered = errors.New("already registered")
	ErrNotRegistered     = errors.New("not registered")
)
