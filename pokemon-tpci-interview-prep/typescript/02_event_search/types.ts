export type EventType = "league_challenge" | "league_cup" | "regional" | "international" | "worlds";

export type PlayEvent = {
  id: string;
  name: string;
  city: string;
  region: "NA" | "EU" | "LATAM" | "OCE";
  type: EventType;
  date: string; // YYYY-MM-DD
};

export type Query = {
  region?: PlayEvent["region"];
  types?: EventType[];
  from?: string;
  to?: string;
  text?: string;
  page?: number;
  pageSize?: number;
};

export type Page<T> = { items: T[]; page: number; pageSize: number; total: number; totalPages: number };
