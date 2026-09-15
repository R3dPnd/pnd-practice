/**
 * Shared PRACTICE/solution toggle loader.
 *
 * Usage from a test file:
 *   const { debounce } = await loadImpl(import.meta.url, "debounce");
 *
 * PRACTICE=0 (or unset "practice", i.e. explicit "0") loads solution_<topic>.mjs;
 * anything else (including unset) loads practice_<topic>.mjs, matching the Python
 * repo's `PRACTICE=0 pytest` convention.
 */
export async function loadImpl(callerUrl, topic) {
  const usePractice = process.env.PRACTICE !== "0";
  const file = usePractice ? `practice_${topic}.mjs` : `solution_${topic}.mjs`;
  const dir = new URL(".", callerUrl);
  return import(new URL(file, dir));
}
