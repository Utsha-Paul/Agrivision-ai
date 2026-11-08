import React from 'react';
import { useApp } from './context/AppContext';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { LandingHero } from './components/LandingHero';
import { DashboardView } from './components/DashboardView';
import { DiseaseView } from './components/DiseaseView';
import { YieldView } from './components/YieldView';
import { StressView } from './components/StressView';
import { LSTMTrendView } from './components/LSTMTrendView';
import { AdvisoryView } from './components/AdvisoryView';
import { GANReportView } from './components/GANReportView';
import { SettingsView } from './components/SettingsView';
import { AuthModal } from './components/AuthModal';
import { ErrorBoundary } from './components/ErrorBoundary';

export const MainApp = () => {
  const { currentView } = useApp();

  if (currentView === 'landing') {
    return (
      <div className="min-h-screen bg-[#F3F6F4]">
        <LandingHero />
        <AuthModal />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-[#F3F6F4] text-slate-800">
      {/* Sidebar matching Reference 2 */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto max-h-screen">
        <Navbar />

        <main className="flex-1 pb-12">
          <ErrorBoundary>
            {currentView === 'dashboard' && <DashboardView />}
            {currentView === 'disease' && <DiseaseView />}
            {currentView === 'yield' && <YieldView />}
            {currentView === 'stress' && <StressView />}
            {currentView === 'forecast' && <LSTMTrendView />}
            {currentView === 'advisory' && <AdvisoryView />}
            {currentView === 'reports' && <GANReportView />}
            {currentView === 'settings' && <SettingsView />}
          </ErrorBoundary>
        </main>
      </div>

      {/* Global Auth Modal */}
      <AuthModal />
    </div>
  );
};

export default MainApp;
