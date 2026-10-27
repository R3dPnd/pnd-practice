//go:build !solution

package lru

type Cache[K comparable, V any] struct {
	// TODO
}

func New[K comparable, V any](capacity int) *Cache[K, V] { panic("not implemented") }

func (c *Cache[K, V]) Get(key K) (V, bool) { panic("not implemented") }

func (c *Cache[K, V]) Put(key K, value V) { panic("not implemented") }

func (c *Cache[K, V]) Len() int { panic("not implemented") }
