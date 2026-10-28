export type EventType = 'wedding' | 'birthday' | 'community';
export type CurrencyCode = 'INR' | 'USD' | 'EUR' | 'GBP' | 'AED';
export type TaskStatus = 'pending' | 'in_progress' | 'completed';
export type VendorStatus = 'researching' | 'contacted' | 'quoted' | 'booked';

export interface ErrorResponse {
  error: string;
  message: string;
  details?: unknown;
}

export interface EventCreatePayload {
  title: string;
  event_type: EventType;
  target_date: string;
  guest_count: number;
  total_budget: number;
  currency: CurrencyCode;
  city: string;
  theme_style?: string | null;
  special_requirements?: string | null;
}

export interface BudgetItem {
  id?: string;
  category: string;
  item_name: string;
  estimated_cost: number;
  actual_cost: number;
  is_paid: boolean;
  priority: number;
  event_id?: string;
  created_at?: string;
}

export interface TaskItem {
  id?: string;
  title: string;
  category: string;
  due_date: string | null;
  status: TaskStatus;
  owner: string;
  depends_on: string[];
  is_day_of: boolean;
  start_time?: string | null;
  event_id?: string;
  created_at?: string;
}

export interface VendorItem {
  id?: string;
  category: string;
  name: string;
  status: VendorStatus;
  quoted_price: number;
  contact_info?: string | null;
  notes?: string | null;
  event_id?: string;
  created_at?: string;
}

export interface RiskScenario {
  id?: string;
  scenario_type: 'weather' | 'budget_cut' | 'vendor_flake' | 'guest_surge';
  trigger_name: string;
  mitigation_plan: string;
  budget_impact: number;
  is_activated: boolean;
  created_at?: string;
}

export interface EventResponse {
  id: string;
  title: string;
  event_type: EventType;
  target_date: string;
  guest_count: number;
  total_budget: number;
  currency: CurrencyCode;
  city: string;
  theme_style?: string | null;
  special_requirements?: string | null;
  created_at: string;
  updated_at: string;
}

export interface EventDetailResponse extends EventResponse {
  budget_items: BudgetItem[];
  tasks: TaskItem[];
  vendors: VendorItem[];
  risk_scenarios: RiskScenario[];
  share_links: ShareLink[];
}

export interface ShareLink {
  id?: string;
  event_id: string;
  token: string;
  is_active: boolean;
  expires_at?: string | null;
  view_count: number;
  created_at?: string;
  share_url?: string | null;
}

export interface BudgetSplitCategory {
  category: string;
  percentage: number;
  reason: string;
}

export interface BudgetSplitOutput {
  categories: BudgetSplitCategory[];
}

export interface PersonalizedIdea {
  aspect: 'theme' | 'decor' | 'food' | 'entertainment' | 'memorable_touch';
  title: string;
  description: string;
  cost_tier: 'low' | 'medium' | 'high';
  why_it_fits: string;
}

export interface IdeaOutput {
  ideas: PersonalizedIdea[];
}

export interface VendorCategoryItem {
  category: string;
  questions: string[];
  red_flags: string[];
}

export interface VendorCategoriesOutput {
  categories: VendorCategoryItem[];
}

export interface RiskScenarioItem {
  scenario_title: string;
  likelihood: 'low' | 'medium' | 'high';
  impact: 'low' | 'medium' | 'high';
  early_warning_sign: string;
  fallback_steps: string;
  cost_impact_percent: number;
}

export interface RiskScenarioOutput {
  risks: RiskScenarioItem[];
}

export interface VendorBriefOutput {
  enquiry_message: string;
  comparison_checklist: string[];
}

export interface PlanResponse {
  title?: string;
  event_id: string;
  used_fallback: boolean;
  budget: BudgetItem[];
  ideas: PersonalizedIdea[];
  vendor_categories: VendorCategoryItem[];
  tasks: TaskItem[];
  vendors: VendorItem[];
  warnings: string[];
}

export interface WhatIfBudgetRequest {
  total?: number;
  locked_categories?: Record<string, number>;
  guest_count?: number;
}

export interface WhatIfBudgetResponse {
  total: number;
  items: Array<{ category: string; amount: number }>;
  warnings: string[];
}

export interface ShareCreatePayload {
  expiry_days?: number;
  event_id: string;
}

export interface SharedPlanResponse {
  event_id: string;
  title: string;
  event_type: EventType;
  target_date: string;
  guest_count: number;
  city: string;
  theme_style?: string | null;
  budget: BudgetItem[];
  tasks: TaskItem[];
  vendors: VendorItem[];
  ideas: PersonalizedIdea[];
}
