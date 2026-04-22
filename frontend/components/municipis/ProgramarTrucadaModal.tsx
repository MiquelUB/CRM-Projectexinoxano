"use client";
import { useState } from "react";
import { X, Calendar, Loader2, Check } from "lucide-react";
import api from "@/lib/api";

export function ProgramarTrucadaModal({ municipiId, onClose, onAdded, contactes }: { municipiId: string, onClose: () => void, onAdded: () => void, contactes: any[] }) {
    const [dataTrucada, setDataTrucada] = useState("");
    const [notes, setNotes] = useState("");
    const [contacteId, setContacteId] = useState(contactes && contactes.length > 0 ? contactes[0].id : "");
    const [saving, setSaving] = useState(false);

    const handleSave = async () => {
        if (!dataTrucada || !notes) return alert("Falten dades");
        setSaving(true);
        try {
            await api.municipis.programarTrucada(municipiId, {
                contacte_id: contacteId || null,
                data_programada: dataTrucada,
                notes: notes
            });
            onAdded();
        } catch (e) {
            console.error(e);
            alert("Error programant trucada");
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
            <div className="bg-white w-full max-w-md rounded-2xl shadow-xl animate-in zoom-in-95 duration-200">
                <div className="p-5 border-b flex justify-between items-center text-slate-800">
                    <div className="flex items-center space-x-2">
                        <Calendar className="w-5 h-5 text-emerald-600" />
                        <h2 className="text-lg font-black tracking-tight">Programar Trucada</h2>
                    </div>
                    <button onClick={onClose} className="p-1 hover:bg-slate-100 rounded-full"><X className="w-5 h-5" /></button>
                </div>
                
                <div className="p-5 space-y-4">
                    {contactes && contactes.length > 0 && (
                        <div>
                            <label className="text-xs font-bold text-slate-500 uppercase">Contacte</label>
                            <select 
                                value={contacteId} 
                                onChange={e => setContacteId(e.target.value)}
                                className="w-full mt-1 border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700"
                            >
                                {contactes.map(c => (
                                    <option key={c.id} value={c.id}>{c.nom} ({c.cargo || c.carrec || "---"})</option>
                                ))}
                            </select>
                        </div>
                    )}
                    
                    <div>
                        <label className="text-xs font-bold text-slate-500 uppercase">Data i Hora</label>
                        <input 
                            type="datetime-local" 
                            value={dataTrucada} 
                            onChange={e => setDataTrucada(e.target.value)}
                            className="w-full mt-1 border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700"
                        />
                    </div>

                    <div>
                        <label className="text-xs font-bold text-slate-500 uppercase">Objectiu / Notes</label>
                        <textarea 
                            value={notes} 
                            onChange={e => setNotes(e.target.value)}
                            className="w-full mt-1 border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 min-h-[100px]"
                            placeholder="Què vols tractar en aquesta trucada?"
                        />
                    </div>
                </div>

                <div className="p-5 border-t bg-slate-50 flex justify-end space-x-3 rounded-b-2xl">
                    <button onClick={onClose} className="px-4 py-2 font-bold text-sm text-slate-500 hover:text-slate-700">Cancel·lar</button>
                    <button 
                        onClick={handleSave}
                        disabled={saving}
                        className="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl flex items-center space-x-2"
                    >
                        {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4" />}
                        <span>Programar</span>
                    </button>
                </div>
            </div>
        </div>
    );
}
