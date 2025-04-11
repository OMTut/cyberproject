import React from 'react';
import { useNavigate } from 'react-router-dom';
import botIcon from '../../assets/botIcon.png';
import '../../dashboard.css';
import PromptsOverview from './PromptsOverview';
import AttacksPanel from './AttacksPanel';
import AttackRows from './AttackRows';


const DashboardContainer: React.FC = () => {
  const navigate = useNavigate();

  const navigateToChat = () => {
    navigate('/');
  };

  return (
    <div className="dashboard">
      <header className="chat-header">
      <img src={botIcon} alt="Bot Icon" className="chat-icon" onClick={navigateToChat}/>
      <h1>NobleGuard</h1>
    </header>
      
      <div className="dashboard-content">
        <div className="dashboard-top-row">
          <PromptsOverview />
          <AttacksPanel />
        </div>
        
        <div className="dashboard-bottom-row">
          <AttackRows />
        </div>
      </div>
      
      <footer className="dashboard-footer">
        <p>&copy; 2025 NobleGuard </p>
      </footer>
    </div>
  );
};

export default DashboardContainer;

