//go:build !solution

package pool

import "context"

func Map[T, R any](ctx context.Context, items []T, workers int, fn func(context.Context, T) (R, error)) ([]R, error) {
	panic("not implemented")
}
