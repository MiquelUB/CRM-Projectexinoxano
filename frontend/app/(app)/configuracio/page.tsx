"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { 
    Shield, UserPlus, Trash2, Edit3, CheckCircle2, 
    XCircle, X, Save, Settings, Layers, MapPin 
} from "lucide-react";

export default function ConfiguracioPage() {
  const [activeTab, setActiveTab] = useState("usuaris");
  const [usuaris, setUsuaris] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isClient, setIsClient] = useState(false);
  
  // State for modals/editing
  const [isEditing, setIsEditing] = useState(false);
  const [editingUser, setEditingUser] = useState<any>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [formData, setFormData] = useState({ nom: "", email: "", password: "", rol: "admin", actiu: true });

  useEffect(() => {
    setIsClient(true);
    if (activeTab === "usuaris") {
        fetchUsuaris();
    } else {
        setLoading(false);
    }
  }, [activeTab]);

  const fetchUsuaris = async () => {
    setLoading(true);
    try {
      const res = await api.usuaris.llistar();
      setUsuaris(res || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEliminar = async (id: string, nom: string) => {
    if (!confirm(`Segur que vols eliminar l'usuari ${nom}?`)) return;
    try {
      await api.usuaris.eliminar(id);
      fetchUsuaris();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const openEdit = (user: any) => {
    setEditingUser(user);
    setFormData({ nom: user.nom, email: user.email, password: "", rol: user.rol, actiu: user.actiu });
    setIsEditing(true);
  };

  const openCreate = () => {
    setFormData({ nom: "", email: "", password: "", rol: "admin", actiu: true });
    setIsCreating(true);
  };

  const handleSave = async () => {
    try {
      if (isCreating) {
        await api.usuaris.crear(formData);
      } else {
        await api.usuaris.editar(editingUser.id, formData);
      }
      setIsEditing(false);
      setIsCreating(false);
      fetchUsuaris();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const tabs = [
    { id: "usuaris", label: "Usuaris i Accessos", icon: Shield },
    { id: "municipis", label: "Camps Municipis", icon: MapPin },
    { id: "deals", label: "Camps Deals", icon: Layers },
  ];

  if (loading && !isEditing && !isCreating) return (
    <div className="p-20 flex flex-col items-center justify-center space-y-4">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px]">Carregant configuració del sistema...</p>
    </div>
  );

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-end">
        <div>
            <h1 className="text-4xl font-extrabold premium-gradient-text tracking-tight">Configuració</h1>
            <p className="text-slate-500 mt-1">Personalització del sistema i gestió d'usuaris.</p>
        </div>
        {activeTab === "usuaris" && (
            <Button 
                onClick={openCreate}
                className="h-12 px-6 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl font-bold shadow-xl shadow-slate-200 transition-all active:scale-[0.98] flex items-center space-x-2"
            >
              <UserPlus className="w-4 h-4" />
              <span>Nou Usuari</span>
            </Button>
        )}
      </div>

      <div className="flex space-x-2 bg-slate-100 p-1.5 rounded-2xl w-fit">
          {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-6 py-3 rounded-xl transition-all duration-200 ${
                  activeTab === tab.id 
                  ? "bg-white text-slate-900 shadow-sm" 
                  : "text-slate-400 hover:text-slate-600"
                }`}
              >
                <tab.icon className={`w-4 h-4 ${activeTab === tab.id ? "text-blue-500" : "text-slate-300"}`} />
                <span className="text-xs font-black uppercase tracking-widest">{tab.label}</span>
              </button>
          ))}
      </div>

      {activeTab === "usuaris" && (
          <div className="grid grid-cols-1 gap-8">
            <div className="glass-card p-8 border-white/60 shadow-xl shadow-slate-200/30">
                <div className="overflow-hidden">
                    <table className="w-full text-left border-collapse">
                        <thead>
                        <tr className="bg-slate-50/50 border-b border-slate-100">
                            <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Nom i Email</th>
                            <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Rol</th>
                            <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Estat</th>
                            <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] text-right">Accions</th>
                        </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 bg-white/40">
                        {usuaris.map((u) => (
                        <tr key={u.id} className="hover:bg-blue-50/30 transition-colors group">
                            <td className="px-6 py-5">
                                <div>
                                    <p className="text-sm font-black text-slate-800">{u.nom}</p>
                                    <p className="text-xs font-bold text-slate-400">{u.email}</p>
                                </div>
                            </td>
                            <td className="px-6 py-5">
                                <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest ${u.rol === 'admin' ? 'bg-indigo-100 text-indigo-700' : 'bg-slate-100 text-slate-500'}`}>
                                    {u.rol}
                                </span>
                            </td>
                            <td className="px-6 py-5">
                                {u.actiu ? (
                                    <div className="flex items-center space-x-2 text-emerald-600">
                                        <CheckCircle2 className="w-4 h-4" />
                                        <span className="text-[10px] font-black uppercase tracking-tighter">Actiu</span>
                                    </div>
                                ) : (
                                    <div className="flex items-center space-x-2 text-slate-400">
                                        <XCircle className="w-4 h-4" />
                                        <span className="text-[10px] font-black uppercase tracking-tighter">Inactiu</span>
                                    </div>
                                )}
                            </td>
                            <td className="px-6 py-5 text-right">
                                <div className="flex items-center justify-end space-x-2">
                                    <button 
                                      disabled={u.email === 'admin@pxx.com'}
                                      onClick={() => openEdit(u)}
                                      className="w-9 h-9 rounded-xl border border-slate-200 flex items-center justify-center text-slate-400 hover:bg-white hover:text-blue-500 hover:border-blue-200 transition-all shadow-sm disabled:opacity-30 disabled:cursor-not-allowed"
                                    >
                                        <Edit3 className="w-4 h-4" />
                                    </button>
                                    <button 
                                        disabled={u.email === 'admin@pxx.com'}
                                        onClick={() => handleEliminar(u.id, u.nom)}
                                        className="w-9 h-9 rounded-xl border border-slate-200 flex items-center justify-center text-slate-400 hover:bg-rose-50 hover:text-rose-500 hover:border-rose-200 transition-all shadow-sm disabled:opacity-30 disabled:cursor-not-allowed"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </div>
                            </td>
                        </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>
          </div>
      )}

      {activeTab === "municipis" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="glass-card p-8">
                  <h3 className="text-lg font-black text-slate-800 mb-6">Tipus de municipi</h3>
                  <div className="space-y-3">
                      {['ajuntament', 'diputacio', 'consell_comarcal'].map(t => (
                          <div key={t} className="flex justify-between items-center p-4 bg-slate-50 rounded-xl border border-slate-100">
                              <span className="font-bold text-slate-700 capitalize">{t.replace('_', ' ')}</span>
                              <Button variant="ghost" size="sm" className="text-slate-400 opacity-50 cursor-not-allowed">Protegit</Button>
                          </div>
                      ))}
                      <Button className="w-full mt-4 py-6 border-dashed border-2 hover:bg-blue-50 transition-all text-blue-500 font-bold">+ Afegir nou tipus</Button>
                  </div>
              </div>
              <div className="glass-card p-8 bg-slate-900 text-white">
                  <h3 className="text-lg font-black mb-4">Provinciès Actives</h3>
                  <p className="text-sm text-slate-400 mb-6">Defineix les províncies que apareixeran als desplegables.</p>
                  <div className="flex flex-wrap gap-2">
                        {['Barcelona', 'Girona', 'Lleida', 'Tarragona'].map(p => (
                            <div key={p} className="px-4 py-2 bg-white/10 rounded-full text-xs font-black uppercase tracking-widest">{p}</div>
                        ))}
                  </div>
              </div>
          </div>
      )}

      {activeTab === "deals" && (
          <div className="space-y-8">
              <div className="glass-card p-8">
                  <h3 className="text-lg font-black text-slate-800 mb-6">Etapes del Pipeline (Kanban)</h3>
                  <div className="space-y-3">
                      {[
                        "Prospecte", "Contacte Inicial", "Demo Feta", "Proposta", "Tramitació", "Tancat", "Perdut"
                      ].map((s, i) => (
                          <div key={s} className="flex justify-between items-center p-4 bg-white border border-slate-100 rounded-xl shadow-sm">
                              <div className="flex items-center space-x-4">
                                  <div className="w-6 h-6 rounded bg-slate-100 flex items-center justify-center text-[10px] font-black text-slate-400">{i+1}</div>
                                  <span className="font-black text-sm text-slate-700">{s}</span>
                              </div>
                              <Button variant="ghost" size="sm" className="text-slate-400 hover:text-blue-500">
                                  <Edit3 className="w-4 h-4" />
                              </Button>
                          </div>
                      ))}
                  </div>
              </div>
          </div>
      )}

      {/* Modal / Form overlay for Editing/Creating */}
      {(isEditing || isCreating) && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-300">
            <div className="glass-card w-full max-w-lg p-8 shadow-2xl border-white/80 animate-in zoom-in-95 duration-300">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-black text-slate-800 tracking-tight">
                        {isCreating ? "Crear Nou Usuari" : "Editar Usuari"}
                    </h2>
                    <button onClick={() => { setIsEditing(false); setIsCreating(false); }} className="text-slate-400 hover:text-slate-600 transition-colors">
                        <X className="w-6 h-6" />
                    </button>
                </div>

                <div className="space-y-4">
                    <div>
                        <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Nom Complet</label>
                        <input 
                            type="text" 
                            className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors"
                            value={formData.nom}
                            onChange={(e) => setFormData({...formData, nom: e.target.value})}
                        />
                    </div>
                    <div>
                        <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Email</label>
                        <input 
                            type="email" 
                            className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors"
                            value={formData.email}
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                        />
                    </div>
                    <div>
                        <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">
                            {isCreating ? "Contrasenya" : "Nova Contrasenya (opcional)"}
                        </label>
                        <input 
                            type="password" 
                            placeholder={isCreating ? "" : "Deixa en blanc per mantenir l'actual"}
                            className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors"
                            value={formData.password}
                            onChange={(e) => setFormData({...formData, password: e.target.value})}
                        />
                    </div>
                    <div className="flex space-x-4">
                        <div className="flex-1">
                            <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Rol</label>
                            <select 
                                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors"
                                value={formData.rol}
                                onChange={(e) => setFormData({...formData, rol: e.target.value})}
                            >
                                <option value="admin">Administrador</option>
                                <option value="comercial">Comercial</option>
                            </select>
                        </div>
                        <div className="flex items-end pb-3">
                            <label className="flex items-center space-x-2 cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    className="w-5 h-5 rounded-lg border-slate-200"
                                    checked={formData.actiu}
                                    onChange={(e) => setFormData({...formData, actiu: e.target.checked})}
                                />
                                <span className="text-xs font-black text-slate-600 uppercase tracking-tight">Usuari Actiu</span>
                            </label>
                        </div>
                    </div>
                </div>

                <div className="mt-8 flex space-x-3">
                    <Button 
                        onClick={() => { setIsEditing(false); setIsCreating(false); }}
                        className="flex-1 h-12 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-xl font-bold transition-all"
                    >
                        Cancel·lar
                    </Button>
                    <Button 
                        onClick={handleSave}
                        className="flex-1 h-12 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold shadow-lg shadow-blue-200 transition-all flex items-center justify-center space-x-2"
                    >
                        <Save className="w-4 h-4" />
                        <span>Guardar Canvis</span>
                    </Button>
                </div>
            </div>
        </div>
      )}
    </div>
  );
}
