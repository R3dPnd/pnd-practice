//go:build !solution

package throttle

import "time"

type Throttle struct {
	// TODO
}

func NewThrottle(maxFailures int, window, lockout time.Duration, now func() time.Time) *Throttle {
	panic("not implemented")
}

func (t *Throttle) Allowed(user string) bool { panic("not implemented") }

func (t *Throttle) RecordFailure(user string) { panic("not implemented") }

func (t *Throttle) RecordSuccess(user string) { panic("not implemented") }
