import React from 'react';
import { 
  LayoutDashboard, 
  ShieldCheck, 
  BarChart3, 
  Droplet, 
  TrendingUp, 
  HelpCircle, 
  FileText, 
  Settings,
  Sprout,
  Compass,
  ArrowRight
} from 'lucide-react';
import { useApp } from '../context/AppContext';

export const Sidebar = () => {
  const { currentView, setCurrentView } = useApp();

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'disease', label: 'Disease Detection', icon: ShieldCheck },
    { id: 'yield', label: 'Yield Prediction', icon: BarChart3 },
    { id: 'stress', label: 'Stress Analysis', icon: Droplet },
    { id: 'forecast', label: 'Forecast', icon: TrendingUp },
    { id: 'advisory', label: 'Advisory', icon: HelpCircle },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 min-h-screen bg-gradient-to-b from-[#0e3721] via-[#13492c] to-[#0a2717] text-white flex flex-col justify-between relative overflow-hidden select-none border-r border-emerald-950/40 shrink-0">
      {/* Top Header / Branding */}
      <div className="p-6 relative z-10">
        <div 
          onClick={() => setCurrentView('landing')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-green-600 flex items-center justify-center shadow-lg shadow-emerald-900/50 group-hover:scale-105 transition-transform">
            <Sprout className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-xl tracking-tight text-white flex items-center gap-1.5">
              AgriVision <span className="text-emerald-400">AI</span>
            </h1>
            <p className="text-[11px] text-emerald-200/70 font-medium tracking-wide">
              Smart Agriculture <br />
              <span className="text-emerald-300/90">Brighter Tomorrow</span>
            </p>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="mt-8 space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl font-medium text-sm transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-emerald-600/90 to-emerald-500/80 text-white shadow-lg shadow-emerald-950/40 border border-emerald-400/30 translate-x-1'
                    : 'text-emerald-100/70 hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-200' : 'text-emerald-300/60'}`} />
                <span>{item.label}</span>
                {isActive && (
                  <span className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-300 shadow-[0_0_8px_#6ee7b7]" />
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Landing quick toggle pill */}
      <div className="px-6 py-2 relative z-10">
        <button
          onClick={() => setCurrentView('landing')}
          className="w-full py-2 px-3 rounded-lg bg-emerald-900/40 hover:bg-emerald-900/60 border border-emerald-700/30 text-xs text-emerald-200/80 flex items-center justify-between transition-colors"
        >
          <span className="flex items-center gap-1.5">
            <Compass className="w-3.5 h-3.5 text-emerald-400" />
            Home / Landing Page
          </span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Decorative Bottom Nature Illustration matching Reference 2 */}
      <div className="relative z-0 pointer-events-none mt-auto">
        <svg 
          viewBox="0 0 300 160" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
          className="w-full opacity-60 translate-y-1"
        >
          <path 
            d="M0 160 C 80 130, 180 150, 300 110 L 300 160 L 0 160 Z" 
            fill="#104A2B" 
          />
          <path 
            d="M0 160 C 90 100, 210 120, 300 80 L 300 160 L 0 160 Z" 
            fill="#1A613A" 
            opacity="0.7"
          />
          <path 
            d="M30 130 C 50 110, 80 110, 90 130 C 80 145, 40 145, 30 130 Z" 
            fill="#34D399" 
            opacity="0.3" 
          />
          <path 
            d="M60 140 C 75 125, 100 125, 110 140 C 95 152, 65 152, 60 140 Z" 
            fill="#10B981" 
            opacity="0.4" 
          />
        </svg>
      </div>
    </aside>
  );
};

