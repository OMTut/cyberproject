import { useState, useEffect, useCallback } from 'react';
import { DashboardMetrics, DashboardState } from '../types/dashboard';

export function useDashboard() {
  // State for dashboard metrics and UI states
  const [state, setState] = useState<DashboardState>({
    metrics: null as DashboardMetrics | null,
    loading: true,
    error: null
  });

  // Function to fetch metrics from the backend
  const fetchMetrics = useCallback(async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      
      console.log('Fetching dashboard metrics...');
      const response = await fetch('http://localhost:5000/api/metrics');
      
      // Check for error responses
      if (!response.ok) {
        throw new Error(`Failed to fetch metrics: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Received metrics:', data);
      
      // Update state with fetched metrics
      setState({
        metrics: data as DashboardMetrics,
        loading: false,
        error: null
      });
    } catch (err) {
      console.error('Error fetching metrics:', err);
      
      setState({
        metrics: null as DashboardMetrics | null,
        loading: false,
        error: 'Failed to load dashboard metrics. Please try again later.'
      });
    }
  }, []);

  // Fetch metrics on component mount
  useEffect(() => {
    fetchMetrics();
  }, [fetchMetrics]);

  // Function to refresh metrics manually
  const refreshMetrics = () => {
    fetchMetrics();
  };

  return {
    ...state,
    refreshMetrics
  };
}

