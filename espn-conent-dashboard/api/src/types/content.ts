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

// 1. A `ContentEvent` discriminated union with variants `created`, `updated`, `published`,
// `archived` — each with a `contentId: string` and event-specific fields.
export type ContentEvent =
  | { type: "created"; contentId: string; authorId: string }
  | { type: "updated"; contentId: string; updatedFields: string[] }
  | { type: "published"; contentId: string; publishedAt: Date }
  | { type: "archived"; contentId: string; archivedAt: Date };

//2. A `SportContentCounts` type using `Record<Sport, number>` that maps each sport to
// a count of articles. Verify TypeScript enforces all five sports are present.
