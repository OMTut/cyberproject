import React from 'react';
import ChatUI from './ChatUI';
import { useChat } from '../hooks/useChat';

const ChatContainer: React.FC = () => {
  const { messages, input, setInput, handleSubmit } = useChat();

  return (
    <ChatUI 
      messages={messages}
      input={input}
      setInput={setInput}
      handleSubmit={handleSubmit}
    />
  );
};

export default ChatContainer;

