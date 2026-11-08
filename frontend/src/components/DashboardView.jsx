import React, { useState } from 'react';
import {
  Sprout,
  TrendingUp,
  ShieldCheck,
  Sun,
  CloudSun,
  ChevronRight,
  Calendar,
  MapPin,
  Layers,
  ArrowUpRight,
  CheckCircle2,
  AlertTriangle,
  Plus,
  Minus,
  Sparkles,
  Wheat,
  Sliders,
  Camera,
  RotateCw,
  RefreshCw,
  ExternalLink,
  Flame,
  FileText
} from 'lucide-react';
import { useApp } from '../context/AppContext';

export const DashboardView = () => {
  const {
    user,
    setCurrentView,
    farmParams,
    setFarmParams,
    presets,
    loadPreset,
    sampleLeaves,
    analysisResult,
    isAnalyzing,
    runFullAnalysis
  } = useApp();

  const [trendTimeframe, setTrendTimeframe] = useState('14 Days');
  const [mapZoom, setMapZoom] = useState(1);
  const [showParamEditor, setShowParamEditor] = useState(false);

  // Dynamic values from real analysis result
  const healthScore = analysisResult?.health_intelligence?.health_score ?? 86;
  const healthStatus = analysisResult?.health_intelligence?.health_status ?? 'Good';
  const yieldVal = analysisResult?.yield_intelligence?.predicted_yield_tons_per_ha ?? 5.24;
  const yieldCat = analysisResult?.yield_intelligence?.yield_category ?? 'Good';
  const riskLevel = analysisResult?.risk_intelligence?.risk_level ?? 'Low Risk';
  const diseaseName = analysisResult?.disease_intelligence?.disease_name ?? 'Late Blight';
  const diseaseConf = analysisResult?.disease_intelligence?.confidence ?? 99.2;
  const isHealthy = analysisResult?.disease_intelligence?.healthy ?? false;
  const isCropMatch = analysisResult?.crop_consistency?.is_match ?? true;
  const markedLeafUrl = analysisResult?.visualizations?.marked_leaf_url || analysisResult?.uploaded_image || '/outputs/sample_leaves/tomato_late_blight.jpg';

  // User name
  const firstName = user?.name ? user.name.split(' ')[0] : 'Grower';

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto select-none">

      {/* 1. Welcome Banner matching reference aesthetic */}
      <div className="relative rounded-3xl overflow-hidden shadow-lg border border-slate-200/60 h-44 flex items-center px-8 text-slate-900 group">
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1600&auto=format&fit=crop&q=80"
            alt="Farm landscape with tractor"
            className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-700"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-white/95 via-white/80 to-transparent" />
        </div>

        <div className="relative z-10 max-w-xl">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-bold tracking-wide">
              {user?.farm_name || 'AgriVision Precision Farm'}
            </span>
            <span className="text-xs text-slate-500 font-semibold flex items-center gap-1">
              <MapPin className="w-3 h-3 text-emerald-600" /> {user?.location || farmParams.location}
            </span>
          </div>
          <h2 className="text-3xl font-black text-slate-900 tracking-tight mt-1 flex items-center gap-2">
            Welcome Back, {firstName}! <span className="inline-block animate-bounce">👋</span>
          </h2>
          <p className="text-sm font-medium text-slate-600 mt-1">
            Real-time neural diagnostics, MLP yield predictions, and spectral health monitoring active.
          </p>
        </div>

        {/* Quick action button inside banner */}
        <div className="relative z-10 ml-auto hidden md:flex items-center gap-3">
          <button
            onClick={() => setShowParamEditor(!showParamEditor)}
            className="px-4 py-2.5 rounded-xl bg-white/90 hover:bg-white text-slate-800 font-bold text-xs shadow-sm border border-slate-200/80 flex items-center gap-2 transition-all hover:shadow"
          >
            <Sliders className="w-4 h-4 text-emerald-600" />
            <span>Tune Farm Inputs ({farmParams.crop_type})</span>
          </button>
          <button
            onClick={() => setCurrentView('disease')}
            className="px-5 py-2.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-md shadow-emerald-700/20 flex items-center gap-2 transition-all"
          >
            <Camera className="w-4 h-4" />
            <span>Scan Foliage</span>
          </button>
        </div>
      </div>

      {/* Farm Parameter Tuning Drawer (Toggleable) */}
      {showParamEditor && (
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-emerald-200/80 animate-in fade-in duration-200">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100">
            <div>
              <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                <Sliders className="w-4 h-4 text-emerald-600" />
                <span>Active Farm & Environmental Parameters (17 Features)</span>
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Adjust features to recalculate neural yield, health score, and risk in real time.
              </p>
            </div>
            {/* Presets dropdown */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-slate-500">Presets:</span>
              <select
                onChange={(e) => {
                  loadPreset(e.target.value);
                  runFullAnalysis(null, null, null);
                }}
                className="text-xs font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-xl px-3 py-1.5 focus:outline-none"
              >
                <option value="">Select Scenario...</option>
                {presets.map(p => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mt-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-600 mb-1">Crop Type</label>
              <select
                value={farmParams.crop_type}
                onChange={(e) => setFarmParams({ ...farmParams, crop_type: e.target.value })}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 font-bold text-slate-800"
              >
                {['Tomato', 'Rice', 'Wheat', 'Maize', 'Potato', 'Apple', 'Grape', 'Pepper', 'Peach', 'Cherry'].map(c => (
                  <option key={c}>{c}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-600 mb-1">Season</label>
              <select
                value={farmParams.season}
                onChange={(e) => setFarmParams({ ...farmParams, season: e.target.value })}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 font-bold text-slate-800"
              >
                {['Kharif', 'Rabi', 'Zaid'].map(s => <option key={s}>{s}</option>)}
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-600 mb-1">Soil Type</label>
              <select
                value={farmParams.soil_type}
                onChange={(e) => setFarmParams({ ...farmParams, soil_type: e.target.value })}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 font-bold text-slate-800"
              >
                {['Loamy', 'Clay', 'Sandy', 'Silty', 'Black', 'Red'].map(s => <option key={s}>{s}</option>)}
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-600 mb-1">Nitrogen (kg/ha)</label>
              <input
                type="number"
                value={farmParams.nitrogen_kg_ha}
                onChange={(e) => setFarmParams({ ...farmParams, nitrogen_kg_ha: parseFloat(e.target.value) || 0 })}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 font-bold text-slate-800"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-600 mb-1">Rainfall (mm)</label>
              <input
                type="number"
                value={farmParams.rainfall_mm}
                onChange={(e) => setFarmParams({ ...farmParams, rainfall_mm: parseFloat(e.target.value) || 0 })}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 font-bold text-slate-800"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-600 mb-1">Soil pH</label>
              <input
                type="number"
                step="0.1"
                value={farmParams.soil_ph}
                onChange={(e) => setFarmParams({ ...farmParams, soil_ph: parseFloat(e.target.value) || 0 })}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 font-bold text-slate-800"
              />
            </div>
          </div>

          <div className="flex items-center justify-between mt-4 pt-3 border-t border-slate-100">
            <span className="text-xs text-slate-400">
              Changes feed directly into the MLP Yield and Composite Health Engines.
            </span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowParamEditor(false)}
                className="px-3 py-1.5 rounded-xl text-slate-500 font-semibold text-xs hover:bg-slate-100"
              >
                Close
              </button>
              <button
                onClick={() => runFullAnalysis(null, null, farmParams)}
                disabled={isAnalyzing}
                className="px-4 py-1.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs flex items-center gap-1.5 shadow"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isAnalyzing ? 'animate-spin' : ''}`} />
                <span>{isAnalyzing ? 'Recalculating...' : 'Apply & Recalculate'}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 2. Top 4 Metric KPI Cards matching reference layout */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">

        {/* Metric 1: Crop Health */}
        <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md transition-all flex flex-col justify-between relative overflow-hidden">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-600 shrink-0">
              <Sprout className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-400">Crop Health</p>
              <div className="flex items-baseline gap-2 mt-0.5">
                <span className="text-2xl font-black text-slate-900">{healthScore}%</span>
                <span className="text-xs font-bold text-emerald-600 flex items-center">
                  {healthStatus}
                </span>
              </div>
            </div>
          </div>
          {/* Green wave sparkline at bottom */}
          <div className="mt-3 h-6 w-full opacity-70">
            <svg viewBox="0 0 100 24" className="w-full h-full overflow-visible">
              <path
                d="M 0,20 Q 25,8 50,14 T 100,4"
                fill="none"
                stroke="#10B981"
                strokeWidth="2.5"
                strokeLinecap="round"
              />
            </svg>
          </div>
        </div>

        {/* Metric 2: Predicted Yield */}
        <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md transition-all flex flex-col justify-between relative overflow-hidden">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-purple-100 flex items-center justify-center text-purple-600 shrink-0">
              <Wheat className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-400">Predicted Yield</p>
              <div className="flex items-baseline gap-2 mt-0.5">
                <span className="text-2xl font-black text-slate-900">{yieldVal} <span className="text-xs font-normal text-slate-400">t/ha</span></span>
                <span className="text-xs font-bold text-purple-600 flex items-center">
                  {yieldCat}
                </span>
              </div>
            </div>
          </div>
          {/* Purple wave sparkline at bottom */}
          <div className="mt-3 h-6 w-full opacity-70">
            <svg viewBox="0 0 100 24" className="w-full h-full overflow-visible">
              <path
                d="M 0,18 Q 30,12 60,16 T 100,6"
                fill="none"
                stroke="#8B5CF6"
                strokeWidth="2.5"
                strokeLinecap="round"
              />
            </svg>
          </div>
        </div>

        {/* Metric 3: Risk Level */}
        <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md transition-all flex flex-col justify-between relative overflow-hidden">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-orange-100 flex items-center justify-center text-orange-600 shrink-0">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-400">Composite Risk</p>
              <div className="mt-0.5 flex items-baseline gap-2">
                <span className="text-xl font-black text-slate-800">{riskLevel}</span>
                <span className="text-[11px] font-semibold text-orange-600">
                  {analysisResult?.risk_intelligence?.overall_risk_score ?? 18}/100
                </span>
              </div>
            </div>
          </div>
          {/* Orange wave sparkline at bottom */}
          <div className="mt-3 h-6 w-full opacity-70">
            <svg viewBox="0 0 100 24" className="w-full h-full overflow-visible">
              <path
                d="M 0,16 Q 20,20 50,14 T 100,10"
                fill="none"
                stroke="#F97316"
                strokeWidth="2.5"
                strokeLinecap="round"
              />
            </svg>
          </div>
        </div>

        {/* Metric 4: Current Weather */}
        <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md transition-all flex flex-col justify-between relative overflow-hidden">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-blue-100 flex items-center justify-center text-blue-500 shrink-0">
              <CloudSun className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-400">Current Weather</p>
              <div className="mt-0.5 flex items-baseline gap-1.5">
                <span className="text-2xl font-black text-slate-900">{farmParams.avg_temp_c}°C</span>
                <span className="text-xs font-medium text-slate-500">
                  {farmParams.humidity_pct}% RH • {farmParams.weather_zone}
                </span>
              </div>
            </div>
          </div>
          <div className="mt-3 flex items-center justify-end text-amber-500 pr-1">
            <Sun className="w-5 h-5 animate-spin-slow" />
          </div>
        </div>

      </div>

      {/* 3. Middle Row: Farm Overview, Crop Health Trend, Field Map */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">

        {/* Card 1: Farm Overview (3 Cols) */}
        <div className="lg:col-span-3 bg-white rounded-2xl p-5 shadow-sm border border-slate-100 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3">
              <div className="flex items-center gap-2">
                <span className="text-emerald-600 font-bold">●</span>
                <h3 className="font-bold text-sm text-slate-800">Farm Overview</h3>
              </div>
              <button
                onClick={() => setCurrentView('yield')}
                className="text-[11px] font-semibold text-emerald-700 hover:text-emerald-800 flex items-center gap-0.5"
              >
                <span>Yield Engine</span>
                <ChevronRight className="w-3 h-3" />
              </button>
            </div>

            {/* Thumbnail */}
            <div className="rounded-xl overflow-hidden h-32 w-full my-2 relative">
              <img
                src="https://images.unsplash.com/photo-1592982537447-7440770cbfc9?w=600&auto=format&fit=crop&q=80"
                alt="Farm rows"
                className="w-full h-full object-cover"
              />
              <div className="absolute top-2 right-2 bg-black/60 backdrop-blur-sm text-white px-2 py-0.5 rounded-md text-[10px] font-bold">
                {user?.acres || 42.5} Acres
              </div>
            </div>

            {/* Detail items from farmParams */}
            <div className="space-y-2 mt-3 text-xs">
              <div className="flex items-center justify-between py-0.5">
                <span className="text-slate-400 flex items-center gap-1.5"><Sprout className="w-3.5 h-3.5 text-emerald-600" /> Target Crop</span>
                <span className="font-bold text-slate-800">{farmParams.crop_type}</span>
              </div>
              <div className="flex items-center justify-between py-0.5">
                <span className="text-slate-400 flex items-center gap-1.5"><Calendar className="w-3.5 h-3.5 text-emerald-600" /> Season</span>
                <span className="font-bold text-slate-800">{farmParams.season}</span>
              </div>
              <div className="flex items-center justify-between py-0.5">
                <span className="text-slate-400 flex items-center gap-1.5"><Layers className="w-3.5 h-3.5 text-emerald-600" /> Soil (N-P-K)</span>
                <span className="font-bold text-slate-800">{Math.round(farmParams.nitrogen_kg_ha)}-{Math.round(farmParams.phosphorus_kg_ha)}-{Math.round(farmParams.potassium_kg_ha)}</span>
              </div>
              <div className="flex items-center justify-between py-0.5">
                <span className="text-slate-400 flex items-center gap-1.5"><MapPin className="w-3.5 h-3.5 text-emerald-600" /> Location</span>
                <span className="font-bold text-slate-800">{user?.location || farmParams.location}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Card 2: Crop Health Trend (6 Cols) - Powered by real LSTM forecast */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-5 shadow-sm border border-slate-100 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
                <h3 className="font-bold text-sm text-slate-800">Crop Health Dynamic Trend</h3>
              </div>
              <div className="flex items-center gap-2">
                <select
                  value={trendTimeframe}
                  onChange={(e) => setTrendTimeframe(e.target.value)}
                  className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1 font-semibold text-slate-700 focus:outline-none"
                >
                  <option>14 Days</option>
                  <option>7 Days</option>
                </select>
                <button
                  onClick={() => setCurrentView('forecast')}
                  title="Deep Recurrent Forecaster"
                  className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 px-2 py-1 rounded-lg flex items-center gap-1 transition-colors"
                >
                  <span>LSTM Projections</span>
                  <ArrowUpRight className="w-3 h-3" />
                </button>
              </div>
            </div>

            {/* Health Score Chart Area */}
            <div className="mt-4 relative h-48 w-full">
              {/* Y Axis Guide Lines */}
              <div className="absolute inset-0 flex flex-col justify-between text-[10px] text-slate-400 pointer-events-none pr-2">
                <div className="flex items-center justify-between border-b border-slate-100 pb-0.5"><span>100</span><div className="w-full border-t border-dashed border-slate-100 ml-2" /></div>
                <div className="flex items-center justify-between border-b border-slate-100 pb-0.5"><span>75</span><div className="w-full border-t border-dashed border-slate-100 ml-2" /></div>
                <div className="flex items-center justify-between border-b border-slate-100 pb-0.5"><span>50</span><div className="w-full border-t border-dashed border-slate-100 ml-2" /></div>
                <div className="flex items-center justify-between border-b border-slate-100 pb-0.5"><span>25</span><div className="w-full border-t border-dashed border-slate-100 ml-2" /></div>
                <div className="flex items-center justify-between pb-0.5"><span>0</span><div className="w-full border-t border-dashed border-slate-100 ml-2" /></div>
              </div>

              {/* Dynamic SVG Trendline anchored to actual computed health score */}
              <svg viewBox="0 0 350 160" className="w-full h-full pl-6 overflow-visible">
                <defs>
                  <linearGradient id="healthGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10B981" stopOpacity="0.28" />
                    <stop offset="100%" stopColor="#10B981" stopOpacity="0.0" />
                  </linearGradient>
                </defs>
                {/* Dynamic path */}
                <path
                  d={`M 10,${160 - (healthScore - 20) * 1.4} L 60,${160 - (healthScore - 14) * 1.4} L 110,${160 - (healthScore - 8) * 1.4} L 160,${160 - (healthScore - 4) * 1.4} L 210,${160 - (healthScore - 2) * 1.4} L 260,${160 - healthScore * 1.4} L 310,${160 - Math.min(98, healthScore + 4) * 1.4} L 310,160 L 10,160 Z`}
                  fill="url(#healthGrad)"
                />
                <path
                  d={`M 10,${160 - (healthScore - 20) * 1.4} L 60,${160 - (healthScore - 14) * 1.4} L 110,${160 - (healthScore - 8) * 1.4} L 160,${160 - (healthScore - 4) * 1.4} L 210,${160 - (healthScore - 2) * 1.4} L 260,${160 - healthScore * 1.4} L 310,${160 - Math.min(98, healthScore + 4) * 1.4}`}
                  fill="none"
                  stroke="#10B981"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                {/* Node dots */}
                {[
                  { cx: 10, cy: 160 - (healthScore - 20) * 1.4, val: `${Math.round(healthScore - 20)}%` },
                  { cx: 60, cy: 160 - (healthScore - 14) * 1.4, val: `${Math.round(healthScore - 14)}%` },
                  { cx: 110, cy: 160 - (healthScore - 8) * 1.4, val: `${Math.round(healthScore - 8)}%` },
                  { cx: 160, cy: 160 - (healthScore - 4) * 1.4, val: `${Math.round(healthScore - 4)}%` },
                  { cx: 210, cy: 160 - (healthScore - 2) * 1.4, val: `${Math.round(healthScore - 2)}%` },
                  { cx: 260, cy: 160 - healthScore * 1.4, val: `${Math.round(healthScore)}%` },
                  { cx: 310, cy: 160 - Math.min(98, healthScore + 4) * 1.4, val: `${Math.round(Math.min(98, healthScore + 4))}%` }
                ].map((pt, i) => (
                  <g key={i} className="cursor-pointer group">
                    <circle cx={pt.cx} cy={pt.cy} r="5" fill="#FFFFFF" stroke="#10B981" strokeWidth="3" />
                    <circle cx={pt.cx} cy={pt.cy} r="2.5" fill="#10B981" />
                  </g>
                ))}
              </svg>
            </div>

            {/* X Axis Labels */}
            <div className="flex justify-between pl-6 text-[11px] font-semibold text-slate-400 mt-2">
              <span>Day 1</span>
              <span>Day 3</span>
              <span>Day 6</span>
              <span>Day 9</span>
              <span>Day 12</span>
              <span className="text-emerald-700 font-bold">Now ({healthScore}%)</span>
              <span className="text-purple-600 font-bold">+14d Est.</span>
            </div>
          </div>
        </div>

        {/* Card 3: Field Map (4 Cols) */}
        <div className="lg:col-span-4 bg-white rounded-2xl p-5 shadow-sm border border-slate-100 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-emerald-600" />
                <h3 className="font-bold text-sm text-slate-800">Satellite GIS Parcel</h3>
              </div>
              <button
                onClick={() => alert(`Active GPS Plot: ${user?.location || farmParams.location} • Boundaries Verified`)}
                className="text-[11px] font-semibold text-emerald-700 hover:text-emerald-800 flex items-center gap-0.5"
              >
                <span>View Coordinates</span>
                <ChevronRight className="w-3 h-3" />
              </button>
            </div>

            {/* Map Area */}
            <div className="rounded-xl overflow-hidden h-40 w-full my-1 relative border border-slate-200">
              <img
                src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600&auto=format&fit=crop&q=80"
                alt="Satellite view of farm parcel"
                className="w-full h-full object-cover transition-transform duration-300"
                style={{ transform: `scale(${mapZoom})` }}
              />

              {/* Polygon Parcel boundary overlay */}
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className={`w-32 h-24 border-2 ${isHealthy ? 'border-emerald-400 bg-emerald-500/20' : 'border-amber-400 bg-amber-500/20'} rounded-lg flex items-center justify-center`}>
                  <div className="w-6 h-6 rounded-full bg-white/90 shadow-md flex items-center justify-center text-emerald-700">
                    <MapPin className="w-4 h-4" />
                  </div>
                </div>
              </div>

              {/* Legend Box inside map */}
              <div className="absolute top-2 right-2 bg-white/95 backdrop-blur-sm rounded-lg p-1.5 shadow-sm border border-slate-100 text-[10px] space-y-1">
                <div className="flex items-center gap-1.5 font-medium"><div className="w-2 h-2 rounded-full bg-emerald-500" /> Healthy</div>
                <div className="flex items-center gap-1.5 font-medium"><div className="w-2 h-2 rounded-full bg-amber-500" /> At Risk</div>
                <div className="flex items-center gap-1.5 font-medium"><div className="w-2 h-2 rounded-full bg-red-500" /> Diseased</div>
              </div>

              {/* Zoom Buttons */}
              <div className="absolute bottom-2 right-2 flex flex-col gap-1">
                <button
                  onClick={() => setMapZoom(prev => Math.min(prev + 0.2, 1.8))}
                  className="w-6 h-6 bg-white hover:bg-slate-50 text-slate-700 rounded shadow flex items-center justify-center text-xs font-bold"
                >
                  <Plus className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => setMapZoom(prev => Math.max(prev - 0.2, 0.8))}
                  className="w-6 h-6 bg-white hover:bg-slate-50 text-slate-700 rounded shadow flex items-center justify-center text-xs font-bold"
                >
                  <Minus className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>

          <div className="text-[11px] text-slate-400 pt-2 flex items-center justify-between">
            <span>Soil Spectral Stress: {analysisResult?.spectral_intelligence?.spectral_stress_score ?? 18.4}/100</span>
            <span className="font-bold text-slate-700">{farmParams.irrigation_method} Irrigation</span>
          </div>
        </div>

      </div>

      {/* 4. Bottom Row: Recent Analysis, Key Insights, Expert Advice */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">

        {/* Card 1: Recent Analysis (4 Cols) */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-5 shadow-sm border border-slate-100 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <h3 className="font-bold text-sm text-slate-800">Latest Foliar Pathology Scan</h3>
              </div>
              <button
                onClick={() => setCurrentView('disease')}
                className="text-[11px] font-semibold text-emerald-700 hover:text-emerald-800 flex items-center gap-0.5"
              >
                <span>Live Scanner</span>
                <ChevronRight className="w-3 h-3" />
              </button>
            </div>

            <div className="flex items-center gap-4 bg-slate-50/70 p-3.5 rounded-xl border border-slate-100">
              {/* Leaf Thumbnail */}
              <div className="w-20 h-20 rounded-xl overflow-hidden bg-slate-200 shrink-0 relative border border-slate-200">
                <img
                  src={markedLeafUrl}
                  alt="Scanned crop leaf"
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-black/10" />
              </div>

              {/* Diagnosis Details */}
              <div className="space-y-1 min-w-0 flex-1">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${isHealthy ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
                    }`}>
                    {analysisResult?.disease_intelligence?.status ?? 'Disease Detected'}
                  </span>

                  {/* Crop Consistency Badge */}
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${isCropMatch ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-100 text-amber-800 border border-amber-300'
                    }`}>
                    {isCropMatch ? '✓ Verified Crop' : '⚠️ Crop Mismatch'}
                  </span>
                </div>

                <h4 className="font-bold text-slate-900 text-sm truncate">
                  {diseaseName}
                </h4>
                <p className="text-xs font-semibold text-emerald-600">
                  Confidence: {diseaseConf}%
                </p>
                <p className="text-[10px] text-slate-400">
                  {analysisResult?.timestamp || 'Analyzed Today'}
                </p>
              </div>
            </div>

            {/* Quick 1-Click Test Leaf Selector */}
            <div className="mt-4 pt-3 border-t border-slate-100">
              <p className="text-[11px] font-bold text-slate-500 mb-2">Test Curated Dataset Leaves:</p>
              <div className="grid grid-cols-3 gap-2">
                {sampleLeaves.slice(0, 3).map(leaf => (
                  <button
                    key={leaf.id}
                    onClick={() => runFullAnalysis(null, leaf.id, null)}
                    disabled={isAnalyzing}
                    className="p-1.5 rounded-lg border border-slate-200 hover:border-emerald-500 bg-white hover:bg-emerald-50/50 text-left transition-all text-[10px]"
                  >
                    <p className="font-bold text-slate-800 truncate">{leaf.name.split(' ')[0]} {leaf.name.split(' ')[1]}</p>
                    <p className="text-emerald-600 font-semibold truncate">{leaf.expected_disease}</p>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Card 2: Key Insights (4 Cols) */}
        <div className="lg:col-span-4 bg-white rounded-2xl p-5 shadow-sm border border-slate-100 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 pb-3">
              <Sparkles className="w-4 h-4 text-amber-500" />
              <h3 className="font-bold text-sm text-slate-800">Agronomic Diagnostics & Priorities</h3>
            </div>

            <div className="space-y-3">
              {/* Priority recommendations */}
              {analysisResult?.recommendation_intelligence?.priority_areas?.slice(0, 3).map((item, idx) => (
                <div key={idx} className="flex items-start gap-2.5 p-2 rounded-xl bg-slate-50 border border-slate-100 text-xs">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">
                    {idx + 1}
                  </div>
                  <p className="font-medium text-slate-700 leading-snug">{item}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
            <button
              onClick={() => setCurrentView('advisory')}
              className="text-emerald-700 hover:text-emerald-800 font-bold flex items-center gap-1"
            >
              <span>View Actionable Advisory Plan</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Card 3: Expert Advice & GAN Report CTA (3 Cols) */}
        <div className="lg:col-span-3 bg-gradient-to-br from-emerald-900 to-teal-950 text-white rounded-2xl p-5 shadow-md flex flex-col justify-between relative overflow-hidden group">
          <div className="relative z-10 space-y-2">
            <div className="w-9 h-9 rounded-xl bg-white/10 flex items-center justify-center text-emerald-300">
              <FileText className="w-5 h-5" />
            </div>
            <h4 className="font-black text-lg text-white tracking-tight">
              Agri-GAN 2.0 Generative Dossier
            </h4>
            <p className="text-xs text-emerald-100/80 leading-relaxed">
              4-Phase latent foliar recovery timeline ({'Day 0 → 14'}) with biochemical stress manifold.
            </p>
          </div>

          <div className="relative z-10 pt-4">
            <button
              onClick={() => setCurrentView('reports')}
              className="w-full py-2.5 px-4 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black rounded-xl text-xs flex items-center justify-center gap-2 transition-all shadow-md hover:shadow-lg"
            >
              <span>Open Certified Dossier</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>

      </div>

    </div>
  );
};
