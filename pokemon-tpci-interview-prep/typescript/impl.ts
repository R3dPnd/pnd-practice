// Tests load practice.ts by default; PRACTICE=0 loads the reference solution.ts.
export async function load<T>(dir: string): Promise<T> {
  const file = process.env.PRACTICE === "0" ? "solution.ts" : "practice.ts";
  return (await import(new URL(`./${dir}/${file}`, import.meta.url).href)) as T;
}
