import React from 'react';
import { 
  Sprout, 
  ArrowRight, 
  ShieldCheck, 
  TrendingUp, 
  Droplet, 
  Sparkles, 
  CheckCircle2, 
  Activity,
  Layers,
  ChevronRight
} from 'lucide-react';
import { useApp } from '../context/AppContext';

export const LandingHero = () => {
  const { setCurrentView, setIsAuthModalOpen, setAuthMode, user } = useApp();

  return (
    <div className="min-h-screen bg-[#F3F6F4] flex flex-col relative overflow-hidden select-none">
      {/* Top Navbar matching Reference 3 */}
      <nav className="w-full max-w-7xl mx-auto px-6 py-6 flex items-center justify-between z-20">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center shadow-lg shadow-emerald-600/20">
            <Sprout className="w-6 h-6 text-white" />
          </div>
          <span className="text-2xl font-black tracking-tight text-slate-900">
            AgriVision <span className="text-emerald-600">AI</span>
          </span>
        </div>

        {/* Center Links */}
        <div className="hidden md:flex items-center gap-8 text-sm font-semibold text-slate-600">
          <button onClick={() => setCurrentView('landing')} className="text-emerald-700 hover:text-emerald-800">Home</button>
          <button onClick={() => setCurrentView('disease')} className="hover:text-emerald-700 transition-colors">Features</button>
          <button onClick={() => setCurrentView('forecast')} className="hover:text-emerald-700 transition-colors">About</button>
          <button onClick={() => setCurrentView('dashboard')} className="hover:text-emerald-700 transition-colors">Dashboard</button>
        </div>

        {/* CTA Button */}
        <div className="flex items-center gap-3">
          {user ? (
            <button
              onClick={() => setCurrentView('dashboard')}
              className="px-5 py-2.5 rounded-full bg-emerald-800 hover:bg-emerald-900 text-white font-semibold text-xs flex items-center gap-2 shadow-lg shadow-emerald-900/20 hover:shadow-emerald-900/30 transition-all hover:scale-105"
            >
              <span>Go to Dashboard</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              onClick={() => {
                setAuthMode('signup');
                setIsAuthModalOpen(true);
              }}
              className="px-6 py-2.5 rounded-full bg-emerald-800 hover:bg-emerald-900 text-white font-semibold text-xs flex items-center gap-2 shadow-lg shadow-emerald-900/20 hover:shadow-emerald-900/30 transition-all hover:scale-105"
            >
              <span>Get Started</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </nav>

      {/* Hero Body */}
      <div className="w-full max-w-7xl mx-auto px-6 pt-6 pb-12 flex-1 flex flex-col justify-between z-10 relative">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center pt-4">
          
          {/* Left Text Column */}
          <div className="lg:col-span-5 space-y-6">
            {/* Pill */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-100/80 border border-emerald-200 text-emerald-800 text-xs font-bold tracking-wide">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>Smart Agriculture • Powered by AI</span>
            </div>

            {/* Title matching Reference 3 */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight leading-[1.1]">
              AgriVision <span className="text-emerald-700">AI</span>
            </h1>
            <p className="text-xl sm:text-2xl font-bold text-slate-800 tracking-tight">
              Unified Crop Intelligence & Precision Agriculture Platform
            </p>

            <p className="text-slate-600 text-sm sm:text-base font-normal leading-relaxed max-w-md">
              Detect diseases, predict yield, analyze stress, and get expert recommendations — all in one place.
            </p>

            {/* CTA Button */}
            <div className="pt-2 flex flex-wrap items-center gap-4">
              <button
                onClick={() => setCurrentView('disease')}
                className="px-7 py-3.5 rounded-full bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm flex items-center gap-2.5 shadow-xl shadow-emerald-800/25 hover:shadow-emerald-800/40 transition-all hover:-translate-y-0.5"
              >
                <Sprout className="w-4 h-4 text-emerald-200" />
                <span>Analyze Your Crop</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <button
                onClick={() => setCurrentView('dashboard')}
                className="px-6 py-3.5 rounded-full bg-white hover:bg-slate-50 text-slate-700 border border-slate-200/90 font-bold text-sm shadow-sm transition-all"
              >
                View Live Dashboard
              </button>
            </div>
          </div>

          {/* Right Floating Perspective Mockup matching Reference 3 */}
          <div className="lg:col-span-7 relative">
            {/* Drone in the sky photo background simulation */}
            <div className="relative rounded-3xl overflow-hidden shadow-2xl border border-slate-200/80 bg-gradient-to-br from-amber-50/50 via-emerald-50/30 to-green-100/40 p-4 sm:p-6">
              
              {/* Drone & Sunset Field Background */}
              <div className="absolute inset-0 z-0 opacity-40">
                <img
                  src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200&auto=format&fit=crop&q=80"
                  alt="Farm field"
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-emerald-950/60 via-transparent to-transparent" />
              </div>

              {/* Floating Glass Mockup Card */}
              <div className="relative z-10 glass-panel rounded-2xl p-5 shadow-2xl border border-white/90">
                {/* Header */}
                <div className="flex items-center justify-between pb-4 border-b border-slate-200/60">
                  <div className="flex items-center gap-2.5">
                    <div className="w-7 h-7 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
                      <Sprout className="w-4 h-4" />
                    </div>
                    <span className="font-bold text-sm text-slate-800">Crop Analysis Dashboard</span>
                  </div>
                  <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-bold">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
                    <span>Live Analysis</span>
                  </div>
                </div>

                {/* Grid Content */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 mt-4">
                  {/* Left: Disease Detection Box */}
                  <div className="bg-white rounded-xl p-3 border border-slate-100 shadow-sm flex items-center gap-3">
                    <div className="w-16 h-16 rounded-lg overflow-hidden relative shrink-0">
                      <img
                        src="https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=300&auto=format&fit=crop&q=80"
                        alt="Leaf"
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute inset-1 border border-emerald-400 rounded flex items-center justify-center">
                        <span className="bg-emerald-600 text-white text-[8px] font-bold px-1 rounded">Healthy</span>
                      </div>
                    </div>
                    <div>
                      <p className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Disease Detection</p>
                      <p className="text-sm font-bold text-slate-800 flex items-center gap-1">
                        Healthy Leaf <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 inline" />
                      </p>
                      <p className="text-xs text-slate-500">Confidence: <span className="font-semibold text-emerald-700">98.7%</span></p>
                    </div>
                  </div>

                  {/* Right: Yield Prediction Box */}
                  <div className="bg-white rounded-xl p-3 border border-slate-100 shadow-sm flex items-center justify-between">
                    <div>
                      <p className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Yield Prediction</p>
                      <p className="text-xl font-black text-slate-900 mt-0.5">8.5 <span className="text-xs font-normal text-slate-500">t/ha</span></p>
                    </div>
                    {/* Mini Sparkline Chart */}
                    <div className="w-16 h-8 flex items-end gap-1">
                      <div className="w-2 bg-emerald-200 rounded-t h-3" />
                      <div className="w-2 bg-emerald-300 rounded-t h-5" />
                      <div className="w-2 bg-emerald-400 rounded-t h-4" />
                      <div className="w-2 bg-emerald-500 rounded-t h-7" />
                      <div className="w-2 bg-emerald-600 rounded-t h-8" />
                    </div>
                  </div>

                  {/* Left bottom: Crop Health Donut Gauge */}
                  <div className="bg-white rounded-xl p-3 border border-slate-100 shadow-sm flex items-center justify-between">
                    <div>
                      <p className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Crop Health</p>
                      <div className="flex items-center gap-3 mt-1">
                        <div className="relative w-12 h-12 flex items-center justify-center">
                          <svg className="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
                            <path
                              className="text-slate-100"
                              strokeWidth="3.5"
                              stroke="currentColor"
                              fill="none"
                              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            />
                            <path
                              className="text-emerald-500"
                              strokeDasharray="92, 100"
                              strokeWidth="3.5"
                              strokeLinecap="round"
                              stroke="currentColor"
                              fill="none"
                              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            />
                          </svg>
                          <span className="absolute text-xs font-black text-slate-900">92%</span>
                        </div>
                        <div className="space-y-0.5 text-[10px]">
                          <span className="flex items-center gap-1 text-slate-600"><span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> Healthy</span>
                          <span className="flex items-center gap-1 text-slate-400"><span className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Stressed</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Right bottom: Risk & Weather */}
                  <div className="bg-white rounded-xl p-3 border border-slate-100 shadow-sm flex items-center justify-between">
                    <div>
                      <p className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Risk Level</p>
                      <p className="text-sm font-bold text-emerald-700 mt-0.5">Low Risk</p>
                      <p className="text-[10px] text-slate-400">All parameters nominal</p>
                    </div>
                    <div className="text-right">
                      <p className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">14-Day Forecast</p>
                      <p className="text-sm font-bold text-slate-800 mt-0.5">28°C</p>
                      <p className="text-[10px] text-slate-400">Mostly Sunny</p>
                    </div>
                  </div>

                </div>
              </div>

            </div>
          </div>

        </div>

        {/* Bottom Feature Badges matching Reference 3 */}
        <div className="mt-12 pt-6 border-t border-slate-200/80">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            
            <div 
              onClick={() => setCurrentView('disease')}
              className="bg-white/80 hover:bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-all cursor-pointer group flex items-center gap-3.5"
            >
              <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-700 group-hover:scale-110 transition-transform">
                <Sprout className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900">Disease Detection</p>
                <p className="text-[11px] text-slate-500">Spot issues early</p>
              </div>
            </div>

            <div 
              onClick={() => setCurrentView('yield')}
              className="bg-white/80 hover:bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-all cursor-pointer group flex items-center gap-3.5"
            >
              <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-700 group-hover:scale-110 transition-transform">
                <TrendingUp className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900">Yield Prediction</p>
                <p className="text-[11px] text-slate-500">Plan better, harvest more</p>
              </div>
            </div>

            <div 
              onClick={() => setCurrentView('stress')}
              className="bg-white/80 hover:bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-all cursor-pointer group flex items-center gap-3.5"
            >
              <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-700 group-hover:scale-110 transition-transform">
                <Droplet className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900">Stress Analysis</p>
                <p className="text-[11px] text-slate-500">Understand plant health</p>
              </div>
            </div>

            <div 
              onClick={() => setCurrentView('advisory')}
              className="bg-white/80 hover:bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-all cursor-pointer group flex items-center gap-3.5"
            >
              <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-700 group-hover:scale-110 transition-transform">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900">Smart Recommendations</p>
                <p className="text-[11px] text-slate-500">Take informed action</p>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
};

