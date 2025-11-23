import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Copy, Download, AlertCircle, CheckCircle, Info } from 'lucide-react';
import clsx from 'clsx';

const AnalysisReport = ({ report, onCopy }) => {
  const [expandedSections, setExpandedSections] = useState({});

  if (!report || !report.sections) {
    return null;
  }

  const toggleSection = (sectionId) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionId]: !prev[sectionId]
    }));
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
      case 'critical':
        return 'bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-800/50 text-red-900 dark:text-red-100';
      case 'medium':
      case 'warning':
        return 'bg-orange-50 dark:bg-orange-950/30 border-orange-200 dark:border-orange-800/50 text-orange-900 dark:text-orange-100';
      case 'low':
      case 'info':
        return 'bg-blue-50 dark:bg-blue-950/30 border-blue-200 dark:border-blue-800/50 text-blue-900 dark:text-blue-100';
      default:
        return 'bg-gray-50 dark:bg-gray-800/50 border-gray-200 dark:border-gray-700/50 text-gray-900 dark:text-gray-100';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
      case 'critical':
        return <AlertCircle size={18} className="text-red-500" />;
      case 'low':
      case 'info':
        return <Info size={18} className="text-blue-500" />;
      default:
        return <CheckCircle size={18} className="text-gray-500" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="w-full rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-700/50 shadow-lg dark:shadow-xl bg-white dark:bg-gray-800/80 backdrop-blur-sm"
    >
      {/* Report Header */}
      {report.title && (
        <div className="bg-gradient-to-r from-emerald-50/50 to-blue-50/50 dark:from-emerald-950/30 dark:to-blue-950/30 border-b border-gray-200 dark:border-gray-700/50 px-6 py-4">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">
                {report.title}
              </h3>
              {report.summary && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {report.summary}
                </p>
              )}
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onCopy?.(report)}
              className="flex-shrink-0 p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-white dark:hover:bg-gray-700/50 rounded-lg transition-all duration-200"
              title="Copy report"
            >
              <Copy size={18} />
            </motion.button>
          </div>
        </div>
      )}

      {/* Report Sections */}
      <div className="divide-y divide-gray-200 dark:divide-gray-700/50">
        {report.sections.map((section, idx) => (
          <motion.div key={idx} className="border-0">
            {/* Section Header */}
            <motion.button
              onClick={() => toggleSection(idx)}
              className={clsx(
                "w-full px-6 py-4 text-left flex items-start justify-between gap-4 hover:bg-gray-50/50 dark:hover:bg-gray-700/30 transition-colors duration-200",
                expandedSections[idx] && "bg-gray-50/50 dark:bg-gray-700/20"
              )}
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3">
                  {getSeverityIcon(section.severity)}
                  <h4 className="font-semibold text-gray-900 dark:text-gray-100">
                    {section.title}
                  </h4>
                </div>
                {section.subtitle && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1 ml-6">
                    {section.subtitle}
                  </p>
                )}
              </div>
              <motion.div
                animate={{ rotate: expandedSections[idx] ? 180 : 0 }}
                transition={{ duration: 0.2 }}
                className="flex-shrink-0 text-gray-400"
              >
                <ChevronDown size={20} />
              </motion.div>
            </motion.button>

            {/* Section Content */}
            <AnimatePresence>
              {expandedSections[idx] && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  className="overflow-hidden"
                >
                  <div className={clsx(
                    "px-6 py-4 border-t border-gray-200 dark:border-gray-700/30",
                    getSeverityColor(section.severity)
                  )}>
                    <div className="space-y-3">
                      {/* Main Content */}
                      {section.content && (
                        <p className="text-sm leading-relaxed">
                          {section.content}
                        </p>
                      )}

                      {/* Key Points */}
                      {section.keyPoints && section.keyPoints.length > 0 && (
                        <div className="space-y-2 pt-2">
                          <p className="text-xs font-semibold uppercase tracking-wide opacity-75">
                            Key Points
                          </p>
                          <ul className="space-y-1">
                            {section.keyPoints.map((point, pointIdx) => (
                              <li key={pointIdx} className="flex items-start gap-2 text-sm">
                                <span className="flex-shrink-0 w-1.5 h-1.5 rounded-full mt-1.5 opacity-60" />
                                <span>{point}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Recommendations */}
                      {section.recommendations && section.recommendations.length > 0 && (
                        <div className="space-y-2 pt-2">
                          <p className="text-xs font-semibold uppercase tracking-wide opacity-75">
                            Recommendations
                          </p>
                          <ul className="space-y-1">
                            {section.recommendations.map((rec, recIdx) => (
                              <li key={recIdx} className="flex items-start gap-2 text-sm">
                                <span className="flex-shrink-0 w-1.5 h-1.5 rounded-full mt-1.5 opacity-60" />
                                <span>{rec}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Values/Data Points */}
                      {section.values && Object.keys(section.values).length > 0 && (
                        <div className="grid grid-cols-2 gap-3 pt-2">
                          {Object.entries(section.values).map(([key, value]) => (
                            <div key={key} className="bg-white/30 dark:bg-gray-700/30 rounded-lg p-3">
                              <p className="text-xs uppercase tracking-wide opacity-60 mb-1">
                                {key}
                              </p>
                              <p className="font-semibold text-base">
                                {value}
                              </p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        ))}
      </div>

      {/* Report Footer */}
      {(report.disclaimer || report.nextSteps) && (
        <div className="bg-gray-50/50 dark:bg-gray-700/20 border-t border-gray-200 dark:border-gray-700/50 px-6 py-4 space-y-3">
          {report.nextSteps && (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-400 mb-2">
                Next Steps
              </p>
              <p className="text-sm text-gray-700 dark:text-gray-300">
                {report.nextSteps}
              </p>
            </div>
          )}
          {report.disclaimer && (
            <div className="pt-2 border-t border-gray-200 dark:border-gray-700/50">
              <p className="text-xs text-gray-500 dark:text-gray-500 italic">
                ⚠️ {report.disclaimer}
              </p>
            </div>
          )}
        </div>
      )}
    </motion.div>
  );
};

export default AnalysisReport;
