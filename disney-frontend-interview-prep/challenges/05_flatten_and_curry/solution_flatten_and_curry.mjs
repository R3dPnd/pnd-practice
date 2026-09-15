export function flatten(arr, depth = Infinity) {
  if (depth < 1) return arr.slice();

  return arr.reduce((acc, item) => {
    if (Array.isArray(item)) {
      acc.push(...flatten(item, depth - 1));
    } else {
      acc.push(item);
    }
    return acc;
  }, []);
}

export function curry(fn) {
  const arity = fn.length;

  return function curried(...args) {
    if (args.length >= arity) return fn.apply(this, args);
    return (...rest) => curried.apply(this, [...args, ...rest]);
  };
}
