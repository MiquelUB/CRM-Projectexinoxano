"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Search, X, UserPlus, Trash2, Mail, Phone, Briefcase, Building2, Edit3, Save } from "lucide-react";
import { EmailComposer } from "@/components/EmailComposer";

export default function ContactesPage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Email states
  const [isComposerOpen, setIsComposerOpen] = useState(false);
  const [composerConfig, setComposerConfig] = useState({ to: "", subject: "", contacteId: "" });

  const handleEmailClick = (contacte: any) => {
    setComposerConfig({
      to: contacte.email || "",
      subject: `Seguiment Projecte Xino Xano`,
      contacteId: contacte.id
    });
    setIsComposerOpen(true);
  };
  const [search, setSearch] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [municipis, setMunicipis] = useState<any[]>([]);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Form state
  const [formData, setFormData] = useState({
    nom: "",
    carrec: "",
    email: "",
    telefon: "",
    municipi_id: ""
  });

  useEffect(() => {
    // Load municipalities for the dropdown (V2)
    api.municipis_v2.llistar({ limit: "200" }).then(res => setMunicipis(res.items || []));
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchData(search);
    }, 300);
    return () => clearTimeout(timer);
  }, [search]);

  const fetchData = async (q: string) => {
    setLoading(true);
    try {
      const params: any = { limit: "100" };
      if (q) params.cerca = q;
      const response = await api.contactes_v2.llistar(params);
      setItems(response.items || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenCreate = () => {
    setEditingId(null);
    setFormData({ nom: "", carrec: "", email: "", telefon: "", municipi_id: "" });
    setIsModalOpen(true);
  };

  const handleOpenEdit = (contacte: any) => {
    setEditingId(contacte.id);
    setFormData({
      nom: contacte.nom,
      carrec: contacte.carrec || "",
      email: contacte.email || "",
      telefon: contacte.telefon || "",
      municipi_id: contacte.municipi_id
    });
    setIsModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.municipi_id) {
        alert("Cal seleccionar un municipi associat.");
        return;
    }
    
    setIsSubmitting(true);
    try {
      // Clean up empty strings to null for the API (except nom and municipi_id which are mandatory)
      const cleanedData = {
          ...formData,
          carrec: formData.carrec || null,
          email: formData.email || null,
          telefon: formData.telefon || null,
      };
      
      if (editingId) {
        await api.contactes_v2.editar(editingId, cleanedData);
      } else {
        await api.contactes_v2.crear(cleanedData);
      }
      
      setIsModalOpen(false);
      setFormData({ nom: "", carrec: "", email: "", telefon: "", municipi_id: "" });
      setEditingId(null);
      fetchData(search);
    } catch (error: any) {
      console.error(error);
      alert(`Error en guardar el contacte: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (id: string, nom: string) => {
    if (!confirm(`Segur que vols eliminar el contacte ${nom}?`)) return;
    try {
      await api.contactes_v2.eliminar(id);
      fetchData(search);
    } catch (e: any) {
      console.error(e);
      alert(`Error a l'esborrar: ${e.message}`);
    }
  };

  return (
    <>
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-end">
        <div>
            <h1 className="text-4xl font-extrabold premium-gradient-text tracking-tight">Contactes</h1>
            <p className="text-slate-500 mt-1">Gestió de persones i representants dels ajuntaments.</p>
        </div>
        <Button 
            onClick={handleOpenCreate}
            className="h-12 px-6 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl font-bold shadow-xl shadow-slate-200 transition-all active:scale-[0.98] flex items-center space-x-2"
        >
          <UserPlus className="w-4 h-4" />
          <span>Nou Contacte</span>
        </Button>
      </div>

      <div className="glass-card p-4 flex items-center space-x-4 border-white/60 shadow-lg shadow-slate-200/40">
        <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center">
            <Search className="text-slate-400 w-5 h-5" />
        </div>
        <input 
          type="text" 
          placeholder="Cerca per nom o email de contacte..." 
          className="flex-1 bg-transparent outline-none font-bold text-slate-700 placeholder:text-slate-300"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="glass-card overflow-hidden border-white/60 shadow-xl shadow-slate-200/30">
        {loading ? (
             <div className="p-20 flex flex-col items-center justify-center space-y-4">
                <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px]">Cercant contactes...</p>
             </div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50 border-b border-slate-100">
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Nom</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Càrrec i Municipi</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Mitjans de Contacte</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] text-right">Accions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {items.map((c) => (
                <tr key={c.id} className="hover:bg-blue-50/30 transition-colors group">
                  <td className="px-8 py-5">
                    <p className="font-extrabold text-slate-800">{c.nom}</p>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">ID: {c.id.substring(0,8)}</p>
                  </td>
                  <td className="px-8 py-5">
                    <div className="flex flex-col space-y-1">
                        <div className="flex items-center space-x-2 text-slate-600">
                            <Briefcase className="w-3.5 h-3.5 text-slate-400" />
                            <span className="text-sm font-bold">{c.carrec || 'Sense càrrec'}</span>
                        </div>
                        <div className="flex items-center space-x-2 text-slate-400">
                            <Building2 className="w-3.5 h-3.5" />
                            <span className="text-xs font-medium">
                                {c.municipi?.nom || (c.municipi_id ? `ID: ${c.municipi_id.substring(0,8)}...` : 'Municipi no vinculat')}
                            </span>
                        </div>
                    </div>
                  </td>
                  <td className="px-8 py-5">
                    <div className="flex flex-col space-y-1">
                        {c.email && (
                            <div className="flex items-center space-x-2 text-blue-600">
                                <Mail className="w-3.5 h-3.5" />
                                <span className="text-xs font-black">{c.email}</span>
                            </div>
                        )}
                        {c.telefon && (
                            <div className="flex items-center space-x-2 text-slate-500">
                                <Phone className="w-3.5 h-3.5" />
                                <span className="text-xs font-bold">{c.telefon}</span>
                            </div>
                        )}
                        {!c.email && !c.telefon && <span className="text-xs italic text-slate-300">Sense contacte</span>}
                    </div>
                  </td>
                  <td className="px-8 py-5 text-right">
                    <div className="flex items-center justify-end space-x-2">
                        {c.email && (
                            <button 
                                onClick={() => handleEmailClick(c)} 
                                className="w-10 h-10 rounded-xl flex items-center justify-center text-blue-500 hover:bg-blue-50 transition-all font-bold"
                                title="Enviar correu ara"
                            >
                                <Mail className="w-5 h-5" />
                            </button>
                        )}
                        <button 
                            onClick={() => handleOpenEdit(c)} 
                            className="w-10 h-10 rounded-xl flex items-center justify-center text-slate-300 hover:bg-blue-50 hover:text-blue-500 transition-all"
                            title="Editar contacte"
                        >
                            <Edit3 className="w-5 h-5" />
                        </button>
                        <button 
                            onClick={() => handleDelete(c.id, c.nom)} 
                            className="w-10 h-10 rounded-xl flex items-center justify-center text-slate-300 hover:bg-rose-50 hover:text-rose-500 transition-all"
                            title="Eliminar contacte"
                        >
                            <Trash2 className="w-5 h-5" />
                        </button>
                    </div>
                  </td>
                </tr>
              ))}
              {items.length === 0 && (
                <tr>
                    <td colSpan={4} className="px-8 py-20 text-center text-slate-400 italic">
                        No s'han trobat contactes
                    </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>

      {/* Modal Creació / Edició */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-card w-full max-w-md p-8 shadow-2xl border-white/80 animate-in zoom-in-95 duration-300">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-black text-slate-800 tracking-tight">
                {editingId ? "Editar Contacte" : "Nou Contacte"}
              </h2>
              <button 
                onClick={() => { setIsModalOpen(false); setEditingId(null); }} 
                className="text-slate-400 hover:text-slate-600 transition-colors"
              >
                <X />
              </button>
            </div>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Nom Complet *</label>
                <input required value={formData.nom} onChange={e => setFormData({...formData, nom: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" />
              </div>
              <div>
                <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Municipi Associat *</label>
                <select required value={formData.municipi_id} onChange={e => setFormData({...formData, municipi_id: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors appearance-none">
                  <option value="">Selecciona municipi</option>
                  {municipis.map(m => <option key={m.id} value={m.id}>{m.nom}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Càrrec</label>
                <input value={formData.carrec} onChange={e => setFormData({...formData, carrec: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                    <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Email</label>
                    <input type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-1.5 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" />
                </div>
                <div>
                    <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Telèfon</label>
                    <input value={formData.telefon} onChange={e => setFormData({...formData, telefon: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-1.5 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" />
                </div>
              </div>
              <div className="flex space-x-3 pt-6">
                <Button type="button" variant="outline" onClick={() => { setIsModalOpen(false); setEditingId(null); }} className="flex-1 h-12 rounded-xl font-bold">Cancel·lar</Button>
                <Button type="submit" disabled={isSubmitting} className="flex-1 h-12 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold shadow-lg shadow-blue-200 transition-all flex items-center justify-center space-x-2">
                    {isSubmitting ? (
                        <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                            <span>Guardant...</span>
                        </>
                    ) : (
                        <>
                            <Save className="w-4 h-4" />
                            <span>{editingId ? 'Guardar Canvis' : 'Crear Contacte'}</span>
                        </>
                    )}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
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
