# Disney/ESPN Business Operations Engineering — Interview Prep

**Stack:** TypeScript · Node.js · React · GraphQL · OpenSearch · Docker · CI/CD

> **Why not Java?** The actual DEEP&T job description specifies JavaScript/TypeScript, Node.js,
> React, GraphQL, and OpenSearch. This entire guide is built around that stack.

---

## What You Are Building

An internal **ESPN Content Operations Dashboard** — the kind of tool Disney's Business Operations
team actually ships. Editors use it to search, filter, and manage content (articles, videos,
show metadata) published across ESPN.com and Disney+.

```
espn-content-ops/
├── api/          Node.js + TypeScript backend (Fastify + Apollo Server)
├── ui/           React + TypeScript frontend (Vite + TanStack Query + Apollo Client)
└── docker-compose.yml
```

Complete each module in order. Every code block is a real file you create or a real command
you run. By the end you have a working project you can demo in the interview.

---

## Prerequisites — Install These First

| Tool | Version | Install |
|------|---------|---------|
| Node.js | 20 LTS | https://nodejs.org |
| Docker Desktop | latest | https://docker.com/products/docker-desktop |
| Git | any | https://git-scm.com |

Verify everything works:

```bash
node --version      # should print v20.x.x
npm --version       # should print 10.x.x
docker --version    # should print Docker version 24.x or higher
```

---

## Project Setup (Do This Once)

```bash
# 1. Create the project root
mkdir espn-content-ops
cd espn-content-ops

# 2. Create the two sub-projects
mkdir api ui

# 3. Initialize git
git init
echo "node_modules/" > .gitignore
echo "dist/" >> .gitignore
echo ".env" >> .gitignore
```

---

## Module 1: TypeScript Fundamentals

**Time: 4–6 hours**
**You will learn:** How to model a content domain with types that prevent entire classes of
runtime bugs — so a mistyped field on an article is caught at compile time, not during a
live playoff broadcast.

---

### Step 1.1 — Initialize the API project

```bash
cd api
npm init -y
npm install -D typescript @types/node tsx
npx tsc --init
```

### Step 1.2 — Configure TypeScript strictly

Open `api/tsconfig.json` and replace the entire file with:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",
    "paths": {
      "@types/*": ["./src/types/*"],
      "@services/*": ["./src/services/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Why each flag matters:**
- `strict: true` — enables `strictNullChecks`, `noImplicitAny`, and five others. Never turn this off.
- `noUncheckedIndexedAccess` — `array[0]` returns `T | undefined`, not `T`. Catches off-by-one bugs.
- `noImplicitReturns` — every code path must return a value. No silent `undefined` returns.

### Step 1.3 — Create the content domain types

```bash
mkdir -p src/types
```

Create `api/src/types/content.ts`:

```typescript
// String literal unions — use these instead of enums.
// They serialize to plain strings in JSON, enums do not.
export type ContentStatus = "draft" | "published" | "archived" | "scheduled";
export type ContentType = "article" | "video" | "gallery" | "scoreboard";
export type Sport = "football" | "basketball" | "baseball" | "hockey" | "soccer";

export interface Author {
  id: string;
  displayName: string;
  email: string;
  avatarUrl?: string;
}

export interface ContentItem {
  id: string;
  slug: string;
  title: string;
  type: ContentType;
  status: ContentStatus;
  sport: Sport;
  author: Author;
  tags: string[];
  publishedAt: Date | null;
  updatedAt: Date;
  metadata: ContentMetadata;
}

export interface ContentMetadata {
  wordCount?: number;
  duration?: number;
  imageCount?: number;
  [key: string]: unknown;
}
```

Create `api/src/types/api.ts`:

```typescript
import type { ContentItem, Sport, ContentStatus } from "./content";

// Generic wrapper — one definition works for any response shape
export interface ApiResponse<T> {
  data: T;
  meta: {
    total: number;
    page: number;
    pageSize: number;
  };
  timestamp: string;
}

// Discriminated union — forces callers to check success before accessing data
export type ApiResult<T> =
  | { success: true; data: T }
  | { success: false; error: string; code: number };

// Utility types — derive new types from existing ones without duplication
export type UpdateContentRequest = Partial<
  Pick<ContentItem, "title" | "status" | "tags" | "sport">
>;

export type CreateContentRequest = Omit<ContentItem, "id" | "publishedAt" | "updatedAt">;

export type ContentListItem = Pick<
  ContentItem,
  "id" | "slug" | "title" | "type" | "status" | "sport" | "publishedAt"
>;

export interface SearchFilters {
  sport?: Sport;
  status?: ContentStatus;
  tags?: string[];
  query?: string;
  page?: number;
  pageSize?: number;
  dateRange?: { from?: Date; to?: Date };
}

export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

export interface AppConfig {
  readonly port: number;
  readonly jwtSecret: string;
  readonly opensearchUrl: string;
  readonly contentfulSpaceId: string;
  readonly contentfulDeliveryToken: string;
  readonly contentfulPreviewToken: string;
}
```

### Step 1.4 — Verify TypeScript is working

Create `api/src/types/index.ts`:

```typescript
export * from "./content";
export * from "./api";
```

Run the type checker:

```bash
npx tsc --noEmit
# Should print nothing (no errors)
```

---

### Module 1 — Interview Question

> **"What is the difference between `type` and `interface` in TypeScript?"**

**Answer to practice out loud:**
Both describe object shapes. Use `interface` for domain objects — it produces cleaner error
messages and supports declaration merging (useful for extending third-party library types).
Use `type` for everything else: unions (`"draft" | "published"`), intersections, mapped types,
and tuples. In this project every content domain object is an `interface`; all unions and
utility combinations are `type`.

---

### Module 1 — Exercise

Add these types to `api/src/types/content.ts`:

1. A `ContentEvent` discriminated union with variants `created`, `updated`, `published`,
   `archived` — each with a `contentId: string` and event-specific fields.
2. A `SportContentCounts` type using `Record<Sport, number>` that maps each sport to
   a count of articles. Verify TypeScript enforces all five sports are present.

---

## Module 2: Node.js & API Development

**Time: 5–7 hours**
**You will learn:** How to build a Fastify API where cross-cutting concerns (auth, logging,
error handling) are enforced by the framework, not by hoping every developer remembers.

---

### Step 2.1 — Install dependencies

```bash
# Make sure you are in api/
npm install fastify @fastify/cors @fastify/jwt @fastify/rate-limit fastify-plugin
npm install @sinclair/typebox @fastify/type-provider-typebox
npm install pino pino-pretty
npm install -D @types/node vitest
```

### Step 2.2 — Create the config loader

Create `api/src/config.ts`:

```typescript
import type { AppConfig } from "./types/api";

// Load config from environment variables at startup.
// Crashing early with a clear message is better than a cryptic runtime failure.
export function loadConfig(): AppConfig {
  const required = [
    "JWT_SECRET",
    "OPENSEARCH_URL",
    "CONTENTFUL_SPACE_ID",
    "CONTENTFUL_DELIVERY_TOKEN",
    "CONTENTFUL_PREVIEW_TOKEN",
  ];

  const missing = required.filter((key) => !process.env[key]);
  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(", ")}`);
  }

  return {
    port: parseInt(process.env["PORT"] ?? "4000", 10),
    jwtSecret: process.env["JWT_SECRET"]!,
    opensearchUrl: process.env["OPENSEARCH_URL"]!,
    contentfulSpaceId: process.env["CONTENTFUL_SPACE_ID"]!,
    contentfulDeliveryToken: process.env["CONTENTFUL_DELIVERY_TOKEN"]!,
    contentfulPreviewToken: process.env["CONTENTFUL_PREVIEW_TOKEN"]!,
  };
}
```

### Step 2.3 — Create the error handler plugin

```bash
mkdir -p src/plugins
```

Create `api/src/plugins/error-handler.ts`:

```typescript
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";

// fp() (fastify-plugin) prevents scope encapsulation so this handler
// catches errors from ALL child routes, not just the ones in this plugin's scope.
export const errorHandlerPlugin: FastifyPluginAsync = fp(async (app) => {
  app.setErrorHandler((error, request, reply) => {
    const statusCode = error.statusCode ?? 500;

    // Log full error details server-side for debugging
    request.log.error({
      err: error,
      requestId: request.id,
      url: request.url,
      method: request.method,
    });

    // Send sanitized response to client — never expose stack traces
    reply.status(statusCode).send({
      error: {
        code: error.code ?? "INTERNAL_ERROR",
        message: statusCode >= 500 ? "An unexpected error occurred" : error.message,
        requestId: request.id,
      },
    });
  });
});
```

### Step 2.4 — Create the auth plugin

Create `api/src/plugins/auth.ts`:

```typescript
import fp from "fastify-plugin";
import type { FastifyPluginAsync, FastifyRequest } from "fastify";

// Extend Fastify's type definitions so request.user is typed everywhere —
// no casting or any-ing needed in route handlers
declare module "fastify" {
  interface FastifyRequest {
    user: {
      id: string;
      email: string;
      role: "editor" | "admin" | "viewer";
    };
  }
  interface FastifyInstance {
    authenticate: (request: FastifyRequest) => Promise<void>;
  }
}

export const authPlugin: FastifyPluginAsync = fp(async (app) => {
  app.decorateRequest("user", null);

  app.decorate("authenticate", async (request: FastifyRequest) => {
    await request.jwtVerify();
    // jwtVerify throws 401 automatically if token is missing or invalid
  });
});
```

### Step 2.5 — Create the health routes

```bash
mkdir -p src/routes
```

Create `api/src/routes/health.ts`:

```typescript
import type { FastifyPluginAsync } from "fastify";

export const healthRoutes: FastifyPluginAsync = async (app) => {
  // Liveness: is the process alive? Container orchestrators restart on failure.
  app.get("/health/live", async () => ({
    status: "ok",
    timestamp: new Date().toISOString(),
  }));

  // Readiness: can this instance serve traffic? Load balancers route away on failure.
  app.get("/health/ready", async (_request, reply) => {
    // In a real system, check OpenSearch and Contentful connectivity here
    // For now, return ready immediately
    return reply.status(200).send({
      status: "ready",
      checks: [],
      timestamp: new Date().toISOString(),
    });
  });
};
```

### Step 2.6 — Create the content routes

Create `api/src/routes/content.ts`:

```typescript
import { Type } from "@sinclair/typebox";
import type { FastifyPluginAsync } from "fastify";

// Define the query schema once — Fastify uses it for both validation AND docs.
// Invalid requests are rejected with 400 before they touch business logic.
const ContentQuerySchema = Type.Object({
  sport: Type.Optional(
    Type.Union([
      Type.Literal("football"),
      Type.Literal("basketball"),
      Type.Literal("baseball"),
      Type.Literal("hockey"),
      Type.Literal("soccer"),
    ])
  ),
  status: Type.Optional(
    Type.Union([
      Type.Literal("draft"),
      Type.Literal("published"),
      Type.Literal("archived"),
    ])
  ),
  q: Type.Optional(Type.String({ minLength: 1, maxLength: 200 })),
  page: Type.Optional(Type.Integer({ minimum: 1, default: 1 })),
  pageSize: Type.Optional(Type.Integer({ minimum: 1, maximum: 100, default: 20 })),
});

const UpdateContentSchema = Type.Partial(
  Type.Object({
    status: Type.Union([
      Type.Literal("draft"),
      Type.Literal("published"),
      Type.Literal("archived"),
    ]),
    tags: Type.Array(Type.String()),
    title: Type.String({ minLength: 1, maxLength: 500 }),
  })
);

export const contentRoutes: FastifyPluginAsync = async (app) => {
  app.get(
    "/content",
    {
      schema: { querystring: ContentQuerySchema },
      preHandler: [app.authenticate],
    },
    async (request) => {
      const { sport, status, q, page, pageSize } = request.query as any;

      // Stub response — replaced with real ContentService in Module 5
      return {
        items: [],
        total: 0,
        page: page ?? 1,
        pageSize: pageSize ?? 20,
        filters: { sport, status, query: q },
        requestedBy: request.user.id,
      };
    }
  );

  app.patch(
    "/content/:id",
    {
      schema: {
        params: Type.Object({ id: Type.String({ minLength: 1 }) }),
        body: UpdateContentSchema,
      },
      preHandler: [app.authenticate],
    },
    async (request, reply) => {
      const { id } = request.params as { id: string };
      const updates = request.body as any;

      // Authorization check: viewers cannot publish
      if (updates.status === "published" && request.user.role === "viewer") {
        return reply.status(403).send({
          error: { code: "FORBIDDEN", message: "Viewers cannot publish content" },
        });
      }

      request.log.info({
        event: "content.update",
        contentId: id,
        updates,
        updatedBy: request.user.id,
      });

      return { id, ...updates, updatedAt: new Date().toISOString() };
    }
  );
};
```

### Step 2.7 — Wire everything together

Create `api/src/app.ts`:

```typescript
import Fastify from "fastify";
import { TypeBoxTypeProvider } from "@fastify/type-provider-typebox";
import cors from "@fastify/cors";
import jwt from "@fastify/jwt";
import rateLimit from "@fastify/rate-limit";

import { authPlugin } from "./plugins/auth";
import { errorHandlerPlugin } from "./plugins/error-handler";
import { healthRoutes } from "./routes/health";
import { contentRoutes } from "./routes/content";
import type { AppConfig } from "./types/api";

export function buildApp(config: AppConfig) {
  const app = Fastify({
    logger: {
      level: process.env["LOG_LEVEL"] ?? "info",
      transport:
        process.env["NODE_ENV"] === "development" ? { target: "pino-pretty" } : undefined,
    },
    genReqId: () => crypto.randomUUID(),
  }).withTypeProvider<TypeBoxTypeProvider>();

  app.register(cors, {
    origin: process.env["ALLOWED_ORIGINS"]?.split(",") ?? ["http://localhost:3000"],
    credentials: true,
  });

  app.register(rateLimit, { max: 200, timeWindow: "1 minute" });

  app.register(jwt, {
    secret: config.jwtSecret,
    sign: { expiresIn: "8h" },
  });

  app.register(errorHandlerPlugin);
  app.register(authPlugin);

  app.register(healthRoutes, { prefix: "/api/v1" });
  app.register(contentRoutes, { prefix: "/api/v1" });

  return app;
}
```

Create `api/src/server.ts`:

```typescript
import { buildApp } from "./app";
import { loadConfig } from "./config";

const config = loadConfig();
const app = buildApp(config);

app.listen({ port: config.port, host: "0.0.0.0" }, (err) => {
  if (err) {
    app.log.error(err);
    process.exit(1);
  }
});
```

### Step 2.8 — Add npm scripts

Edit `api/package.json` and add a `"scripts"` section:

```json
{
  "scripts": {
    "dev": "NODE_ENV=development JWT_SECRET=dev-secret OPENSEARCH_URL=http://localhost:9200 CONTENTFUL_SPACE_ID=fake CONTENTFUL_DELIVERY_TOKEN=fake CONTENTFUL_PREVIEW_TOKEN=fake tsx src/server.ts",
    "build": "tsc",
    "typecheck": "tsc --noEmit",
    "start": "node dist/server.js",
    "test": "vitest run"
  }
}
```

### Step 2.9 — Start the server and test it

```bash
# From api/
npm run dev
```

In a second terminal, test the endpoints:

```bash
# Health check — should return 200 {"status":"ok",...}
curl http://localhost:4000/api/v1/health/live

# Protected route without token — should return 401
curl http://localhost:4000/api/v1/content

# Generate a test token (use Node REPL or a small script):
node -e "
const jwt = require('jsonwebtoken');
const token = jwt.sign({ id: 'u1', email: 'editor@espn.com', role: 'editor' }, 'dev-secret');
console.log(token);
"

# Use the token — should return 200 with empty items array
curl -H "Authorization: Bearer <paste-token-here>" http://localhost:4000/api/v1/content

# Test validation — should return 400
curl -H "Authorization: Bearer <token>" "http://localhost:4000/api/v1/content?sport=cricket"
```

---

### Module 2 — Interview Question

> **"How do you prevent internal error details from leaking to API clients?"**

**Answer to practice out loud:**
Centralized error handler plugin that intercepts every thrown error before it reaches the
client. The handler logs the full error (stack trace, request context, user ID) to the
server-side log aggregator, then sends a sanitized response to the client: the specific
message for 4xx errors (bad input, not found, forbidden), and a generic "unexpected error"
message for all 5xx. Every response includes a `requestId` so support staff can correlate
a user complaint with the exact log entry without exposing internals.

---

### Module 2 — Exercise

Add `POST /api/v1/webhooks/contentful` to `api/src/routes/content.ts`:
1. Read a `x-contentful-webhook-secret` header
2. Compare it to `process.env.CONTENTFUL_WEBHOOK_SECRET` using `crypto.timingSafeEqual`
   (prevents timing attacks — do NOT use `===` for secret comparison)
3. Return 401 if missing or wrong, 200 with `{ synced: true }` if valid
4. Log `event: "webhook.received"` with the content ID from the request body

---

## Module 3: React Patterns

**Time: 5–7 hours**
**You will learn:** How to structure a React dashboard so every component has one job,
server state is managed with TanStack Query instead of hand-rolled `useEffect`, and
the app doesn't stutter when a 200-row table updates.

---

### Step 3.1 — Initialize the UI project

```bash
# From the espn-content-ops/ root
cd ui
npm create vite@latest . -- --template react-ts
npm install
npm install @tanstack/react-query @tanstack/react-query-devtools
npm install react-router-dom
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

### Step 3.2 — Set up TanStack Query

Edit `ui/src/main.tsx`:

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./index.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,     // data stays fresh for 30s — no redundant refetches
      retry: 1,              // retry once on failure, then show error
      refetchOnWindowFocus: true,  // refresh when editor switches back to the tab
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </React.StrictMode>
);
```

### Step 3.3 — Create the API client

```bash
mkdir -p src/lib src/types src/hooks src/components/ContentList src/pages
```

Create `ui/src/lib/api-client.ts`:

```typescript
const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:4000/api/v1";

function getToken(): string | null {
  return localStorage.getItem("auth_token");
}

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const token = getToken();

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error?.error?.message ?? `HTTP ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const contentApi = {
  listContent: (params: Record<string, string | number | undefined>) => {
    const query = new URLSearchParams(
      Object.entries(params)
        .filter(([, v]) => v !== undefined)
        .map(([k, v]) => [k, String(v)])
    ).toString();
    return apiFetch<any>(`/content${query ? `?${query}` : ""}`);
  },

  updateContent: (id: string, updates: Record<string, unknown>) =>
    apiFetch<any>(`/content/${id}`, {
      method: "PATCH",
      body: JSON.stringify(updates),
    }),
};
```

### Step 3.4 — Create query key factory and hooks

Create `ui/src/hooks/useContentItems.ts`:

```typescript
import {
  useQuery,
  useMutation,
  useQueryClient,
  keepPreviousData,
} from "@tanstack/react-query";
import { contentApi } from "../lib/api-client";

// Centralized query key factory — keeps cache keys consistent.
// queryKeys.contentItems() invalidates ALL content list queries at once.
export const queryKeys = {
  contentItems: (filters?: Record<string, unknown>) =>
    ["content", "list", filters] as const,
  contentItem: (id: string) => ["content", "detail", id] as const,
};

export function useContentItems(filters: Record<string, unknown> = {}) {
  return useQuery({
    queryKey: queryKeys.contentItems(filters),
    queryFn: () => contentApi.listContent(filters as any),
    placeholderData: keepPreviousData, // show old data while new data loads
  });
}

export function useUpdateContentStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, status }: { id: string; status: string }) =>
      contentApi.updateContent(id, { status }),

    // Optimistic update: reflect the change immediately, roll back on error
    onMutate: async ({ id, status }) => {
      await queryClient.cancelQueries({ queryKey: queryKeys.contentItems() });
      const previous = queryClient.getQueriesData({ queryKey: ["content", "list"] });

      queryClient.setQueriesData(
        { queryKey: ["content", "list"] },
        (old: any) =>
          old
            ? {
                ...old,
                items: old.items?.map((item: any) =>
                  item.id === id ? { ...item, status } : item
                ),
              }
            : old
      );

      return { previous };
    },

    onError: (_err, _vars, context) => {
      if (context?.previous) {
        context.previous.forEach(([key, data]) => {
          queryClient.setQueryData(key, data);
        });
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.contentItems() });
    },
  });
}
```

### Step 3.5 — Create the ContentTable component

Create `ui/src/components/ContentList/ContentTable.tsx`:

```tsx
import { memo, useCallback } from "react";

interface ContentItem {
  id: string;
  title: string;
  sport: string;
  status: string;
  publishedAt: string | null;
}

interface ContentTableProps {
  items: ContentItem[];
  total: number;
  onStatusChange?: (id: string, status: string) => void;
}

// memo() prevents re-render when parent updates but these props haven't changed.
// In a 200-row table this avoids re-rendering every row when one row changes.
const ContentRow = memo(function ContentRow({
  item,
  onStatusChange,
}: {
  item: ContentItem;
  onStatusChange?: (id: string, status: string) => void;
}) {
  // useCallback stabilizes the reference — without it memo() on this component
  // is useless because every render creates a new function object
  const handlePublish = useCallback(() => {
    onStatusChange?.(item.id, "published");
  }, [item.id, onStatusChange]);

  const statusColors: Record<string, string> = {
    published: "bg-green-100 text-green-800",
    draft: "bg-yellow-100 text-yellow-800",
    archived: "bg-gray-100 text-gray-800",
  };

  return (
    <tr className="border-b hover:bg-gray-50">
      <td className="py-3 px-4 font-medium">{item.title}</td>
      <td className="py-3 px-4 capitalize">{item.sport}</td>
      <td className="py-3 px-4">
        <span
          className={`px-2 py-1 rounded text-xs font-medium ${statusColors[item.status] ?? ""}`}
        >
          {item.status}
        </span>
      </td>
      <td className="py-3 px-4 text-sm text-gray-500">
        {item.publishedAt ? new Date(item.publishedAt).toLocaleDateString() : "—"}
      </td>
      <td className="py-3 px-4">
        {item.status !== "published" && (
          <button
            onClick={handlePublish}
            className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            Publish
          </button>
        )}
      </td>
    </tr>
  );
});

export function ContentTable({ items, total, onStatusChange }: ContentTableProps) {
  return (
    <div>
      <p className="text-sm text-gray-500 mb-4">
        Showing {items.length} of {total} items
      </p>
      <table className="w-full border rounded">
        <thead className="bg-gray-50 text-left text-sm font-semibold text-gray-600">
          <tr>
            <th className="py-3 px-4">Title</th>
            <th className="py-3 px-4">Sport</th>
            <th className="py-3 px-4">Status</th>
            <th className="py-3 px-4">Published</th>
            <th className="py-3 px-4">Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <ContentRow key={item.id} item={item} onStatusChange={onStatusChange} />
          ))}
          {items.length === 0 && (
            <tr>
              <td colSpan={5} className="py-8 text-center text-gray-400">
                No content found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
```

### Step 3.6 — Create the ContentList page

Create `ui/src/pages/ContentListPage.tsx`:

```tsx
import { useState, useDeferredValue, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { useContentItems, useUpdateContentStatus } from "../hooks/useContentItems";
import { ContentTable } from "../components/ContentList/ContentTable";

export function ContentListPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchInput, setSearchInput] = useState(searchParams.get("q") ?? "");
  // useDeferredValue: keeps the input responsive while the results update
  const deferredSearch = useDeferredValue(searchInput);

  const filters = {
    sport: searchParams.get("sport") ?? undefined,
    status: searchParams.get("status") ?? undefined,
    q: deferredSearch || undefined,
    page: parseInt(searchParams.get("page") ?? "1", 10),
    pageSize: 20,
  };

  const { data, isLoading, error } = useContentItems(filters);
  const { mutate: updateStatus } = useUpdateContentStatus();

  // Persist search to URL so filters survive page refresh
  useEffect(() => {
    const next = new URLSearchParams(searchParams);
    if (deferredSearch) next.set("q", deferredSearch);
    else next.delete("q");
    setSearchParams(next, { replace: true });
  }, [deferredSearch]);

  if (error) {
    return (
      <div className="p-8 text-red-600">
        Failed to load content: {(error as Error).message}
      </div>
    );
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Content Operations</h1>

      {/* Filters */}
      <div className="flex gap-4 mb-6">
        <input
          type="search"
          placeholder="Search content..."
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          className="px-4 py-2 border rounded w-64"
        />
        <select
          value={searchParams.get("sport") ?? ""}
          onChange={(e) => {
            const next = new URLSearchParams(searchParams);
            if (e.target.value) next.set("sport", e.target.value);
            else next.delete("sport");
            setSearchParams(next);
          }}
          className="px-4 py-2 border rounded"
        >
          <option value="">All sports</option>
          <option value="football">Football</option>
          <option value="basketball">Basketball</option>
          <option value="baseball">Baseball</option>
          <option value="hockey">Hockey</option>
          <option value="soccer">Soccer</option>
        </select>
        <select
          value={searchParams.get("status") ?? ""}
          onChange={(e) => {
            const next = new URLSearchParams(searchParams);
            if (e.target.value) next.set("status", e.target.value);
            else next.delete("status");
            setSearchParams(next);
          }}
          className="px-4 py-2 border rounded"
        >
          <option value="">All statuses</option>
          <option value="draft">Draft</option>
          <option value="published">Published</option>
          <option value="archived">Archived</option>
        </select>
        {(searchParams.get("sport") || searchParams.get("status") || searchInput) && (
          <button
            onClick={() => {
              setSearchInput("");
              setSearchParams({});
            }}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
          >
            Clear filters
          </button>
        )}
      </div>

      {/* Results */}
      {isLoading ? (
        <div className="py-12 text-center text-gray-400">Loading...</div>
      ) : (
        <ContentTable
          items={data?.items ?? []}
          total={data?.total ?? 0}
          onStatusChange={(id, status) => updateStatus({ id, status })}
        />
      )}
    </div>
  );
}
```

Replace `ui/src/App.tsx` with:

```tsx
import { Routes, Route } from "react-router-dom";
import { ContentListPage } from "./pages/ContentListPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<ContentListPage />} />
    </Routes>
  );
}
```

### Step 3.7 — Start the UI and verify it loads

```bash
# From ui/
npm run dev
```

Open `http://localhost:5173`. You should see the Content Operations page with the search
bar and filter dropdowns. It will show "No content found" until the API returns real data.

---

### Module 3 — Interview Question

> **"Why use TanStack Query instead of `useEffect` + `useState` for fetching?"**

**Answer to practice out loud:**
Manual `useEffect` data fetching has at least five bugs waiting to happen: no deduplication
(two components mount, two requests fire), no loading state for subsequent fetches, no
background refresh, no cache (every mount refetches), and race conditions when the component
unmounts before the fetch resolves. TanStack Query solves all of these with a single hook
call. It also handles optimistic updates, pagination, and infinite scroll patterns that would
each require significant custom code. The real value is that the happy path and all the edge
cases are tested by the library maintainers — I don't have to rediscover those bugs.

---

### Module 3 — Exercise

1. Add a pagination row below the table with "Previous" and "Next" buttons. Read the current
   page from URL params and write the new page back to URL params on click.
2. The "Next" button should be disabled when `items.length < pageSize` (you're on the last page).

---

## Module 4: GraphQL Client Development

**Time: 4–5 hours**
**You will learn:** How to set up Apollo Server on the backend and Apollo Client on the
frontend with end-to-end TypeScript types — so GraphQL feels like calling a typed function,
not writing query strings and hoping.

---

### Step 4.1 — Install Apollo Server on the backend

```bash
# From api/
npm install @apollo/server graphql graphql-tag
```

### Step 4.2 — Define the GraphQL schema

```bash
mkdir -p src/graphql
```

Create `api/src/graphql/schema.ts`:

```typescript
import { gql } from "graphql-tag";

export const typeDefs = gql`
  type Author {
    id: ID!
    displayName: String!
    email: String!
    avatarUrl: String
  }

  type ContentItem {
    id: ID!
    slug: String!
    title: String!
    type: ContentType!
    status: ContentStatus!
    sport: Sport!
    author: Author!
    tags: [String!]!
    publishedAt: String
    updatedAt: String!
  }

  type ContentPage {
    items: [ContentItem!]!
    total: Int!
    page: Int!
    pageSize: Int!
  }

  enum ContentType { ARTICLE VIDEO GALLERY SCOREBOARD }
  enum ContentStatus { DRAFT PUBLISHED ARCHIVED SCHEDULED }
  enum Sport { FOOTBALL BASKETBALL BASEBALL HOCKEY SOCCER }

  input ContentFiltersInput {
    sport: Sport
    status: ContentStatus
    query: String
    page: Int
    pageSize: Int
  }

  input UpdateContentInput {
    title: String
    status: ContentStatus
    tags: [String!]
  }

  type Query {
    contentItems(filters: ContentFiltersInput): ContentPage!
    contentItem(id: ID!): ContentItem
  }

  type Mutation {
    updateContent(id: ID!, input: UpdateContentInput!): ContentItem!
    publishContent(id: ID!): ContentItem!
  }
`;
```

### Step 4.3 — Write the resolvers

Create `api/src/graphql/resolvers.ts`:

```typescript
import { GraphQLError } from "graphql";

interface RequestContext {
  user: { id: string; email: string; role: string };
}

export const resolvers = {
  Query: {
    contentItems: async (
      _: unknown,
      { filters }: { filters?: Record<string, unknown> },
      context: RequestContext
    ) => {
      // Stub — replace with real ContentService in Module 5
      console.log("contentItems queried by", context.user.id, "filters:", filters);
      return { items: [], total: 0, page: 1, pageSize: 20 };
    },

    contentItem: async (_: unknown, { id }: { id: string }) => {
      console.log("contentItem queried:", id);
      return null;
    },
  },

  Mutation: {
    updateContent: async (
      _: unknown,
      { id, input }: { id: string; input: Record<string, unknown> },
      context: RequestContext
    ) => {
      console.log("updateContent by", context.user.id, id, input);
      return { id, ...input, slug: id, type: "ARTICLE", status: "DRAFT", sport: "FOOTBALL",
        author: { id: context.user.id, displayName: "Editor", email: context.user.email },
        tags: [], updatedAt: new Date().toISOString() };
    },

    publishContent: async (
      _: unknown,
      { id }: { id: string },
      context: RequestContext
    ) => {
      if (context.user.role === "viewer") {
        // Use GraphQLError — it maps to the right error shape in the response
        throw new GraphQLError("Viewers cannot publish content", {
          extensions: { code: "FORBIDDEN" },
        });
      }

      return { id, slug: id, title: "Published Article", type: "ARTICLE",
        status: "PUBLISHED", sport: "FOOTBALL",
        author: { id: context.user.id, displayName: "Editor", email: context.user.email },
        tags: [], publishedAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
    },
  },
};
```

### Step 4.4 — Register Apollo Server with Fastify

```bash
npm install @as-integrations/fastify
```

Add Apollo to `api/src/app.ts` — insert before the `return app` line:

```typescript
// Add these imports at the top of app.ts:
import { ApolloServer } from "@apollo/server";
import { fastifyApolloDrainPlugin, fastifyApolloHandler } from "@as-integrations/fastify";
import { typeDefs } from "./graphql/schema";
import { resolvers } from "./graphql/resolvers";

// Add this inside buildApp, before the return:
const apollo = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [fastifyApolloDrainPlugin(app)],
});

await apollo.start();

app.route({
  url: "/graphql",
  method: ["GET", "POST", "OPTIONS"],
  handler: fastifyApolloHandler(apollo, {
    context: async (request) => ({ user: (request as any).user }),
  }),
});
```

### Step 4.5 — Install Apollo Client on the frontend

```bash
# From ui/
npm install @apollo/client graphql
```

Create `ui/src/lib/apollo-client.ts`:

```typescript
import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
  from,
} from "@apollo/client";
import { setContext } from "@apollo/client/link/context";
import { onError } from "@apollo/client/link/error";

const httpLink = createHttpLink({
  uri: `${import.meta.env.VITE_API_URL ?? "http://localhost:4000"}/graphql`,
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem("auth_token");
  return {
    headers: { ...headers, ...(token ? { authorization: `Bearer ${token}` } : {}) },
  };
});

const errorLink = onError(({ graphQLErrors, networkError }) => {
  graphQLErrors?.forEach((err) => {
    if (err.extensions?.["code"] === "UNAUTHENTICATED") {
      window.location.href = "/login";
    }
  });
  if (networkError) console.error("Network error:", networkError);
});

export const apolloClient = new ApolloClient({
  link: from([errorLink, authLink, httpLink]),
  cache: new InMemoryCache({
    typePolicies: {
      ContentItem: { keyFields: ["id"] },
    },
  }),
});
```

### Step 4.6 — Write a typed GraphQL query and use it in a component

Create `ui/src/lib/queries/content.ts`:

```typescript
import { gql } from "@apollo/client";
import type { TypedDocumentNode } from "@apollo/client";

interface ContentPage {
  items: {
    id: string;
    slug: string;
    title: string;
    type: string;
    status: string;
    sport: string;
    publishedAt: string | null;
    author: { id: string; displayName: string };
  }[];
  total: number;
  page: number;
  pageSize: number;
}

interface ContentFiltersInput {
  sport?: string;
  status?: string;
  query?: string;
  page?: number;
  pageSize?: number;
}

export const GET_CONTENT_ITEMS: TypedDocumentNode<
  { contentItems: ContentPage },
  { filters?: ContentFiltersInput }
> = gql`
  query GetContentItems($filters: ContentFiltersInput) {
    contentItems(filters: $filters) {
      items {
        id
        slug
        title
        type
        status
        sport
        publishedAt
        author {
          id
          displayName
        }
      }
      total
      page
      pageSize
    }
  }
`;

export const PUBLISH_CONTENT: TypedDocumentNode<
  { publishContent: { id: string; status: string; publishedAt: string } },
  { id: string }
> = gql`
  mutation PublishContent($id: ID!) {
    publishContent(id: $id) {
      id
      status
      publishedAt
    }
  }
`;
```

### Step 4.7 — Test the GraphQL endpoint

Restart the API server and open `http://localhost:4000/graphql` in your browser.
You should see Apollo Sandbox. Run this query:

```graphql
query {
  contentItems(filters: { sport: FOOTBALL }) {
    items {
      id
      title
      status
    }
    total
  }
}
```

It should return `{ contentItems: { items: [], total: 0 } }`.

---

### Module 4 — Interview Question

> **"When would you use GraphQL instead of REST?"**

**Answer to practice out loud:**
GraphQL wins when multiple clients need different subsets of the same data, or when the
data is highly relational and a REST client would need multiple round trips to assemble
a complete view. In ESPN's case, a mobile app might need only `title` and `thumbnailUrl`
for a content card, while the editorial dashboard needs the full metadata. GraphQL lets
each client declare exactly what it needs. REST wins for simpler CRUD operations, webhooks,
file uploads, and anywhere HTTP-level caching (CDN, Varnish) is important — GraphQL POST
requests aren't cacheable the same way. In this project I use both: REST for webhooks and
health checks, GraphQL for the editorial data graph.

---

### Module 4 — Exercise

1. Add a `GET_CONTENT_ITEM` query that fetches a single item by ID including `tags`, `metadata`
   fields, and the full author object.
2. Create a `ContentDetailPage` at `/content/:id` that uses this query and shows a loading
   skeleton while the data arrives.
3. Wire the content title in `ContentTable` to navigate to this detail page on click.

---

## Module 5: Headless CMS Integration

**Time: 3–4 hours**
**You will learn:** How to fetch content from Contentful, transform it to your domain model,
and handle CMS user roles — so your API is the single source of truth, not a pass-through
that leaks CMS internals to the frontend.

---

### Step 5.1 — Install the Contentful SDK

```bash
# From api/
npm install contentful
```

### Step 5.2 — Create the ContentService

```bash
mkdir -p src/services
```

Create `api/src/services/content-service.ts`:

```typescript
import contentful from "contentful";
import type { AppConfig, SearchFilters, PaginatedResult, ContentListItem } from "../types";

interface ContentfulArticleFields {
  title: contentful.EntryFieldTypes.Symbol;
  slug: contentful.EntryFieldTypes.Symbol;
  sport: contentful.EntryFieldTypes.Symbol;
  tags: contentful.EntryFieldTypes.Array<contentful.EntryFieldTypes.Symbol>;
  body?: contentful.EntryFieldTypes.RichText;
  wordCount?: contentful.EntryFieldTypes.Integer;
}

type ContentfulArticle = contentful.EntrySkeletonType<ContentfulArticleFields, "article">;

export class ContentService {
  private deliveryClient: contentful.ContentfulClientApi<undefined>;
  private previewClient: contentful.ContentfulClientApi<undefined>;

  constructor(config: AppConfig) {
    this.deliveryClient = contentful.createClient({
      space: config.contentfulSpaceId,
      accessToken: config.contentfulDeliveryToken,
    });

    // Preview client can see draft entries — only offer to editors/admins
    this.previewClient = contentful.createClient({
      space: config.contentfulSpaceId,
      accessToken: config.contentfulPreviewToken,
      host: "preview.contentful.com",
    });
  }

  async list(
    filters: SearchFilters & { userRole?: string; includeUnpublished?: boolean }
  ): Promise<PaginatedResult<ContentListItem>> {
    const usePreview =
      filters.includeUnpublished && filters.userRole !== "viewer";
    const client = usePreview ? this.previewClient : this.deliveryClient;

    const response = await client.getEntries<ContentfulArticle>({
      content_type: "article",
      ...(filters.sport ? { "fields.sport": filters.sport } : {}),
      limit: filters.pageSize ?? 20,
      skip: ((filters.page ?? 1) - 1) * (filters.pageSize ?? 20),
      order: ["-sys.updatedAt"],
    });

    return {
      items: response.items.map((entry) => this.transformEntry(entry)),
      total: response.total,
      page: filters.page ?? 1,
      pageSize: filters.pageSize ?? 20,
    };
  }

  async findById(contentfulId: string): Promise<ContentListItem | null> {
    try {
      const entry = await this.deliveryClient.getEntry<ContentfulArticle>(contentfulId);
      return this.transformEntry(entry);
    } catch {
      return null;
    }
  }

  // Transformation layer — isolates CMS schema changes from your domain model.
  // If Contentful renames a field, you fix it here and nowhere else.
  private transformEntry(
    entry: contentful.Entry<ContentfulArticle>
  ): ContentListItem {
    return {
      id: entry.sys.id,
      slug: entry.fields.slug as string,
      title: entry.fields.title as string,
      type: "article",
      status: entry.sys.publishedAt ? "published" : "draft",
      sport: (entry.fields.sport as string).toLowerCase() as any,
      publishedAt: entry.sys.publishedAt ? new Date(entry.sys.publishedAt) : null,
    };
  }
}
```

### Step 5.3 — Render CMS rich text safely in the UI

```bash
# From ui/
npm install @contentful/rich-text-react-renderer @contentful/rich-text-types
```

Create `ui/src/components/RichTextRenderer.tsx`:

```tsx
import { documentToReactComponents } from "@contentful/rich-text-react-renderer";
import { BLOCKS, INLINES } from "@contentful/rich-text-types";
import type { Document, Block, Inline } from "@contentful/rich-text-types";

// NEVER use dangerouslySetInnerHTML for CMS content — XSS risk if the CMS
// is compromised or an editor pastes malicious content.
// This renderer uses a whitelist of allowed node types.
const renderOptions = {
  renderNode: {
    [BLOCKS.PARAGRAPH]: (_node: Block | Inline, children: React.ReactNode) => (
      <p className="mb-4 leading-relaxed text-gray-700">{children}</p>
    ),
    [BLOCKS.HEADING_2]: (_node: Block | Inline, children: React.ReactNode) => (
      <h2 className="text-2xl font-bold mt-8 mb-4">{children}</h2>
    ),
    [BLOCKS.HEADING_3]: (_node: Block | Inline, children: React.ReactNode) => (
      <h3 className="text-xl font-semibold mt-6 mb-3">{children}</h3>
    ),
    [BLOCKS.EMBEDDED_ASSET]: (node: any) => {
      const url: string = node.data?.target?.fields?.file?.url ?? "";
      const title: string = node.data?.target?.fields?.title ?? "";
      // Validate the URL is from Contentful's CDN before rendering
      if (!url.startsWith("//images.ctfassets.net")) return null;
      return (
        <img
          src={`https:${url}`}
          alt={title}
          className="w-full rounded my-4"
          loading="lazy"
        />
      );
    },
    // Strip external links — editors should not embed arbitrary external URLs
    [INLINES.HYPERLINK]: (node: any, children: React.ReactNode) => {
      const url: string = node.data?.uri ?? "";
      const isInternal =
        url.startsWith("/") ||
        url.includes("espn.com") ||
        url.includes("disney.com");
      if (!isInternal) return <span>{children}</span>;
      return (
        <a href={url} className="text-blue-600 underline">
          {children}
        </a>
      );
    },
  },
};

export function RichTextRenderer({ document }: { document: Document }) {
  return (
    <div className="prose max-w-none">
      {documentToReactComponents(document, renderOptions)}
    </div>
  );
}
```

---

### Module 5 — Interview Question

> **"How do you keep your search index in sync when content changes in the CMS?"**

**Answer to practice out loud:**
Event-driven sync via webhooks. Contentful sends an HTTP POST to our API whenever an entry
is published, updated, or deleted. The webhook handler validates the request signature with
`crypto.timingSafeEqual`, identifies the content ID, fetches the canonical version from
Contentful, and upserts it into OpenSearch. This is eventually consistent — there's a brief
gap between the publish event and the index update — which is acceptable for an editorial
dashboard. For a higher-reliability system I would put a queue between the webhook and the
indexing worker so failed indexing jobs are retried automatically without dropping events.
A periodic full re-sync job acts as a safety net for any events that were missed.

---

### Module 5 — Exercise

1. Add a `syncFromCMS(contentfulId: string)` method to `ContentService` that fetches
   the entry from Contentful and logs `event: "content.cms_sync"` with the content ID,
   title, and sport.
2. Wire this to the webhook endpoint from Module 2's exercise.
3. Handle the case where the Contentful entry is not found (404) — log a warning and
   return without throwing.

---

## Module 6: OpenSearch / Elasticsearch

**Time: 5–6 hours**
**You will learn:** How to design an index for content search, write queries that balance
relevance and speed, and run aggregations that give editors instant analytics.

---

### Step 6.1 — Start OpenSearch locally

Add `docker-compose.yml` to the project root (`espn-content-ops/`):

```yaml
version: "3.9"

services:
  opensearch:
    image: opensearchproject/opensearch:2.11.0
    environment:
      - discovery.type=single-node
      - DISABLE_SECURITY_PLUGIN=true
      - OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m
    ports:
      - "9200:9200"
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:9200/_cluster/health || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 8

  opensearch-dashboards:
    image: opensearchproject/opensearch-dashboards:2.11.0
    ports:
      - "5601:5601"
    environment:
      - OPENSEARCH_HOSTS=["http://opensearch:9200"]
    depends_on:
      - opensearch
```

```bash
# From espn-content-ops/ root
docker compose up -d

# Verify OpenSearch is running
curl http://localhost:9200/_cluster/health
# Should print {"status":"green",...}
```

### Step 6.2 — Install the OpenSearch client

```bash
# From api/
npm install @opensearch-project/opensearch
```

### Step 6.3 — Create the index

```bash
mkdir -p src/opensearch/indices src/opensearch/query-builders
```

Create `api/src/opensearch/indices/content-index.ts`:

```typescript
import { Client } from "@opensearch-project/opensearch";

export const CONTENT_INDEX = "espn_content_v1";
export const CONTENT_ALIAS = "espn_content";

export async function createContentIndex(client: Client): Promise<void> {
  const exists = await client.indices.exists({ index: CONTENT_INDEX });
  if (exists.body) {
    console.log(`Index ${CONTENT_INDEX} already exists`);
    return;
  }

  await client.indices.create({
    index: CONTENT_INDEX,
    body: {
      settings: {
        number_of_shards: 2,
        number_of_replicas: 1,
        analysis: {
          analyzer: {
            // Lowercase + remove stopwords + stem: "Running Backs" matches "running back"
            content_analyzer: {
              type: "custom",
              tokenizer: "standard",
              filter: ["lowercase", "stop", "snowball"],
            },
          },
        },
      },
      mappings: {
        properties: {
          id:    { type: "keyword" },   // exact match, no text analysis
          slug:  { type: "keyword" },
          title: {
            type: "text",
            analyzer: "content_analyzer",
            // 'fields' lets you search (text) AND sort/aggregate (keyword)
            // on the same field without storing it twice
            fields: { keyword: { type: "keyword", ignore_above: 512 } },
          },
          body:       { type: "text", analyzer: "content_analyzer" },
          type:       { type: "keyword" },
          status:     { type: "keyword" },
          sport:      { type: "keyword" },
          tags:       { type: "keyword" },
          publishedAt: { type: "date" },
          updatedAt:   { type: "date" },
          author: {
            type: "object",
            properties: {
              id:          { type: "keyword" },
              displayName: { type: "text", fields: { keyword: { type: "keyword" } } },
            },
          },
        },
      },
    },
  });

  await client.indices.putAlias({ index: CONTENT_INDEX, name: CONTENT_ALIAS });
  console.log(`Created index ${CONTENT_INDEX} with alias ${CONTENT_ALIAS}`);
}
```

### Step 6.4 — Build the query builder

Create `api/src/opensearch/query-builders/content-query.ts`:

```typescript
import type { SearchFilters } from "../../types";

export function buildContentQuery(filters: SearchFilters) {
  const must: object[] = [];
  const filter: object[] = [];

  if (filters.query) {
    // multi_match: search title, body, and tags.
    // title^3 means a title match is 3x more relevant than a body match.
    must.push({
      multi_match: {
        query: filters.query,
        fields: ["title^3", "body", "tags^2"],
        type: "best_fields",
        fuzziness: "AUTO",           // handles typos
        minimum_should_match: "75%", // at least 75% of query terms must match
      },
    });
  }

  // IMPORTANT: use filter (not must) for exact-match conditions.
  // filter clauses are cached by OpenSearch — much faster for repeated queries.
  // must affects the relevance score; filter does not.
  if (filters.sport)  filter.push({ term: { sport: filters.sport } });
  if (filters.status) filter.push({ term: { status: filters.status } });
  if (filters.tags?.length) filter.push({ terms: { tags: filters.tags } });

  if (filters.dateRange) {
    filter.push({
      range: {
        publishedAt: {
          ...(filters.dateRange.from ? { gte: filters.dateRange.from.toISOString() } : {}),
          ...(filters.dateRange.to   ? { lte: filters.dateRange.to.toISOString() }   : {}),
        },
      },
    });
  }

  const page = filters.page ?? 1;
  const pageSize = filters.pageSize ?? 20;

  return {
    query: {
      bool: {
        must: must.length > 0 ? must : [{ match_all: {} }],
        filter,
      },
    },
    // Sort by relevance score when searching, by date when browsing
    sort: filters.query ? [{ _score: "desc" }] : [{ publishedAt: "desc" }],
    from: (page - 1) * pageSize,
    size: pageSize,
    highlight: {
      fields: {
        title: { number_of_fragments: 1, fragment_size: 150 },
        body:  { number_of_fragments: 2, fragment_size: 200 },
      },
    },
    // Aggregations — answer analytics questions without extra queries
    aggs: {
      by_sport:  { terms: { field: "sport", size: 10 } },
      by_status: { terms: { field: "status", size: 5 } },
      published_over_time: {
        date_histogram: {
          field: "publishedAt",
          calendar_interval: "week",
          format: "yyyy-MM-dd",
          min_doc_count: 1,
        },
      },
    },
    // Return only the fields needed for the list view — don't send full body text
    _source: ["id", "slug", "title", "type", "status", "sport", "publishedAt", "author"],
  };
}
```

### Step 6.5 — Create the SearchService

Create `api/src/services/search-service.ts`:

```typescript
import { Client } from "@opensearch-project/opensearch";
import { CONTENT_ALIAS, createContentIndex } from "../opensearch/indices/content-index";
import { buildContentQuery } from "../opensearch/query-builders/content-query";
import type { SearchFilters, ContentListItem, PaginatedResult } from "../types";

export class SearchService {
  private client: Client;

  constructor(opensearchUrl: string) {
    this.client = new Client({ node: opensearchUrl });
  }

  async initialize(): Promise<void> {
    await createContentIndex(this.client);
  }

  async search(
    filters: SearchFilters
  ): Promise<PaginatedResult<ContentListItem> & { aggregations: unknown }> {
    const body = buildContentQuery(filters);

    const response = await this.client.search({ index: CONTENT_ALIAS, body });
    const { hits, aggregations } = response.body as any;

    return {
      items: hits.hits.map((hit: any) => ({
        ...hit._source,
        highlights: hit.highlight,
      })),
      total: hits.total.value,
      page: filters.page ?? 1,
      pageSize: filters.pageSize ?? 20,
      aggregations,
    };
  }

  async indexContent(item: ContentListItem & { body?: string }): Promise<void> {
    await this.client.index({
      index: CONTENT_ALIAS,
      id: item.id,
      body: item,
      refresh: "wait_for",
      // In high-throughput production use refresh: false (eventual consistency)
    });
  }

  async deleteContent(id: string): Promise<void> {
    await this.client.delete({ index: CONTENT_ALIAS, id });
  }
}
```

### Step 6.6 — Seed test data and verify search

Create `api/src/scripts/seed-opensearch.ts`:

```typescript
import { SearchService } from "../services/search-service";

const searchService = new SearchService("http://localhost:9200");

const articles = [
  { id: "1", slug: "brady-retires", title: "Tom Brady Announces Retirement",
    type: "article" as const, status: "published" as const, sport: "football" as const,
    publishedAt: new Date("2024-02-01"), body: "Seven-time Super Bowl champion Tom Brady..." },
  { id: "2", slug: "lebron-season", title: "LeBron James Season Preview",
    type: "article" as const, status: "published" as const, sport: "basketball" as const,
    publishedAt: new Date("2024-10-01"), body: "Lakers star LeBron James enters his 22nd season..." },
  { id: "3", slug: "world-series", title: "World Series Preview 2024",
    type: "article" as const, status: "draft" as const, sport: "baseball" as const,
    publishedAt: null, body: "This year's World Series matchup promises..." },
];

async function seed() {
  await searchService.initialize();
  for (const article of articles) {
    await searchService.indexContent(article);
    console.log(`Indexed: ${article.title}`);
  }
  console.log("Done.");
}

seed().catch(console.error);
```

```bash
# From api/
npx tsx src/scripts/seed-opensearch.ts

# Test the search directly against OpenSearch
curl -X POST "http://localhost:9200/espn_content/_search" \
  -H "Content-Type: application/json" \
  -d '{"query":{"match":{"title":"Brady"}}}'
```

---

### Module 6 — Interview Question

> **"What is the difference between `must` and `filter` in an OpenSearch bool query?"**

**Answer to practice out loud:**
Both require documents to match, but `must` contributes to the relevance `_score` and
`filter` does not. More importantly, `filter` results are cached by OpenSearch — subsequent
requests with the same filter clause skip the computation entirely. For exact-match conditions
like `sport: "football"` or `status: "published"`, always use `filter`. A document doesn't
become "more relevant" because it's about football — so putting it in `must` adds noise to
the score with no benefit, and burns cache. Use `must` only for full-text search clauses
where match quality genuinely signals relevance. Getting this wrong causes measurably slower
queries at scale.

---

### Module 6 — Exercise

1. Add `GET /api/v1/content/:id/similar` to the content routes.
2. Use OpenSearch's `more_like_this` query, filtering to the same `sport`.
3. Return 5 results in `ContentListItem` shape.
4. Open `http://localhost:5601` (OpenSearch Dashboards) and use Dev Tools to run the query
   manually first, then translate it to the SDK call.

---

## Module 7: Testing Practices

**Time: 5–6 hours**
**You will learn:** How to write tests that catch real bugs — not tests that achieve coverage
by testing implementation details that change on every refactor.

---

### Step 7.1 — Configure Vitest

Add `api/vitest.config.ts`:

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
      exclude: ["dist/**", "src/scripts/**"],
    },
  },
});
```

### Step 7.2 — Write unit tests for the query builder

```bash
mkdir -p tests/unit/query-builders
```

Create `api/tests/unit/query-builders/content-query.test.ts`:

```typescript
import { describe, it, expect } from "vitest";
import { buildContentQuery } from "../../../src/opensearch/query-builders/content-query";

describe("buildContentQuery", () => {
  it("returns match_all when no filters are provided", () => {
    const query = buildContentQuery({ page: 1, pageSize: 20 });
    expect(query.query.bool.must).toEqual([{ match_all: {} }]);
    expect(query.query.bool.filter).toHaveLength(0);
  });

  it("adds multi_match clause for text queries", () => {
    const query = buildContentQuery({ query: "LeBron James" });
    expect(query.query.bool.must[0]).toMatchObject({
      multi_match: { query: "LeBron James", fuzziness: "AUTO" },
    });
  });

  it("places sport in filter, not must (performance critical)", () => {
    // This test protects a performance-critical behavior:
    // filter clauses are cached; must clauses are not.
    // Moving filters to must would cause measurable query slowdowns at scale.
    const query = buildContentQuery({ sport: "basketball" });
    expect(query.query.bool.filter).toContainEqual({ term: { sport: "basketball" } });
    expect(JSON.stringify(query.query.bool.must)).not.toContain("basketball");
  });

  it("sorts by score when searching, by date when browsing", () => {
    const withSearch = buildContentQuery({ query: "touchdown" });
    const withoutSearch = buildContentQuery({});
    expect(withSearch.sort).toContainEqual({ _score: "desc" });
    expect(withoutSearch.sort).toContainEqual({ publishedAt: "desc" });
  });

  it("paginates correctly", () => {
    const query = buildContentQuery({ page: 3, pageSize: 10 });
    expect(query.from).toBe(20); // (3-1) * 10
    expect(query.size).toBe(10);
  });

  it("adds date range filter when provided", () => {
    const from = new Date("2024-01-01");
    const to = new Date("2024-12-31");
    const query = buildContentQuery({ dateRange: { from, to } });

    const rangeFilter = query.query.bool.filter.find((f: any) => f.range);
    expect(rangeFilter).toBeDefined();
    expect((rangeFilter as any).range.publishedAt.gte).toBe(from.toISOString());
  });
});
```

### Step 7.3 — Write an integration test for the route

```bash
mkdir -p tests/integration/routes
npm install -D @vitest/coverage-v8
```

Create `api/tests/integration/routes/content.test.ts`:

```typescript
import { describe, it, beforeAll, afterAll, expect, vi } from "vitest";
import { buildApp } from "../../../src/app";

// Integration tests: real route handlers, real middleware, real validation.
// Only external dependencies are mocked.
const testConfig = {
  port: 0,
  jwtSecret: "test-secret",
  opensearchUrl: "http://localhost:9200",
  contentfulSpaceId: "test",
  contentfulDeliveryToken: "test",
  contentfulPreviewToken: "test",
};

describe("Content Routes", () => {
  let app: ReturnType<typeof buildApp>;
  let editorToken: string;
  let viewerToken: string;

  beforeAll(async () => {
    app = buildApp(testConfig);
    await app.ready();

    editorToken = app.jwt.sign({ id: "u1", email: "editor@espn.com", role: "editor" });
    viewerToken = app.jwt.sign({ id: "u2", email: "viewer@espn.com", role: "viewer" });
  });

  afterAll(() => app.close());

  describe("GET /api/v1/content", () => {
    it("returns 401 without a token", async () => {
      const res = await app.inject({ method: "GET", url: "/api/v1/content" });
      expect(res.statusCode).toBe(401);
    });

    it("returns 200 for an authenticated editor", async () => {
      const res = await app.inject({
        method: "GET",
        url: "/api/v1/content",
        headers: { authorization: `Bearer ${editorToken}` },
      });
      expect(res.statusCode).toBe(200);
    });

    it("rejects an invalid sport enum value with 400", async () => {
      // This test protects schema validation — if validation were removed,
      // 'cricket' would reach business logic and cause unpredictable behavior
      const res = await app.inject({
        method: "GET",
        url: "/api/v1/content?sport=cricket",
        headers: { authorization: `Bearer ${editorToken}` },
      });
      expect(res.statusCode).toBe(400);
    });
  });

  describe("PATCH /api/v1/content/:id", () => {
    it("returns 403 when a viewer tries to publish", async () => {
      const res = await app.inject({
        method: "PATCH",
        url: "/api/v1/content/article-1",
        headers: { authorization: `Bearer ${viewerToken}` },
        payload: { status: "published" },
      });
      expect(res.statusCode).toBe(403);
      expect(res.json().error.code).toBe("FORBIDDEN");
    });

    it("allows an editor to change status", async () => {
      const res = await app.inject({
        method: "PATCH",
        url: "/api/v1/content/article-1",
        headers: { authorization: `Bearer ${editorToken}` },
        payload: { status: "archived" },
      });
      expect(res.statusCode).toBe(200);
    });
  });
});
```

### Step 7.4 — Create a test fixture factory

```bash
mkdir -p tests/fixtures
```

Create `api/tests/fixtures/content.ts`:

```typescript
import type { ContentListItem } from "../../src/types";

let counter = 0;

// Factory function — call with overrides to get a valid object for any test
// Don't create one hard-coded fixture object that all tests share and fight over
export function makeContentListItem(
  overrides: Partial<ContentListItem> = {}
): ContentListItem {
  counter++;
  return {
    id: `item-${counter}`,
    slug: `article-${counter}`,
    title: `Test Article ${counter}`,
    type: "article",
    status: "draft",
    sport: "football",
    publishedAt: null,
    ...overrides,
  };
}
```

### Step 7.5 — Run all tests

```bash
# From api/
npm test

# With coverage report
npm test -- --coverage
```

---

### Module 7 — Interview Question

> **"How do you decide what to unit test versus what to integration test?"**

**Answer to practice out loud:**
Unit tests verify isolated logic — ideal for pure functions like query builders, data
transformers, and utility functions. They're fast and precise. Integration tests verify
that layers work together through their real interfaces — ideal for routes, middleware
chains, and anything where the interaction between components is what matters. A route
test that mocks the route handler itself isn't testing anything real. I test the full
request-response cycle including auth, validation, error handling, and serialization.
The boundary: anything external (Contentful API, OpenSearch, a database) gets mocked
in integration tests because I don't control those systems; everything within my service
boundaries I try to hit for real.

---

### Module 7 — Exercise

1. Write a test for `PATCH /api/v1/content/:id` that verifies the request body is
   validated — sending `{ status: "invalid" }` should return 400.
2. Write a unit test for `ContentService.transformEntry` in isolation. Use a mock
   Contentful entry object and assert the returned `ContentListItem` fields.
3. In the UI (`ui/`), configure Vitest and write one test for `ContentTable` that renders
   two items and asserts both titles appear in the document.

---

## Module 8: Docker & CI/CD

**Time: 4–5 hours**
**You will learn:** How to containerize the API so it runs identically in every environment,
and how to build a CI pipeline that prevents broken code from reaching production.

---

### Step 8.1 — Write the Dockerfile

Create `api/Dockerfile`:

```dockerfile
# Multi-stage build: builder stage has all dev tools and compiles TypeScript.
# Production stage copies only compiled output + prod dependencies.
# Result: ~200MB image instead of ~900MB.

FROM node:20-alpine AS builder
WORKDIR /app

# Copy manifests first — Docker caches this layer until package.json changes.
# The expensive npm install only re-runs when dependencies actually change.
COPY package*.json tsconfig.json ./
RUN npm ci --include=dev

COPY src ./src
RUN npm run build

# ---- Production stage ----
FROM node:20-alpine AS production
WORKDIR /app

# Run as non-root — if a container escape happens, attacker is not root
RUN addgroup -S espn && adduser -S espn -G espn

COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

COPY --from=builder /app/dist ./dist

USER espn

EXPOSE 4000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD wget -qO- http://localhost:4000/api/v1/health/live || exit 1

CMD ["node", "dist/server.js"]
```

Create `api/.dockerignore`:

```
node_modules
dist
.env
*.log
tests
```

### Step 8.2 — Test the Docker build locally

```bash
# From api/
docker build -t espn-content-ops-api .

# Run it
docker run -p 4000:4000 \
  -e JWT_SECRET=test-secret \
  -e OPENSEARCH_URL=http://host.docker.internal:9200 \
  -e CONTENTFUL_SPACE_ID=fake \
  -e CONTENTFUL_DELIVERY_TOKEN=fake \
  -e CONTENTFUL_PREVIEW_TOKEN=fake \
  espn-content-ops-api

# Verify health check
curl http://localhost:4000/api/v1/health/live
```

### Step 8.3 — Write the CI pipeline

```bash
# From espn-content-ops/ root
mkdir -p .github/workflows
```

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Cancel duplicate runs — if you push twice, the first run is cancelled
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # ── Stage 1: Lint and type-check ───────────────────────────────────────────
  # Cheap and fast. Run first to fail fast before slower tests.
  lint-typecheck:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: api/package-lock.json

      - name: Install
        working-directory: api
        run: npm ci

      - name: Type check
        working-directory: api
        run: npm run typecheck

  # ── Stage 2: Tests ─────────────────────────────────────────────────────────
  test:
    name: Tests
    runs-on: ubuntu-latest
    needs: lint-typecheck   # only run if lint passes

    services:
      opensearch:
        image: opensearchproject/opensearch:2.11.0
        env:
          discovery.type: single-node
          DISABLE_SECURITY_PLUGIN: "true"
          OPENSEARCH_JAVA_OPTS: "-Xms512m -Xmx512m"
        ports:
          - 9200:9200
        options: >-
          --health-cmd "curl -sf http://localhost:9200/_cluster/health"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 10

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: api/package-lock.json

      - name: Install
        working-directory: api
        run: npm ci

      - name: Run tests
        working-directory: api
        run: npm test -- --coverage
        env:
          OPENSEARCH_URL: http://localhost:9200
          NODE_ENV: test
          JWT_SECRET: ci-test-secret
          CONTENTFUL_SPACE_ID: fake
          CONTENTFUL_DELIVERY_TOKEN: fake
          CONTENTFUL_PREVIEW_TOKEN: fake

  # ── Stage 3: Docker build ──────────────────────────────────────────────────
  # Only on main branch merges, only if tests passed
  build:
    name: Build & Push Docker Image
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'

    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v5
        with:
          context: ./api
          push: true
          # Tag with commit SHA (pinnable, rollback-safe) AND 'latest' (convenience)
          tags: |
            ghcr.io/${{ github.repository }}/api:${{ github.sha }}
            ghcr.io/${{ github.repository }}/api:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
          target: production
```

### Step 8.4 — Push to GitHub and watch the pipeline

```bash
# From espn-content-ops/
git add .
git commit -m "Add CI pipeline and Dockerfile"
git remote add origin https://github.com/YOUR_USERNAME/espn-content-ops.git
git push -u origin main
```

Open GitHub → Actions. You should see the pipeline run through lint → test → build.

---

### Module 8 — Interview Question

> **"What gates do you require before code reaches production?"**

**Answer to practice out loud:**
I think of CI as a risk filter — each stage catches a class of problem before it reaches
the next environment. Minimum gates I require: type-check and lint first (cheap, fail-fast);
unit and integration tests second (need service dependencies in CI); Docker build only after
all tests pass; production deploy requires a manual approval gate for a content ops system
where a bad deploy during a live event is immediately visible to millions of users. I also
require that every artifact is tagged with the exact commit SHA — not just `latest` — so
any deploy can be rolled back to a specific known-good build in under two minutes.

---

### Module 8 — Exercise

1. Add a `lint` script to `api/package.json` using ESLint with TypeScript support.
   Install: `npm install -D eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser`
2. Add an `.eslintrc.json` that enforces `no-console` (use the structured logger instead)
   and `@typescript-eslint/no-explicit-any`.
3. Add `npm run lint` as a step in the `lint-typecheck` job before `typecheck`.
4. Introduce a deliberate `console.log` in a route file, push, and verify the CI pipeline
   fails at the lint step.

---

## Module 9: Observability & Operational Readiness

**Time: 3–4 hours**
**You will learn:** How to instrument the API so incidents can be debugged in minutes,
what a production-ready service looks like beyond "it works," and how to write a runbook
that another engineer can execute at 2 AM.

---

### Step 9.1 — Add structured request logging

Create `api/src/plugins/logging.ts`:

```typescript
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";

export const loggingPlugin: FastifyPluginAsync = fp(async (app) => {
  app.addHook("onRequest", (request, _reply, done) => {
    request.log.info({
      event: "request.received",
      requestId: request.id,
      method: request.method,
      url: request.url,
      userAgent: request.headers["user-agent"],
    });
    done();
  });

  app.addHook("onResponse", (request, reply, done) => {
    request.log.info({
      event: "request.completed",
      requestId: request.id,
      statusCode: reply.statusCode,
      responseTimeMs: Math.round(reply.elapsedTime),
      // Flag slow requests for alerting — alert before users complain
      slow: reply.elapsedTime > 1000,
    });
    done();
  });
});
```

Register the plugin in `api/src/app.ts`:

```typescript
import { loggingPlugin } from "./plugins/logging";
// Add this line after the other plugin registrations:
app.register(loggingPlugin);
```

### Step 9.2 — Add request ID to all responses

In `api/src/plugins/error-handler.ts`, update the `onResponse` hook to always send `X-Request-ID`:

```typescript
// Add this hook inside the errorHandlerPlugin
app.addHook("onSend", (_request, reply, _payload, done) => {
  reply.header("X-Request-ID", _request.id);
  done();
});
```

### Step 9.3 — Harden the readiness check

Replace `api/src/routes/health.ts` with a version that actually checks dependencies:

```typescript
import type { FastifyPluginAsync, FastifyInstance } from "fastify";
import { Client } from "@opensearch-project/opensearch";

export const healthRoutes: FastifyPluginAsync = async (app) => {
  app.get("/health/live", async () => ({
    status: "ok",
    timestamp: new Date().toISOString(),
  }));

  app.get("/health/ready", async (_request, reply) => {
    const checks = await Promise.allSettled([
      checkOpenSearch(),
    ]);

    const results = [
      {
        name: "opensearch",
        status: checks[0]?.status === "fulfilled" ? "ok" : "degraded",
        error: checks[0]?.status === "rejected" ? String((checks[0] as any).reason) : undefined,
      },
    ];

    const allHealthy = results.every((r) => r.status === "ok");

    return reply.status(allHealthy ? 200 : 503).send({
      status: allHealthy ? "ready" : "degraded",
      checks: results,
      timestamp: new Date().toISOString(),
    });
  });
};

async function checkOpenSearch() {
  const client = new Client({ node: process.env["OPENSEARCH_URL"] ?? "http://localhost:9200" });
  const health = await client.cluster.health({ timeout: "3s" });
  if ((health.body as any).status === "red") {
    throw new Error("OpenSearch cluster status is red");
  }
}
```

### Step 9.4 — Write the runbook

Create `api/RUNBOOK.md`:

```markdown
# ESPN Content Ops API — Runbook

## Overview
Internal content operations API serving the ESPN editorial dashboard.
Port: 4000 | OpenSearch: 9200 | Health: GET /api/v1/health/ready

## First Steps for Any Incident
1. Check `GET /api/v1/health/ready` — identifies which dependency is failing
2. Search logs for the `requestId` from the error report
3. Look for `event: "request.completed"` with `slow: true` or 5xx status codes

## Incident Playbooks

### Search returns no results after a publish
**Symptom:** Editor publishes content; it doesn't appear in search for >2 minutes
**Check:** Search logs for `event: "webhook.received"` with the content ID
**If webhook was received but not indexed:**
  - POST /api/v1/admin/content/:id/reindex (requires admin role)
**If no webhook received:**
  - Check Contentful webhook settings at app.contentful.com
  - Manually trigger: POST /api/v1/admin/sync/full
  - Warning: full sync takes ~5 minutes and stresses the Contentful API rate limit

### API returning 503
**Check:** GET /api/v1/health/ready (shows which check failed)
**OpenSearch degraded:** Run `curl http://OPENSEARCH_HOST:9200/_cluster/health`
  - Status "red": one or more primary shards unavailable — escalate to infra
  - Status "yellow": replicas missing but reads/writes working — monitor, non-urgent

### Slow responses (>2s)
**Check:** Logs for `slow: true` — includes full request context including userId
**Common causes:**
  - OpenSearch query missing filter cache hit (check for `must` where `filter` should be used)
  - Missing `_source` filtering (query returning full document bodies for list views)
  - Contentful API latency spike (check status.contentful.com)

## Rollback
All images are tagged with commit SHA in GHCR.
To rollback: `docker pull ghcr.io/ORG/espn-content-ops/api:PREVIOUS_SHA`
Then redeploy with that tag.
```

---

### Module 9 — Interview Question

> **"How do you communicate a production incident to a non-technical stakeholder?"**

**Answer to practice out loud:**
I answer three questions they actually care about: what was impacted, for how long, and
what prevents it from happening again. I avoid technical jargon. A good communication
sounds like: "From 3:15 to 3:47 PM, our content search feature was showing results from
earlier in the day instead of the latest published content. Editors who published articles
during that window would have seen them not appear in search. The root cause was a missed
notification from our content management system. We've re-synced all content and are
adding automatic retries so missed notifications don't cause visible gaps in the future."
I follow up with a written incident summary within 24 hours — the written record matters
as much as the live communication.

---

### Module 9 — Exercise

1. Add `userId` to the `onRequest` log hook — the user isn't authenticated yet at that
   hook, so you'll need to move user logging to `onResponse` where the JWT has been verified.
2. Add a `slow_query` event that logs when an OpenSearch query takes longer than 500ms.
   Use `Date.now()` before and after the `client.search()` call in `SearchService`.
3. Write a test that verifies the `/health/ready` endpoint returns 503 when OpenSearch
   returns a "red" cluster status. Mock the OpenSearch client in the test.

---

## Module 10: AI-Assisted Development

**Time: 2–3 hours**
**You will learn:** How to use AI coding tools to go faster without introducing bugs,
and how to articulate your review process in an interview.

---

### The Core Principle

AI tools accelerate boilerplate and first drafts. You remain responsible for every line
that ships. The review process below is the skill the interview is testing — not whether
you use AI, but whether you use it with professional judgment.

---

### Step 10.1 — Your AI Code Review Checklist

Before accepting any non-trivial AI-generated code, verify each category:

```
CORRECTNESS
  [ ] Null/undefined inputs handled where possible?
  [ ] Error paths (catch blocks) handled?
  [ ] Empty array, zero, empty string cases?
  [ ] Async: race conditions possible? Cancellation handled?

SECURITY
  [ ] User input in a SQL/OpenSearch/shell template? (injection)
  [ ] Fetch call with a URL from user input? (SSRF)
  [ ] Secrets or PII being logged?
  [ ] Auth check present where action requires authorization?

FIT WITH OUR ARCHITECTURE
  [ ] Follows our error pattern (ApiResult<T>, not throw)?
  [ ] Uses structured logging (pino), not console.log?
  [ ] Business logic in service layer, not route handler?
  [ ] Duplicates something that already exists?

PERFORMANCE
  [ ] Fetching inside a loop (N+1)?
  [ ] Unbounded result set (missing pagination)?
  [ ] Large payload being buffered instead of streamed?

MAINTAINABILITY
  [ ] Magic strings/numbers that should be named constants?
  [ ] Function doing more than one thing?
  [ ] TypeScript `any` used where a real type is possible?
```

---

### Step 10.2 — Review This AI-Generated Code

The following bulk-publish route was generated by an AI assistant.
Find every problem before you look at the answer below.

```typescript
// AI-generated — DO NOT MERGE without review
app.post("/api/v1/content/bulk-publish", async (request, reply) => {
  const { ids } = request.body as { ids: string[] };

  const results = [];
  for (const id of ids) {
    const content = await db.query(`SELECT * FROM content WHERE id = '${id}'`);
    if (content) {
      await db.query(
        `UPDATE content SET status = 'published', published_at = NOW() WHERE id = '${id}'`
      );
      results.push({ id, success: true });
    }
  }

  console.log(`Published ${results.length} items`);
  return { results };
});
```

**Issues — check yours against this list:**

| # | Issue | Risk |
|---|-------|------|
| 1 | SQL injection in SELECT via string interpolation | Critical |
| 2 | SQL injection in UPDATE via string interpolation | Critical |
| 3 | No auth check — any unauthenticated request can bulk-publish | Critical |
| 4 | No input validation — `ids` could be absent or not an array | High |
| 5 | No limit on `ids` array size — could publish thousands at once or DoS the DB | High |
| 6 | N+1 query pattern — one SELECT + one UPDATE per ID in a loop | High |
| 7 | `console.log` instead of structured logger — not queryable in production | Medium |
| 8 | No audit trail — who bulk-published what and when? | Medium |
| 9 | No error handling — if any query throws, the request crashes | Medium |
| 10 | Casting `request.body as { ids: string[] }` bypasses Fastify schema validation | Medium |

---

### Step 10.3 — Write the fixed version yourself

Using the checklist and issues above, write the corrected route in
`api/src/routes/content.ts`. It should:
- Use Fastify schema validation (TypeBox) for the request body
- Require authentication with `preHandler: [app.authenticate]`
- Check that `request.user.role !== "viewer"` before proceeding
- Use parameterized queries (or the ORM equivalent — no string interpolation)
- Log `event: "content.bulk_publish"` with `ids`, `count`, and `publishedBy`
- Return `{ published: number, failed: Array<{ id: string; reason: string }> }`

---

### Module 10 — Interview Question

> **"How do you use AI coding tools, and what's your review process?"**

**Answer to practice out loud:**
I use AI tools for the parts of development where the output is cheap to verify: boilerplate,
test stubs, first drafts of documentation, and translating an API pattern I already understand
to a library I'm less familiar with. I treat every AI-generated code block the same way I'd
treat a PR from a junior engineer I haven't worked with before: plausible but unverified. I
work through a checklist covering correctness edge cases, security vectors (injection, SSRF,
data exposure), fit with our architecture and patterns, and performance (N+1 queries, missing
pagination). The security category gets the most scrutiny — AI models are trained on a corpus
that includes a lot of insecure patterns, and they'll confidently generate SQL injection or
fetch an arbitrary external URL without hesitation. At Disney, a security mistake in an
internal tool is still a security incident. AI helps me write faster; I remain responsible
for everything that ships.

---

## Interview Day Checklist

### The week before
- [ ] Complete all 10 modules in order
- [ ] Run `docker compose up` and verify the full stack (API + OpenSearch + UI) works
- [ ] Push to GitHub and watch the CI pipeline pass
- [ ] Open OpenSearch Dashboards (`http://localhost:5601`) and explore your indexed content

### The day before
- [ ] Read the job description line by line — map each requirement to a module
- [ ] Prepare a 2-minute answer: "Tell me about a system you built that needed to be reliable"
- [ ] Prepare a 2-minute answer: "Tell me about a technical decision you'd make differently"
- [ ] Be able to whiteboard the full system architecture from memory

### In the interview
- **Lead with the problem, not the implementation.** "I used TanStack Query because I
  needed cache invalidation and background refetching, and reinventing that with `useEffect`
  is a known source of subtle bugs — not because it's fashionable."
- **Say so when you don't know something, then reason forward.** "I haven't used that
  specific OpenSearch feature, but based on how bool queries work, I'd expect..."
- **Weave Disney-specific themes into technical answers:** reliability, auditability,
  security mindset, and clear communication with non-technical partners. These are the
  stated priorities of the Business Operations team.

---

## Quick Reference — Commands

```bash
# Start full local stack
docker compose up -d

# Start API in dev mode
cd api && npm run dev

# Start UI in dev mode
cd ui && npm run dev

# Run API tests
cd api && npm test

# Type-check without compiling
cd api && npm run typecheck

# Build Docker image
docker build -t espn-content-ops-api ./api

# Index test data into OpenSearch
cd api && npx tsx src/scripts/seed-opensearch.ts

# Check OpenSearch cluster health
curl http://localhost:9200/_cluster/health

# Open OpenSearch Dashboards
open http://localhost:5601
```
