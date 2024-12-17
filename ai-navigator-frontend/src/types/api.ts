export interface Category {
  id: number;
  name: string;
  description?: string;
}

export interface DataSource {
  id: number;
  name: string;
  url: string;
  category_id: number;
  description?: string;
  is_preset: boolean;
  active: boolean;
  crawl_frequency: number;
  created_at: string;
  updated_at: string;
}

export interface DataSourceCreate {
  name: string;
  url: string;
  category_id: number;
  description?: string;
  crawl_frequency: number;
}

export interface DataSourceUpdate {
  name?: string;
  url?: string;
  description?: string;
  crawl_frequency?: number;
  active?: boolean;
}

export interface UserPreferences {
  categories: { id: number }[];
  keywords: string[];
  schedule_time: string;
  timezone: string;
}

export interface Report {
  id: number;
  title: string;
  content: string;
  created_at: string;
  user_id: number;
  format: 'pdf' | 'html' | 'text';
  type: string;
  date: string;
}

export interface ReportPreferences {
  delivery_method: string[];
  schedule_time: string;
  timezone: string;
  delivery_time: string;
  email?: string;
  email_enabled: boolean;
  pdf_enabled: boolean;
}

export interface ApiResponse<T> {
  status: string;
  message?: string;
  data: T;
}
