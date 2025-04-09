//Ally - Note for Team: App.tsx must be used for routing!
import { useState } from 'react';
import React from 'react';
import './App.css';
import ChatUI from './ChatUI';

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
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! How can I help you today?' }
  ]);
  const [input, setInput] = useState('');

  // Helper function to clean response text
  const cleanResponseText = (text: string): string => {
    // Remove excessive newlines (more than 2 consecutive)
    let cleaned = text.replace(/\n{3,}/g, '\n\n');
    
    // Trim leading and trailing whitespace
    cleaned = cleaned.trim();
    
    // Remove any non-printable characters
    cleaned = cleaned.replace(/[\x00-\x09\x0B\x0C\x0E-\x1F\x7F]/g, '');
    
    return cleaned;
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Store user input before clearing it
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
        // Extract and clean the response text
        let responseText: string;
        
        if (data.generated_text) {
          // If we have a generated_text field, use that
          responseText = data.generated_text;
        } else if (data.response) {
          // If we have a response field, use that
          responseText = data.response;
        } else if (data.message) {
          // Fallback to message field
          responseText = data.message;
        } else {
          // Last resort, stringify the whole data
          responseText = JSON.stringify(data);
        }
        
        // Clean the text to remove excessive formatting
        const cleanedText = cleanResponseText(responseText);
        
        // Add the assistant's response to the chat
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: cleanedText
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
    <ChatUI 
      messages={messages}
      input={input}
      setInput={setInput}
      handleSubmit={handleSubmit}
    />
  );
}

export default App;
