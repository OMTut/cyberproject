import { useState } from 'react';
import { Prompt, ApiState, AttackType } from '../types/prompts';

const API_BASE_URL = 'http://localhost:5000';

export const usePromptsApi = () => {
  const [allPromptsState, setAllPromptsState] = useState<ApiState<Prompt[]>>({
    data: null,
    loading: false,
    error: null
  });

  const [attacksState, setAttacksState] = useState<ApiState<Prompt[]>>({
    data: null,
    loading: false,
    error: null
  });

  const [cleanPromptsState, setCleanPromptsState] = useState<ApiState<Prompt[]>>({
    data: null,
    loading: false,
    error: null
  });

  const [attacksByTypeState, setAttacksByTypeState] = useState<ApiState<Prompt[]>>({
    data: null,
    loading: false,
    error: null
  });

  /**
   * Generic function to make API requests with proper error handling
   */
  const fetchFromApi = async <T,>(endpoint: string, options = {}): Promise<T> => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      ...options
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`API Error (${response.status}):`, errorText);
      throw new Error(`API returned ${response.status}: ${errorText || response.statusText}`);
    }

    return await response.json();
  };

  /**
   * Fetch all prompts from the API
   */
  const getAllPrompts = async (): Promise<Prompt[]> => {
    try {
      setAllPromptsState({ ...allPromptsState, loading: true, error: null });
      console.log('Fetching all prompts...');
      
      const data = await fetchFromApi<Prompt[]>('/prompts');
      console.log('Received prompts:', data);
      
      setAllPromptsState({ data, loading: false, error: null });
      return data;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error fetching prompts';
      console.error('Error fetching all prompts:', errorMessage);
      
      setAllPromptsState({ data: null, loading: false, error: errorMessage });
      return [];
    }
  };

  /**
   * Fetch only attack prompts from the API
   */
  const getAttacks = async (): Promise<Prompt[]> => {
    try {
      setAttacksState({ ...attacksState, loading: true, error: null });
      console.log('Fetching attack prompts...');
      
      const data = await fetchFromApi<Prompt[]>('/prompts/attacks');
      console.log('Received attack prompts:', data);
      
      setAttacksState({ data, loading: false, error: null });
      return data;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error fetching attack prompts';
      console.error('Error fetching attack prompts:', errorMessage);
      
      setAttacksState({ data: null, loading: false, error: errorMessage });
      return [];
    }
  };

  /**
   * Fetch only clean (non-attack) prompts from the API
   */
  const getCleanPrompts = async (): Promise<Prompt[]> => {
    try {
      setCleanPromptsState({ ...cleanPromptsState, loading: true, error: null });
      console.log('Fetching clean prompts...');
      
      const data = await fetchFromApi<Prompt[]>('/prompts/clean');
      console.log('Received clean prompts:', data);
      
      setCleanPromptsState({ data, loading: false, error: null });
      return data;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error fetching clean prompts';
      console.error('Error fetching clean prompts:', errorMessage);
      
      setCleanPromptsState({ data: null, loading: false, error: errorMessage });
      return [];
    }
  };

  /**
   * Fetch attack prompts by type
   */
  const getAttacksByType = async (type: AttackType): Promise<Prompt[]> => {
    try {
      setAttacksByTypeState({ ...attacksByTypeState, loading: true, error: null });
      console.log(`Fetching attacks of type: ${type}...`);
      
      const data = await fetchFromApi<Prompt[]>(`/prompts/type?type=${type}`);
      console.log(`Received ${type} attacks:`, data);
      
      setAttacksByTypeState({ data, loading: false, error: null });
      return data;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : `Unknown error fetching ${type} attacks`;
      console.error(`Error fetching ${type} attacks:`, errorMessage);
      
      setAttacksByTypeState({ data: null, loading: false, error: errorMessage });
      return [];
    }
  };

  return {
    // Functions
    getAllPrompts,
    getAttacks,
    getCleanPrompts,
    getAttacksByType,
    
    // States
    allPromptsState,
    attacksState,
    cleanPromptsState,
    attacksByTypeState,
  };
};

