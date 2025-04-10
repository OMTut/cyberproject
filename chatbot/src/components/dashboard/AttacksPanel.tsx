import React, { useEffect } from 'react';
import { usePromptsApi } from '../../hooks/usePromptsApi';
import '../../dashboard.css';

const AttacksPanel: React.FC = () => {
  const { getAttacks, attacksState } = usePromptsApi();
  const { data: attacks, loading, error } = attacksState;

  // Fetch all attacks on component mount
  useEffect(() => {
    getAttacks();
  }, []);

  // Calculate attack type distribution
  const attackTypes: Record<string, number> = {};
  
  if (attacks) {
    attacks.forEach(attack => {
      const type = attack.attack_type || 'unknown';
      attackTypes[type] = (attackTypes[type] || 0) + 1;
    });
  }

  return (
    <section className="attacks-panel">
      <h2>Attack Analysis</h2>
      
      {loading ? (
        <div className="loading-indicator">Loading attack data...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : attacks && attacks.length > 0 ? (
        <div className="simple-stats">
          <p><strong>Number of Attacks:</strong> {attacks.length}</p>
          
          <h3>Attacks by Type:</h3>
          <ul className="simple-attack-list">
            {Object.entries(attackTypes).map(([type, count]) => (
              <li key={type}>
                <strong>{type}:</strong> {count}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>No attack data available</p>
      )}
    </section>
  );
};

export default AttacksPanel;

