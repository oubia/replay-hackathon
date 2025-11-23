import React, { useState, useEffect } from 'react';
import { Menu, Moon, Sun, BarChart3 } from 'lucide-react';
import { motion } from 'framer-motion';
import Sidebar from './components/Chatbot/Sidebar';
import MessageList from './components/Chatbot/MessageList';
import InputBar from './components/Chatbot/InputBar';
import WelcomeScreen from './components/WelcomeScreen';
import { useChat } from './hooks/useChat';

function App() {
  const { messages, isTyping, sendMessage, clearHistory } = useChat();
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [selectedTab, setSelectedTab] = useState('chat');

  const quickActionMessages = {
    'symptom-check': 'I want to analyze my symptoms. Can you help me?',
    'lab-results': 'I have lab test results to analyze. Please help me understand them.',
    'medication': 'Can you provide information about a medication?',
    'imaging': 'I have a medical imaging file (X-ray/CT scan) to analyze.'
  };

  const handleQuickAction = (actionId) => {
    const message = quickActionMessages[actionId];
    if (message) {
      sendMessage(message);
    }
  };

  // Check system preference or local storage for theme
  useEffect(() => {
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      setIsDarkMode(true);
      document.documentElement.classList.add('dark');
    } else {
      setIsDarkMode(false);
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const toggleTheme = () => {
    if (isDarkMode) {
      document.documentElement.classList.remove('dark');
      localStorage.theme = 'light';
      setIsDarkMode(false);
    } else {
      document.documentElement.classList.add('dark');
      localStorage.theme = 'dark';
      setIsDarkMode(true);
    }
  };

  return (
    <div className="flex h-screen bg-slate-50 dark:bg-[#1a1d2e] text-gray-900 dark:text-gray-100 font-sans overflow-hidden transition-colors duration-300">
      {/* Sidebar */}
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        onClearHistory={clearHistory}
      />

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative bg-white dark:bg-[#252837] transition-colors duration-300">
        {/* Mobile Header */}
        <header className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700/30 md:hidden">
          <motion.button
            onClick={() => setIsSidebarOpen(true)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="p-2.5 -ml-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700/50 rounded-lg transition-all duration-200"
          >
            <Menu size={24} />
          </motion.button>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-gradient-to-r from-blue-500 to-cyan-400 animate-pulse" />
            <span className="font-semibold text-gray-800 dark:text-gray-100">MediAssist</span>
          </div>
          <motion.button
            onClick={toggleTheme}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="p-2.5 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700/50 rounded-lg transition-all duration-200"
          >
            {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
          </motion.button>
        </header>

        {/* Desktop Theme Toggle */}
        <motion.div
          className="hidden md:block absolute top-4 right-4 z-10"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <button
            onClick={toggleTheme}
            className="p-3 rounded-lg text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-all duration-200"
          >
            {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </motion.div>

        {/* Messages Container */}
        <div className="flex-1 relative w-full h-full flex flex-col overflow-hidden">
          {messages.length === 0 ? (
            <WelcomeScreen onQuickAction={handleQuickAction} />
          ) : (
            <MessageList messages={messages} isTyping={isTyping} />
          )}
          <InputBar onSendMessage={sendMessage} disabled={isTyping} />
        </div>
      </main>
    </div>
  );
}

export default App;
