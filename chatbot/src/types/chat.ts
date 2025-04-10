// Define types for our chat messages
export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

// Define analysis result type for attack detection
export interface AnalysisResult {
  isAttack: boolean;
  attackType: string;
  confidence: number;
  matches?: string[];
  [key: string]: any;
}

// Define API response type
export interface ApiResponse {
  // Normal response fields
  response?: string;
  message?: string;
  generated_text?: string;
  
  // Attack detection response fields
  status?: 'rejected' | 'success';
  reason?: string;
  analysis?: AnalysisResult;
  
  // Allow other properties
  [key: string]: any;
}

