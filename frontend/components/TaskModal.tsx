"use client";

import { useState } from "react";
import { X, Calendar, Type, Clock, AlertCircle, Save, Loader2 } from "lucide-react";
import api from "@/lib/api";

interface TaskModalProps {
  onClose: () => void;
  onSaved: () => void;
  initialDate?: Date;
  task?: any;
}

export function TaskModal({ onClose, onSaved, initialDate, task }: TaskModalProps) {
  const [titol, setTitol] = useState(task?.titol || "");
  const [descripcio, setDescripcio] = useState(task?.descripcio || "");
  const [dataVenciment, setDataVenciment] = useState(
    task?.data_venciment 
      ? new Date(task.data_venciment).toISOString().split('T')[0]
      : initialDate 
        ? initialDate.toISOString().split('T')[0] 
        : new Date().toISOString().split('T')[0]
  );
  const [tipus, setTipus] = useState(task?.tipus || "trucada");
  const [prioritat, setPrioritat] = useState(task?.prioritat || "mitjana");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deals, setDeals] = useState<any[]>([]);
  const [selectedMunicipiId, setSelectedMunicipiId] = useState(task?.municipi_id || task?.deal_id || "");

  useState(() => {
    api.municipis.llistar({ limit: "200" }).then(res => setDeals(res.items || []));
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
      const priorityMap: Record<string, number> = { baixa: 1, mitjana: 2, alta: 3 };
      const data = {
        titol,
        descripcio,
        data_venciment: dataVenciment,
        tipus,
        prioritat: typeof prioritat === 'string' ? priorityMap[prioritat] : prioritat,
        municipi_id: selectedMunicipiId || null
      };

      if (task?.id && !task.is_pseudo) {
        await api.tasques.editar(task.id, data);
      } else {
        await api.tasques.crear(data);
      }
      onSaved();
      onClose();
    } catch (error) {
      console.error("Error guardant tasca", error);
      alert("No s'ha pogut guardar la tasca.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!task?.id || task.is_pseudo) return;
    if (!confirm("Segur que vols eliminar aquesta tasca?")) return;
    
    setIsDeleting(true);
    try {
      await api.tasques.eliminar(task.id);
      onSaved();
      onClose();
    } catch (error) {
      console.error("Error eliminant tasca", error);
      alert("No s'ha pogut eliminar la tasca.");
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[150] flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-md rounded-3xl shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
        <div className="p-6 border-b flex justify-between items-center bg-slate-50">
          <h2 className="text-xl font-black text-slate-800 tracking-tight">
            {task ? "Editar Tasca" : "Nova Tasca d'Agenda"}
          </h2>
          <button onClick={onClose} className="p-2 hover:bg-slate-200 rounded-full transition-colors">
            <X className="w-6 h-6 text-slate-400" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-8 space-y-6">
          <div className="space-y-4">
            <div>
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Què cal fer?</label>
              <div className="relative">
                <Type className="absolute left-4 top-3.5 w-4 h-4 text-slate-300" />
                <input 
                  autoFocus
                  required
                  value={titol}
                  onChange={e => setTitol(e.target.value)}
                  placeholder="Ex: Trucada de seguiment..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-all font-sans"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Quan?</label>
                <div className="relative">
                  <Calendar className="absolute left-4 top-3.5 w-4 h-4 text-slate-300" />
                  <input 
                    type="date"
                    required
                    value={dataVenciment}
                    onChange={e => setDataVenciment(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-12 pr-4 py-3 font-bold text-slate-700 outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-all text-sm"
                  />
                </div>
              </div>
              <div>
                <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Tipus d'acció</label>
                <select 
                  value={tipus}
                  onChange={e => setTipus(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-all text-sm appearance-none"
                >
                  <option value="trucada">Trucada</option>
                  <option value="email">Email</option>
                  <option value="demo">Demo / Presentació</option>
                  <option value="reunio">Reunió</option>
                  <option value="altre">Altre</option>
                </select>
              </div>
            </div>

            <div>
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Relacionar amb Municipi / Deal (Opcional)</label>
              <select 
                value={selectedMunicipiId}
                onChange={e => setSelectedMunicipiId(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-all text-sm"
              >
                <option value="">Cap municipi (Tasca general)</option>
                {deals.map((d: any) => (
                  <option key={d.id} value={d.id}>{d.nom}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Prioritat</label>
              <div className="flex bg-slate-100 p-1 rounded-xl space-x-1">
                {['baixa', 'mitjana', 'alta'].map(p => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setPrioritat(p)}
                    className={`flex-1 py-2 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
                      prioritat === p 
                      ? "bg-white text-slate-900 shadow-sm" 
                      : "text-slate-400 hover:text-slate-600"
                    }`}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Notes addicionals</label>
              <textarea 
                value={descripcio}
                onChange={e => setDescripcio(e.target.value)}
                placeholder="Detalls sobre la feina a fer..."
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-medium text-slate-700 outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-all min-h-[100px] text-sm"
              />
            </div>
          </div>

          <div className="pt-4 flex flex-col space-y-3">
            <div className="flex space-x-3">
              <button 
                type="button"
                onClick={onClose}
                className="flex-1 py-4 text-slate-400 font-bold text-sm hover:text-slate-600 transition-colors"
              >
                Cancel·lar
              </button>
              <button 
                type="submit"
                disabled={isSubmitting || !titol || !dataVenciment}
                className="flex-[2] h-14 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl font-black text-sm transition-all disabled:opacity-50 flex items-center justify-center space-x-3 shadow-xl shadow-slate-200"
              >
                {isSubmitting ? <Loader2 className="w-5 h-5 animate-spin" /> : <Save className="w-5 h-5" />}
                <span>{task ? "GUARDAR CANVIS" : "GUARDAR TASCA"}</span>
              </button>
            </div>
            
            {task && !task.is_pseudo && (
              <button
                type="button"
                onClick={handleDelete}
                disabled={isDeleting}
                className="w-full py-3 text-xs font-bold text-rose-400 hover:text-rose-600 transition-colors uppercase tracking-widest"
              >
                {isDeleting ? "ELIMINANT..." : "ELIMINAR TASCA"}
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
