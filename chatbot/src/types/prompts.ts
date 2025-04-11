// Define prompt types for API responses

export interface Prompt {
  _id: string;
  prompt: string;
  isAttack: boolean;
  attackType?: string;
  confidence?: number;
  matches?: string[];
  created_at: string;
}

export interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export type AttackType = 'prompt_injection' | 'jailbreak' | 'unauthorized_access' | 'data_exfiltration' | 'other';

