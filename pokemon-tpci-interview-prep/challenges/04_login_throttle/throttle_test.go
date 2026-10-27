package throttle

import (
	"testing"
	"time"
)

type clock struct{ t time.Time }

func (c *clock) now() time.Time          { return c.t }
func (c *clock) advance(d time.Duration) { c.t = c.t.Add(d) }

func setup() (*Throttle, *clock) {
	c := &clock{t: time.Date(2026, 8, 14, 9, 0, 0, 0, time.UTC)}
	return NewThrottle(3, time.Minute, 10*time.Minute, c.now), c
}

func TestLocksAfterMaxFailures(t *testing.T) {
	th, c := setup()
	for i := 0; i < 2; i++ {
		th.RecordFailure("ash")
		c.advance(time.Second)
	}
	if !th.Allowed("ash") {
		t.Fatal("2 failures should still be allowed")
	}
	th.RecordFailure("ash")
	if th.Allowed("ash") {
		t.Fatal("3rd failure should lock")
	}
	if !th.Allowed("misty") {
		t.Fatal("other users unaffected")
	}
}

func TestLockoutExpires(t *testing.T) {
	th, c := setup()
	for i := 0; i < 3; i++ {
		th.RecordFailure("ash")
	}
	c.advance(10*time.Minute - time.Second)
	th.RecordFailure("ash") // ignored while locked
	if th.Allowed("ash") {
		t.Fatal("still locked")
	}
	c.advance(time.Second)
	if !th.Allowed("ash") {
		t.Fatal("lockout should have expired")
	}
	th.RecordFailure("ash")
	if !th.Allowed("ash") {
		t.Fatal("fresh start after lockout: 1 failure should not lock")
	}
}

func TestOldFailuresSlideOut(t *testing.T) {
	th, c := setup()
	th.RecordFailure("ash")
	th.RecordFailure("ash")
	c.advance(61 * time.Second)
	th.RecordFailure("ash")
	if !th.Allowed("ash") {
		t.Fatal("first two failures are outside the window")
	}
}

func TestSuccessResets(t *testing.T) {
	th, _ := setup()
	th.RecordFailure("ash")
	th.RecordFailure("ash")
	th.RecordSuccess("ash")
	th.RecordFailure("ash")
	if !th.Allowed("ash") {
		t.Fatal("success should clear failure history")
	}
}
