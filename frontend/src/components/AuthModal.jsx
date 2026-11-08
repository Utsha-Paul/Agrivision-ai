import React, { useState } from 'react';
import { 
  X, 
  Mail, 
  Phone, 
  Lock, 
  User, 
  Check, 
  ArrowRight, 
  Sparkles,
  Camera,
  Upload,
  Smartphone,
  ShieldAlert
} from 'lucide-react';
import { useApp } from '../context/AppContext';

// Curated high quality avatars for farmers, agronomists, and researchers
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

export const AuthModal = () => {
  const { isAuthModalOpen, setIsAuthModalOpen, authMode, setAuthMode, loginUser } = useApp();

  // Selected auth tab: 'google' | 'email' | 'phone'
  const [authMethod, setAuthMethod] = useState('email');

  // Form fields
  const [name, setName] = useState('Rishu Kumar Singh');
  const [email, setEmail] = useState('rishu@agrivision.ai');
  const [password, setPassword] = useState('password123');
  const [phone, setPhone] = useState('+91 98765 43210');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [selectedAvatar, setSelectedAvatar] = useState(AVATAR_PRESETS[0].url);
  const [customAvatarUrl, setCustomAvatarUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  if (!isAuthModalOpen) return null;

  // Handle custom file upload for avatar
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedAvatar(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // Google Sign-In Handler
  const handleGoogleAuth = async (accountType = 'default') => {
    setIsLoading(true);
    setErrorMsg('');
    try {
      let gName = 'Rishu Kumar Singh';
      let gEmail = 'rishu.singh@gmail.com';
      let gPic = 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80';

      if (accountType === 'custom') {
        gName = name || 'Google Farmer';
        gEmail = email.includes('@') ? email : 'user@gmail.com';
        gPic = selectedAvatar;
      }

      const res = await fetch('/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: gEmail, name: gName, picture: gPic })
      });
      const data = await res.json();
      if (data.success) {
        loginUser(data.user);
      } else {
        setErrorMsg('Unable to authenticate with Google.');
      }
    } catch (err) {
      // Fallback local signin if server not yet started
      loginUser({
        id: 'usr-google-local',
        name: name || 'Rishu Kumar Singh',
        email: email || 'rishu@gmail.com',
        auth_provider: 'google',
        avatar: selectedAvatar,
        pfp_type: 'google',
        role: 'Farm Manager',
        farm_name: 'Bengal Precision Farmstead',
        location: 'Kolkata, WB',
        season: 'Kharif 2026',
        crop: 'Rice',
        npk: '78-32-60',
        acres: 42.5
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Email Sign In / Sign Up
  const handleEmailAuth = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMsg('');
    try {
      const endpoint = authMode === 'signup' ? 'signup' : 'login';
      const res = await fetch(`/api/auth/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          password,
          name,
          avatar: selectedAvatar
        })
      });
      const data = await res.json();
      if (data.success) {
        loginUser(data.user);
      } else {
        setErrorMsg(data.detail || 'Authentication failed');
      }
    } catch (err) {
      // Offline fallback
      loginUser({
        id: `usr-email-${Date.now()}`,
        name: name || email.split('@')[0],
        email,
        auth_provider: 'email',
        avatar: selectedAvatar,
        pfp_type: 'custom',
        role: 'Agricultural Specialist',
        farm_name: 'AgriVision Plot 4',
        location: 'Kolkata, WB',
        season: 'Kharif 2026',
        crop: 'Rice',
        npk: '78-32-60',
        acres: 30.0
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Phone OTP Flow
  const handleSendOtp = async () => {
    if (!phone) {
      setErrorMsg('Please enter a valid phone number');
      return;
    }
    setIsLoading(true);
    setErrorMsg('');
    try {
      const res = await fetch('/api/auth/otp/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone })
      });
      const data = await res.json();
      setOtpSent(true);
      setOtp('7729'); // autofill demo OTP
    } catch (err) {
      setOtpSent(true);
      setOtp('7729');
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMsg('');
    try {
      const res = await fetch('/api/auth/otp/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone, otp, name, avatar: selectedAvatar })
      });
      const data = await res.json();
      if (data.success) {
        loginUser(data.user);
      } else {
        setErrorMsg(data.detail || 'Invalid verification code');
      }
    } catch (err) {
      loginUser({
        id: `usr-phone-${Date.now()}`,
        name: name || 'Verified Grower',
        phone,
        email: `${phone.replace(/\D/g, '')}@mobile.agri`,
        auth_provider: 'phone',
        avatar: selectedAvatar,
        pfp_type: 'phone',
        role: 'Verified Grower',
        farm_name: 'Bengal Precision Farmstead',
        location: 'Kolkata, WB',
        season: 'Kharif 2026',
        crop: 'Rice',
        npk: '78-32-60',
        acres: 42.5
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 w-full max-w-lg overflow-hidden relative">
        {/* Close Button */}
        <button
          onClick={() => setIsAuthModalOpen(false)}
          className="absolute right-5 top-5 w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-slate-500 hover:text-slate-800 transition-colors z-10"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Top Decorative Banner */}
        <div className="bg-gradient-to-r from-emerald-800 via-emerald-700 to-green-800 px-8 pt-8 pb-6 text-white relative">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/15 text-emerald-200 text-xs font-semibold backdrop-blur-sm mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Secure Access Portal</span>
          </div>
          <h2 className="text-2xl font-bold tracking-tight">
            {authMode === 'signup' ? 'Create Your AgriVision Account' : 'Welcome Back to AgriVision'}
          </h2>
          <p className="text-emerald-100/80 text-xs mt-1">
            Access unified crop diagnostics, real-time LSTM trends & GAN dossiers.
          </p>

          {/* Mode Switch Tabs */}
          <div className="flex bg-black/20 p-1 rounded-xl mt-5">
            <button
              onClick={() => setAuthMode('signin')}
              className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                authMode === 'signin'
                  ? 'bg-white text-emerald-900 shadow-sm'
                  : 'text-emerald-100/80 hover:text-white'
              }`}
            >
              Sign In
            </button>
            <button
              onClick={() => setAuthMode('signup')}
              className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                authMode === 'signup'
                  ? 'bg-white text-emerald-900 shadow-sm'
                  : 'text-emerald-100/80 hover:text-white'
              }`}
            >
              Sign Up
            </button>
          </div>
        </div>

        {/* Auth Methods Selector */}
        <div className="px-8 pt-5">
          {/* Method Tabs */}
          <div className="grid grid-cols-3 gap-2 p-1 bg-slate-100 rounded-xl text-xs font-medium text-slate-600">
            <button
              type="button"
              onClick={() => setAuthMethod('google')}
              className={`py-2 rounded-lg flex items-center justify-center gap-1.5 transition-all ${
                authMethod === 'google' ? 'bg-white text-slate-900 shadow-sm font-semibold' : 'hover:text-slate-900'
              }`}
            >
              <svg className="w-3.5 h-3.5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
              </svg>
              <span>Google</span>
            </button>
            <button
              type="button"
              onClick={() => setAuthMethod('email')}
              className={`py-2 rounded-lg flex items-center justify-center gap-1.5 transition-all ${
                authMethod === 'email' ? 'bg-white text-slate-900 shadow-sm font-semibold' : 'hover:text-slate-900'
              }`}
            >
              <Mail className="w-3.5 h-3.5 text-emerald-600" />
              <span>Email</span>
            </button>
            <button
              type="button"
              onClick={() => setAuthMethod('phone')}
              className={`py-2 rounded-lg flex items-center justify-center gap-1.5 transition-all ${
                authMethod === 'phone' ? 'bg-white text-slate-900 shadow-sm font-semibold' : 'hover:text-slate-900'
              }`}
            >
              <Smartphone className="w-3.5 h-3.5 text-emerald-600" />
              <span>Phone</span>
            </button>
          </div>

          {errorMsg && (
            <div className="mt-3 p-2.5 rounded-xl bg-red-50 border border-red-200 text-xs text-red-600 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 shrink-0 text-red-500" />
              <span>{errorMsg}</span>
            </div>
          )}
        </div>

        {/* Content Body Based on Method */}
        <div className="p-8 pt-4">
          {/* 1. Google Auth Panel */}
          {authMethod === 'google' && (
            <div className="space-y-4 text-center">
              <p className="text-xs text-slate-500">
                Sign in seamlessly using your official Google Account credentials. Your Google profile photo and name will be imported automatically.
              </p>

              {/* One Click Google Button */}
              <button
                type="button"
                onClick={() => handleGoogleAuth('default')}
                disabled={isLoading}
                className="w-full py-3 px-4 rounded-xl border border-slate-300 hover:border-slate-400 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-sm flex items-center justify-center gap-3 shadow-sm hover:shadow transition-all"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
                </svg>
                <span>Continue with Google Account</span>
              </button>

              <div className="relative my-4">
                <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-200" /></div>
                <div className="relative flex justify-center text-[10px] uppercase"><span className="bg-white px-2 text-slate-400">Or use specific account</span></div>
              </div>

              {/* Sample Google accounts selector */}
              <div className="space-y-2 text-left">
                <div
                  onClick={() => handleGoogleAuth('default')}
                  className="p-2.5 rounded-xl border border-slate-200 hover:border-emerald-500 hover:bg-emerald-50/50 flex items-center justify-between cursor-pointer transition-all"
                >
                  <div className="flex items-center gap-3">
                    <img 
                      src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80" 
                      alt="Rishu" 
                      className="w-8 h-8 rounded-full object-cover ring-1 ring-emerald-500" 
                    />
                    <div>
                      <p className="text-xs font-bold text-slate-800">Rishu Kumar Singh</p>
                      <p className="text-[11px] text-slate-400">rishu.singh@gmail.com</p>
                    </div>
                  </div>
                  <span className="text-[10px] bg-emerald-100 text-emerald-800 font-semibold px-2 py-0.5 rounded">Active Reference</span>
                </div>
              </div>
            </div>
          )}

          {/* 2. Email Auth Panel */}
          {authMethod === 'email' && (
            <form onSubmit={handleEmailAuth} className="space-y-3.5">
              {authMode === 'signup' && (
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                  <div className="relative">
                    <User className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      required
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="e.g. Rishu Kumar Singh"
                      className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
                    />
                  </div>
                </div>
              )}

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@domain.com"
                    className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
                  />
                </div>
              </div>

              {/* Avatar / PFP selection for signup */}
              {authMode === 'signup' && (
                <div className="pt-2">
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5 flex items-center justify-between">
                    <span>Choose Your Avatar / PFP</span>
                    <span className="text-[10px] text-emerald-700 font-normal">Custom upload or preset</span>
                  </label>
                  <div className="flex items-center gap-2 overflow-x-auto pb-1">
                    {AVATAR_PRESETS.map((av) => (
                      <button
                        key={av.id}
                        type="button"
                        onClick={() => setSelectedAvatar(av.url)}
                        className={`w-9 h-9 rounded-full overflow-hidden shrink-0 transition-transform ${
                          selectedAvatar === av.url ? 'ring-2 ring-emerald-500 ring-offset-2 scale-110' : 'opacity-70 hover:opacity-100'
                        }`}
                      >
                        <img src={av.url} alt={av.name} className="w-full h-full object-cover" />
                      </button>
                    ))}
                    {/* File upload pill */}
                    <label className="w-9 h-9 rounded-full border border-dashed border-emerald-600 flex items-center justify-center text-emerald-600 hover:bg-emerald-50 cursor-pointer shrink-0">
                      <Upload className="w-3.5 h-3.5" />
                      <input type="file" accept="image/*" className="hidden" onChange={handleFileUpload} />
                    </label>
                  </div>
                </div>
              )}

              <button
                type="submit"
                disabled={isLoading}
                className="w-full mt-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-700 hover:to-green-700 text-white font-semibold text-xs shadow-md shadow-emerald-900/20 flex items-center justify-center gap-2 transition-all"
              >
                <span>{authMode === 'signup' ? 'Create Account' : 'Sign In'}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </form>
          )}

          {/* 3. Phone Auth Panel */}
          {authMethod === 'phone' && (
            <div className="space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Mobile Phone Number</label>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Phone className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                    <input
                      type="tel"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="+91 98765 43210"
                      className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
                    />
                  </div>
                  <button
                    type="button"
                    onClick={handleSendOtp}
                    disabled={isLoading}
                    className="px-3 py-2 bg-emerald-100 hover:bg-emerald-200 text-emerald-800 text-xs font-semibold rounded-xl transition-colors whitespace-nowrap"
                  >
                    {otpSent ? 'Resend' : 'Send OTP'}
                  </button>
                </div>
              </div>

              {otpSent && (
                <div className="animate-in fade-in duration-200 space-y-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Enter 4-Digit OTP Code <span className="text-[10px] text-emerald-600 font-normal">(Demo OTP: 7729)</span>
                    </label>
                    <input
                      type="text"
                      maxLength={6}
                      value={otp}
                      onChange={(e) => setOtp(e.target.value)}
                      placeholder="7729"
                      className="w-full px-3 py-2 text-center tracking-widest text-base font-bold rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Your Name</label>
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="Rishu Kumar Singh"
                      className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
                    />
                  </div>

                  <button
                    type="button"
                    onClick={handleVerifyOtp}
                    disabled={isLoading}
                    className="w-full py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-700 hover:to-green-700 text-white font-semibold text-xs shadow-md shadow-emerald-900/20 flex items-center justify-center gap-2 transition-all"
                  >
                    <span>Verify Code & Sign In</span>
                    <Check className="w-3.5 h-3.5" />
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

