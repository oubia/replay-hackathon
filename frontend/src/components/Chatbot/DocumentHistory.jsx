import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Image, Trash2, Clock, ChevronRight } from 'lucide-react';
import clsx from 'clsx';

const DocumentHistory = ({ documents = [], onSelectDocument, onDeleteDocument }) => {
  const [expandedCategory, setExpandedCategory] = useState('recent');

  const getFileIcon = (type) => {
    if (type.startsWith('image/')) {
      return { icon: Image, color: 'text-blue-500' };
    }
    return { icon: FileText, color: 'text-orange-500' };
  };

  const categorizeDocuments = () => {
    const now = Date.now();
    const today = [];
    const thisWeek = [];
    const older = [];

    documents.forEach(doc => {
      const diff = now - doc.timestamp;
      const daysDiff = diff / (1000 * 60 * 60 * 24);

      if (daysDiff < 1) {
        today.push(doc);
      } else if (daysDiff < 7) {
        thisWeek.push(doc);
      } else {
        older.push(doc);
      }
    });

    return { today, thisWeek, older };
  };

  const categories = categorizeDocuments();

  const DocumentCategory = ({ title, docs, categoryId }) => {
    if (docs.length === 0) return null;

    const isExpanded = expandedCategory === categoryId;

    return (
      <div className="space-y-2">
        <button
          onClick={() => setExpandedCategory(isExpanded ? null : categoryId)}
          className="w-full flex items-center justify-between px-3 py-2 text-xs font-semibold uppercase tracking-wider text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
        >
          <span>{title}</span>
          <motion.div
            animate={{ rotate: isExpanded ? 90 : 0 }}
            transition={{ duration: 0.2 }}
          >
            <ChevronRight size={14} />
          </motion.div>
        </button>

        <motion.div
          initial={false}
          animate={{
            height: isExpanded ? 'auto' : 0,
            opacity: isExpanded ? 1 : 0,
          }}
          transition={{ duration: 0.2 }}
          className="overflow-hidden space-y-1"
        >
          {docs.map((doc) => {
            const { icon: Icon, color } = getFileIcon(doc.type);

            return (
              <motion.button
                key={doc.id}
                onClick={() => onSelectDocument?.(doc)}
                whileHover={{ x: 4 }}
                className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-800/60 transition-all duration-200 text-sm text-gray-300 text-left group"
              >
                <Icon size={16} className={`flex-shrink-0 ${color}`} />
                <div className="flex-1 min-w-0">
                  <p className="truncate text-gray-200 group-hover:text-white font-medium">
                    {doc.name}
                  </p>
                  <p className="text-xs text-gray-500 flex items-center gap-1">
                    <Clock size={12} />
                    {formatDate(doc.timestamp)}
                  </p>
                </div>
                <motion.button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteDocument?.(doc.id);
                  }}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  className="flex-shrink-0 opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-400 transition-all duration-200"
                >
                  <Trash2 size={14} />
                </motion.button>
              </motion.button>
            );
          })}
        </motion.div>
      </div>
    );
  };

  if (documents.length === 0) {
    return (
      <div className="px-3 py-6 text-center">
        <FileText size={24} className="text-gray-600 mx-auto mb-2 opacity-50" />
        <p className="text-xs text-gray-500">No documents yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-3 px-3 py-4">
      <DocumentCategory title="Today" docs={categories.today} categoryId="today" />
      <DocumentCategory title="This Week" docs={categories.thisWeek} categoryId="thisWeek" />
      <DocumentCategory title="Older" docs={categories.older} categoryId="older" />
    </div>
  );
};

function formatDate(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;
  const hours = diff / (1000 * 60 * 60);

  if (hours < 1) {
    const minutes = Math.floor(diff / (1000 * 60));
    return `${minutes}m ago`;
  } else if (hours < 24) {
    return `${Math.floor(hours)}h ago`;
  } else {
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  }
}

export default DocumentHistory;
