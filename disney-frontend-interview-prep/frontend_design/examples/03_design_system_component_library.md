# Worked example: shared design system / component library

Practice prompt 3 from `../notes.md`: a component library shared across multiple web
properties (Disney+, Hulu, ESPN web).

- **Clarify**: How many consuming teams/properties? Do they share one visual brand or
  need per-brand theming (Disney+ vs. ESPN look very different)? Is this components
  only, or does it also own design tokens (spacing, color, typography)?
- **Contract**: Each component ships with a typed props API, a documented
  accessibility contract (e.g., "this Button is always a real `<button>`, always
  keyboard-operable, always has a visible focus ring"), and a Storybook entry per
  variant/state — the props API and the accessibility contract are the actual product,
  the visual styling is almost secondary.
- **Architecture**: Design tokens (colors, spacing, type scale) as a themeable layer
  underneath the components — components consume tokens via CSS variables or a theme
  object, never hardcoded values, so swapping a theme (Disney+ vs. ESPN) doesn't
  require touching component internals. Published as a versioned package consumed by
  each property's app, not copy-pasted.
- **Deep dive** (likely steered here): rolling out a breaking change without breaking
  every consumer at once. Semantic versioning + a deprecation window: ship the new
  behavior alongside the old one behind a prop or a new component name for one or two
  release cycles, log a console warning on the old path, migrate consumers on their own
  schedule, then remove the old path in a major version bump — never a flag-day change
  that forces every consuming team to update in lockstep.
- **FE review pass**:
  - *Accessibility*: this is the single most important review-pass item for a shared
    library specifically — a bug here multiplies across every consuming property, so
    each component needs real automated a11y testing (axe or similar) in CI, not just a
    visual review.
  - *Performance*: tree-shakeable exports (consumers importing one component shouldn't
    pull in the whole library's bundle) and no runtime CSS-in-JS cost if it can be
    avoided at this shared-infrastructure layer.
  - *Testability*: visual regression testing (Chromatic/Storybook snapshots) in
    addition to unit tests, since "does this still look right across every theme" isn't
    something a plain unit test catches.
- **Tradeoffs**: a shared library adds coordination overhead (every breaking change
  needs a migration plan) versus each property owning its own components — worth it
  once you have 2+ properties that would otherwise visibly diverge or duplicate
  significant component logic; probably not worth it for a single property alone.
- **What I'd do differently with more time**: a codemod for common breaking changes
  (auto-migrate consumers' usage of a renamed prop) instead of relying on manual
  migration during the deprecation window — reduces the real cost of shipping a
  breaking change across many consuming teams.
