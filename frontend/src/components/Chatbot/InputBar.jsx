import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, MicOff, Plus, X, FileText, Image } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const InputBar = ({ onSendMessage, disabled }) => {
  const [input, setInput] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [isFocused, setIsFocused] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const textareaRef = useRef(null);
  const recognitionRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = true;

      recognitionRef.current.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0].transcript)
          .join('');
        
        // If it's a final result, append it. If interim, we could show it differently, 
        // but for simplicity let's just set the input.
        // Note: This simple implementation replaces input. 
        // For appending, we'd need to track previous input.
        setInput(prev => {
            // A simple way to handle this is to just use the transcript if it's final
            // or if we want to support appending, we need to be careful about duplicates.
            // For this demo, let's just set the input to the transcript.
            return transcript;
        });
        
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
        }
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, []);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in this browser.');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      const newFiles = files.map(file => {
        return {
          name: file.name,
          type: file.type,
          size: file.size,
          file: file,
          id: Math.random().toString(36).substr(2, 9)
        };
      });
      setSelectedFiles(prev => [...prev, ...newFiles]);
    }
  };

  const removeFile = (fileId) => {
    setSelectedFiles(prev => prev.filter(f => f.id !== fileId));
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSend = () => {
    if (input.trim() && !disabled) {
      // Only send message if there's text input
      // Send files only if they exist
      const filesToSend = selectedFiles.length > 0 ? selectedFiles : [];
      onSendMessage(input, filesToSend);
      setInput('');
      setSelectedFiles([]);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleChange = (e) => {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 200)}px`;
  };

  const hasInput = input.trim().length > 0 || selectedFiles.length > 0;

  return (
    <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-white dark:from-[#252837] via-white/95 dark:via-[#252837]/95 to-transparent pt-8 md:pt-10 pb-6 px-4 md:px-6">
      <div className="max-w-3xl mx-auto space-y-3">
        {/* File Preview */}
        <AnimatePresence>
          {selectedFiles.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="flex gap-3 flex-wrap"
            >
              {selectedFiles.map(file => (
                <motion.div
                  key={file.id}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  className="relative inline-block"
                >
                  {file.type.startsWith('image/') ? (
                    <motion.div className="relative">
                      <img
                        src={URL.createObjectURL(file.file)}
                        alt={file.name}
                        className="h-20 w-auto rounded-xl border border-slate-300 dark:border-slate-600 shadow-md object-cover"
                      />
                      <button
                        onClick={() => removeFile(file.id)}
                        className="absolute -top-3 -right-3 bg-red-500 text-white rounded-full p-1.5 shadow-lg hover:bg-red-600 transition-colors"
                      >
                        <X size={14} />
                      </button>
                    </motion.div>
                  ) : (
                    <div className="flex items-center gap-2 px-3.5 py-2.5 bg-slate-100 dark:bg-slate-700/60 rounded-xl border border-slate-300 dark:border-slate-600 shadow-sm">
                      <FileText size={18} className="text-blue-600 dark:text-blue-400 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-medium text-slate-700 dark:text-slate-200 truncate">
                          {file.name}
                        </p>
                        <p className="text-xs text-slate-500 dark:text-slate-400">
                          {(file.size / 1024).toFixed(1)} KB
                        </p>
                      </div>
                      <button
                        onClick={() => removeFile(file.id)}
                        className="flex-shrink-0 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                      >
                        <X size={16} />
                      </button>
                    </div>
                  )}
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Input Container */}
        <motion.div
          className={`relative flex items-end gap-2 md:gap-3 rounded-2xl border-2 transition-all duration-200 p-2.5 md:p-3.5 ${
            isFocused
              ? 'border-blue-500/50 bg-gray-50 dark:bg-[#2d3349] shadow-lg shadow-blue-500/20'
              : 'border-gray-300 dark:border-gray-600/40 bg-gray-50/80 dark:bg-[#2d3349]/80 shadow-md'
          }`}
          animate={{
            boxShadow: isFocused
              ? '0 20px 40px -12px rgba(59, 130, 246, 0.3)'
              : '0 8px 16px -4px rgba(0, 0, 0, 0.2)',
            borderColor: isListening ? '#ef4444' : undefined
          }}
        >
          {/* Hidden File Input */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            accept="image/*,.pdf,.doc,.docx,.xls,.xlsx"
            multiple
            className="hidden"
          />

          {/* Plus Button (Attachment) */}
          <motion.button
            onClick={() => fileInputRef.current?.click()}
            disabled={disabled}
            whileHover={{ scale: 1.08 }}
            whileTap={{ scale: 0.95 }}
            className="flex h-8 w-8 md:h-9 md:w-9 shrink-0 items-center justify-center rounded-lg bg-gray-200 dark:bg-gray-700/50 text-gray-600 dark:text-gray-400 hover:bg-gray-300 dark:hover:bg-gray-600/60 transition-all duration-200 disabled:opacity-50"
            title="Attach files"
          >
            <Plus size={18} />
          </motion.button>

          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder={isListening ? "Listening..." : "Ask a question..."}
            disabled={disabled}
            rows={1}
            className="flex-1 max-h-[180px] min-h-[28px] w-full resize-none bg-transparent px-2 py-2 md:px-3 text-sm md:text-base text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none disabled:opacity-50 font-medium"
          />

          {/* Voice Button */}
          <motion.button
            onClick={toggleListening}
            disabled={disabled}
            whileHover={{ scale: 1.08 }}
            whileTap={{ scale: 0.95 }}
            className={`flex h-8 w-8 md:h-9 md:w-9 shrink-0 items-center justify-center rounded-lg transition-all duration-200 ${
              isListening
                ? 'bg-red-500 text-white animate-pulse shadow-lg shadow-red-500/40'
                : 'bg-gray-200 dark:bg-gray-700/50 text-gray-600 dark:text-gray-400 hover:bg-gray-300 dark:hover:bg-gray-600/60'
            }`}
            title="Voice input"
          >
            {isListening ? <MicOff size={18} /> : <Mic size={18} />}
          </motion.button>

          {/* Send Button */}
          <motion.button
            onClick={handleSend}
            disabled={!hasInput || disabled}
            whileHover={hasInput && !disabled ? { scale: 1.08 } : {}}
            whileTap={hasInput && !disabled ? { scale: 0.95 } : {}}
            className={`flex h-8 w-8 md:h-9 md:w-9 shrink-0 items-center justify-center rounded-lg transition-all duration-200 font-semibold ${
              hasInput && !disabled
                ? 'bg-gradient-to-br from-blue-600 to-cyan-500 text-white shadow-lg shadow-blue-600/30 hover:shadow-blue-600/50'
                : 'bg-gray-200 dark:bg-gray-700/50 text-gray-400 dark:text-gray-500'
            }`}
          >
            <Send size={18} />
          </motion.button>
        </motion.div>

        {/* Info Text */}
        <p className="text-center text-xs text-gray-500 leading-relaxed">
          Reply Assistant may produce inaccurate information about people, places, or facts.
        </p>
      </div>
    </div>
  );
};

export default InputBar;
