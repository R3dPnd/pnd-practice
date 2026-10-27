export type Region = "NA" | "EU" | "LATAM" | "OCE";
export type EventType = "league_challenge" | "league_cup" | "regional" | "international" | "worlds";

export type PlayEvent = {
  id: string;
  name: string;
  city: string;
  region: Region;
  type: EventType;
  date: string; // YYYY-MM-DD
};

const EVENTS: PlayEvent[] = [
  { id: "e1", name: "Bellevue League Challenge", city: "Bellevue", region: "NA", type: "league_challenge", date: "2026-11-01" },
  { id: "e2", name: "Seattle League Cup", city: "Seattle", region: "NA", type: "league_cup", date: "2026-11-08" },
  { id: "e3", name: "Portland Regional Championships", city: "Portland", region: "NA", type: "regional", date: "2026-11-14" },
  { id: "e4", name: "Stuttgart Regional Championships", city: "Stuttgart", region: "EU", type: "regional", date: "2026-12-05" },
  { id: "e5", name: "Latin America International Championships", city: "São Paulo", region: "LATAM", type: "international", date: "2026-11-21" },
  { id: "e6", name: "Oceania International Championships", city: "Melbourne", region: "OCE", type: "international", date: "2027-02-20" },
  { id: "e7", name: "Europe International Championships", city: "London", region: "EU", type: "international", date: "2027-04-10" },
  { id: "e8", name: "Pokémon World Championships", city: "San Francisco", region: "NA", type: "worlds", date: "2027-08-20" },
];

export function fetchEvents(params: { region?: Region; text?: string; signal?: AbortSignal }): Promise<PlayEvent[]> {
  const { region, text, signal } = params;
  return new Promise((resolve, reject) => {
    const delay = 200 + Math.random() * 600;
    const timer = setTimeout(() => {
      if (Math.random() < 0.15) return reject(new Error("503 Service Unavailable"));
      const q = text?.trim().toLowerCase();
      resolve(
        EVENTS.filter((e) => (!region || e.region === region) && (!q || `${e.name} ${e.city}`.toLowerCase().includes(q))),
      );
    }, delay);
    signal?.addEventListener("abort", () => {
      clearTimeout(timer);
      reject(new DOMException("Aborted", "AbortError"));
    });
  });
}
