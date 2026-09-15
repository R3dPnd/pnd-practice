export function memoize(fn, { resolver, maxSize = Infinity } = {}) {
  const cache = new Map();
  const keyOf = resolver ?? ((...args) => JSON.stringify(args));

  return function memoized(...args) {
    const key = keyOf(...args);

    if (cache.has(key)) {
      const value = cache.get(key);
      // Refresh recency: delete + re-insert moves this key to the end of
      // the Map's iteration order.
      cache.delete(key);
      cache.set(key, value);
      return value;
    }

    const value = fn.apply(this, args);
    cache.set(key, value);

    if (cache.size > maxSize) {
      const oldestKey = cache.keys().next().value;
      cache.delete(oldestKey);
    }

    return value;
  };
}
