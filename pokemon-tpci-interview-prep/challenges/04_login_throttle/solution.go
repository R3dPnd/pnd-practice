//go:build solution

// Login throttle / lockout — reference solution.
//
// Big picture, per user:
//   - `failures`: timestamps of recent failed logins, oldest first.
//   - `lockedUntil`: when the current lockout ends (zero time = never locked).
//   - On each failure: drop timestamps outside the window, add now, and lock the user
//     out (clearing their history) once the count reaches the limit.
//
// The clock is injected as `now func() time.Time` instead of calling time.Now() directly,
// so tests can control time without sleeping.
package throttle

import (
	"sync"
	"time"
)

type state struct {
	failures    []time.Time
	lockedUntil time.Time // zero value is year 1, which is "always in the past"
}

type Throttle struct {
	mu          sync.Mutex
	maxFailures int
	window      time.Duration // time.Duration is an int64 count of nanoseconds
	lockout     time.Duration
	now         func() time.Time
	users       map[string]*state
}

func NewThrottle(maxFailures int, window, lockout time.Duration, now func() time.Time) *Throttle {
	return &Throttle{maxFailures: maxFailures, window: window, lockout: lockout, now: now, users: map[string]*state{}}
}

func (t *Throttle) Allowed(user string) bool {
	t.mu.Lock()
	defer t.mu.Unlock()
	s := t.users[user]
	// Allowed if we've never seen this user (nil), or now >= lockedUntil.
	// Go's time API has Before/After/Equal but no ">=", so "not before" means ">=".
	// Use these methods rather than ==, which also compares time zones and other internals.
	return s == nil || !t.now().Before(s.lockedUntil)
}

func (t *Throttle) RecordFailure(user string) {
	t.mu.Lock()
	defer t.mu.Unlock()

	now := t.now()
	s := t.users[user]
	if s == nil {
		s = &state{}
		t.users[user] = s
	}

	// Locked right now? Ignore the failure so a lockout can't be extended or stacked.
	if now.Before(s.lockedUntil) {
		return
	}

	// Slide the window: keep only failures newer than the cutoff.
	cutoff := now.Add(-t.window)

	// "Filter in place" idiom: kept := s.failures[:0] is an empty slice that SHARES
	// s.failures' backing array, so appending to it overwrites the old entries from
	// the front, with no new allocation. This is safe because the write position never
	// gets ahead of the read position.
	kept := s.failures[:0]
	for _, f := range s.failures {
		// f.After(cutoff): still inside the window.
		// !f.Before(s.lockedUntil): happened after the last lockout ended. That's
		// defensive, because we already clear failures when we lock.
		if f.After(cutoff) && !f.Before(s.lockedUntil) {
			kept = append(kept, f)
		}
	}
	s.failures = append(kept, now) // record this failure

	// Hit the limit → lock out for `lockout`, starting now, and start fresh afterwards.
	if len(s.failures) >= t.maxFailures {
		s.lockedUntil = now.Add(t.lockout)
		s.failures = nil
	}
}

func (t *Throttle) RecordSuccess(user string) {
	t.mu.Lock()
	defer t.mu.Unlock()
	// A successful login clears the failure history. It does NOT lift an active lockout,
	// though a locked-out user shouldn't be able to succeed anyway.
	if s := t.users[user]; s != nil { // if-with-initializer: s only exists inside this if
		s.failures = nil
	}
}
