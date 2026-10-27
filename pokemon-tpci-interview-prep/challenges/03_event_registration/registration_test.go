package registration

import (
	"errors"
	"fmt"
	"reflect"
	"sync"
	"testing"
)

func TestFillsThenWaitlists(t *testing.T) {
	e := NewEvent(2)
	for _, id := range []string{"ash", "misty"} {
		if st, err := e.Register(id); err != nil || st != Confirmed {
			t.Fatalf("%s: %v %v", id, st, err)
		}
	}
	if st, _ := e.Register("brock"); st != Waitlisted {
		t.Fatalf("brock should be waitlisted")
	}
	if _, err := e.Register("ash"); !errors.Is(err, ErrAlreadyRegistered) {
		t.Fatalf("duplicate: got %v", err)
	}
	if _, err := e.Register("brock"); !errors.Is(err, ErrAlreadyRegistered) {
		t.Fatalf("duplicate waitlisted: got %v", err)
	}
}

func TestCancelConfirmedPromotesFIFO(t *testing.T) {
	e := NewEvent(1)
	e.Register("ash")
	e.Register("misty")
	e.Register("brock")
	promoted, err := e.Cancel("ash")
	if err != nil || promoted != "misty" {
		t.Fatalf("promoted=%q err=%v", promoted, err)
	}
	if !reflect.DeepEqual(e.Confirmed(), []string{"misty"}) || !reflect.DeepEqual(e.Waitlist(), []string{"brock"}) {
		t.Fatalf("confirmed=%v waitlist=%v", e.Confirmed(), e.Waitlist())
	}
	// ash can register again after cancelling.
	if st, err := e.Register("ash"); err != nil || st != Waitlisted {
		t.Fatalf("re-register: %v %v", st, err)
	}
}

func TestCancelWaitlistedDoesNotPromote(t *testing.T) {
	e := NewEvent(1)
	e.Register("ash")
	e.Register("misty")
	e.Register("brock")
	if p, err := e.Cancel("misty"); err != nil || p != "" {
		t.Fatalf("p=%q err=%v", p, err)
	}
	if !reflect.DeepEqual(e.Waitlist(), []string{"brock"}) {
		t.Fatalf("waitlist=%v", e.Waitlist())
	}
	if _, err := e.Cancel("gary"); !errors.Is(err, ErrNotRegistered) {
		t.Fatalf("unknown: %v", err)
	}
}

func TestAccessorsReturnCopies(t *testing.T) {
	e := NewEvent(2)
	e.Register("ash")
	c := e.Confirmed()
	c[0] = "hacked"
	if e.Confirmed()[0] != "ash" {
		t.Fatal("Confirmed() must return a copy")
	}
}

func TestConcurrentRegistrationNeverOversells(t *testing.T) {
	e := NewEvent(100)
	var wg sync.WaitGroup
	for i := range 1000 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			e.Register(fmt.Sprintf("p%d", i))
		}()
	}
	wg.Wait()
	if n := len(e.Confirmed()); n != 100 {
		t.Fatalf("confirmed %d, want 100", n)
	}
	if n := len(e.Waitlist()); n != 900 {
		t.Fatalf("waitlist %d, want 900", n)
	}
}
