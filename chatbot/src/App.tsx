import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatContainer from './components/ChatContainer';
import DashboardContainer from './components/dashboard/DashboardContainer';

function App() {
  return(
    <Router>
      <Routes>
        <Route path="/" element={<ChatContainer />} />
        <Route path="/dashboard" element={<DashboardContainer />} />
      </Routes>
    </Router>
  );
}
export default App;
