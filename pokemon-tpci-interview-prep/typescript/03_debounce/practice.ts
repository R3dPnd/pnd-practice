export type Debounced<A extends unknown[]> = ((...args: A) => void) & { cancel(): void; flush(): void };

export function debounce<A extends unknown[]>(fn: (...args: A) => void, waitMs: number): Debounced<A> {
  throw new Error("not implemented");
}
