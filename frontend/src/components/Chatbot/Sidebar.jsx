import React, { useState, useEffect } from 'react';
import { Plus, MessageSquare, Trash2, Settings, X } from 'lucide-react';
import clsx from 'clsx';
import DocumentHistory from './DocumentHistory';

const Sidebar = ({ isOpen, onClose, onClearHistory }) => {
  const [documents, setDocuments] = useState([]);
  const [activeTab, setActiveTab] = useState('chats');

  useEffect(() => {
    const savedDocs = localStorage.getItem('health_documents');
    if (savedDocs) {
      try {
        setDocuments(JSON.parse(savedDocs));
      } catch (e) {
        console.error('Failed to parse documents', e);
      }
    }
  }, []);

  const handleDeleteDocument = (docId) => {
    const updatedDocs = documents.filter(doc => doc.id !== docId);
    setDocuments(updatedDocs);
    localStorage.setItem('health_documents', JSON.stringify(updatedDocs));
  };

  return (
    <>
      {/* Mobile Overlay */}
      <div
        className={clsx(
          "fixed inset-0 bg-black/40 backdrop-blur-sm z-40 md:hidden transition-opacity duration-300",
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        onClick={onClose}
      />

      {/* Sidebar Content */}
      <div className={clsx(
        "fixed inset-y-0 left-0 z-50 w-64 bg-gray-50 dark:bg-[#1a1d2e] text-gray-900 dark:text-gray-100 transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0 flex flex-col border-r border-gray-200 dark:border-gray-700/30",
        isOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        {/* Header */}
        <div className="p-4 flex-shrink-0 flex items-center justify-between border-b border-gray-200 dark:border-gray-800/30">
          <button
            onClick={onClearHistory}
            className="flex-1 flex items-center gap-2 px-3 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-800/50 transition-all duration-200 text-sm text-left font-medium group"
          >
            <Plus size={16} className="group-hover:text-primary transition-colors" />
            New chat
          </button>
          <button onClick={onClose} className="md:hidden ml-2 p-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800/50 rounded-lg transition-all duration-200">
            <X size={20} />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-gray-200 dark:border-gray-800/30 px-3">
          <button
            onClick={() => setActiveTab('chats')}
            className={clsx(
              "flex-1 px-3 py-3 text-xs font-semibold uppercase tracking-wider transition-all duration-200 border-b-2",
              activeTab === 'chats'
                ? 'text-primary border-primary'
                : 'text-gray-500 border-transparent hover:text-gray-700 dark:hover:text-gray-300'
            )}
          >
            Chats
          </button>
          <button
            onClick={() => setActiveTab('documents')}
            className={clsx(
              "flex-1 px-3 py-3 text-xs font-semibold uppercase tracking-wider transition-all duration-200 border-b-2",
              activeTab === 'documents'
                ? 'text-primary border-primary'
                : 'text-gray-500 border-transparent hover:text-gray-700 dark:hover:text-gray-300'
            )}
          >
            Documents
          </button>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto">
          {activeTab === 'chats' ? (
            <div className="px-3 py-4 space-y-2">
              <div className="text-xs font-semibold text-gray-500 px-3 mb-3 uppercase tracking-wider">Today</div>
              <button className="w-full flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800/60 transition-all duration-200 text-sm text-gray-700 dark:text-gray-200 text-left truncate group">
                <MessageSquare size={16} className="text-gray-500 group-hover:text-primary transition-colors" />
                <span className="truncate font-medium">Current Chat</span>
              </button>
            </div>
          ) : (
            <DocumentHistory
              documents={documents}
              onDeleteDocument={handleDeleteDocument}
            />
          )}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-gray-200 dark:border-gray-800/30 space-y-1">
          <button
            onClick={onClearHistory}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800/50 transition-all duration-200 text-sm text-left group"
          >
            <Trash2 size={16} className="text-gray-500 group-hover:text-red-500 dark:group-hover:text-red-400 transition-colors" />
            <span className="font-medium group-hover:text-gray-800 dark:group-hover:text-gray-100">Clear conversations</span>
          </button>
          <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800/50 transition-all duration-200 text-sm text-left group">
            <Settings size={16} className="text-gray-500 group-hover:text-primary transition-colors" />
            <span className="font-medium group-hover:text-gray-800 dark:group-hover:text-gray-100">Settings</span>
          </button>
          <div className="mt-4 pt-3 border-t border-gray-200 dark:border-gray-800/30 flex items-center gap-3 px-3 py-3">
            <div className="h-10 w-10 rounded-full bg-gradient-to-br from-emerald-500 to-primary flex items-center justify-center text-white font-bold text-sm shadow-lg">
              H
            </div>
            <div className="flex-1">
              <div className="text-sm font-semibold text-gray-800 dark:text-gray-100">Health AI</div>
              <div className="text-xs text-gray-500">Active</div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
