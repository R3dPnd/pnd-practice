# REST Interview Quiz

Answer each question out loud (or in writing) before revealing the answer.

---

## Part 1 — HTTP Methods

**Q1:** What is the difference between PUT and PATCH?

<details>
<summary>Answer</summary>

- **PUT** replaces the entire resource. If you PUT a user with only `{ "name": "Alice" }`, all other fields are removed/reset.
- **PATCH** partially updates the resource. Only the fields you send are changed; others stay as-is.
- Use PATCH when updating one or two fields on a large object.

</details>

---

**Q2:** A client tries to create a new user with an email that already exists. What status code should the server return, and what is it called?

<details>
<summary>Answer</summary>

**409 Conflict** — the request conflicts with the current state of the resource (duplicate email).

</details>

---

**Q3:** What is the difference between 401 and 403?

<details>
<summary>Answer</summary>

- **401 Unauthorized** — the client is not authenticated (no token, or token is invalid/expired). Logging in may fix it.
- **403 Forbidden** — the client IS authenticated but does not have permission to access this resource. Logging in again will not help.

Memory trick: 401 = "Who are you?", 403 = "I know who you are, but you can't come in."

</details>

---

**Q4:** Match each status code to its meaning:

| Code | Meaning |
|------|---------|
| 200  | ? |
| 201  | ? |
| 204  | ? |
| 400  | ? |
| 404  | ? |
| 500  | ? |

<details>
<summary>Answer</summary>

| Code | Meaning |
|------|---------|
| 200  | OK — request succeeded |
| 201  | Created — POST succeeded, new resource created |
| 204  | No Content — success but no body (common for DELETE) |
| 400  | Bad Request — client sent invalid data |
| 404  | Not Found — resource doesn't exist |
| 500  | Internal Server Error — server-side failure |

</details>

---

## Part 2 — REST Design

**Q5:** Design REST endpoints for a blog with posts and comments. Write the full endpoint for each action:

| Action | Your answer |
|--------|-------------|
| List all posts | |
| Get one post | |
| Create a post | |
| Update a post (full replace) | |
| Delete a post | |
| List comments on a post | |
| Add a comment to a post | |
| Delete a specific comment | |

<details>
<summary>Answer</summary>

| Action | Endpoint |
|--------|----------|
| List all posts | `GET /posts` |
| Get one post | `GET /posts/{id}` |
| Create a post | `POST /posts` |
| Update a post (full replace) | `PUT /posts/{id}` |
| Delete a post | `DELETE /posts/{id}` |
| List comments on a post | `GET /posts/{id}/comments` |
| Add a comment to a post | `POST /posts/{id}/comments` |
| Delete a specific comment | `DELETE /posts/{id}/comments/{commentId}` |

Key rules:
- Nouns in URLs, not verbs (`/posts` not `/getPosts`)
- Plural resource names (`/posts` not `/post`)
- Nested resources for belongs-to relationships (`/posts/{id}/comments`)

</details>

---

## Part 3 — REST Concepts

**Q6:** What does "stateless" mean in REST?

<details>
<summary>Answer</summary>

Every request must contain all the information needed to process it. The server does not store any session state between requests. Authentication tokens, filters, and pagination parameters must all be sent with each request.

This makes REST APIs horizontally scalable — any server can handle any request.

</details>

---

**Q7:** What goes in the `Authorization` header? What is a Bearer token?

<details>
<summary>Answer</summary>

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

A **Bearer token** is a credential (usually a JWT) that grants access to a resource. Anyone who "bears" (possesses) the token can use it — hence "Bearer." The server validates the token on each request.

</details>

---

**Q8:** What is the difference between REST and SOAP?

<details>
<summary>Answer</summary>

| | REST | SOAP |
|--|------|------|
| Format | JSON or XML (flexible) | XML only (strict) |
| Protocol | HTTP | Any transport (HTTP, SMTP, etc.) |
| Standards | Lightweight, no strict spec | Heavy WS-* standards (WS-Security, etc.) |
| Usage | Web/mobile APIs | Enterprise/banking/legacy systems |
| Performance | Faster, smaller payloads | Slower, verbose XML |

Say: "REST is the modern standard for web APIs. SOAP is still found in enterprise environments, especially banking and insurance, because of its strict security and transaction standards."

</details>

---

**Q9:** A GET request to `/users/42` returns the user. The same request 10 seconds later returns the same user. A POST to `/users` creates a new user each time it's called. What REST property does GET have that POST does not?

<details>
<summary>Answer</summary>

**Idempotency** — calling the same request multiple times produces the same result.

- **GET, PUT, DELETE** are idempotent
- **POST** is NOT (each call creates a new resource)
- **PATCH** is NOT guaranteed to be idempotent (e.g., incrementing a counter)

Idempotency matters for retry logic — if a network error occurs, you can safely retry a GET or DELETE but not a POST.

</details>

---

## Part 4 — Quick-fire Round

Answer each in one sentence:

1. Where should authentication tokens be sent — URL params, request body, or headers?
2. What HTTP method is used when submitting an HTML form by default?
3. What does CORS stand for, and when does it matter?
4. What is the difference between a query parameter and a path parameter?
5. Should a DELETE endpoint return a body?

<details>
<summary>Answers</summary>

1. **Headers** (`Authorization: Bearer ...`) — never in URL params (logged in server access logs).
2. **POST** (or GET for search forms with `method="get"`).
3. **Cross-Origin Resource Sharing** — it matters when a browser makes a request from domain A to domain B (e.g., `localhost:3000` calling `localhost:8000`). The server must send CORS headers to allow it.
4. **Path parameter** identifies a specific resource (`/users/42` — the 42 is the path param). **Query parameter** filters or modifies (`/users?role=admin`).
5. Typically **no body** — return `204 No Content`. Some APIs return the deleted resource for confirmation, but `204` is the standard.

</details>
