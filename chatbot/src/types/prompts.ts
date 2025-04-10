// Define prompt types for API responses

export interface Prompt {
  id: string;
  text: string;
  timestamp: string;
  is_attack: boolean;
  attack_type?: string;
  confidence?: number;
  matches?: string[];
}

export interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export type AttackType = 'prompt_injection' | 'jailbreak' | 'unauthorized_access' | 'data_exfiltration' | 'other';

