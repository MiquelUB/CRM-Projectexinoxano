"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api, { setToken } from "@/lib/api";
import { Button } from "@/components/ui/button";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.auth.login(email.trim(), password.trim());
      const { access_token } = response;
      
      setToken(access_token);
      
      // Also store in cookie for middleware
      document.cookie = `token=${access_token}; path=/; max-age=86400; SameSite=Strict`;

      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Credencials incorrectes");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F4F7FB] p-4 font-inter">
      {/* Background patterns */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-[#1B3A6B]/5 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[#2E6DA4]/5 rounded-full blur-[120px]" />
      </div>

      <div className="glass-card w-full max-w-5xl flex flex-col md:flex-row overflow-hidden border-white/40 z-10">
        {/* Left Side — Branding/Image */}
        <div className="w-full md:w-1/2 premium-sidebar p-12 flex flex-col justify-between relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]" />
            
            <div className="z-10">
                <div className="w-12 h-12 bg-white/20 rounded-2xl flex items-center justify-center backdrop-blur-md border border-white/20 mb-6">
                    <span className="text-2xl font-black italic">P</span>
                </div>
                <h1 className="text-4xl font-black tracking-tighter leading-tight text-white">
                    Projecte <br />
                    <span className="text-blue-300">Xino Xano</span> CRM
                </h1>
                <p className="mt-4 text-blue-100/70 max-w-xs font-medium leading-relaxed">
                    La plataforma intel·ligent per a la gestió de pipeline comercial i municipis.
                </p>
            </div>

            <div className="z-10 mt-12 md:mt-0">
                <div className="flex -space-x-3 mb-4">
                    {[1,2,3,4].map(i => (
                        <div key={i} className={`w-8 h-8 rounded-full border-2 border-[#1B3A6B] bg-slate-200`} />
                    ))}
                    <div className="w-8 h-8 rounded-full border-2 border-[#1B3A6B] bg-blue-500 flex items-center justify-center text-[10px] font-bold">+12</div>
                </div>
                <p className="text-xs text-blue-200 font-medium">Més de 50 ajuntaments ja confien en PXX.</p>
            </div>
        </div>

        {/* Right Side — Form */}
        <div className="w-full md:w-1/2 p-8 md:p-16 bg-white/40 backdrop-blur-sm flex flex-col justify-center">
            <div className="max-w-sm mx-auto w-full">
                <h2 className="text-3xl font-black text-slate-800 tracking-tight mb-2">Benvingut</h2>
                <p className="text-slate-500 text-sm font-medium mb-8">Introdueix les teves dades per accedir al tauler.</p>
                
                <form onSubmit={handleLogin} className="space-y-6">
                    <div className="space-y-1.5">
                        <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-1">Email corporatiu</label>
                        <input
                            type="email"
                            required
                            className="w-full px-5 py-4 bg-white/50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all text-slate-800 font-medium placeholder:text-slate-300 shadow-sm"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="nom@projectexinoxano.cat"
                        />
                    </div>
                    
                    <div className="space-y-1.5">
                        <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-1">Contrasenya</label>
                        <input
                            type="password"
                            required
                            className="w-full px-5 py-4 bg-white/50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all text-slate-800 font-medium placeholder:text-slate-300 shadow-sm"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                        />
                    </div>
                    
                    {error && (
                        <div className="text-rose-500 text-xs font-bold bg-rose-50/50 backdrop-blur-md border border-rose-100 p-4 rounded-2xl animate-in shake duration-300">
                            {error}
                        </div>
                    )}
                    
                    <div className="pt-2">
                        <Button 
                            type="submit" 
                            className="w-full h-14 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-white rounded-2xl font-bold shadow-xl shadow-slate-200 transition-all active:scale-[0.98] disabled:opacity-50"
                            disabled={loading}
                        >
                            {loading ? (
                                <div className="flex items-center space-x-2">
                                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                    <span>Accedint...</span>
                                </div>
                            ) : "Entrar al CRM"}
                        </Button>
                    </div>
                </form>

                <div className="mt-8 text-center">
                    <p className="text-xs text-slate-400 font-medium italic">Accés restringit a personal autoritzat.</p>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
}
