"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { format } from "date-fns";
import { Button } from "@/components/ui/button";
import { CreditCard, TrendingUp, AlertCircle, Clock, CheckCircle2 } from "lucide-react";

export default function PagamentsPage() {
  const [pagaments, setPagaments] = useState<any[]>([]);
  const [kpis, setKpis] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await api.pagaments.llistar();
      setPagaments(res.items || []);
      setKpis(res.resum);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmar = async (id: string) => {
    if (!confirm("Vols confirmar aquest pagament?")) return;
    try {
      await api.pagaments.confirmar(id, { estat: "confirmat", data_confirmacio: new Date().toISOString().split('T')[0] });
      fetchData();
    } catch (err: any) {
      alert(`Error en confirmar pagament: ${err.message}`);
    }
  };

  if (loading) return (
    <div className="p-20 flex flex-col items-center justify-center space-y-4">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px]">Carregant dades financeres...</p>
    </div>
  );

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-end">
        <div>
            <h1 className="text-4xl font-extrabold premium-gradient-text tracking-tight">Pagaments</h1>
            <p className="text-slate-500 mt-1">Control de facturació, subscripcions i estat del flux de caixa.</p>
        </div>
      </div>

      {kpis && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="glass-card p-6 border-emerald-100 shadow-emerald-100/20 shadow-lg relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-50 rounded-full -mr-8 -mt-8 transition-transform group-hover:scale-110 duration-500 opcity-50" />
            <TrendingUp className="w-5 h-5 text-emerald-600 mb-4 relative z-10" />
            <h3 className="text-slate-500 text-[10px] font-black uppercase tracking-widest relative z-10">ARR Total</h3>
            <p className="text-2xl font-black text-slate-800 relative z-10 mt-1">{Number(kpis.arr_total).toLocaleString('es-ES', {style:'currency', currency:'EUR'})}</p>
          </div>
          
          <div className="glass-card p-6 border-amber-100 shadow-amber-100/20 shadow-lg relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-amber-50 rounded-full -mr-8 -mt-8 transition-transform group-hover:scale-110 duration-500 opacity-50" />
            <Clock className="w-5 h-5 text-amber-600 mb-4 relative z-10" />
            <h3 className="text-slate-500 text-[10px] font-black uppercase tracking-widest relative z-10">Pendent</h3>
            <p className="text-2xl font-black text-slate-800 relative z-10 mt-1">{Number(kpis.pendent).toLocaleString('es-ES', {style:'currency', currency:'EUR'})}</p>
          </div>

          <div className="glass-card p-6 border-rose-100 shadow-rose-100/20 shadow-lg relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-rose-50 rounded-full -mr-8 -mt-8 transition-transform group-hover:scale-110 duration-500 opacity-50" />
            <AlertCircle className="w-5 h-5 text-rose-600 mb-4 relative z-10" />
            <h3 className="text-slate-500 text-[10px] font-black uppercase tracking-widest relative z-10">Vencut</h3>
            <p className="text-2xl font-black text-slate-800 relative z-10 mt-1">{Number(kpis.vencut).toLocaleString('es-ES', {style:'currency', currency:'EUR'})}</p>
          </div>

          <div className="glass-card p-6 border-blue-100 shadow-blue-100/20 shadow-lg relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-blue-50 rounded-full -mr-8 -mt-8 transition-transform group-hover:scale-110 duration-500 opacity-50" />
            <CheckCircle2 className="w-5 h-5 text-blue-600 mb-4 relative z-10" />
            <h3 className="text-slate-500 text-[10px] font-black uppercase tracking-widest relative z-10">Renovacions 30d</h3>
            <p className="text-2xl font-black text-slate-800 relative z-10 mt-1">{kpis.proper_30}</p>
          </div>
        </div>
      )}

      <div className="glass-card overflow-hidden border-white/60 shadow-xl shadow-slate-200/30">
        <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50 border-b border-slate-100">
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Estat</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Concepte</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Import</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Dates Clau</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] text-right">Accions</th>
              </tr>
            </thead>
          <tbody className="divide-y divide-slate-100 bg-white/40">
            {pagaments.map((pagament) => (
              <tr key={pagament.id} className="hover:bg-blue-50/30 transition-colors group">
                <td className="px-8 py-5">
                  <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest ${
                    pagament.estat === 'confirmat' ? 'bg-emerald-100 text-emerald-700' :
                    pagament.estat === 'vencut' ? 'bg-rose-100 text-rose-700' :
                    pagament.estat === 'proper' ? 'bg-blue-100 text-blue-700' :
                    'bg-amber-100 text-amber-700'
                  }`}>
                    {pagament.estat}
                  </span>
                </td>
                <td className="px-8 py-5 text-sm font-black text-slate-800 capitalize">
                  {pagament.tipus.replace('_', ' ')}
                </td>
                <td className="px-8 py-5 text-sm font-black text-slate-700">
                  {Number(pagament.import).toLocaleString('es-ES', {style:'currency', currency:'EUR'})}
                </td>
                <td className="px-8 py-5">
                   <div className="flex flex-col space-y-1">
                      <div className="flex items-center space-x-2">
                        <span className="text-[9px] font-black text-slate-300 uppercase">Emès:</span>
                        <span className="text-xs font-bold text-slate-500">{format(new Date(pagament.data_emisio), "dd/MM/yyyy")}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-[9px] font-black text-slate-300 uppercase">
                          {pagament.estat === 'confirmat' ? 'Pagat:' : 'Límit:'}
                        </span>
                        <span className={`text-xs font-bold ${pagament.estat === 'vencut' ? 'text-rose-500' : 'text-slate-500'}`}>
                          {pagament.estat === 'confirmat' && pagament.data_confirmacio 
                            ? format(new Date(pagament.data_confirmacio), "dd/MM/yyyy")
                            : pagament.data_limit 
                              ? format(new Date(pagament.data_limit), "dd/MM/yyyy") 
                              : '-'}
                        </span>
                      </div>
                   </div>
                </td>
                <td className="px-8 py-5 text-right">
                  {pagament.estat !== 'confirmat' && (
                    <Button 
                      onClick={() => handleConfirmar(pagament.id)} 
                      className="h-10 px-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold shadow-lg shadow-emerald-100 transition-all text-xs"
                    >
                      Confirmar
                    </Button>
                  )}
                  {pagament.estat === 'confirmat' && (
                      <div className="text-emerald-500 opacity-50">
                          <CheckCircle2 className="w-6 h-6 ml-auto" />
                      </div>
                  )}
                </td>
              </tr>
            ))}
            {pagaments.length === 0 && (
              <tr>
                <td colSpan={5} className="px-8 py-20 text-center text-slate-400 font-bold uppercase tracking-widest text-xs opacity-40">
                    No hi ha dades de facturació disponibles
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
