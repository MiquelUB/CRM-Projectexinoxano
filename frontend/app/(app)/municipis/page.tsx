"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Search, MapPin, Settings, X, Save, Building2, Globe, Phone, Map as MapIcon, Users as UsersIcon } from "lucide-react";
import Link from "next/link";

export default function MunicipisPage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  
  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    nom: "",
    tipus: "ajuntament",
    provincia: "Barcelona",
    poblacio: "",
    web: "",
    telefon: "",
    adreca: "",
    notes: ""
  });

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchData(search);
    }, 300);

    return () => clearTimeout(timer);
  }, [search]);

  const fetchData = async (q: string) => {
    setLoading(true);
    try {
      const params: any = { limit: "50" };
      if (q) params.cerca = q; // The backend uses 'cerca' for filtering by name
      const response = await api.municipis.llistar(params);
      setItems(response.items || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const dataToSave = {
        ...formData,
        poblacio: formData.poblacio ? parseInt(formData.poblacio) : null,
        web: formData.web || null,
        telefon: formData.telefon || null,
        adreca: formData.adreca || null,
        notes: formData.notes || null,
      };
      
      await api.municipis.crear(dataToSave);
      setIsModalOpen(false);
      setFormData({
        nom: "",
        tipus: "ajuntament",
        provincia: "Barcelona",
        poblacio: "",
        web: "",
        telefon: "",
        adreca: "",
        notes: ""
      });
      fetchData(search);
    } catch (error: any) {
      console.error(error);
      alert(`Error en crear el municipi: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-end">
        <div>
            <h1 className="text-4xl font-extrabold premium-gradient-text tracking-tight">Municipis</h1>
            <p className="text-slate-500 mt-1">Gestió i consulta del cens de municipis i ajuntaments.</p>
        </div>
        <div className="flex items-center space-x-3">
            <Link href="/configuracio">
                <Button variant="outline" className="h-12 w-12 p-0 border-slate-200 rounded-2xl text-slate-400 hover:text-blue-500 hover:border-blue-100 transition-all bg-white shadow-sm">
                    <Settings className="w-5 h-5" />
                </Button>
            </Link>
            <Button 
                onClick={() => setIsModalOpen(true)}
                className="h-12 px-6 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl font-bold shadow-xl shadow-slate-200 transition-all active:scale-[0.98] flex items-center space-x-2"
            >
                <Building2 className="w-4 h-4" />
                <span>Nou Municipi</span>
            </Button>
        </div>
      </div>

      <div className="glass-card p-4 flex items-center space-x-4 border-white/60 shadow-lg shadow-slate-200/40">
        <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center">
            <Search className="text-slate-400 w-5 h-5" />
        </div>
        <input 
          type="text" 
          placeholder="Cerca per nom de municipi..." 
          className="flex-1 bg-transparent outline-none font-bold text-slate-700 placeholder:text-slate-300"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="glass-card overflow-hidden border-white/60 shadow-xl shadow-slate-200/30">
        {loading ? (
             <div className="p-20 flex flex-col items-center justify-center space-y-4">
                <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px]">Cercant a la base de dades...</p>
             </div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50 border-b border-slate-100">
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Nom</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Tipus</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Provincia</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Poblacio</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 bg-white/40">
              {items.map((m) => (
                <tr key={m.id} className="hover:bg-blue-50/30 transition-colors group cursor-pointer">
                  <td className="px-8 py-5">
                    <Link href={`/municipis/${m.id}`} className="flex items-center space-x-3">
                        <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-500 flex items-center justify-center group-hover:bg-blue-500 group-hover:text-white transition-all">
                            <MapPin className="w-4 h-4" />
                        </div>
                        <span className="font-extrabold text-slate-800 transition-colors block text-sm">
                            {m.nom}
                        </span>
                    </Link>
                  </td>
                  <td className="px-8 py-5">
                    <span className="text-[10px] font-black text-slate-500 bg-slate-100 px-2 py-1 rounded-md uppercase tracking-widest leading-none">
                        {m.tipus.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-8 py-5 text-xs font-black text-slate-400 uppercase tracking-tight">{m.provincia}</td>
                  <td className="px-8 py-5">
                    <span className="text-sm font-black text-slate-700">
                        {m.poblacio?.toLocaleString('es-ES') || '—'}
                    </span>
                  </td>
                </tr>
              ))}
              {items.length === 0 && (
                <tr>
                    <td colSpan={4} className="px-8 py-20 text-center">
                        <div className="flex flex-col items-center opacity-40">
                            <div className="text-4xl mb-4">🔍</div>
                            <p className="text-slate-400 font-bold">Cap municipi coincideix amb la cerca</p>
                        </div>
                    </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>

      {/* Modal Creació */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-card w-full max-w-2xl p-8 shadow-2xl border-white/80 animate-in zoom-in-95 duration-300">
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center text-blue-600">
                      <Building2 className="w-6 h-6" />
                  </div>
                  <h2 className="text-2xl font-black text-slate-800 tracking-tight">Nou Municipi</h2>
              </div>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600 transition-colors"><X /></button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Nom Oficial *</label>
                  <input required value={formData.nom} onChange={e => setFormData({...formData, nom: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" placeholder="Ex: Ajuntament de Barcelona" />
                </div>
                <div>
                  <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Tipus d'Entitat *</label>
                  <select required value={formData.tipus} onChange={e => setFormData({...formData, tipus: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors appearance-none">
                    <option value="ajuntament">Ajuntament</option>
                    <option value="diputacio">Diputació</option>
                    <option value="consell_comarcal">Consell Comarcal</option>
                  </select>
                </div>
                <div>
                  <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Província *</label>
                  <select required value={formData.provincia} onChange={e => setFormData({...formData, provincia: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors appearance-none">
                    <option value="Barcelona">Barcelona</option>
                    <option value="Girona">Girona</option>
                    <option value="Lleida">Lleida</option>
                    <option value="Tarragona">Tarragona</option>
                  </select>
                </div>
                <div>
                  <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Població (Habitants)</label>
                  <div className="relative">
                      <UsersIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                      <input type="number" value={formData.poblacio} onChange={e => setFormData({...formData, poblacio: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" placeholder="0" />
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Pàgina Web</label>
                    <div className="relative">
                        <Globe className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                        <input type="url" value={formData.web} onChange={e => setFormData({...formData, web: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" placeholder="https://..." />
                    </div>
                </div>
                <div>
                    <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Telèfon de Contacte</label>
                    <div className="relative">
                        <Phone className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                        <input value={formData.telefon} onChange={e => setFormData({...formData, telefon: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" placeholder="93..." />
                    </div>
                </div>
              </div>

              <div>
                <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Adreça Postal</label>
                <div className="relative">
                    <MapIcon className="absolute left-4 top-4 w-4 h-4 text-slate-400" />
                    <textarea value={formData.adreca} onChange={e => setFormData({...formData, adreca: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors h-24 resize-none" placeholder="Carrer, Número, CP..." />
                </div>
              </div>

              <div className="flex space-x-3 pt-4">
                <Button type="button" variant="outline" onClick={() => setIsModalOpen(false)} className="flex-1 h-14 rounded-2xl font-bold border-slate-200 text-slate-500">Cancel·lar</Button>
                <Button type="submit" disabled={isSubmitting} className="flex-1 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-black shadow-lg shadow-blue-100 transition-all flex items-center justify-center space-x-2">
                    {isSubmitting ? (
                        <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                            <span>Guardant...</span>
                        </>
                    ) : (
                        <>
                            <Save className="w-4 h-4" />
                            <span>Crear Municipi</span>
                        </>
                    )}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
