// "Find an Event" page — reference solution.
//
// Big picture:
//   - Two custom hooks keep the component simple:
//       useDebouncedValue: delays the search text by 300ms so we don't fetch on every keystroke.
//       useEvents: fetches whenever region/text/attempt change, and models the request as a
//                  discriminated union (loading | error | success).
//   - Race safety: each fetch gets an AbortController. When the inputs change, React runs
//     the effect's CLEANUP function before running the effect again. Cleanup aborts the old
//     request, so a slow, stale response can never overwrite a newer one.
//   - "Saved" stars live in a Set of IDs that's separate from the fetched data, so they
//     survive refetches.
import { useEffect, useState } from "react";
import { fetchEvents, type PlayEvent, type Region } from "./mockApi";

// A DISCRIMINATED UNION: each variant has a `status` tag. Checking state.status narrows
// the type, so TypeScript knows state.events exists ONLY when status === "success".
// You can't accidentally render data while loading, or show an error with no message.
type State =
  | { status: "loading" }
  | { status: "error"; error: string }
  | { status: "success"; events: PlayEvent[] };

const REGIONS: Region[] = ["NA", "EU", "LATAM", "OCE"];

// Record<K, V> is an object type with exactly these keys. If a new EventType is added
// and isn't listed here, this line stops compiling, which reminds you to add a label.
const TYPE_LABEL: Record<PlayEvent["type"], string> = {
  league_challenge: "League Challenge",
  league_cup: "League Cup",
  regional: "Regional",
  international: "International",
  worlds: "Worlds",
};

// Returns `value`, but only after it has stopped changing for `ms` milliseconds.
function useDebouncedValue<T>(value: T, ms: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    // Every time `value` changes, start a timer to publish it...
    const id = setTimeout(() => setDebounced(value), ms);
    // ...and if value changes again before the timer fires, React runs this cleanup
    // first, which cancels that timer. Only the last value survives the quiet period.
    return () => clearTimeout(id);
  }, [value, ms]); // re-run the effect when either of these changes
  return debounced;
}

// Fetches events for the given filters. `attempt` exists only so a Retry button can
// force a refetch with the same filters: incrementing it changes the dependency array.
function useEvents(region: Region | undefined, text: string, attempt: number): State {
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    // One controller per request. Passing controller.signal to the fetch lets us cancel it.
    const controller = new AbortController();
    setState({ status: "loading" });

    fetchEvents({ region, text, signal: controller.signal })
      .then((events) => setState({ status: "success", events }))
      // The `unknown` annotation: a JS catch can receive ANYTHING (not only Error objects),
      // so we narrow it below before reading .message.
      .catch((err: unknown) => {
        // If WE aborted this request (because the inputs changed), it's not a real error.
        // Ignore it, because a newer request now owns the state.
        if (controller.signal.aborted) return;
        setState({ status: "error", error: err instanceof Error ? err.message : String(err) });
      });

    // Cleanup runs before the next effect run, and on unmount. This one line is the whole
    // race-condition fix.
    return () => controller.abort();
  }, [region, text, attempt]);

  return state;
}

// Append T00:00:00 (no "Z") so the date is parsed as LOCAL midnight. new Date("2026-11-01")
// alone is parsed as UTC midnight, which shows as Oct 31 in US time zones.
const formatDate = (iso: string) =>
  new Date(`${iso}T00:00:00`).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });

export default function EventFinder() {
  // "" means "All regions". A <select> value is always a string, so "" works better
  // here than undefined.
  const [region, setRegion] = useState<Region | "">("");
  const [text, setText] = useState("");          // what's in the box right now (updates every keystroke)
  const [attempt, setAttempt] = useState(0);     // bump to retry
  // Lazy initializer `() => new Set()`: the function runs only on the FIRST render, not
  // every render. That matters for expensive initial values, and is a good habit here.
  const [saved, setSaved] = useState<Set<string>>(() => new Set());

  const debouncedText = useDebouncedValue(text, 300);
  // `region || undefined` turns "" into undefined, which the API reads as "no filter".
  // Changing region refetches immediately; only the text is debounced.
  const state = useEvents(region || undefined, debouncedText, attempt);

  const toggleSaved = (id: string) =>
    // Functional update (prev => next): always works from the latest state, even if
    // several updates are queued.
    setSaved((prev) => {
      // Never mutate state in place. Copy it, change the copy, and return the copy.
      // React compares by reference (prev === next), so mutating prev wouldn't re-render.
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

  return (
    <main>
      <h1>Find an Event</h1>

      {/* Wrapping the control in <label> associates the text with the input, so screen
          readers announce "Region" and clicking the text focuses the control. */}
      <label>
        Region{" "}
        {/* A CONTROLLED input: React state is the source of truth (value + onChange).
            The `as` cast is needed because e.target.value is typed as a plain string. */}
        <select value={region} onChange={(e) => setRegion(e.target.value as Region | "")}>
          <option value="">All</option>
          {REGIONS.map((r) => (
            // `key` lets React match list items between renders. Use a stable unique
            // value, not the array index.
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
      </label>{" "}
      <label>
        Search <input type="search" value={text} onChange={(e) => setText(e.target.value)} />
      </label>

      {/* `cond && <JSX/>` renders the JSX only when cond is true. Each branch checks
          state.status, and that check is what lets TypeScript allow state.error /
          state.events inside it. */}

      {/* role="status" is a polite live region: screen readers announce it when it appears. */}
      {state.status === "loading" && <p role="status">Loading…</p>}

      {/* role="alert" is announced immediately. Retry bumps `attempt`, which re-runs the effect. */}
      {state.status === "error" && (
        <p role="alert">
          Couldn't load events ({state.error}).{" "}
          <button onClick={() => setAttempt((a) => a + 1)}>Retry</button>
        </p>
      )}

      {state.status === "success" && state.events.length === 0 && <p>No events found</p>}

      {state.status === "success" && state.events.length > 0 && (
        // A real <ul>/<li> list, so assistive tech announces "list, 8 items".
        <ul>
          {state.events.map((e) => (
            <li key={e.id}>
              <strong>{e.name}</strong> — {e.city} · {formatDate(e.date)} · <span>{TYPE_LABEL[e.type]}</span>{" "}
              {/* aria-pressed makes this a toggle button that screen readers announce
                  as "pressed" or "not pressed". */}
              <button aria-pressed={saved.has(e.id)} onClick={() => toggleSaved(e.id)}>
                {saved.has(e.id) ? "★ Saved" : "☆ Save"}
              </button>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
