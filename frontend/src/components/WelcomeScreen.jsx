import React from 'react';
import { motion } from 'framer-motion';
import { Activity, FileText, Pill, Heart, Eye, Brain, Zap } from 'lucide-react';

const WelcomeScreen = ({ onQuickAction }) => {
  const quickActions = [
    {
      id: 'symptom-check',
      icon: Activity,
      title: 'Symptom Checker',
      description: 'Describe your symptoms for analysis',
      gradient: 'from-blue-600 to-cyan-500',
      textColor: 'text-blue-600 dark:text-blue-400'
    },
    {
      id: 'lab-results',
      icon: FileText,
      title: 'Lab Results',
      description: 'Analyze and understand test results',
      gradient: 'from-indigo-600 to-blue-500',
      textColor: 'text-indigo-600 dark:text-indigo-400'
    },
    {
      id: 'medication',
      icon: Pill,
      title: 'Medications',
      description: 'Get information about medications',
      gradient: 'from-cyan-500 to-blue-600',
      textColor: 'text-cyan-600 dark:text-cyan-400'
    },
    {
      id: 'imaging',
      icon: Eye,
      title: 'Medical Records',
      description: 'Upload and analyze medical images',
      gradient: 'from-blue-500 to-indigo-600',
      textColor: 'text-blue-600 dark:text-blue-400'
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5, ease: 'easeOut' },
    },
  };

  return (
    <div className="flex flex-col items-center justify-center h-full text-center p-6 md:p-8">
      {/* Header */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="relative mb-8"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 via-cyan-500/20 to-indigo-600/20 rounded-full blur-3xl" />
        <div className="relative bg-gradient-to-br from-blue-100 to-cyan-100 dark:from-blue-900/40 dark:to-cyan-900/40 p-6 md:p-8 rounded-3xl shadow-2xl ring-4 ring-blue-200 dark:ring-blue-500/20">
          <Heart size={56} className="text-blue-600 dark:text-cyan-400 mx-auto" />
        </div>
      </motion.div>

      {/* Welcome Text */}
      <motion.h1
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.1, duration: 0.5 }}
        className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-gray-100 mb-2"
      >
        Welcome to Nexus Health AI
      </motion.h1>

      <motion.p
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.5 }}
        className="text-base md:text-lg text-gray-600 dark:text-gray-300 max-w-2xl mb-12"
      >
        Your intelligent health companion. Upload documents, describe symptoms, or ask health-related questions for AI-powered insights.
      </motion.p>

      {/* Quick Actions */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl mb-8"
      >
        {quickActions.map((action) => {
          const Icon = action.icon;
          return (
            <motion.button
              key={action.id}
              variants={itemVariants}
              onClick={() => onQuickAction(action.id)}
              className="group relative overflow-hidden rounded-2xl p-6 text-left transition-all duration-300 hover:shadow-lg"
            >
              {/* Gradient Background */}
              <div className={`absolute inset-0 bg-gradient-to-br ${action.gradient} opacity-5 group-hover:opacity-15 transition-opacity duration-300`} />

              {/* Border */}
              <div className="absolute inset-0 rounded-2xl border border-gray-200 dark:border-gray-600/30 group-hover:border-blue-300 dark:group-hover:border-cyan-500/50 transition-colors duration-300" />

              {/* Content */}
              <div className="relative z-10 flex items-start gap-4">
                <div className={`flex-shrink-0 p-3 rounded-xl bg-gradient-to-br ${action.gradient} shadow-lg`}>
                  <Icon size={24} className="text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-800 dark:text-gray-100 mb-1">
                    {action.title}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {action.description}
                  </p>
                </div>
              </div>
            </motion.button>
          );
        })}
      </motion.div>

      {/* Features List */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.5 }}
        className="flex gap-6 md:gap-8 flex-wrap justify-center text-sm"
      >
        <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
          <Brain size={16} className="text-blue-600 dark:text-cyan-400" />
          <span>Medical AI</span>
        </div>
        <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
          <Zap size={16} className="text-cyan-600 dark:text-cyan-500" />
          <span>Real-Time Analysis</span>
        </div>
        <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
          <FileText size={16} className="text-indigo-600 dark:text-indigo-400" />
          <span>HIPAA-Compatible</span>
        </div>
      </motion.div>
    </div>
  );
};

export default WelcomeScreen;
