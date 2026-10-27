// Retry with exponential backoff — reference solution.
//
// Big picture: call fn. If it throws, wait baseMs, then 2×baseMs, then 4×baseMs, ...
// and try again, up to `retries` extra attempts. Stop early if shouldRetry says the error
// isn't worth retrying (e.g. a 400 Bad Request will fail the same way every time).

export type RetryOptions = {
  retries: number;
  baseMs: number;
  // `?:` makes these optional. Their type is then `X | undefined`.
  shouldRetry?: (err: unknown) => boolean;
  // `sleep` is injectable so tests can record the delays instead of really waiting.
  sleep?: (ms: number) => Promise<void>;
};

// Wrap setTimeout in a Promise so it can be awaited.
// new Promise<void>((resolve) => ...) is the standard way to turn a callback API into a promise.
const defaultSleep = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));

// <T> is a generic type parameter: whatever type fn resolves to, retry resolves to the
// same type. retry(() => fetchUser()) gives Promise<User>, for example.
export async function retry<T>(fn: (attempt: number) => Promise<T>, opts: RetryOptions): Promise<T> {
  // Destructure the options, with defaults for the optional ones.
  // `shouldRetry = () => true` means retry every error unless told otherwise.
  const { retries, baseMs, shouldRetry = () => true, sleep = defaultSleep } = opts;

  // `for (...; ; ...)` has no condition, so it loops until we return or throw.
  // attempt starts at 1: the first call is attempt 1, the first retry is attempt 2.
  for (let attempt = 1; ; attempt++) {
    try {
      // `return await` (not just `return`) matters INSIDE a try block. It makes a
      // rejected promise throw HERE, where our catch can see it. A bare `return fn()`
      // would hand the rejection straight to the caller and skip the retry logic.
      return await fn(attempt);
    } catch (err) {
      // Give up if we've used all the retries (the attempt count is retries + 1 total),
      // or the error isn't retryable. `throw err` rethrows the ORIGINAL error so the
      // caller sees the real cause.
      if (attempt > retries || !shouldRetry(err)) throw err;

      // Exponential backoff: baseMs * 2^(attempt-1) gives 100, 200, 400, ... for baseMs=100.
      // `**` is the exponent operator. In production you'd also add random JITTER, so
      // 1,000 clients that failed together don't all retry at the same instant.
      await sleep(baseMs * 2 ** (attempt - 1));
    }
  }
}
