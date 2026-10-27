import type { Page, PlayEvent, Query } from "./types.ts";

export function searchEvents(events: PlayEvent[], q: Query): Page<PlayEvent> {
  throw new Error("not implemented");
}
