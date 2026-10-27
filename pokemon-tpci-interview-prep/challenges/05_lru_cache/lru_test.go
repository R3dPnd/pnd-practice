package lru

import "testing"

func TestEvictsLeastRecentlyUsed(t *testing.T) {
	c := New[string, int](2)
	c.Put("pikachu", 25)
	c.Put("eevee", 133)
	c.Get("pikachu") // eevee is now LRU
	c.Put("snorlax", 143)
	if _, ok := c.Get("eevee"); ok {
		t.Fatal("eevee should be evicted")
	}
	if v, ok := c.Get("pikachu"); !ok || v != 25 {
		t.Fatal("pikachu should remain")
	}
	if c.Len() != 2 {
		t.Fatalf("len %d", c.Len())
	}
}

func TestUpdateRefreshesRecency(t *testing.T) {
	c := New[string, int](2)
	c.Put("a", 1)
	c.Put("b", 2)
	c.Put("a", 10) // b is now LRU
	c.Put("c", 3)
	if _, ok := c.Get("b"); ok {
		t.Fatal("b should be evicted")
	}
	if v, _ := c.Get("a"); v != 10 {
		t.Fatalf("a = %d want 10", v)
	}
}

func TestZeroCapacity(t *testing.T) {
	c := New[int, int](0)
	c.Put(1, 1)
	if _, ok := c.Get(1); ok || c.Len() != 0 {
		t.Fatal("zero-capacity cache must store nothing")
	}
}
