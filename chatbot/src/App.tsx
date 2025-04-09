//Ally - Note for Team: App.tsx must be used for routing!
import { useState } from 'react'
import React from 'react'
//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import './App.css'

// Define types for our chat messages
interface Message {
  role: 'user' | 'assistant';
  content: string;
}

// Define API response type
interface ApiResponse {
  response?: string;
  message?: string;
  [key: string]: any;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! How can I help you today?' }
  ]);
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Store user input befor clearing it
    const userInput = input;

    // add user message to chat
    setMessages([...messages, { role: 'user', content: userInput }]);
    setInput('');
    
    // Send the message to the API
    fetch('http://localhost:5000/chat/prompt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: userInput }),
    })
    .then((response: Response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data: ApiResponse) => {
        // Add the assistant's response to the chat
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: data.response || data.message || JSON.stringify(data)
        }]);
      })
      .catch((error: Error) => {
        console.error('Error calling chat API:', error);
        // Add an error message to the chat
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: 'Sorry, there was an error processing your request. Please try again later.'
        }]);
      });
  };


  return (
    <>
    <div className="chat-app">
      <div className="chat-container">
        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-content">{message.content}</div>
            </div>
          ))}
        </div>
        
        <form className="input-area" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
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