# Worked example: secrets management service (mini Vault/Key Vault)

Practice prompt 4 from `../notes.md`: services fetch DB credentials/API keys at
runtime instead of them being baked into config. Full run through the framework in
`../notes.md`, compressed to the key beats — this is what "narrate it out loud" should
actually sound like, not a diagram substitute. Use it to check your own mock reps
against, not to memorize verbatim.

- **Clarify**: Who's the client — internal services fetching DB creds/API keys at
  runtime (assume yes, not end users), does it need dynamic (short-lived, generated
  on demand) or just static encrypted secret storage (assume support both, dynamic is
  the more interesting design point), expected scale (thousands of services, not
  millions of secrets).
- **API**: `POST /auth` (service authenticates to the secrets service itself —
  see deep dive), `GET /secrets/{path}` (returns a secret, scoped by policy),
  `POST /secrets/{path}/rotate`.
- **Architecture**: service → secrets service authenticates the caller (see below) →
  policy engine checks the caller's identity against an ACL for the requested
  secret path → secret is decrypted on the fly from an encrypted store (secrets are
  never stored plaintext, even server-side) and returned over TLS, typically as a
  short-lived credential rather than a static one where the backing system supports it
  (e.g. a dynamically-generated DB user valid for 1 hour instead of a shared password).
- **Deep dive** (likely steered here, and the hardest part of this design): bootstrapping
  trust — how does a service authenticate *to* the secrets service without already
  having a secret to do so? Answer: platform-provided identity (e.g. a cloud instance
  identity token, or a Kubernetes service account token) that the secrets service
  trusts because it was issued by infrastructure the service didn't choose for itself,
  not a credential baked into the service's own config/image.
- **Security pass**:
  - Every fetch is logged (who fetched what secret, when) — this is close to the
    core product for a Security org, not a nice-to-have.
  - Short-lived dynamic credentials over long-lived static ones wherever the backing
    system supports generating them, to shrink the blast radius of a leak.
  - Rotation: automatic on a schedule, plus an emergency "revoke and rotate now" path
    for a known compromise.
  - Self-attack pass: "I'd target the bootstrap step — if the platform identity token
    itself can be forged or replayed from another host, the whole chain collapses." →
    mitigate with short-lived platform tokens and binding to instance/pod identity.
- **Tradeoffs / scale**: dynamic secrets are more secure but add latency/complexity
  (a live call to the backing system, e.g. the DB, to mint a new user) — for very
  high-QPS services, cache a short-lived credential for its lifetime rather than
  minting one per request, explicitly trading a little blast-radius width for latency.
- **What I'd do differently**: break-glass audit alerting (page someone the moment an
  emergency/root-level secret is fetched, even by an authorized caller).
