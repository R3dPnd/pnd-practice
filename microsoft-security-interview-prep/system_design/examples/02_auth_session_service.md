# Worked example: authentication/session service (SSO for internal apps)

Practice prompt 2 from `../notes.md`: an auth/session service for a suite of internal
apps (think SSO). Full run through the framework in `../notes.md`, compressed to the
key beats — this is what "narrate it out loud" should actually sound like, not a
diagram substitute. Use it to check your own mock reps against, not to memorize
verbatim.

- **Clarify**: Employee-facing internal SSO (assume yes, not consumer-facing), does it
  need to federate with an external IdP (assume it *is* the IdP, using OIDC to
  downstream apps), MFA required (assume yes — internal + Security org context makes
  this a given), expected scale (tens of thousands of employees, not millions).
- **API**: `POST /login` (credentials + MFA challenge), `POST /token` (OIDC-style
  authorization code exchange for access + refresh token), `POST /token/refresh`,
  `POST /sessions/{id}/revoke`.
- **Architecture**: client → auth service (credential + MFA verification) → issues a
  short-lived signed access token (JWT, ~15 min) + a longer-lived opaque refresh token
  stored server-side (in a sessions table, not just trusted client-side) → downstream
  apps validate the access token's signature locally (no round trip per request) →
  refresh flow re-checks the session store so a revoked session actually stops working
  even though the access token would otherwise still verify.
- **Deep dive** (likely steered here): token leak / blast-radius — what happens the
  moment a refresh token is stolen. Answer: refresh tokens are single-use with
  rotation (each refresh issues a new one and invalidates the old), so a replayed
  stolen token after the legitimate client has already rotated is detectable and
  triggers revoking the whole session family, not just that token.
- **Security pass**:
  - Password storage: salted, slow hash (bcrypt/argon2), never reversible encryption.
  - MFA required for the initial login, step-up MFA for sensitive downstream actions.
  - Access tokens are short-lived and stateless (fast to verify); refresh tokens are
    the actual revocation lever — this split is the key design decision to justify.
  - Auditability: every issuance/refresh/revocation logged with actor, IP, device.
  - Self-attack pass: "I'd target the refresh flow — replay an old refresh token, or
    try to use a token issued for one app against another (audience confusion)." →
    mitigate with the `aud` claim checked by every downstream service, not just `iss`.
- **Tradeoffs / scale**: stateless access tokens avoid a DB hit on every downstream
  request (scales well), at the cost of a ~15 min window where a revoked-but-not-yet-
  expired access token still verifies — acceptable given refresh tokens are the real
  revocation point and 15 min is an explicit, stated tradeoff, not an oversight.
- **What I'd do differently**: device-bound refresh tokens (tied to a device
  fingerprint/key) to make a bare token-theft-and-replay harder even before rotation
  catches it.
