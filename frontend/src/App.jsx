import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import {
  Search, Play, Loader2, Mail, Users, TrendingUp, AlertCircle,
  CheckCircle2, Sparkles, LayoutDashboard, BarChart3,
  ChevronRight, Database, Zap, X, ArrowRight, Bot, Globe, Target, Send, Inbox, LineChart
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

// --- ONBOARDING MODAL COMPONENT ---
function OnboardingModal({ isOpen, onClose }) {
  const [step, setStep] = useState(0);

  const steps = [
    {
      icon: Bot,
      color: 'bg-accent',
      title: 'Welcome to SalesAI',
      description: 'Your AI-powered sales automation agent that finds, qualifies, and engages leads automatically.',
      details: [
        'Automates the entire B2B sales prospecting process',
        'Uses 6 specialized AI agents working together',
        'Saves hours of manual research and outreach'
      ]
    },
    {
      icon: Globe,
      color: 'bg-accent',
      title: 'Step 1: Lead Generation',
      description: 'Enter a search query describing your ideal customer profile.',
      details: [
        'Example: "SaaS startups in Berlin looking for AI tools"',
        'The agent searches the web for matching companies',
        'Collects URLs of potential prospects'
      ]
    },
    {
      icon: Mail,
      color: 'bg-accent',
      title: 'Step 2: Enrichment & Scoring',
      description: 'The AI enriches leads and scores them based on fit.',
      details: [
        'Scrapes websites to find contact emails',
        'AI analyzes each lead for relevance',
        'Classifies as Hot, Warm, or Cold prospects'
      ]
    },
    {
      icon: Send,
      color: 'bg-green-500',
      title: 'Step 3: Engagement & Tracking',
      description: 'Automated outreach and response monitoring.',
      details: [
        'Sends personalized emails to qualified leads',
        'Monitors inbox for replies',
        'Forecasts conversion potential'
      ]
    },
    {
      icon: Target,
      color: 'bg-orange-500',
      title: 'How to Use',
      description: 'Follow these simple steps to get started:',
      details: [
        '1. Type your target audience in the search box',
        '2. Click "Run" to start the AI pipeline',
        '3. Watch real-time status updates',
        '4. View results in Dashboard, Leads, and Analytics tabs'
      ]
    }
  ];

  const currentStep = steps[step];

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          className="bg-card rounded-none shadow-2xl max-w-lg w-full overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className={cn("p-8 text-white text-center relative", currentStep.color)}>
            <button onClick={onClose} className="absolute top-4 right-4 text-white/70 hover:text-white">
              <X className="w-6 h-6" />
            </button>
            <div className="w-20 h-20 bg-card/20 rounded-full mx-auto flex items-center justify-center mb-4">
              <currentStep.icon className="w-10 h-10" />
            </div>
            <h2 className="text-2xl font-bold">{currentStep.title}</h2>
          </div>

          {/* Content */}
          <div className="p-8">
            <p className="text-slate-400 text-center mb-6">{currentStep.description}</p>
            <ul className="space-y-3">
              {currentStep.details.map((detail, i) => (
                <li key={i} className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-300">{detail}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Footer */}
          <div className="px-8 pb-8 flex items-center justify-between">
            {/* Progress Dots */}
            <div className="flex gap-2">
              {steps.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setStep(i)}
                  className={cn(
                    "w-2.5 h-2.5 rounded-full transition-all",
                    i === step ? "bg-accent w-6" : "bg-line hover:bg-line"
                  )}
                />
              ))}
            </div>

            {/* Navigation */}
            <div className="flex gap-3">
              {step > 0 && (
                <button
                  onClick={() => setStep(step - 1)}
                  className="px-4 py-2 text-slate-400 hover:text-white font-medium"
                >
                  Back
                </button>
              )}
              {step < steps.length - 1 ? (
                <button
                  onClick={() => setStep(step + 1)}
                  className="px-6 py-2.5 bg-accent text-white rounded-none font-medium hover:bg-accent-hover flex items-center gap-2"
                >
                  Next <ArrowRight className="w-4 h-4" />
                </button>
              ) : (
                <button
                  onClick={onClose}
                  className="px-6 py-2.5 bg-green-600 text-white rounded-none font-medium hover:bg-green-700 flex items-center gap-2"
                >
                  Get Started <Sparkles className="w-4 h-4" />
                </button>
              )}
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');
  const [forecast, setForecast] = useState([]);
  const [leads, setLeads] = useState([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [error, setError] = useState('');
  const [showOnboarding, setShowOnboarding] = useState(true); // Show on first load

  const runPipeline = async () => {
    if (!query) return;
    setLoading(true);
    setStatus('Initializing AI Agents...');
    setError('');
    setActiveTab('dashboard');

    try {
      await axios.post(`${API_BASE}/api/pipeline/run`, { query });

      const intervalId = setInterval(async () => {
        try {
          const res = await axios.get(`${API_BASE}/api/pipeline/status`);
          const { status: pipelineStatus, message } = res.data;

          setStatus(message);

          if (pipelineStatus === 'completed') {
            clearInterval(intervalId);
            setLoading(false);
            setStatus('Pipeline Finished! Loading data...');
            await fetchData();
            setStatus('Ready');
          } else if (pipelineStatus === 'error') {
            clearInterval(intervalId);
            setLoading(false);
            setError(`Pipeline failed: ${message}`);
          }
        } catch (pollErr) {
          console.error("Polling error", pollErr);
        }
      }, 2000);

    } catch (err) {
      console.error(err);
      setLoading(false);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Failed to start pipeline. Is the backend running?');
      }
    }
  };

  const fetchData = async () => {
    try {
      const [forecastRes, leadsRes] = await Promise.all([
        axios.get(`${API_BASE}/api/data/forecast`),
        axios.get(`${API_BASE}/api/data/leads`),
      ]);
      setForecast(forecastRes.data);
      setLeads(leadsRes.data);
    } catch (err) {
      console.error("Error fetching data", err);
    }
  };

  const chartData = React.useMemo(() => {
    const counts = {};
    forecast.forEach(item => {
      counts[item.category] = (counts[item.category] || 0) + 1;
    });
    return Object.keys(counts).map(key => ({ name: key, value: counts[key] }));
  }, [forecast]);

  const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  const hasData = forecast.length > 0 || leads.length > 0;

  // --- RENDER FUNCTIONS FOR EACH TAB ---

  const renderDashboard = () => {
    if (!hasData) {
      return (
        <div className="text-center py-16 glass rounded-none">
          <div className="w-20 h-20 bg-accent/15 rounded-full mx-auto flex items-center justify-center mb-6">
            <LayoutDashboard className="w-10 h-10 text-accent" />
          </div>
          <h3 className="text-xl font-semibold text-slate-300">Dashboard Overview</h3>
          <p className="text-slate-400 mt-2 max-w-md mx-auto">Run a search query to see your lead metrics, pipeline forecast, and recent opportunities here.</p>
        </div>
      );
    }

    return (
      <div className="space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { label: "Leads Generated", value: leads.length, icon: Users, color: "text-accent", bg: "bg-accent/10" },
            { label: "Emails Qualified", value: leads.filter(l => l.emails && l.emails !== "N/A").length, icon: Mail, color: "text-accent", bg: "bg-accent/10" },
            { label: "Hot Opportunities", value: forecast.filter(f => f.category === 'hot').length, icon: TrendingUp, color: "text-emerald-400", bg: "bg-emerald-500/10" }
          ].map((stat, idx) => (
            <div key={idx} className="glass-card p-6 rounded-none">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-slate-400 font-medium mb-1">{stat.label}</p>
                  <h3 className="text-4xl font-bold text-white">{stat.value}</h3>
                </div>
                <div className={cn("p-3 rounded-none", stat.bg, stat.color)}>
                  <stat.icon className="w-6 h-6" />
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="glass p-6 rounded-none lg:col-span-1 min-h-[350px] flex flex-col">
            <h3 className="text-lg font-bold text-white mb-4">Pipeline Forecast</h3>
            <div className="flex-1 w-full">
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={chartData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} dataKey="value">
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="glass p-6 rounded-none lg:col-span-2 flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white">Recent Opportunities</h3>
              <button onClick={() => setActiveTab('leads')} className="text-sm text-accent font-medium hover:underline flex items-center">
                View All <ChevronRight className="w-4 h-4" />
              </button>
            </div>
            <div className="overflow-auto flex-1">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="pb-3 text-slate-400">Email</th>
                    <th className="pb-3 text-slate-400">Status</th>
                    <th className="pb-3 text-slate-400">Insight</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {forecast.slice(0, 5).map((item, idx) => (
                    <tr key={idx}>
                      <td className="py-3 truncate max-w-[150px]">{item.email}</td>
                      <td className="py-3">
                        <span className={cn("px-2 py-1 rounded-full text-xs font-semibold", item.category === 'hot' ? "bg-red-500/15 text-red-400" : "bg-accent/15 text-accent")}>
                          {item.category}
                        </span>
                      </td>
                      <td className="py-3 text-slate-400 truncate max-w-xs">{item.reason}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderLeads = () => {
    if (!hasData) {
      return (
        <div className="text-center py-16 glass rounded-none">
          <div className="w-20 h-20 bg-accent/15 rounded-full mx-auto flex items-center justify-center mb-6">
            <Database className="w-10 h-10 text-accent" />
          </div>
          <h3 className="text-xl font-semibold text-slate-300">Leads Database</h3>
          <p className="text-slate-400 mt-2 max-w-md mx-auto">Your collected leads will appear here with URLs, emails, and enrichment data after you run a search.</p>
        </div>
      );
    }

    return (
      <div className="glass p-6 rounded-none">
        <h3 className="text-xl font-bold text-white mb-6">All Leads ({leads.length})</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-line">
                <th className="pb-4 text-sm font-semibold text-slate-400 uppercase">URL</th>
                <th className="pb-4 text-sm font-semibold text-slate-400 uppercase">Emails Found</th>
              </tr>
            </thead>
            <tbody className="divide-y text-sm">
              {leads.map((lead, i) => (
                <tr key={i} className="hover:bg-surface/50">
                  <td className="py-4 pr-4">
                    <a href={lead.url} target="_blank" rel="noreferrer" className="text-accent hover:underline truncate block max-w-md">{lead.url}</a>
                  </td>
                  <td className="py-4 text-slate-300">
                    {lead.emails && lead.emails !== 'N/A' ? (
                      <div className="flex flex-wrap gap-2">
                        {String(lead.emails).split(',').map((email, j) => (
                          <span key={j} className="bg-accent/10 text-accent px-2 py-1 rounded-none text-xs">{email.trim()}</span>
                        ))}
                      </div>
                    ) : <span className="text-slate-500 italic">No emails found</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  const renderAnalytics = () => {
    if (!hasData) {
      return (
        <div className="text-center py-16 glass rounded-none">
          <div className="w-20 h-20 bg-emerald-500/15 rounded-full mx-auto flex items-center justify-center mb-6">
            <Zap className="w-10 h-10 text-green-500" />
          </div>
          <h3 className="text-xl font-semibold text-slate-300">Advanced Analytics</h3>
          <p className="text-slate-400 mt-2 max-w-md mx-auto">Conversion rates, lead distribution charts, and AI-powered insights will be available after your first pipeline run.</p>
        </div>
      );
    }

    const hotRate = ((forecast.filter(f => f.category === 'hot').length / (forecast.length || 1)) * 100).toFixed(0);

    return (
      <div className="glass p-6 rounded-none space-y-8">
        <div className="flex items-center gap-3">
          <BarChart3 className="w-6 h-6 text-accent" />
          <h3 className="text-xl font-bold text-white">Advanced Analytics</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-card/50 rounded-none p-6 border border-line">
            <h4 className="font-semibold text-slate-300 mb-4">Lead Distribution</h4>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={chartData} innerRadius={50} outerRadius={70} dataKey="value">
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-card/50 rounded-none p-6 border border-line flex flex-col justify-center items-center text-center">
            <TrendingUp className="w-12 h-12 text-green-500 mb-3" />
            <h4 className="text-5xl font-bold text-white">{hotRate}%</h4>
            <p className="text-slate-400 mt-2">Hot Lead Rate</p>
            <p className="text-xs text-slate-500 mt-2 max-w-xs">Percentage of leads classified as 'hot' by AI scoring.</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen font-sans text-white flex">
      {/* Onboarding Modal */}
      <OnboardingModal isOpen={showOnboarding} onClose={() => setShowOnboarding(false)} />

      {/* Sidebar */}
      <motion.aside
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        className="w-64 glass border-r border-line hidden md:flex flex-col sticky top-0 h-screen z-10"
      >
        <div className="p-6 flex items-center gap-3">
          <div className="bg-accent p-2.5 shadow-lg shadow-accent/20">
            <Sparkles className="text-black w-6 h-6" />
          </div>
          <span className="font-[Syne] text-xl font-extrabold uppercase tracking-tight text-white">Sales<span className="text-accent">AI</span></span>
        </div>

        <nav className="flex-1 px-4 space-y-2 mt-4">
          {[
            { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
            { id: 'leads', icon: Users, label: 'Leads' },
            { id: 'analytics', icon: BarChart3, label: 'Analytics' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={cn(
                "w-full flex items-center gap-3 px-4 py-3 rounded-none transition-all duration-200 group relative",
                activeTab === item.id
                  ? "bg-accent/10 text-accent font-medium"
                  : "text-slate-400 hover:bg-card/50 hover:text-white"
              )}
            >
              <item.icon className={cn("w-5 h-5", activeTab === item.id ? "text-accent" : "text-slate-500")} />
              {item.label}
              {activeTab === item.id && (
                <motion.div layoutId="active-pill" className="absolute left-0 top-0 bottom-0 w-1 bg-accent rounded-r-full" />
              )}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-line">
          <button
            onClick={() => setShowOnboarding(true)}
            className="w-full text-left glass-card p-4 rounded-none hover:bg-accent/10 transition"
          >
            <p className="eyebrow mb-1">Need Help?</p>
            <p className="text-sm text-accent font-medium">View User Guide</p>
          </button>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 overflow-x-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-8 py-8 md:py-12 space-y-8">

          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold text-white">Welcome back, <span className="text-accent">Agent</span></h1>
            <p className="text-slate-400 mt-1">Manage your automated sales pipelines efficiently.</p>
          </div>

          {/* Search Hero */}
          <div className="glass p-1 rounded-none shadow-xl ring-1 ring-black/5">
            <div className="bg-card/80 rounded-none p-6 md:p-8 backdrop-blur-sm">
              <div className="max-w-3xl mx-auto text-center space-y-6">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/30 text-accent text-sm font-medium">
                  <Sparkles className="w-4 h-4" />
                  <span>New Campaign Wizard</span>
                </div>
                <h2 className="text-2xl md:text-3xl font-semibold text-white">
                  What leads are we targeting today?
                </h2>
                <div className="relative group max-w-2xl mx-auto">
                  <div className="absolute -inset-1 bg-gradient-to-r from-accent to-accent-hover rounded-none opacity-20 group-hover:opacity-40 transition blur-lg"></div>
                  <div className="relative flex items-center bg-card rounded-none shadow-lg border border-line p-2">
                    <Search className="ml-4 text-slate-500 w-6 h-6" />
                    <input
                      type="text"
                      placeholder="e.g. 'SaaS startups in Berlin looking for AI tools'"
                      className="w-full px-4 py-3 text-lg bg-transparent border-none focus:ring-0 placeholder-gray-400"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && runPipeline()}
                    />
                    <button
                      onClick={runPipeline}
                      disabled={loading || !query}
                      className={cn(
                        "px-6 py-3 rounded-none font-medium text-white flex items-center gap-2 shadow-md",
                        loading || !query ? "bg-line cursor-not-allowed" : "bg-canvas hover:bg-card"
                      )}
                    >
                      {loading ? <Loader2 className="animate-spin w-5 h-5" /> : <Play className="w-5 h-5 fill-current" />}
                      <span className="hidden sm:inline">Run</span>
                    </button>
                  </div>
                </div>
                {status && (
                  <div className="flex items-center justify-center gap-2 text-sm text-slate-400">
                    {loading ? <Loader2 className="w-4 h-4 animate-spin text-accent" /> : <CheckCircle2 className="w-4 h-4 text-green-500" />}
                    {status}
                  </div>
                )}
              </div>
            </div>
          </div>

          {error && (
            <div className="p-4 bg-red-500/10 text-red-400 rounded-none flex items-center gap-3 border border-red-100">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              {error}
            </div>
          )}

          {/* TAB CONTENT */}
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {activeTab === 'dashboard' && renderDashboard()}
            {activeTab === 'leads' && renderLeads()}
            {activeTab === 'analytics' && renderAnalytics()}
          </motion.div>

        </div>
      </main>
    </div>
  );
}

export default App;
