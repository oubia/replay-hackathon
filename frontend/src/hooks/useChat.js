import { useState, useEffect } from 'react';

const STORAGE_KEY = 'reply_chat_history';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  // Load from local storage
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        setMessages(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse chat history', e);
      }
    } else {
      // Start with empty history for the welcome screen
      setMessages([]);
    }
  }, []);

  // Save to local storage
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    }
  }, [messages]);

  const toggleChat = () => setIsOpen(!isOpen);

  const clearHistory = () => {
    setMessages([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  const sendMessage = async (text, files = []) => {
    // Get the first image file if any
    const imageFile = files.find(f => f.type.startsWith('image/'));
    let imageDataUrl = null;
    
    if (imageFile) {
      // Convert to base64
      const reader = new FileReader();
      imageDataUrl = await new Promise((resolve) => {
        reader.onloadend = () => resolve(reader.result);
        reader.readAsDataURL(imageFile.file);
      });
    }

    const userMsg = {
      id: Date.now().toString(),
      text,
      image: imageDataUrl,
      sender: 'user',
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    try {
      const botMsgId = (Date.now() + 1).toString();
      
      // Add empty bot message first
      setMessages(prev => [...prev, {
        id: botMsgId,
        text: '',
        sender: 'bot',
        timestamp: Date.now(),
        isStreaming: true
      }]);

      // Connect to real backend
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: text,
          history: messages.map(m => ({ role: m.sender, content: m.text })),
          image: imageDataUrl // Send base64 image if exists
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      const responseText = data.response;
      
      // Simulate streaming for the received text (since backend isn't streaming yet)
      // Or just set it directly if we want instant response. 
      // Let's keep the streaming effect for UX consistency.
      
      let currentText = '';
      const chunkSize = 5; // Faster streaming
      
      for (let i = 0; i < responseText.length; i += chunkSize) {
        await new Promise(resolve => setTimeout(resolve, 10));
        currentText += responseText.slice(i, i + chunkSize);
        
        setMessages(prev => prev.map(msg => 
          msg.id === botMsgId 
            ? { ...msg, text: currentText }
            : msg
        ));
      }
      
      // Ensure full text is set at the end
      setMessages(prev => prev.map(msg => 
        msg.id === botMsgId 
          ? { ...msg, text: responseText, isStreaming: false }
          : msg
      ));

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => prev.map(msg => 
        msg.isStreaming 
          ? { ...msg, text: "Sorry, I encountered an error connecting to the server.", isStreaming: false }
          : msg
      ));
    } finally {
      setIsTyping(false);
    }
  };

  return {
    messages,
    isTyping,
    isOpen,
    toggleChat,
    sendMessage,
    clearHistory
  };
};
