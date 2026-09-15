# Worked example: secure file upload/storage service

Practice prompt 1 from `../notes.md`: users upload attachments, other users download
them by link. Full run through the framework in `../notes.md`, compressed to the key
beats — this is what "narrate it out loud" should actually sound like, not a diagram
substitute. Use it to check your own mock reps against, not to memorize verbatim.

- **Clarify**: Who uploads/downloads — authenticated users only, or public links?
  Assume: authenticated upload, shareable download link with configurable expiry/scope.
  Max file size (assume 5 GB), expected scale (assume 10M uploads/day), is malware
  scanning in scope (yes, ask explicitly since Security cares).
- **API**: `POST /uploads` (returns a pre-signed upload URL + file ID),
  `GET /files/{id}` (auth-checked, streams or redirects to blob storage),
  `POST /files/{id}/share` (creates a scoped, expiring share link).
- **Architecture**: client → API gateway (authN) → upload service issues a pre-signed
  URL directly to blob storage (S3/Azure Blob equivalent) so the API tier doesn't
  proxy multi-GB bytes → async virus-scan worker picks up new objects off an event
  queue → metadata DB (owner, ACL, scan status) gates whether `GET /files/{id}` will
  serve the object yet.
- **Deep dive** (likely steered here): the malware-scan pipeline — object lands in a
  quarantine bucket first, scanner (e.g. ClamAV or a vendor API) consumes from the
  event queue, only moves the object to the servable bucket on a clean verdict; a
  flagged file is quarantined and the uploader is notified, never silently served.
- **Security pass**:
  - AuthZ: every `GET` re-checks the caller against the file's ACL, not just a
    guessable ID — this is the `03_safe_path_resolver` lesson at the architecture
    level (never trust a client-supplied path/ID to imply access).
  - Share links: signed, short-TTL tokens (not the raw file ID) so a leaked link
    expires and can be revoked by rotating a per-file signing key.
  - Encryption at rest (server-side, provider-managed keys is fine to state as a
    baseline) and TLS in transit for both upload and download legs.
  - Self-attack pass: "if I were attacking this, I'd try uploading an executable
    renamed with an image extension to slip past extension-based filtering — so
    scanning must be content-based (magic bytes / actual AV), not extension-based."
    Also: link enumeration (sequential/guessable IDs) → use random UUIDs/opaque tokens.
- **Tradeoffs / scale**: pre-signed direct-to-blob upload avoids the API tier becoming
  a bandwidth bottleneck; scanning is async so upload latency isn't blocked on it, at
  the cost of a short window where a file exists but isn't yet servable — acceptable
  since it's not servable until scanned clean anyway.
- **What I'd do differently with more time**: per-org key management (customer-managed
  encryption keys) instead of provider-managed, and a content-defined dedup/CDC layer
  to cut storage costs at scale.
