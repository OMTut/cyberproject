// Define interface for metrics
export interface DashboardMetrics {
  totalConversations: number;
  totalMessages: number;
  averageResponseTime: number;
  popularTopics: Array<Topic>;
}

// Define interface for topic
export interface Topic {
  topic: string;
  count: number;
}

// Define dashboard state interface
export interface DashboardState {
  metrics: DashboardMetrics | null;
  loading: boolean;
  error: string | null;
}

