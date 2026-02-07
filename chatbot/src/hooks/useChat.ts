import { useState } from 'react';
import { Message, ApiResponse } from '../types/chat';

export function useChat() {
  // State for chat messages and input text
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! How can I help you today?' }
  ]);
  const [input, setInput] = useState('');

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (!input.trim()) return;

    // Add user message to chat
    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    
    // Clear input field
    const userInput = input;
    setInput('');

    try {
      console.log('Sending request with payload:', JSON.stringify({
        text: userInput
      }));
      
      // Make API call to backend
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
      const response = await fetch(`${apiBaseUrl}/chat/prompt`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          text: userInput
        }),
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', [...response.headers.entries()]);
      
      // Check if the response is OK
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`API Error (${response.status}):`, errorText);
        throw new Error(`API returned ${response.status}: ${errorText || response.statusText}`);
      }

      const data: ApiResponse = await response.json();
      console.log('Received data:', data);

      let responseText: string;
      
      // Check if this is an attack detection response
      if (data.status === 'rejected') {
        // It's an attack - display detailed information
        responseText = `⚠️ ${data.reason || 'Your message was flagged as potentially harmful'}`;
        
        // Add analysis details if available
        if (data.analysis) {
          const attackType = data.analysis.attackType || 'unknown';
          const confidence = data.analysis.confidence 
            ? `${Math.round(data.analysis.confidence * 100)}%` 
            : 'unknown';
          
          responseText += `\n\nAttack type: ${attackType}\nConfidence: ${confidence}`;
          
          // Add any matched patterns if available
          if (data.analysis.matches && data.analysis.matches.length > 0) {
            responseText += `\n\nMatched patterns:\n- ${data.analysis.matches.join('\n- ')}`;
          }
        }
      } else {
        // Normal response - extract the text
        responseText = data.response || data.message || data.generated_text || 'Sorry, I could not process your request.';
      }
      
      // Add bot response to chat
      const botMessage: Message = { role: 'assistant', content: responseText };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error communicating with API:', error);
      
      // Add error message to chat
      const errorMessage: Message = { 
        role: 'assistant', 
        content: `Error: ${error instanceof Error ? error.message : 'Failed to process request. Please check the console for details.'}`
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  return {
    messages,
    input,
    setInput,
    handleSubmit
  };
}

