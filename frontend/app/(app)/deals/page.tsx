"use client";

import { useState, useEffect } from "react";
import KanbanBoard from "@/components/KanbanBoard";
import { Button } from "@/components/ui/button";
import { Settings, Plus, X, Save, Building2, User, Briefcase, Euro, Calendar, AlertCircle } from "lucide-react";
import Link from "next/link";
import api from "@/lib/api";

const PLANS = [
  { id: "roure", nom: "ROURE", setup: 3500, manteniment: 2500, desc: "5 rutas / 10 POIs / 5k MAU" },
  { id: "mirador", nom: "MIRADOR", setup: 5500, manteniment: 5000, desc: "10 rutas / 20 POIs / 10k MAU" },
  { id: "territori", nom: "TERRITORI", setup: 9500, manteniment: 14000, desc: "20 rutas / 35 POIs / 20k MAU + Multi-Bioma" },
];

export default function DealsPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [municipis, setMunicipis] = useState<any[]>([]);
  const [contactes, setContactes] = useState<any[]>([]);
  const [formData, setFormData] = useState({
    municipi_id: "",
    actor_principal_id: "",
    nom: "",
    etapa_actual: "research",
    valor_setup: "0",
    valor_llicencia: "0",
    prioritat: "mitjana",
    proper_pas: "",
    data_seguiment: ""
  });
  const [selectedPlan, setSelectedPlan] = useState("");

  useEffect(() => {
    if (isModalOpen) {
      loadSelectData();
    }
  }, [isModalOpen]);

  const loadSelectData = async () => {
    try {
      const [munRes, conRes] = await Promise.all([
        api.municipis.llistar({ limit: "200" }),
        api.contactes.llistar({ limit: "200" })
      ]);
      setMunicipis(munRes.items || []);
      setContactes(conRes.items || []);
    } catch (e) {
      console.error("Error carregant dades per al formulari", e);
    }
  };

  const handlePlanChange = (planId: string) => {
    setSelectedPlan(planId);
    const plan = PLANS.find(p => p.id === planId);
    if (plan) {
      setFormData({
        ...formData,
        valor_setup: plan.setup.toString(),
        valor_llicencia: plan.manteniment.toString()
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const dataToSave = {
        nom: formData.nom,
        etapa_actual: formData.etapa_actual,
        valor_setup: parseFloat(formData.valor_setup),
        valor_llicencia: parseFloat(formData.valor_llicencia),
        actor_principal_id: formData.actor_principal_id || null,
        data_seguiment: formData.data_seguiment || null,
        proper_pas: formData.proper_pas || null,
        prioritat: formData.prioritat
      };
      
      // Actualitzem el municipi per "activar-lo" com a deal
      await api.municipis.editar(formData.municipi_id, dataToSave);
      
      setIsModalOpen(false);
      setFormData({
        municipi_id: "",
        actor_principal_id: "",
        nom: "",
        etapa_actual: "research",
        valor_setup: "0",
        valor_llicencia: "0",
        prioritat: "mitjana",
        proper_pas: "",
        data_seguiment: ""
      });
      setSelectedPlan("");
      // No fem reload, el Kanban ja hauria de refrescar-se si l'estimulem (per simplicitat aquí fem reload o refresh de dades)
      window.location.reload(); 
    } catch (error: any) {
      console.error(error);
      alert(`Error en activar l'oportunitat: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="h-full flex flex-col space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-end">
        <div>
            <h1 className="text-4xl font-extrabold premium-gradient-text tracking-tight">Pipeline de Vendes</h1>
            <p className="text-slate-500 mt-1">Gestió visual dels acords i oportunitats en curs.</p>
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
              <Plus className="w-4 h-4" />
              <span>Nou Deal</span>
            </Button>
        </div>
      </div>
      
      <div className="flex-1 overflow-x-auto overflow-y-hidden pb-8 -mx-4 px-4 overflow-hidden">
        <KanbanBoard />
      </div>

      {/* Modal Creació Deal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-card w-full max-w-2xl p-8 shadow-2xl border-white/80 animate-in zoom-in-95 duration-300 max-h-[90vh] overflow-y-auto custom-scrollbar">
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-600">
                      <Briefcase className="w-6 h-6" />
                  </div>
                  <h2 className="text-2xl font-black text-slate-800 tracking-tight">Nou Deal (Oportunitat)</h2>
              </div>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600 transition-colors"><X /></button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Selecciona PLA (Opcional)</label>
                  <select value={selectedPlan} onChange={e => handlePlanChange(e.target.value)} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors appearance-none">
                    <option value="">Personalitzat / Altre</option>
                    {PLANS.map(p => (
                      <option key={p.id} value={p.id}>{p.nom} ({p.setup + p.manteniment}€)</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Nom del Projecte / Label *</label>
                  <input required value={formData.nom} onChange={e => setFormData({...formData, nom: e.target.value})} className="w-full bg-slate-50 border border-slate-100 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" placeholder="Ex: Passaport Digital 2026" />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Municipi / Ajuntament *</label>
                  <div className="relative">
                      <Building2 className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                      <select required value={formData.municipi_id} onChange={e => setFormData({...formData, municipi_id: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors appearance-none">
                        <option value="" disabled>Selecciona un municipi...</option>
                        {municipis.map(m => <option key={m.id} value={m.id}>{m.nom}</option>)}
                      </select>
                  </div>
                </div>
                <div>
                  <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Actor Principal</label>
                  <div className="relative">
                      <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                      <select value={formData.actor_principal_id} onChange={e => setFormData({...formData, actor_principal_id: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors appearance-none">
                        <option value="">Cap contacte assignat</option>
                        {contactes.map(c => <option key={c.id} value={c.id}>{c.nom} ({c.municipi_nom || 'S/M'})</option>)}
                      </select>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Set Up (€)</label>
                  <div className="relative">
                      <Euro className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                      <input type="number" value={formData.valor_setup} onChange={e => setFormData({...formData, valor_setup: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" placeholder="0" />
                  </div>
                </div>
                <div>
                  <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Manteniment (€)</label>
                  <div className="relative">
                      <Euro className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                      <input type="number" value={formData.valor_llicencia} onChange={e => setFormData({...formData, valor_llicencia: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" placeholder="0" />
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                    <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Prioritat</label>
                    <select value={formData.prioritat} onChange={e => setFormData({...formData, prioritat: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors appearance-none">
                        <option value="alta">Alta 🔥</option>
                        <option value="mitjana">Mitjana ⚡</option>
                        <option value="baixa">Baixa 🧊</option>
                    </select>
                </div>
                <div className="md:col-span-2">
                    <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Propera data de seguiment</label>
                    <div className="relative">
                        <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                        <input type="date" value={formData.data_seguiment} onChange={e => setFormData({...formData, data_seguiment: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" />
                    </div>
                </div>
              </div>

              <div>
                <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Proper pas / Acció immediata</label>
                <div className="relative">
                    <AlertCircle className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input value={formData.proper_pas} onChange={e => setFormData({...formData, proper_pas: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 transition-colors" placeholder="Ex: Trucar per tancar demo" />
                </div>
              </div>

              <div className="flex space-x-3 pt-4">
                <Button type="button" variant="outline" onClick={() => setIsModalOpen(false)} className="flex-1 h-14 rounded-2xl font-bold border-slate-200 text-slate-500">Cancel·lar</Button>
                <Button type="submit" disabled={isSubmitting} className="flex-1 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-black shadow-lg shadow-blue-100 transition-all flex items-center justify-center space-x-2">
                    {isSubmitting ? (
                        <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                            <span>Creant oportunitat...</span>
                        </>
                    ) : (
                        <>
                            <Save className="w-4 h-4" />
                            <span>Obrir Deal</span>
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
