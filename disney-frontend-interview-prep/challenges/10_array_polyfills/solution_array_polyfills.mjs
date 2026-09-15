export function myMap(arr, callback) {
  const result = [];
  for (let i = 0; i < arr.length; i += 1) {
    result.push(callback(arr[i], i, arr));
  }
  return result;
}

export function myFilter(arr, predicate) {
  const result = [];
  for (let i = 0; i < arr.length; i += 1) {
    if (predicate(arr[i], i, arr)) result.push(arr[i]);
  }
  return result;
}

const NO_INITIAL_VALUE = Symbol("no-initial-value");

export function myReduce(arr, reducer, initialValue = NO_INITIAL_VALUE) {
  let accumulator = initialValue;
  let startIndex = 0;

  if (accumulator === NO_INITIAL_VALUE) {
    if (arr.length === 0) {
      throw new TypeError("Reduce of empty array with no initial value");
    }
    accumulator = arr[0];
    startIndex = 1;
  }

  for (let i = startIndex; i < arr.length; i += 1) {
    accumulator = reducer(accumulator, arr[i], i, arr);
  }

  return accumulator;
}
