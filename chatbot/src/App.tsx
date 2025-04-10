import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatContainer from './components/ChatContainer';
import Dashboard from './dashboard';

function App() {
  return(
    <Router>
      <Routes>
        <Route path="/" element={<ChatContainer />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}
export default App;
