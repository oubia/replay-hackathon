import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, User, Copy, ThumbsUp, ThumbsDown, ArrowDown, Stethoscope, Activity } from 'lucide-react';
import clsx from 'clsx';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import AnalysisReport from '../AnalysisReport';

const MessageList = ({ messages, isTyping }) => {
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);
  const [showScrollButton, setShowScrollButton] = useState(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleScroll = () => {
    if (containerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
      const isNearBottom = scrollHeight - scrollTop - clientHeight < 100;
      setShowScrollButton(!isNearBottom);
    }
  };

  if (messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8 space-y-8">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-slate-800 dark:to-slate-900 p-6 rounded-3xl shadow-2xl ring-4 ring-blue-100 dark:ring-slate-700/50"
        >
          <Stethoscope size={64} className="text-blue-600 dark:text-cyan-400" />
        </motion.div>
        <motion.h1 
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-slate-50"
        >
          How can I assist you today?
        </motion.h1>
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="flex gap-4 text-sm text-slate-600 dark:text-slate-400"
        >
          <div className="flex items-center gap-2 bg-blue-50 dark:bg-slate-800/50 px-4 py-2 rounded-full border border-blue-200 dark:border-slate-700">
            <Activity size={16} />
            <span>Health Advice</span>
          </div>
          <div className="flex items-center gap-2 bg-cyan-50 dark:bg-slate-800/50 px-4 py-2 rounded-full border border-cyan-200 dark:border-slate-700">
            <Stethoscope size={16} />
            <span>Assessment</span>
          </div>
        </motion.div>
      </div>
    );
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.3, ease: 'easeOut' },
    },
  };

  return (
    <div className="relative flex-1 h-full overflow-hidden">
      <div 
        ref={containerRef}
        onScroll={handleScroll}
        className="h-full overflow-y-auto p-4 md:p-6 scroll-smooth"
      >
        <motion.div
          className="flex flex-col space-y-5 pb-32 max-w-3xl mx-auto"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {messages.map((msg, index) => (
            <motion.div
              key={index}
              variants={itemVariants}
              className={clsx(
                "flex w-full gap-3 md:gap-4",
                msg.sender === 'user' ? "justify-end" : "justify-start"
              )}
            >
              {/* Avatar for Bot */}
              {msg.sender === 'bot' && (
                <div className="flex h-8 w-8 md:h-9 md:w-9 shrink-0 items-center justify-center rounded-full bg-blue-600 shadow-md mt-1">
                  <Stethoscope size={16} className="text-white" />
                </div>
              )}

              {/* Message Bubble */}
              {msg.type === 'report' ? (
                <AnalysisReport report={msg.report} />
              ) : (
                <div className="flex flex-col gap-2 max-w-[85%] md:max-w-[70%]">
                  {/* Only show image if it exists and there's text with it */}
                  {msg.image && msg.text && msg.sender === 'user' && (
                    <div className="rounded-xl overflow-hidden border border-slate-200 dark:border-slate-700 shadow-sm">
                      <img
                        src={msg.image}
                        alt="User upload"
                        className="max-h-48 w-auto object-cover"
                      />
                    </div>
                  )}
                  
                  {/* Show message bubble only if there's text */}
                  {msg.text && (
                    <div className={clsx(
                      "message-bubble text-sm md:text-base rounded-2xl overflow-hidden",
                      msg.sender === 'user'
                        ? "bg-gradient-to-br from-blue-600 to-cyan-600 text-white shadow-sm"
                        : "bg-gray-100 dark:bg-[#343849] text-gray-800 dark:text-gray-100 shadow-sm"
                    )}>
                      <div className="px-4 md:px-5 py-3 md:py-3.5 min-h-[20px] leading-relaxed">
                        {msg.sender === 'bot' ? (
                          <div className="prose prose-sm dark:prose-invert max-w-none prose-headings:font-semibold prose-h1:text-xl prose-h2:text-lg prose-h3:text-base prose-h3:mt-4 prose-h3:mb-2 prose-p:my-2 prose-ul:my-2 prose-ol:my-2 prose-li:my-1">
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                              {msg.text}
                            </ReactMarkdown>
                            {msg.isStreaming && (
                              <span className="inline-block w-1.5 h-4 ml-1 align-middle bg-current animate-pulse" />
                            )}
                          </div>
                        ) : (
                          <p className="whitespace-pre-wrap break-words">
                            {msg.text}
                            {msg.isStreaming && (
                              <span className="inline-block w-1.5 h-4 ml-1 align-middle bg-current animate-pulse" />
                            )}
                          </p>
                        )}
                      </div>

                      {/* Actions for Bot Messages */}
                      {msg.sender === 'bot' && !msg.isStreaming && (
                        <div className="flex items-center gap-1 px-4 md:px-5 pb-2.5 pt-1">
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            className="p-1.5 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 rounded-md transition-colors"
                            title="Copy"
                          >
                            <Copy size={14} />
                          </motion.button>
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            className="p-1.5 text-gray-400 dark:text-gray-500 hover:text-green-600 dark:hover:text-green-400 rounded-md transition-colors"
                            title="Good response"
                          >
                            <ThumbsUp size={14} />
                          </motion.button>
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            className="p-1.5 text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 rounded-md transition-colors"
                            title="Bad response"
                          >
                            <ThumbsDown size={14} />
                          </motion.button>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}

              {/* Avatar for User */}
              {msg.sender === 'user' && (
                <div className="flex h-8 w-8 md:h-9 md:w-9 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-purple-600 to-purple-700 shadow-md mt-1">
                  <User size={16} className="text-white" />
                </div>
              )}
            </motion.div>
          ))}

          {/* Typing Indicator */}
          {isTyping && !messages.some(m => m.isStreaming) && (
            <motion.div
              variants={itemVariants}
              className="flex w-full justify-start gap-3 md:gap-4"
            >
              <div className="flex h-8 w-8 md:h-9 md:w-9 shrink-0 items-center justify-center rounded-full bg-blue-600 shadow-md mt-1">
                <Stethoscope size={16} className="text-white" />
              </div>
              <div className="bg-gray-100 dark:bg-[#343849] rounded-2xl px-5 py-4 shadow-sm">
                <div className="flex space-x-2 items-center">
                  <motion.div
                    className="h-2 w-2 rounded-full bg-gray-400 dark:bg-gray-500"
                    animate={{ y: [0, -6, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
                  />
                  <motion.div
                    className="h-2 w-2 rounded-full bg-gray-400 dark:bg-gray-500"
                    animate={{ y: [0, -6, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
                  />
                  <motion.div
                    className="h-2 w-2 rounded-full bg-gray-400 dark:bg-gray-500"
                    animate={{ y: [0, -6, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
                  />
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} className="h-4" />
        </motion.div>
      </div>

      {/* Scroll to Bottom Button */}
      <AnimatePresence>
        {showScrollButton && (
          <motion.button
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            onClick={scrollToBottom}
            className="absolute bottom-40 left-1/2 -translate-x-1/2 z-20 p-2 rounded-full bg-gray-800 dark:bg-gray-700 text-white shadow-lg hover:bg-gray-700 dark:hover:bg-gray-600 transition-colors border border-gray-700 dark:border-gray-600"
          >
            <ArrowDown size={20} />
          </motion.button>
        )}
      </AnimatePresence>
    </div>
  );
};

export default MessageList;
