"use client";
import { useState } from "react";
import { X, Check, Loader2, Save } from "lucide-react";
import api from "@/lib/api";

export function EditarMunicipiModal({ municipi, onClose, onUpdated }: { municipi: any, onClose: () => void, onUpdated: () => void }) {
    const [formData, setFormData] = useState({
        nom: municipi.nom || "",
        poblacio: municipi.poblacio || "",
        etapa_actual: municipi.etapa_actual || "research",
        temperatura: municipi.temperatura || "fred",
        geografia: municipi.geografia || "costa",
        estat_pagament: municipi.estat_pagament || ""
    });
    const [saving, setSaving] = useState(false);

    const handleSave = async () => {
        setSaving(true);
        try {
            await api.municipis_v2.editar(municipi.id, {
                nom: formData.nom,
                poblacio: parseInt(formData.poblacio) || null,
                etapa_actual: formData.etapa_actual,
                temperatura: formData.temperatura,
                geografia: formData.geografia,
                estat_pagament: formData.estat_pagament,
            });
            onUpdated();
        } catch (e: any) {
            alert(`Error actualitzant municipi: ${e.message}`);
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
            <div className="bg-white w-full max-w-lg rounded-2xl shadow-xl animate-in zoom-in-95 duration-200">
                <div className="p-5 border-b flex justify-between items-center text-slate-800">
                    <div className="flex items-center space-x-2">
                        <Save className="w-5 h-5 text-blue-600" />
                        <h2 className="text-lg font-black tracking-tight">Editar Municipi</h2>
                    </div>
                    <button onClick={onClose} className="p-1 hover:bg-slate-100 rounded-full text-slate-400 hover:text-slate-600">
                        <X className="w-5 h-5" />
                    </button>
                </div>
                
                <div className="p-5 space-y-4 max-h-[70vh] overflow-y-auto">
                    <div>
                        <label className="text-xs font-bold text-slate-500 uppercase flex items-center mb-1">Nom del Municipi</label>
                        <input 
                            type="text" 
                            value={formData.nom} 
                            onChange={e => setFormData({ ...formData, nom: e.target.value })}
                            className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700"
                        />
                    </div>
                    
                    <div>
                        <label className="text-xs font-bold text-slate-500 uppercase flex items-center mb-1">Població</label>
                        <input 
                            type="number" 
                            value={formData.poblacio} 
                            onChange={e => setFormData({ ...formData, poblacio: e.target.value })}
                            className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700"
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="text-xs font-bold text-slate-500 uppercase flex items-center mb-1">Etapa Actual</label>
                            <select 
                                value={formData.etapa_actual} 
                                onChange={e => setFormData({ ...formData, etapa_actual: e.target.value })}
                                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 font-medium"
                            >
                                <option value="research">Research</option>
                                <option value="contacte">Contacte Inicial</option>
                                <option value="demo_pendent">Demo Pendent</option>
                                <option value="demo_ok">Demo Completada</option>
                                <option value="oferta">Oferta Enviada</option>
                                <option value="documentacio">Tràmit RLT/PLIEGOS</option>
                                <option value="aprovacio">Aprovació Ajuntament</option>
                                <option value="contracte">Contracte Signat</option>
                                <option value="client">Client Actiu</option>
                                <option value="pausa">En Pausa</option>
                                <option value="perdut">Perdut</option>
                            </select>
                        </div>
                        
                        <div>
                            <label className="text-xs font-bold text-slate-500 uppercase flex items-center mb-1">Temperatura</label>
                            <select 
                                value={formData.temperatura} 
                                onChange={e => setFormData({ ...formData, temperatura: e.target.value })}
                                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 font-medium"
                            >
                                <option value="fred">❄️ Fred (Molt d'hora / Sense resposta)</option>
                                <option value="templat">🌤️ Templat (Hi ha interès)</option>
                                <option value="calent">🔥 Calent (A prop de tancar)</option>
                            </select>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="text-xs font-bold text-slate-500 uppercase flex items-center mb-1">Geografia</label>
                            <select 
                                value={formData.geografia} 
                                onChange={e => setFormData({ ...formData, geografia: e.target.value })}
                                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 font-medium"
                            >
                                <option value="costa">Costa</option>
                                <option value="interior">Interior</option>
                                <option value="muntanya">Muntanya</option>
                                <option value="metropolita">Àrea Metropolitana</option>
                            </select>
                        </div>

                        <div>
                            <label className="text-xs font-bold text-slate-500 uppercase flex items-center mb-1">Estat Pagament</label>
                            <select 
                                value={formData.estat_pagament} 
                                onChange={e => setFormData({ ...formData, estat_pagament: e.target.value })}
                                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 font-medium"
                            >
                                <option value="">Sense informació</option>
                                <option value="pendent">Pendent</option>
                                <option value="facturat">Facturat</option>
                                <option value="pagat">Pagat</option>
                                <option value="renovacio">Pendent Renovació</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div className="p-5 border-t bg-slate-50 flex justify-end space-x-3 rounded-b-2xl">
                    <button onClick={onClose} className="px-4 py-2 font-bold text-sm text-slate-500 hover:text-slate-700">Cancel·lar</button>
                    <button 
                        onClick={handleSave}
                        disabled={saving}
                        className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl flex items-center space-x-2"
                    >
                        {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4" />}
                        <span>Guardar Canvis</span>
                    </button>
                </div>
            </div>
        </div>
    );
}
