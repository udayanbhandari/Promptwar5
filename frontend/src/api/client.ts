import type {
  BudgetItem,
  ErrorResponse,
  EventCreatePayload,
  EventDetailResponse,
  EventResponse,
  PlanResponse,
  RiskScenario,
  ShareCreatePayload,
  SharedPlanResponse,
  TaskItem,
  VendorBriefOutput,
  VendorItem,
  WhatIfBudgetRequest,
  WhatIfBudgetResponse,
} from '../types';

const DEFAULT_BASE = 'http://localhost:8000';

export interface ApiRequestOptions {
  method?: string;
  headers?: Record<string, string>;
  body?: string;
  signal?: AbortSignal;
}

export class ApiError extends Error {
  status: number;
  error: string;
  details?: unknown;

  constructor(message: string, status: number, error: string, details?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.error = error;
    this.details = details;
  }
}

export function getApiBaseUrl(): string {
  return import.meta.env.VITE_API_URL || DEFAULT_BASE;
}

async function parseJson<T>(response: Response): Promise<T> {
  const text = await response.text();
  if (!text) return {} as T;
  try {
    return JSON.parse(text) as T;
  } catch {
    return {} as T;
  }
}

async function request<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const url = `${getApiBaseUrl()}${path}`;
  const { signal, headers, ...rest } = options;

  const response = await fetch(url, {
    ...rest,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    signal,
  });

  if (!response.ok) {
    const payload = (await parseJson<ErrorResponse>(response)) ?? {
      error: 'request_failed',
      message: 'Request failed',
    };
    throw new ApiError(
      payload.message || 'Request failed',
      response.status,
      payload.error || 'request_failed',
      payload.details,
    );
  }

  return parseJson<T>(response);
}

export const api = {
  getEvents: (signal?: AbortSignal) => request<EventResponse[]>('/api/v1/events', { method: 'GET', signal }),
  createEvent: (payload: EventCreatePayload, signal?: AbortSignal) =>
    request<EventResponse>('/api/v1/events', { method: 'POST', body: JSON.stringify(payload), signal }),
  getEvent: (id: string, signal?: AbortSignal) => request<EventDetailResponse>(`/api/v1/events/${id}`, { method: 'GET', signal }),
  updateEvent: (id: string, payload: Partial<EventCreatePayload>, signal?: AbortSignal) =>
    request<EventResponse>(`/api/v1/events/${id}`, { method: 'PATCH', body: JSON.stringify(payload), signal }),
  generatePlan: (eventId: string, signal?: AbortSignal) =>
    request<PlanResponse>(`/api/v1/events/${eventId}/generate-plan`, { method: 'POST', signal }),
  getPlan: (eventId: string, signal?: AbortSignal) => request<PlanResponse>(`/api/v1/events/${eventId}/plan`, { method: 'GET', signal }),
  updateTask: (taskId: string, payload: Partial<TaskItem>, signal?: AbortSignal) =>
    request<TaskItem>(`/api/v1/events/tasks/${taskId}`, { method: 'PATCH', body: JSON.stringify(payload), signal }),
  getRunsheet: (eventId: string, signal?: AbortSignal) =>
    request<{ event_id: string; runsheet: unknown[] }>(`/api/v1/events/${eventId}/runsheet`, { method: 'GET', signal }),
  getRisks: (eventId: string, signal?: AbortSignal) => request<RiskScenario[]>(`/api/v1/events/${eventId}/risks`, { method: 'GET', signal }),
  generateRisks: (eventId: string, signal?: AbortSignal) =>
    request<RiskScenario[]>(`/api/v1/events/${eventId}/risks/generate`, { method: 'POST', signal }),
  simulateRisk: (eventId: string, riskId: string, signal?: AbortSignal) =>
    request<{ before_budget: { total: number }; after_budget: { total: number }; affected_tasks: unknown[]; fallback_steps: string }>(`/api/v1/events/${eventId}/risks/${riskId}/simulate`, { method: 'POST', signal }),
  getBudgetWhatIf: (eventId: string, payload: WhatIfBudgetRequest, signal?: AbortSignal) =>
    request<WhatIfBudgetResponse>(`/api/v1/events/${eventId}/budget/what-if`, { method: 'POST', body: JSON.stringify(payload), signal }),
  applyBudget: (eventId: string, payload: WhatIfBudgetRequest, signal?: AbortSignal) =>
    request<BudgetItem[]>(`/api/v1/events/${eventId}/budget/apply`, { method: 'POST', body: JSON.stringify(payload), signal }),
  getVendors: (eventId: string, signal?: AbortSignal) =>
    request<VendorItem[]>(`/api/v1/events/${eventId}/vendors`, { method: 'GET', signal }),
  generateVendorBrief: (eventId: string, category: string, signal?: AbortSignal) =>
    request<VendorBriefOutput>(`/api/v1/events/${eventId}/vendors/${encodeURIComponent(category)}/brief`, { method: 'POST', signal }),
  patchVendor: (vendorId: string, payload: Partial<VendorItem>, signal?: AbortSignal) =>
    request<VendorItem>(`/api/v1/vendors/${vendorId}`, { method: 'PATCH', body: JSON.stringify(payload), signal }),
  createShareLink: (eventId: string, payload: ShareCreatePayload, signal?: AbortSignal) =>
    request<{ share_url: string; token: string }>(`/api/v1/events/${eventId}/share`, { method: 'POST', body: JSON.stringify(payload), signal }),
  getSharedPlan: (token: string, signal?: AbortSignal) =>
    request<SharedPlanResponse>(`/api/v1/shared/${token}`, { method: 'GET', signal }),
  revokeShare: (eventId: string, shareId: string, signal?: AbortSignal) =>
    request<{ message: string }>(`/api/v1/events/${eventId}/share/${shareId}`, { method: 'DELETE', signal }),
};

export const typedEndpoints = api;
