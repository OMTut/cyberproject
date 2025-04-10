import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';
import botIcon from './assets/botIcon.png'; 


function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! How can I help you today?' }
  ]);
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    //adds user message to chat
    setMessages([...messages, { role: 'user', content: input }]);
    setInput('');
    
    //API response holder (we can take this out/tweak it once we figure out how to connect everything)
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'This is a placeholder response. The actual implementation will go here.'
      }]);
    }, 500);
  };

  const navigate = useNavigate();

    const navigateToDash = () => {
      navigate('/dashboard');
    };
  return (
    <>
    <div className="chat-app">
    <header className="chat-header">
    <img src={botIcon} alt="Bot Icon" className="chat-icon" onClick={navigateToDash}/>
     <h1>NobleGuard</h1>
      </header>
      <div className="chat-container">
        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
               {message.role === 'assistant' && (
               <img src={botIcon} alt="Bot Icon" className="message-icon" />
              )}
              <div className="message-content">{message.content}</div>
            </div>
          ))}
        </div>
        
        <form className="input-area" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            className="message-input"
          />
          <button type="submit" className="send-button">Send</button>
        </form>
      </div>
    </div>

    </>
  )
}

export default App;