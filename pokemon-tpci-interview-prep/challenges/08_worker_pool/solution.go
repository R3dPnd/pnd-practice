//go:build solution

// Bounded worker pool with cancellation — reference solution.
//
// Big picture:
//   - A buffered channel of capacity `workers` acts as a SEMAPHORE: sending takes a
//     slot, receiving gives it back. When the channel is full, the next send blocks, so
//     at most `workers` goroutines run fn at once.
//   - Each goroutine writes to results[i], its own index, so output order matches input.
//   - The first error cancels a derived context. That tells in-flight fn calls to stop,
//     and stops the loop from launching more.
//
// In real code you'd use golang.org/x/sync/errgroup with g.SetLimit(workers), which
// does all of this for you.
package pool

import (
	"context"
	"sync"
)

// [T, R any]: generic over the input type T and the result type R.
func Map[T, R any](ctx context.Context, items []T, workers int, fn func(context.Context, T) (R, error)) ([]R, error) {
	if workers <= 0 {
		workers = 1 // a 0-capacity semaphore would block forever
	}

	// Derive a cancellable child context. Cancelling it cancels everything we pass it to,
	// but NOT the caller's parent ctx. `defer cancel()` always releases its resources;
	// `go vet` warns if you forget.
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	results := make([]R, len(items))
	sem := make(chan struct{}, workers) // struct{} takes zero bytes: a pure signal
	var (
		wg       sync.WaitGroup // counts running goroutines so we can wait for all of them
		once     sync.Once      // makes sure only the FIRST error is recorded
		firstErr error
	)

	// fail records the first error and cancels everyone else. sync.Once makes it safe
	// to call from many goroutines at once: the function inside runs exactly one time,
	// so firstErr is written once and later readers see that write.
	fail := func(err error) {
		once.Do(func() {
			firstErr = err
			cancel()
		})
	}

	// `loop:` is a LABEL. Inside a select, a plain `break` only exits the select;
	// `break loop` exits the for loop.
loop:
	for i, item := range items {
		// select waits on several channel operations and runs whichever is ready first:
		//   - ctx.Done() is closed on cancellation (our error, or the parent's): stop.
		//   - sem <- struct{}{} succeeds once a slot is free: go ahead.
		select {
		case <-ctx.Done():
			break loop
		case sem <- struct{}{}:
		}

		wg.Add(1) // Add BEFORE starting the goroutine, or Wait() could return too early
		// Since Go 1.22, each loop iteration gets its own i and item, so the closure
		// captures the right values. (Before 1.22 you had to copy them first.)
		go func() {
			defer wg.Done()          // runs last: mark this goroutine finished
			defer func() { <-sem }() // runs first (defers are LIFO): free the slot
			r, err := fn(ctx, item)
			if err != nil {
				fail(err)
				return
			}
			// No mutex needed: each goroutine writes a different index, and wg.Wait()
			// below guarantees these writes are visible before we read results.
			results[i] = r
		}()
	}

	// Block until every started goroutine has finished, so none outlives this function.
	wg.Wait()

	if firstErr != nil {
		return nil, firstErr
	}
	// No fn failed, but the parent ctx may have been cancelled (or timed out). Our child
	// ctx reports that too: Err() is context.Canceled or context.DeadlineExceeded.
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	return results, nil
}
