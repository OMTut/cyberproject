import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';
import botIcon from './assets/botIcon.png'; 

// Define types for our chat messages
interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatUIProps {
  messages: Message[];
  input: string;
  setInput: (input: string) => void;
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
}

function ChatUI({ messages, input, setInput, handleSubmit }: ChatUIProps) {

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

export default ChatUI;