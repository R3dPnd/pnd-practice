# The Pokémon Company International — company & domain notes

## The company

- **TPCi** manages Pokémon outside Asia: brand, licensing, marketing, the **Trading Card
  Game**, the anime, home entertainment, and **pokemon.com**. HQ in **Bellevue, WA**; offices
  in London and elsewhere. (Distinct from Game Freak / Creatures / Nintendo / Niantic — TPCi
  doesn't build the main-series games or Pokémon GO.)
- Customers are frequently **kids** → COPPA (US) and GDPR (EU) compliance is a constant
  constraint, especially for accounts (Pokémon Trainer Club) and anything social.

## Tech facts that are public (good to drop naturally, not to show off)

- **AWS shop.** Public AWS case study + re:Invent 2019 talk (GAM304, "Migrating the live
  Pokémon database to Aurora PostgreSQL"): Pokémon Trainer Club auth moved from a
  third-party NoSQL document DB to **Aurora PostgreSQL**; global config and **TTL** data went
  to **DynamoDB**; ~300 DB nodes → ~30; reported 168 downtime hours → zero after migration;
  DynamoDB-tracked login attempts with a deny threshold cut bot logins ~90%. The surge came
  from Pokémon GO launch (Trainer Club was a GO login option).
- Other TPCi JDs (Pokémon Center eCommerce, London): **Java** backend, **React / Next.js /
  TypeScript** frontend, Bloomreach CMS, REST + GraphQL, Jest + Playwright, Datadog /
  CloudWatch / New Relic, **GitLab CI/CD**, Scaled Agile (SAFe).
- **This JD's stack is different**: Go, TypeScript/React, AWS CDK, Postgres + NoSQL,
  containers + serverless. Likely a newer team / newer platform. Ask about it.
- Security: Palo Alto Networks published a case study on TPCi's SOC using Cortex XSOAR.

## What "communities, from small gatherings to our largest events" almost certainly means

**Play! Pokémon** — the organized-play program:

- **Pokémon Leagues** at local game stores, run by **Professors / Tournament Organizers (TOs)**.
- Event tiers: **League Challenge → League Cup → Regional Championships → International
  Championships (NA, EU, LATAM, Oceania) → World Championships**.
- Games: **TCG**, **VGC** (video game), **Pokémon GO**, **Pokémon UNITE**.
- Age divisions: **Juniors, Seniors, Masters**.
- **Championship Points (CP)** earned across the season qualify players for Worlds.
- Swiss rounds → top cut (single elimination). Tiebreakers: match points, then
  **OWP**, then **OOWP** (see `challenges/02`).
- Tooling in the ecosystem:
  - **TOM (Tournament Operations Manager)** — legacy desktop app for running events
    (pairings, standings, results upload).
  - **Pokémon Event Manager (PEM)** — newer replacement for TOM: create tournaments in-app,
    online Player ID verification, streamlined results upload; initially couldn't handle
    Regionals-scale events.
  - **Play! Tools** (play-tools.pokemon.com) — organizer-facing web tools.
  - **RK9** (rk9.gg) — third-party registration platform used for Regionals/Internationals.
  - **Event Locator** on pokemon.com — find nearby events.
  - **Play! Pokémon Player ID** + Pokémon Trainer Club account.

So "technology that enables our communities" = organizer tooling, player registration,
event discovery, pairings/standings, results & CP, and the account/identity layer under it.
Every challenge and design prompt in this folder is aimed at that.

## 30-minute homework before the interview

- [ ] Browse pokemon.com → Play! Pokémon → Event Locator; find an event near Bellevue.
- [ ] Skim the Play! Pokémon Tournament Rules Handbook (pairings, tiebreakers, divisions).
- [ ] Look at an rk9.gg event page (registration flow, pairings/standings pages).
- [ ] Read the Play! Tools guide / TOM FAQ on support.play.pokemon.com.
- [ ] Watch 10 minutes of the latest Worlds broadcast.
- [ ] Look up your interviewers on LinkedIn — which team/products they've worked on.
