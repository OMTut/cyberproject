import { useNavigate } from 'react-router-dom';
import botIcon from './assets/botIcon.png';
import './dashboard.css'

function Dashboard() {

    const navigate = useNavigate();

    const navigateToChat = () => {
      navigate('/');
    };
  
    return (
      <div className="dashboard">
        <header className="dashboard-header">
        <img 
          src={botIcon} alt="Bot Icon"  className="dashboard-icon" onClick={navigateToChat}
        />
          <h1>Welcome to The Dashboard</h1>
        </header>
        <div className="dashboard-container">
          <section>
            <p>This is a simple example of the dashboard.</p>
          </section>
        </div>
        <footer className="dashboard-footer">
          <p>&copy; 2025 NobleGuard </p>
        </footer>
      </div>
    );
  }
  
  export default Dashboard;