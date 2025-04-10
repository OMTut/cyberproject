import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatUI from './ChatUI';
import Dashboard from './dashboard';

// Define types for our chat messages
interface Message {
  role: 'user' | 'assistant';
  content: string;
}

// Define API response type
interface ApiResponse {
  response?: string;
  message?: string;
  generated_text?: string;
  [key: string]: any;
}

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
