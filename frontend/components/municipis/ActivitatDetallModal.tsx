"use client";
import { X, Search } from "lucide-react";

export function ActivitatDetallModal({ activitat, onClose }: { activitat: any, onClose: () => void }) {
    if (!activitat) return null;

    let contingutObj = {};
    try {
        contingutObj = typeof activitat.contingut === "string" ? JSON.parse(activitat.contingut) : activitat.contingut;
    } catch(e) {}

    return (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
            <div className="bg-white w-full max-w-lg rounded-2xl shadow-2xl flex flex-col max-h-[85vh] animate-in zoom-in-95 duration-200">
                <div className="p-4 border-b flex justify-between items-center bg-slate-50 rounded-t-2xl">
                    <div className="flex items-center space-x-2 text-slate-800">
                        <Search className="w-5 h-5" />
                        <h2 className="text-base font-black tracking-tight uppercase">Detall d'Activitat</h2>
                    </div>
                    <button onClick={onClose} className="p-1 hover:bg-slate-200 rounded-full"><X className="w-5 h-5 text-slate-500" /></button>
                </div>
                
                <div className="p-5 flex-1 overflow-y-auto space-y-4">
                    <div>
                        <span className="text-[10px] font-black uppercase text-slate-400">Model Meta</span>
                        <div className="grid grid-cols-2 gap-2 mt-1">
                            <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                                <p className="text-[10px] text-slate-500 uppercase">Tipus</p>
                                <p className="text-xs font-bold text-slate-800">{activitat.tipus_activitat}</p>
                            </div>
                            <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                                <p className="text-[10px] text-slate-500 uppercase">Data</p>
                                <p className="text-xs font-bold text-slate-800">{new Date(activitat.data_activitat).toLocaleString()}</p>
                            </div>
                            <div className="bg-slate-50 p-2 rounded-lg border border-slate-100 col-span-2">
                                <p className="text-[10px] text-slate-500 uppercase">Actor</p>
                                <p className="text-xs font-bold text-slate-800">{activitat.actor || "Desconegut"}</p>
                            </div>
                        </div>
                    </div>

                    {activitat.notes_comercial && (
                        <div>
                            <span className="text-[10px] font-black uppercase text-slate-400">Notes Comercial</span>
                            <div className="mt-1 bg-yellow-50/50 border border-yellow-100 p-3 rounded-lg text-sm text-slate-700 whitespace-pre-wrap">
                                {activitat.notes_comercial}
                            </div>
                        </div>
                    )}

                    {contingutObj && Object.keys(contingutObj).length > 0 && (
                        <div>
                            <span className="text-[10px] font-black uppercase text-slate-400">Payload / Contingut (JSONB)</span>
                            <pre className="mt-1 bg-slate-900 text-slate-300 p-3 rounded-lg text-[11px] overflow-x-auto">
                                {JSON.stringify(contingutObj, null, 2)}
                            </pre>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
