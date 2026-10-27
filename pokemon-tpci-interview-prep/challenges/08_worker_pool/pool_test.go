package pool

import (
	"context"
	"errors"
	"reflect"
	"sync/atomic"
	"testing"
	"time"
)

func TestPreservesOrder(t *testing.T) {
	items := []int{5, 1, 4, 2, 3}
	got, err := Map(context.Background(), items, 3, func(_ context.Context, n int) (int, error) {
		time.Sleep(time.Duration(n) * time.Millisecond)
		return n * n, nil
	})
	if err != nil || !reflect.DeepEqual(got, []int{25, 1, 16, 4, 9}) {
		t.Fatalf("got %v err %v", got, err)
	}
}

func TestBoundsConcurrency(t *testing.T) {
	var inFlight, peak atomic.Int32
	items := make([]int, 50)
	_, err := Map(context.Background(), items, 4, func(_ context.Context, _ int) (int, error) {
		n := inFlight.Add(1)
		for {
			p := peak.Load()
			if n <= p || peak.CompareAndSwap(p, n) {
				break
			}
		}
		time.Sleep(2 * time.Millisecond)
		inFlight.Add(-1)
		return 0, nil
	})
	if err != nil {
		t.Fatal(err)
	}
	if p := peak.Load(); p > 4 || p < 2 {
		t.Fatalf("peak concurrency %d, want 2..4", p)
	}
}

func TestFirstErrorCancelsRest(t *testing.T) {
	boom := errors.New("boom")
	var started atomic.Int32
	items := make([]int, 100)
	for i := range items {
		items[i] = i
	}
	_, err := Map(context.Background(), items, 2, func(ctx context.Context, n int) (int, error) {
		started.Add(1)
		if n == 3 {
			return 0, boom
		}
		select {
		case <-ctx.Done():
			return 0, ctx.Err()
		case <-time.After(5 * time.Millisecond):
			return n, nil
		}
	})
	if !errors.Is(err, boom) {
		t.Fatalf("err = %v, want boom", err)
	}
	if s := started.Load(); s > 20 {
		t.Fatalf("started %d items; should stop launching after the error", s)
	}
}

func TestParentCancellation(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	_, err := Map(ctx, []int{1, 2, 3}, 2, func(ctx context.Context, n int) (int, error) {
		return n, nil
	})
	if !errors.Is(err, context.Canceled) {
		t.Fatalf("err = %v", err)
	}
}
