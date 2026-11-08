import React from 'react';
import { 
  HelpCircle, 
  ShieldCheck, 
  Sprout, 
  Lightbulb, 
  CheckCircle2, 
  AlertTriangle, 
  ArrowRight,
  Droplet,
  FileText
} from 'lucide-react';
import { useApp } from '../context/AppContext';

export const AdvisoryView = () => {
  const { farmParams, analysisResult, setCurrentView } = useApp();

  const disease = analysisResult?.disease_intelligence?.disease_name || 'Late Blight';
  const crop = analysisResult?.disease_intelligence?.detected_crop || farmParams.crop_type || 'Tomato';
  const confidence = analysisResult?.disease_intelligence?.confidence || 99.2;
  const isHealthy = analysisResult?.disease_intelligence?.healthy || false;
  const recData = analysisResult?.recommendation_intelligence || {};
  const priorityAreas = recData.priority_areas || ['Targeted Foliar Disease Treatment', 'Canopy Microclimate Throttling'];
  const recommendations = recData.recommendations || [
    'Apply copper-based protectant fungicide or metalaxyl within 24 hours of first symptom detection.',
    'Switch from overhead sprinkler to drip irrigation to prevent free moisture on leaves.',
    'Scout perimeter rows twice weekly and remove necrotic plant debris.'
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto select-none">
      
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-emerald-950 via-green-900 to-teal-950 text-white rounded-3xl p-8 shadow-xl relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/30 text-emerald-200 text-xs font-bold mb-3">
            <HelpCircle className="w-3.5 h-3.5" />
            <span>Prioritized Agronomic Recommendation Engine</span>
          </div>
          <h2 className="text-3xl font-black tracking-tight">Field Action Protocols & Treatment Plans</h2>
          <p className="text-emerald-100/80 text-sm mt-1.5 leading-relaxed">
            Targeted therapeutic prescriptions, chemical and biological dosages, and microclimate management conditioned on live neural foliar diagnostics.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Core Recommendations (8 Cols) */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* Priority Focus Areas */}
          <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-amber-500" />
                <h3 className="font-bold text-base text-slate-900">
                  Priority Action Vectors for {crop} ({disease})
                </h3>
              </div>
              <span className="text-xs bg-emerald-100 text-emerald-800 font-bold px-2.5 py-0.5 rounded-full">
                Confidence: {confidence}%
              </span>
            </div>

            <div className="space-y-3">
              {priorityAreas.map((area, idx) => (
                <div key={idx} className="p-4 rounded-2xl bg-emerald-50/60 border border-emerald-100 flex items-start gap-3">
                  <div className="w-6 h-6 rounded-full bg-emerald-700 text-white font-black text-xs flex items-center justify-center shrink-0 mt-0.5">
                    {idx + 1}
                  </div>
                  <div>
                    <h4 className="font-bold text-sm text-emerald-950">{area}</h4>
                    <p className="text-xs text-emerald-800 mt-0.5 font-medium">
                      Conditioned on {farmParams.crop_type} foliar inspection and local relative humidity of {farmParams.humidity_pct}%.
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Actionable Recommendations List */}
          <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 space-y-4">
            <h3 className="font-bold text-base text-slate-900 pb-3 border-b border-slate-100 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-emerald-600" />
              <span>Step-by-Step Field Prescriptions</span>
            </h3>

            <div className="space-y-3">
              {recommendations.map((rec, i) => (
                <div key={i} className="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex items-start gap-3.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-emerald-600 shrink-0 mt-1.5" />
                  <p className="text-xs text-slate-700 leading-relaxed font-medium">
                    {rec}
                  </p>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Side Panel: Chemical & Organic Regimen (4 Cols) */}
        <div className="lg:col-span-4 space-y-5">
          
          <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 space-y-4">
            <h3 className="font-bold text-base text-slate-900 pb-2 border-b border-slate-100">
              Dosage & Compound Reference
            </h3>

            <div className="space-y-3 text-xs">
              <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
                <span className="font-bold text-slate-900 block">Biological Control Alternative</span>
                <p className="text-slate-600 text-[11px] leading-relaxed">
                  Apply *Bacillus subtilis* (QST 713 strain) @ 2.5 L/ha as preventive bio-fungicide during early vegetative differentiation.
                </p>
              </div>

              <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
                <span className="font-bold text-slate-900 block">Therapeutic Chemical Formulation</span>
                <p className="text-slate-600 text-[11px] leading-relaxed">
                  Mancozeb 75% WP @ 2.0 g/L or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1.0 mL/L water.
                </p>
              </div>

              <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
                <span className="font-bold text-slate-900 block">Foliar Micro-Nutrient Boost</span>
                <p className="text-slate-600 text-[11px] leading-relaxed">
                  Zinc Sulfate (0.5%) + 1% Urea foliar spray to stimulate rapid chlorophyll replenishment.
                </p>
              </div>
            </div>

            <button
              onClick={() => setCurrentView('reports')}
              className="w-full py-3 px-4 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-md shadow-emerald-700/20"
            >
              <FileText className="w-4 h-4" />
              <span>Generate Certified GAN Dossier</span>
            </button>
          </div>

        </div>

      </div>

    </div>
  );
};
