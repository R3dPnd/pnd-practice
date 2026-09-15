export function debounce(fn, wait) {
  let timeoutId;
  return function debounced(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), wait);
  };
}

export function throttle(fn, wait) {
  let lastCallTime = -Infinity;
  let timeoutId = null;
  let pendingArgs = null;
  let pendingThis = null;

  return function throttled(...args) {
    const now = Date.now();
    const remaining = wait - (now - lastCallTime);
    pendingArgs = args;
    pendingThis = this;

    if (remaining <= 0) {
      lastCallTime = now;
      fn.apply(pendingThis, pendingArgs);
      return;
    }

    if (!timeoutId) {
      timeoutId = setTimeout(() => {
        lastCallTime = Date.now();
        timeoutId = null;
        fn.apply(pendingThis, pendingArgs);
      }, remaining);
    }
  };
}
