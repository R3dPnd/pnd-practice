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