import React, { useEffect } from 'react';
import { usePromptsApi } from '../../hooks/usePromptsApi';
import '../../dashboard.css';

const PromptsOverview: React.FC = () => {
  const { getAllPrompts, allPromptsState } = usePromptsApi();
  const { data: prompts, loading, error } = allPromptsState;

  useEffect(() => {
    getAllPrompts();
  }, []);

  // Calculate statistics
  const totalPrompts = prompts?.length || 0;
  const attackPrompts = prompts?.filter(p => p.is_attack)?.length || 0;
  const attackPercentage = totalPrompts > 0 ? (attackPrompts / totalPrompts) * 100 : 0;

  return (
    <section className="prompts-overview">
      <h2>Prompts Overview</h2>
      
      {loading ? (
        <div className="loading-indicator">Loading prompts data...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : prompts ? (
        <div className="simple-stats">
          <p><strong>Total Prompts:</strong> {totalPrompts}</p>
          <p><strong>Total Attacks:</strong> {attackPrompts}</p>
          <p><strong>Attack Percentage:</strong> {attackPercentage.toFixed(1)}%</p>
        </div>
      ) : (
        <p>No prompts data available</p>
      )}
    </section>
  );
};

export default PromptsOverview;

