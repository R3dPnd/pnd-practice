// Debounce with cancel/flush — reference solution.
//
// Big picture: every call REPLACES the pending call and restarts the timer. fn only runs
// once the calls stop for `waitMs`, and it runs with the LAST arguments. The state
// (`timer`, `pending`) lives in a closure: variables from debounce() that the returned
// function keeps access to after debounce() returns.

// The return type is a function AND an object with two methods. `&` is an intersection
// type: "both of these at once". Functions in JS are objects, so we can attach methods.
// `A extends unknown[]` captures fn's parameter list as a tuple type, so the debounced
// function accepts exactly the same arguments as fn (e.g. [query: string]).
export type Debounced<A extends unknown[]> = ((...args: A) => void) & { cancel(): void; flush(): void };

export function debounce<A extends unknown[]>(fn: (...args: A) => void, waitMs: number): Debounced<A> {
  // ReturnType<typeof setTimeout> is "whatever setTimeout returns". That's a number in
  // browsers and a Timeout object in Node; this type works in both.
  let timer: ReturnType<typeof setTimeout> | undefined;
  // The arguments of the most recent call, waiting to be used. undefined means "nothing pending".
  let pending: A | undefined;

  // run fires fn with the pending args, if there are any. It clears the state FIRST, so
  // that if fn itself calls the debounced function again, it sees a clean slate.
  const run = () => {
    const args = pending;
    timer = undefined;
    pending = undefined;
    if (args) fn(...args); // spread the tuple back into separate arguments
  };

  // `...args: A` is a rest parameter: it collects every argument into a tuple.
  const debounced = (...args: A) => {
    pending = args;                     // newest args win
    clearTimeout(timer);                // cancel the previous countdown (clearTimeout(undefined) is a no-op)
    timer = setTimeout(run, waitMs);    // start a fresh countdown
  };

  // Attach the extra methods. TypeScript allows adding properties to a function declared
  // with const like this (it's called "expando"), and that's how `debounced` satisfies Debounced<A>.
  debounced.cancel = () => {
    clearTimeout(timer);
    timer = undefined;
    pending = undefined;                // drop the pending call entirely
  };
  debounced.flush = () => {
    clearTimeout(timer);                // stop the timer so fn won't ALSO fire later
    run();                              // run now (a no-op if nothing is pending)
  };

  return debounced;
}
