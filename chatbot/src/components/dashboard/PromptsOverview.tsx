import React, { useEffect } from 'react';
import { usePromptsApi } from '../../hooks/usePromptsApi';
import '../../dashboard.css';

const PromptsOverview: React.FC = () => {
  const { getAllPrompts, allPromptsState } = usePromptsApi();
  const { data: prompts, loading, error } = allPromptsState;

  useEffect(() => {
    getAllPrompts();
  }, []);

  // Log prompts data for debugging
  useEffect(() => {
    if (prompts) {
      console.log('Prompts data:', prompts);
      console.log('First prompt example:', prompts[0]);
    }
  }, [prompts]);

  // Calculate statistics
  const totalPrompts = prompts?.length || 0;
  const attackPrompts = prompts?.filter(p => p.isAttack)?.length || 0;
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
          <p>Total Prompts: {totalPrompts}</p>
          <p>Total Attacks: {attackPrompts}</p>
          <p>Attack Percentage: {attackPercentage.toFixed(1)}%</p>
        </div>
      ) : (
        <p>No prompts data available</p>
      )}
    </section>
  );
};

export default PromptsOverview;

