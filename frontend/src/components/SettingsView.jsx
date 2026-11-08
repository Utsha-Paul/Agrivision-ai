import React, { useState } from 'react';
import { 
  Settings, 
  User, 
  Camera, 
  Upload, 
  Key, 
  MapPin, 
  Sprout, 
  Check, 
  Save, 
  ShieldCheck,
  Sparkles
} from 'lucide-react';
import { useApp } from '../context/AppContext';

const AVATAR_PRESETS = [
  {
    id: 'avatar-rishu',
    name: 'Rishu (Reference)',
    url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80'
  },
  {
    id: 'avatar-grower-1',
    name: 'Marcus Chen',
    url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80'
  },
  {
    id: 'avatar-agronomist-1',
    name: 'Dr. Priya Sharma',
    url: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80'
  },
  {
    id: 'avatar-tech-1',
    name: 'Alex Rivera',
    url: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80'
  },
  {
    id: 'avatar-farmer-2',
    name: 'Sunita Roy',
    url: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80'
  },
  {
    id: 'avatar-bot',
    name: 'Agri Bot',
    url: 'https://api.dicebear.com/7.x/bottts/svg?seed=AgriBot'
  }
];

export const SettingsView = () => {
  const { user, setUser, geminiApiKey, updateApiKey, farmParams, setFarmParams } = useApp();

  const [name, setName] = useState(user?.name || 'Rishu Kumar Singh');
  const [email, setEmail] = useState(user?.email || 'rishu@agrivision.ai');
  const [phone, setPhone] = useState(user?.phone || '+91 98765 43210');
  const [role, setRole] = useState(user?.role || 'Lead Agronomist');
  const [farmName, setFarmName] = useState(user?.farm_name || 'Bengal Precision Farmstead');
  const [location, setLocation] = useState(user?.location || 'Kolkata, WB');
  const [crop, setCrop] = useState(user?.crop || 'Rice');
  const [season, setSeason] = useState(user?.season || 'Kharif 2026');
  const [npk, setNpk] = useState(user?.npk || '78-32-60');
  const [avatar, setAvatar] = useState(user?.avatar || AVATAR_PRESETS[0].url);
  const [apiKeyInput, setApiKeyInput] = useState(geminiApiKey || '');
  const [savedSuccess, setSavedSuccess] = useState(false);

  // File upload for custom PFP
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setAvatar(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = (e) => {
    e.preventDefault();
    const updated = {
      ...user,
      name,
      email,
      phone,
      role,
      farm_name: farmName,
      location,
      crop,
      season,
      npk,
      avatar
    };
    setUser(updated);
    if (setFarmParams) {
      setFarmParams(prev => ({
        ...prev,
        crop_type: crop,
        season: season.split(' ')[0],
        location: location
      }));
    }
    if (apiKeyInput !== geminiApiKey) {
      updateApiKey(apiKeyInput);
    }
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2500);
  };

  return (
    <div className="p-8 space-y-6 max-w-4xl mx-auto select-none">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-200">
        <div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight">Account & Farm Profile Settings</h2>
          <p className="text-xs text-slate-500 mt-0.5">Manage your user profile, avatar/PFP, agricultural plot parameters, and neural engine preferences.</p>
        </div>
        {savedSuccess && (
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold animate-in fade-in">
            <Check className="w-3.5 h-3.5" />
            <span>Profile Saved Successfully</span>
          </span>
        )}
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        
        {/* Avatar & PFP Management Card */}
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <Camera className="w-4 h-4 text-emerald-600" />
            <h3 className="font-bold text-sm text-slate-800">Avatar & Profile Picture (PFP)</h3>
          </div>

          <div className="flex flex-col sm:flex-row items-center gap-6">
            {/* Current PFP preview with badge */}
            <div className="relative group shrink-0">
              <div className="w-24 h-24 rounded-full overflow-hidden ring-4 ring-emerald-500/30 group-hover:ring-emerald-500 transition-all shadow-md">
                <img src={avatar} alt="PFP" className="w-full h-full object-cover" />
              </div>
              <label className="absolute bottom-0 right-0 w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center shadow-lg hover:bg-emerald-700 cursor-pointer transition-transform hover:scale-110">
                <Upload className="w-3.5 h-3.5" />
                <input type="file" accept="image/*" onChange={handleFileUpload} className="hidden" />
              </label>
            </div>

            {/* Presets and details */}
            <div className="space-y-2 flex-1">
              <p className="text-xs font-semibold text-slate-700">Choose from preset agronomy avatars or upload your custom photo:</p>
              <div className="flex items-center gap-2.5 flex-wrap">
                {AVATAR_PRESETS.map((p) => (
                  <button
                    key={p.id}
                    type="button"
                    onClick={() => setAvatar(p.url)}
                    className={`w-10 h-10 rounded-full overflow-hidden transition-all ${
                      avatar === p.url ? 'ring-2 ring-emerald-500 ring-offset-2 scale-110' : 'opacity-70 hover:opacity-100'
                    }`}
                  >
                    <img src={p.url} alt={p.name} className="w-full h-full object-cover" />
                  </button>
                ))}
              </div>
              <p className="text-[11px] text-slate-400">
                Active source: <span className="font-semibold text-slate-600">{user?.auth_provider === 'google' ? 'Google Account Sync' : 'Custom Profile'}</span>
              </p>
            </div>
          </div>
        </div>

        {/* User Details */}
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <User className="w-4 h-4 text-emerald-600" />
            <h3 className="font-bold text-sm text-slate-800">Personal Information</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Phone Number</label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Role / Specialization</label>
              <input
                type="text"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 focus:outline-none focus:border-emerald-500"
              />
            </div>
          </div>
        </div>

        {/* Farm & Agronomic Parameters */}
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <Sprout className="w-4 h-4 text-emerald-600" />
            <h3 className="font-bold text-sm text-slate-800">Farm Plot & Default Agro-Parameters</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Farm Name</label>
              <input
                type="text"
                value={farmName}
                onChange={(e) => setFarmName(e.target.value)}
                className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Location</label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Primary Crop</label>
              <select
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                className="w-full text-xs font-semibold bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5"
              >
                {['Rice', 'Wheat', 'Maize', 'Tomato', 'Potato', 'Apple'].map(c => <option key={c}>{c}</option>)}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Soil Profile (N-P-K)</label>
              <input
                type="text"
                value={npk}
                onChange={(e) => setNpk(e.target.value)}
                className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5"
              />
            </div>
          </div>
        </div>

        {/* Neural Engine / Optional Key */}
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <Key className="w-4 h-4 text-purple-600" />
            <h3 className="font-bold text-sm text-slate-800">Advanced Neural Sequence Acceleration (Optional)</h3>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Neural Trend Acceleration Key
            </label>
            <input
              type="password"
              value={apiKeyInput}
              onChange={(e) => setApiKeyInput(e.target.value)}
              placeholder="AIzaSy..."
              className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-mono"
            />
            <p className="text-[11px] text-slate-400 mt-1">
              Used to power high-dimensional multi-horizon recurrent forecasting. If omitted, internal trained LSTM weights run deterministically.
            </p>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            className="px-8 py-3 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-emerald-900/20 transition-all hover:scale-105"
          >
            <Save className="w-4 h-4" />
            <span>Save Profile & Preferences</span>
          </button>
        </div>

      </form>

    </div>
  );
};

