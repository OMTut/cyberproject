import { useNavigate } from 'react-router-dom';
import botIcon from './assets/botIcon.png';
import './dashboard.css'

function Dashboard() {

    const navigate = useNavigate();

    const navigateToChat = () => {
      navigate('/');
    };

    const dashboardCards = [
      {
        id: 1,
        title: "Prompts",
        description: "View system metrics and reports",
        icon: "📊"
      },
      {
        id: 2,
        title: "Attacks",
        description: "View system metrics and reports",
        icon: "📊"
      },
      {
        id:3,
        title: "Clean Prompts",
        description: "View system metrics and reports",
        icon: "📊"
      },
      {
        id: 4,
        title: "Type",
        description: "View system metrics and reports",
        icon: "📊"
      }
    ];


    return (
      <div className="dashboard">
        <header className="dashboard-header">
        <img 
          src={botIcon} alt="Bot Icon"  className="dashboard-icon" onClick={navigateToChat}
        />
          <h1>Welcome to The Dashboard</h1>
        </header>


        <div className="dashboard-container">
        
      <div className="dashboard-container">
        <section className="intro-section">
          <p>This is the NobleGuard control center.</p>
        </section>

        {/* Grid layout for the four cards */}
        <section className="dashboard-grid">
          {dashboardCards.map(card => (
            <div className="dashboard-card" key={card.id}>
              <div className="card-icon">{card.icon}</div>
              <h3 className="card-title">{card.title}</h3>
              <p className="card-description">{card.description}</p>
              <button className="card-button">Open</button>
            </div>
          ))}
        </section>
      </div>
        </div>
        <footer className="dashboard-footer">
          <p>&copy; 2025 NobleGuard </p>
        </footer>
      </div>


    );
  }
  
  export default Dashboard;