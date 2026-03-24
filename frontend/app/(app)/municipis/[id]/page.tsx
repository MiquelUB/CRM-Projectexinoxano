"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { useParams } from "next/navigation";
import { DealCard } from "@/components/DealCard";
import { EmailComposer } from "@/components/EmailComposer";
import { Mail } from "lucide-react";

export default function MunicipiDetailPage() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  // Email states
  const [isComposerOpen, setIsComposerOpen] = useState(false);
  const [composerConfig, setComposerConfig] = useState({ to: "", subject: "", contacteId: "" });

  const handleEmailClick = (contacte: any) => {
    setComposerConfig({
      to: contacte.email || "",
      subject: `Seguiment Projecte Xino Xano - ${data?.nom}`,
      contacteId: contacte.id
    });
    setIsComposerOpen(true);
  };

  useEffect(() => {
    if (id) {
      fetchData();
    }
  }, [id]);

  const fetchData = async () => {
    try {
      const response = await api.municipis.detall(id as string);
      setData(response);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return (
    <div className="p-20 flex flex-col items-center justify-center space-y-4">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-400 font-bold uppercase tracking-widest text-xs">Carregant dades del municipi...</p>
    </div>
  );
  
  if (!data) return (
    <div className="p-20 text-center">
        <div className="text-6xl mb-4">📍</div>
        <h2 className="text-2xl font-black text-slate-800">Municipi no trobat</h2>
        <p className="text-slate-500 mt-2">No hem pogut trobar la fitxa que busques.</p>
    </div>
  );

  return (
    <>
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="glass-card p-10 border-white/60 shadow-xl shadow-slate-200/40 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/5 rounded-full blur-3xl -mr-32 -mt-32" />
        
        <div className="flex flex-col md:flex-row justify-between items-start relative z-10">
          <div>
            <div className="flex items-center space-x-3 mb-2">
                <span className="px-3 py-1 bg-blue-100 text-blue-700 text-[10px] font-black uppercase tracking-widest rounded-full">
                    {data.tipus}
                </span>
                <span className="text-slate-300 font-bold">•</span>
                <span className="text-sm font-bold text-slate-400 uppercase tracking-tighter">{data.provincia}</span>
            </div>
            <h1 className="text-5xl font-black premium-gradient-text tracking-tighter mb-4">{data.nom}</h1>
            <div className="flex items-center space-x-6 text-sm">
                <div className="flex flex-col">
                    <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Població</span>
                    <span className="text-slate-700 font-extrabold">{data.poblacio || 'Desconeguda'}</span>
                </div>
                <div className="w-px h-8 bg-slate-100" />
                <div className="flex flex-col">
                    <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Codi Municipi</span>
                    <span className="text-slate-700 font-extrabold">{id?.toString().slice(0, 5)}</span>
                </div>
            </div>
          </div>
          
          <div className="mt-8 md:mt-0 glass-card p-6 bg-white/40 border-white/20 shadow-none backdrop-blur-none text-right">
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.15em] mb-2 leading-none">Despesa Energètica Estimada</p>
            <p className="text-4xl font-black text-slate-800 tracking-tighter">
                {Number(data.pressupost_energia || 0).toLocaleString('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Contactes */}
        <div className="glass-card p-8 border-white/60">
          <div className="flex items-center justify-between mb-8">
            <h3 className="text-xl font-black text-slate-800 tracking-tight">Contactes Municipals</h3>
            <span className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 font-black text-xs">
                {data.contactes?.length || 0}
            </span>
          </div>
          
          {data.contactes?.length ? (
            <div className="space-y-4">
              {data.contactes.map((c: any) => (
                <div key={c.id} className="p-5 bg-white/50 border border-slate-100 rounded-2xl hover:border-blue-100 transition-all group">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-sm font-black text-slate-800 group-hover:text-blue-600 transition-colors">{c.nom}</p>
                            <p className="text-[11px] font-bold text-slate-400 uppercase mt-0.5">{c.carrec || 'Càrrec no definit'}</p>
                        </div>
                        <button 
                            onClick={() => handleEmailClick(c)}
                            disabled={!c.email}
                            className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 hover:bg-blue-50 hover:text-blue-500 transition-all disabled:opacity-30 disabled:cursor-not-allowed group-hover:bg-blue-50/50"
                            title={c.email ? "Enviar correu" : "Sense email"}
                        >
                            <Mail className="w-4 h-4" />
                        </button>
                    </div>
                    <div className="mt-4 pt-4 border-t border-slate-50 flex items-center space-x-4">
                        <span className="text-xs font-medium text-slate-500">{c.email}</span>
                        <span className="text-slate-200">|</span>
                        <span className="text-xs font-medium text-slate-500">{c.telefon || 'Sense telèfon'}</span>
                    </div>
                </div>
              ))}
            </div>
          ) : (
             <div className="py-20 text-center opacity-30">
                <div className="text-4xl mb-2">👤</div>
                <p className="text-sm font-bold italic">Cap contacte registrat encara</p>
             </div>
          )}
        </div>

        {/* Deals */}
        <div className="glass-card p-8 border-white/60">
          <div className="flex items-center justify-between mb-8">
            <h3 className="text-xl font-black text-slate-800 tracking-tight">Acords i Oportunitats</h3>
            <div className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest ${data.deals?.length ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-400'}`}>
                {data.deals?.length || 0} Actius
            </div>
          </div>
          
          {data.deals?.length ? (
            <div className="space-y-4">
              {data.deals.map((d: any) => (
                <DealCard key={d.id} deal={d} />
              ))}
            </div>
          ) : (
            <div className="py-20 text-center opacity-30">
                <div className="text-4xl mb-2">🤝</div>
                <p className="text-sm font-bold italic">No hi ha activitat comercial actualment</p>
            </div>
          )}
        </div>
      </div>
    </div>

    {isComposerOpen && (
      <EmailComposer 
        onClose={() => setIsComposerOpen(false)}
        initialTo={composerConfig.to}
        initialSubject={composerConfig.subject}
        contacteId={composerConfig.contacteId}
      />
    )}
    </>
  );
}
