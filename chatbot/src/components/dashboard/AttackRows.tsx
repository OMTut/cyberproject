import React, { useEffect } from 'react';
import { usePromptsApi } from '../../hooks/usePromptsApi';
import '../../dashboard.css';

const AttackRows: React.FC = () => {
  const { getAttacks, attacksState } = usePromptsApi();
  const { data: attacks, loading, error } = attacksState;

  // Fetch all attacks on component mount
  useEffect(() => {
    getAttacks();
  }, []);

  return (
    <section className="attack-rows">
      <h2>Recent Attack Details</h2>
      
      {loading ? (
        <div className="loading-indicator">Loading attack data...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : attacks && attacks.length > 0 ? (
        <div className="attack-table-container">
          <table className="attack-table">
            <thead>
              <tr>
                <th>Attack Type</th>
                <th>Prompt</th>
                <th>Confidence</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
            {[...attacks]
                // Sort by created_at in descending order (most recent first)
                .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
                .map((attack) => (
                <tr key={attack._id}>
                  <td className="attack-type">{attack.attackType || 'Unknown'}</td>
                  <td className="attack-prompt">{attack.prompt}</td>
                  <td className="attack-confidence">{attack.confidence ? `${(attack.confidence * 100).toFixed(1)}%` : 'N/A'}</td>
                  <td className="attack-date">{new Date(attack.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No attack data available</p>
      )}
    </section>
  );
};

export default AttackRows;