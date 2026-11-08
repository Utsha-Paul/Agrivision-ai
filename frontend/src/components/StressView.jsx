import React, { useState } from 'react';
import { 
  Droplet, 
  Activity, 
  Layers, 
  Sparkles, 
  CheckCircle2, 
  Eye, 
  FileText,
  Thermometer,
  ShieldAlert,
  ArrowRight
} from 'lucide-react';
import { useApp } from '../context/AppContext';

export const StressView = () => {
  const { analysisResult, setCurrentView } = useApp();

  const [activeVisualMode, setActiveVisualMode] = useState('marked'); // 'marked' | 'heatmap' | 'overlay'

  const vis = analysisResult?.visualizations || {};
  const spec = analysisResult?.spectral_intelligence || {};
  const hyperleaf = analysisResult?.hyperleaf_spectral;

  const markedUrl = vis.marked_leaf_url || analysisResult?.uploaded_image || '/outputs/sample_leaves/tomato_late_blight.jpg';
  const heatmapUrl = vis.heatmap_url || '';
  const overlayUrl = vis.overlay_url || '';

  const activeImageDisplay = activeVisualMode === 'heatmap' && heatmapUrl 
    ? heatmapUrl 
    : (activeVisualMode === 'overlay' && overlayUrl ? overlayUrl : markedUrl);

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto select-none">
      
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-teal-950 via-emerald-900 to-green-950 text-white rounded-3xl p-8 shadow-xl relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/20 border border-teal-400/30 text-teal-200 text-xs font-bold mb-3">
            <Droplet className="w-3.5 h-3.5" />
            <span>Spectral Stress & Chromatic Pathology Engine</span>
          </div>
          <h2 className="text-3xl font-black tracking-tight">Foliar Stress & Optical Index Mapping</h2>
          <p className="text-teal-100/80 text-sm mt-1.5 leading-relaxed">
            Multi-spectral decomposition calculating Excess Green Index ($ExG = 2g - r - b$), Normalized Difference Greenness ($NDI$), chlorotic discoloration, and thermal stress contours.
          </p>
        </div>
      </div>

      {/* Grid Content */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Visualizer Heatmap, Overlay & Marked Leaf (7 Cols) */}
        <div className="lg:col-span-7 bg-white rounded-3xl p-6 shadow-sm border border-slate-100 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-100 gap-2">
            <div>
              <h3 className="font-bold text-base text-slate-900">Pathological Stress Visualizations</h3>
              <p className="text-xs text-slate-400">Contours, thermal heatmaps, and lesion boundary segmentations.</p>
            </div>
            
            {/* Mode Switcher Tabs */}
            <div className="flex bg-slate-100 p-1 rounded-xl text-xs font-bold text-slate-700">
              <button
                onClick={() => setActiveVisualMode('marked')}
                className={`px-3 py-1.5 rounded-lg transition-all ${activeVisualMode === 'marked' ? 'bg-white text-emerald-800 shadow-sm' : 'hover:text-slate-900'}`}
              >
                Marked Leaf
              </button>
              <button
                onClick={() => setActiveVisualMode('heatmap')}
                className={`px-3 py-1.5 rounded-lg transition-all ${activeVisualMode === 'heatmap' ? 'bg-white text-emerald-800 shadow-sm' : 'hover:text-slate-900'}`}
              >
                Thermal Heatmap
              </button>
              <button
                onClick={() => setActiveVisualMode('overlay')}
                className={`px-3 py-1.5 rounded-lg transition-all ${activeVisualMode === 'overlay' ? 'bg-white text-emerald-800 shadow-sm' : 'hover:text-slate-900'}`}
              >
                Blended Overlay
              </button>
            </div>
          </div>

          {/* Main Visual Display */}
          <div className="rounded-2xl overflow-hidden bg-slate-950 aspect-video max-h-[420px] mx-auto border border-slate-200 relative shadow-inner flex items-center justify-center">
            <img
              src={activeImageDisplay}
              alt="Optical Stress Analysis"
              className="w-full h-full object-contain"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = markedUrl;
              }}
            />

            {/* Top Badge */}
            <div className="absolute top-3 left-3 bg-black/70 backdrop-blur-md px-3 py-1 rounded-full text-white text-xs font-bold border border-white/20">
              {activeVisualMode === 'marked' && 'Contoured Pathogen Regions'}
              {activeVisualMode === 'heatmap' && 'Thermal Jet Stress Heatmap'}
              {activeVisualMode === 'overlay' && 'Micro-Lesion Segmentation'}
            </div>

            {/* Bottom Stats Overlay */}
            <div className="absolute bottom-3 inset-x-3 bg-black/70 backdrop-blur-md px-4 py-2 rounded-xl text-white text-xs flex justify-between items-center border border-white/20">
              <div className="flex items-center gap-3">
                <span>Affected Area: <strong className="text-amber-400">{vis.affected_area_percentage || 14.2}%</strong></span>
                <span>•</span>
                <span>Stressed Regions: <strong className="text-emerald-400">{vis.num_stressed_regions || 3}</strong></span>
              </div>
              <span className="font-bold text-emerald-400">Stress: {vis.average_stress || spec.spectral_stress_score || 18.4}/100</span>
            </div>
          </div>

          {/* Thumbnail Gallery */}
          <div className="grid grid-cols-3 gap-3 pt-2">
            <div 
              onClick={() => setActiveVisualMode('marked')}
              className={`p-1.5 rounded-xl border cursor-pointer transition-all ${activeVisualMode === 'marked' ? 'border-emerald-600 bg-emerald-50/40' : 'border-slate-200 hover:border-slate-300'}`}
            >
              <div className="h-16 rounded-lg overflow-hidden bg-slate-900">
                <img src={markedUrl} alt="Marked" className="w-full h-full object-cover" />
              </div>
              <p className="text-[10px] font-bold text-center text-slate-700 mt-1">1. Marked Leaf</p>
            </div>

            <div 
              onClick={() => setActiveVisualMode('heatmap')}
              className={`p-1.5 rounded-xl border cursor-pointer transition-all ${activeVisualMode === 'heatmap' ? 'border-emerald-600 bg-emerald-50/40' : 'border-slate-200 hover:border-slate-300'}`}
            >
              <div className="h-16 rounded-lg overflow-hidden bg-slate-900">
                <img src={heatmapUrl || markedUrl} alt="Heatmap" className="w-full h-full object-cover" />
              </div>
              <p className="text-[10px] font-bold text-center text-slate-700 mt-1">2. Heatmap</p>
            </div>

            <div 
              onClick={() => setActiveVisualMode('overlay')}
              className={`p-1.5 rounded-xl border cursor-pointer transition-all ${activeVisualMode === 'overlay' ? 'border-emerald-600 bg-emerald-50/40' : 'border-slate-200 hover:border-slate-300'}`}
            >
              <div className="h-16 rounded-lg overflow-hidden bg-slate-900">
                <img src={overlayUrl || markedUrl} alt="Overlay" className="w-full h-full object-cover" />
              </div>
              <p className="text-[10px] font-bold text-center text-slate-700 mt-1">3. Overlay</p>
            </div>
          </div>
        </div>

        {/* Spectral Index Metrics (5 Cols) */}
        <div className="lg:col-span-5 bg-white rounded-3xl p-6 shadow-sm border border-slate-100 space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-600" />
              <h3 className="font-bold text-base text-slate-900">Optical Index Signatures</h3>
            </div>
            <span className="text-xs bg-emerald-100 text-emerald-800 font-black px-2.5 py-0.5 rounded-full">
              {spec.stress_level || 'Normal'} Condition
            </span>
          </div>

          <div className="space-y-3 text-xs">
            {/* Excess Green Index */}
            <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 flex items-center justify-between">
              <div>
                <p className="font-bold text-slate-900">ExG (Excess Green Index)</p>
                <p className="text-[10px] text-slate-400">Formula: 2g - r - b</p>
              </div>
              <span className="text-lg font-black text-emerald-700">
                {spec.excess_green_index_exg ?? 42.5}
              </span>
            </div>

            {/* Normalized Difference Greenness */}
            <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 flex items-center justify-between">
              <div>
                <p className="font-bold text-slate-900">NDI (Normalized Vegetation)</p>
                <p className="text-[10px] text-slate-400">Formula: (g - r) / (g + r)</p>
              </div>
              <span className="text-lg font-black text-emerald-700">
                {spec.vegetation_index_ndi ?? 0.385}
              </span>
            </div>

            {/* Discoloration & Tissue Damage */}
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] font-bold text-slate-400 uppercase">Discoloration</span>
                <p className="text-base font-black text-slate-900 mt-0.5">{spec.discoloration_level || 'Low'}</p>
              </div>
              <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] font-bold text-slate-400 uppercase">Tissue Damage</span>
                <p className="text-base font-black text-slate-900 mt-0.5">{spec.tissue_damage_level || 'Mild'}</p>
              </div>
            </div>

            {/* Green Ratio & Saturation */}
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] font-bold text-slate-400 uppercase">Green Ratio</span>
                <p className="text-base font-black text-emerald-700 mt-0.5">{spec.green_ratio ?? 0.612}</p>
              </div>
              <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] font-bold text-slate-400 uppercase">Canopy Saturation</span>
                <p className="text-base font-black text-slate-900 mt-0.5">{spec.saturation ?? 145.2}</p>
              </div>
            </div>
          </div>

          {/* HyperLeaf Model (when TIFF is available) */}
          {hyperleaf ? (
            <div className="p-4 rounded-2xl bg-indigo-50 border border-indigo-100 space-y-2 text-xs">
              <div className="flex items-center gap-1.5 font-bold text-indigo-900">
                <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
                <span>HyperLeaf Trained Spectral Model</span>
              </div>
              <div className="grid grid-cols-3 gap-2 pt-1 font-mono text-[11px]">
                <div><span className="text-slate-400 block">Grain Weight</span><strong>{hyperleaf.grain_weight}</strong></div>
                <div><span className="text-slate-400 block">Gsw</span><strong>{hyperleaf.gsw}</strong></div>
                <div><span className="text-slate-400 block">PhiPS2</span><strong>{hyperleaf.phi_ps2}</strong></div>
              </div>
            </div>
          ) : (
            <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 text-[11px] text-slate-500">
              <span className="font-bold text-slate-700 block mb-0.5">Hyperspectral TIFF Support:</span>
              Upload multi-band <code>.tif</code> leaf imagery to activate trained HyperLeaf stomatal conductance (g_sw) and photosynthetic quantum yield (Phi_PS2) calculations.
            </div>
          )}

          {/* Jump to GAN Report */}
          <button
            onClick={() => setCurrentView('reports')}
            className="w-full py-3 px-4 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-md shadow-emerald-700/20"
          >
            <FileText className="w-4 h-4" />
            <span>Generate Agri-GAN Recovery Dossier</span>
          </button>

        </div>

      </div>

    </div>
  );
};
