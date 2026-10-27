//go:build solution

// Generic LRU cache — reference solution.
//
// Big picture:
//   - The map finds any entry in O(1): key → *list.Element.
//   - A doubly linked list (container/list) keeps recency order, so any element can be
//     moved to the front, or the back element removed, in O(1).
//   - Front = most recently used. Back = least recently used, which is evicted first.
package lru

import "container/list"

// entry is what each list element stores. Keeping the KEY in it matters: when we evict
// the back element, we need its key to delete the matching map entry.
// [K comparable, V any] are type parameters (generics, Go 1.18+). K must be comparable
// because it's used as a map key; V can be anything.
type entry[K comparable, V any] struct {
	key   K
	value V
}

type Cache[K comparable, V any] struct {
	capacity int
	order    *list.List // front = most recently used
	items    map[K]*list.Element
}

func New[K comparable, V any](capacity int) *Cache[K, V] {
	return &Cache[K, V]{capacity: capacity, order: list.New(), items: map[K]*list.Element{}}
}

func (c *Cache[K, V]) Get(key K) (V, bool) {
	el, ok := c.items[key]
	if !ok {
		// We have to return SOME V. `var zero V` declares the zero value of whatever
		// type V turns out to be (0, "", nil, ...): the generic way to say "nothing".
		var zero V
		return zero, false
	}
	// A read counts as a use, so move the element to the front.
	c.order.MoveToFront(el)

	// container/list predates generics, so el.Value has type `any`. The type assertion
	// .(*entry[K, V]) converts it back. It would panic on a wrong type, but we only ever
	// store *entry[K, V].
	return el.Value.(*entry[K, V]).value, true
}

func (c *Cache[K, V]) Put(key K, value V) {
	if c.capacity <= 0 {
		return // a zero-capacity cache stores nothing
	}

	// Existing key: update the value in place and mark it most recently used.
	if el, ok := c.items[key]; ok {
		el.Value.(*entry[K, V]).value = value
		c.order.MoveToFront(el)
		return
	}

	// New key: PushFront returns the new *list.Element, which we index in the map.
	c.items[key] = c.order.PushFront(&entry[K, V]{key, value})

	// Over capacity → evict the least recently used element (the back of the list).
	if c.order.Len() > c.capacity {
		oldest := c.order.Back()
		c.order.Remove(oldest)
		delete(c.items, oldest.Value.(*entry[K, V]).key) // this is why entry stores key
	}
}

func (c *Cache[K, V]) Len() int { return c.order.Len() }
