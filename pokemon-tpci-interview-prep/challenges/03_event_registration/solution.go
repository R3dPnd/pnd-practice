//go:build solution

// Event registration with capacity + FIFO waitlist — reference solution.
//
// Big picture:
//   - `confirmed` holds players with a seat, in the order they got it.
//   - `waitlist` is a FIFO queue of players waiting for a seat.
//   - `status` maps player → Confirmed/Waitlisted for O(1) "where is this player?".
//   - One mutex guards all of it, and every method locks first. So "check capacity,
//     then append" can never interleave between goroutines (that's how you oversell).
package registration

import (
	"slices"
	"sync"
)

type Event struct {
	// Convention: put the mutex directly above the fields it protects.
	// The zero value of sync.Mutex is an unlocked mutex, so it needs no setup.
	mu        sync.Mutex
	capacity  int
	confirmed []string
	waitlist  []string
	status    map[string]Status
}

func NewEvent(capacity int) *Event {
	// Maps MUST be initialized before you write to them (writing to a nil map panics).
	// Slices don't need it: append works on a nil slice.
	return &Event{capacity: capacity, status: map[string]Status{}}
}

func (e *Event) Register(playerID string) (Status, error) {
	// Lock, then `defer` the unlock. A deferred call runs when the function returns,
	// on EVERY return path, so we can't forget to unlock on an early return.
	e.mu.Lock()
	defer e.mu.Unlock()

	// The "comma ok" idiom: ok reports whether the key exists. We don't need the
	// value, so it goes to _.
	if _, ok := e.status[playerID]; ok {
		return 0, ErrAlreadyRegistered // 0 is just a placeholder; callers check err first
	}

	// The critical section: the check and the append happen under the same lock.
	if len(e.confirmed) < e.capacity {
		e.confirmed = append(e.confirmed, playerID)
		e.status[playerID] = Confirmed
		return Confirmed, nil
	}
	e.waitlist = append(e.waitlist, playerID) // join the back of the line
	e.status[playerID] = Waitlisted
	return Waitlisted, nil
}

func (e *Event) Cancel(playerID string) (string, error) {
	e.mu.Lock()
	defer e.mu.Unlock()

	st, ok := e.status[playerID]
	if !ok {
		return "", ErrNotRegistered
	}
	delete(e.status, playerID) // built-in: remove a key from a map

	// A waitlisted player leaving frees no seat, so nobody gets promoted.
	if st == Waitlisted {
		e.waitlist = remove(e.waitlist, playerID)
		return "", nil
	}

	// A confirmed player leaving frees one seat.
	e.confirmed = remove(e.confirmed, playerID)
	if len(e.waitlist) == 0 {
		return "", nil // nobody to promote
	}

	// Promote the FRONT of the queue (FIFO). Re-slicing waitlist[1:] is an O(1)
	// "dequeue". The underlying array isn't freed until the slice is reallocated,
	// which is fine at this scale.
	next := e.waitlist[0]
	e.waitlist = e.waitlist[1:]
	e.confirmed = append(e.confirmed, next)
	e.status[next] = Confirmed
	return next, nil
}

func (e *Event) Confirmed() []string {
	e.mu.Lock()
	defer e.mu.Unlock()
	// Return a COPY. A slice is a view onto a shared array, so returning e.confirmed
	// itself would let callers read or modify our state without holding the lock.
	return slices.Clone(e.confirmed)
}

func (e *Event) Waitlist() []string {
	e.mu.Lock()
	defer e.mu.Unlock()
	return slices.Clone(e.waitlist)
}

// remove deletes the first occurrence of id from s and returns the shortened slice.
// It assumes id is present: callers only use it after checking `status`.
// (slices.Index returns -1 for a missing id, and slices.Delete would then panic.)
func remove(s []string, id string) []string {
	i := slices.Index(s, id)
	return slices.Delete(s, i, i+1)
}
