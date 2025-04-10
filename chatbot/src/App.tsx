import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatUI from './ChatUI';
import Dashboard from './dashboard';

function App() {
return(
  <Router>
    <Routes>
       <Route path="/" element={<ChatUI />} />
       <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  </Router>
);
}
export default App;
