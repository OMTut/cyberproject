import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import botIcon from './assets/botIcon.png';
import './dashboard.css';

// Define interface for metrics
interface DashboardMetrics {
  totalConversations: number;
  totalMessages: number;
  averageResponseTime: number;
  popularTopics: Array<{topic: string, count: number}>;
}

function Dashboard() {
    const navigate = useNavigate();
    const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const navigateToChat = () => {
      navigate('/');
    };
    
    useEffect(() => {
      // Function to fetch metrics from the backend
      const fetchMetrics = async () => {
        try {
          setLoading(true);
          const response = await fetch('http://localhost:8000/api/metrics');
          
          if (!response.ok) {
            throw new Error(`Failed to fetch metrics: ${response.status}`);
          }
          
          const data = await response.json();
          setMetrics(data);
          setError(null);
        } catch (err) {
          console.error('Error fetching metrics:', err);
          setError('Failed to load dashboard metrics. Please try again later.');
        } finally {
          setLoading(false);
        }
      };
      
      fetchMetrics();
    }, []);
  
    return (
      <div className="dashboard">
        <header className="dashboard-header">
          <img 
            src={botIcon} alt="Bot Icon" className="dashboard-icon" onClick={navigateToChat}
          />
          <h1>NobleGuard Dashboard</h1>
        </header>
        
        <div className="dashboard-container">
          {loading ? (
            <div className="loading-indicator">Loading metrics...</div>
          ) : error ? (
            <div className="error-message">{error}</div>
          ) : metrics ? (
            <>
              <section className="metrics-overview">
                <h2>Conversation Statistics</h2>
                <div className="metrics-grid">
                  <div className="metric-card">
                    <h3>Total Conversations</h3>
                    <p className="metric-value">{metrics.totalConversations}</p>
                  </div>
                  <div className="metric-card">
                    <h3>Total Messages</h3>
                    <p className="metric-value">{metrics.totalMessages}</p>
                  </div>
                  <div className="metric-card">
                    <h3>Avg. Response Time</h3>
                    <p className="metric-value">{metrics.averageResponseTime.toFixed(2)}s</p>
                  </div>
                </div>
              </section>
              
              <section className="popular-topics">
                <h2>Popular Topics</h2>
                <div className="topics-list">
                  {metrics.popularTopics.map((topic, index) => (
                    <div key={index} className="topic-item">
                      <span className="topic-name">{topic.topic}</span>
                      <span className="topic-count">{topic.count}</span>
                    </div>
                  ))}
                </div>
              </section>
            </>
          ) : (
            <p>No metrics available</p>
          )}
        </div>
        
        <footer className="dashboard-footer">
          <p>&copy; 2025 NobleGuard </p>
        </footer>
      </div>
    );
}
  
export default Dashboard;
