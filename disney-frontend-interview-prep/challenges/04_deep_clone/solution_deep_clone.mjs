export function deepClone(value, seen = new WeakMap()) {
  if (value === null || typeof value !== "object") return value;

  if (seen.has(value)) return seen.get(value);

  if (value instanceof Date) return new Date(value.getTime());
  if (value instanceof RegExp) return new RegExp(value.source, value.flags);

  if (Array.isArray(value)) {
    const clone = [];
    seen.set(value, clone);
    value.forEach((item, index) => {
      clone[index] = deepClone(item, seen);
    });
    return clone;
  }

  if (value instanceof Map) {
    const clone = new Map();
    seen.set(value, clone);
    for (const [key, val] of value) clone.set(deepClone(key, seen), deepClone(val, seen));
    return clone;
  }

  if (value instanceof Set) {
    const clone = new Set();
    seen.set(value, clone);
    for (const item of value) clone.add(deepClone(item, seen));
    return clone;
  }

  const clone = {};
  seen.set(value, clone);
  for (const key of Object.keys(value)) clone[key] = deepClone(value[key], seen);
  return clone;
}
