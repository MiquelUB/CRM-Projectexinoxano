"use client";
import { Sparkles, Mail, Phone, Pause, Loader2 } from "lucide-react";
import { useState, useEffect } from "react";
// import Modals (We'll implement these simply or adapt EmailDraftModal)
import { RedactarEmailModal } from "./RedactarEmailModal";
import { ProgramarTrucadaModal } from "./ProgramarTrucadaModal";

export function KimiRecommendation({ municipiId, onActionComplete }: { municipiId: string, onActionComplete: () => void }) {
    const [recomanacio, setRecomanacio] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [showEmailModal, setShowEmailModal] = useState(false);
    const [showTrucadaModal, setShowTrucadaModal] = useState(false);
    const [pausant, setPausant] = useState(false);

    useEffect(() => {
        fetchRecomanacio();
    }, [municipiId]);

    const fetchRecomanacio = async () => {
        setLoading(true);
        try {
            const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
            const token = sessionStorage.getItem("token") || "";
            const res = await fetch(`${BASE_URL}/api/v2/municipis/${municipiId}/recomanacio`, {
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setRecomanacio(data);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    const handleMarcarPausa = async () => {
        if (!confirm("Vols marcar aquest municipi en pausa? L'Agent afegirà una nota automàtica.")) return;
        setPausant(true);
        try {
            const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
            const token = sessionStorage.getItem("token") || "";
            const res = await fetch(`${BASE_URL}/api/v2/municipis/${municipiId}/accions/marcar-pausa`, {
                method: "POST",
                headers: { 
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ notes: "Pausa manual des de Mission Control per l'usuari." })
            });
            if (res.ok) {
                onActionComplete();
                fetchRecomanacio(); // refresh
            } else {
                alert("Error en marcar pausa");
            }
        } catch(e) {
            console.error(e);
        } finally {
            setPausant(false);
        }
    };

    if (loading) {
        return (
            <div className="bg-slate-900 text-white p-6 rounded-2xl flex items-center justify-center min-h-[250px] shadow-xl border border-slate-800">
                <Loader2 className="w-6 h-6 animate-spin text-slate-400" />
            </div>
        );
    }

    if (!recomanacio) return null;

    return (
        <div className="bg-slate-900 text-white p-6 rounded-2xl shadow-xl border border-slate-800 flex flex-col h-full relative overflow-hidden group">
            <div className="absolute -top-16 -right-16 w-48 h-48 bg-blue-600/20 blur-[50px] rounded-full transition-all group-hover:bg-blue-500/30"></div>
            
            <div className="flex items-center space-x-2 mb-5 z-10 border-b border-white/10 pb-4">
                <div className="bg-blue-500/20 p-1.5 rounded-lg border border-blue-500/30">
                    <Sparkles className="w-4 h-4 text-blue-400" />
                </div>
                <h3 className="text-[11px] font-black tracking-widest text-blue-400 uppercase">Kimi K2 Diu</h3>
            </div>

            <div className="z-10 flex-1 flex flex-col space-y-6">
                <div className="space-y-4">
                    <div>
                        <p className="text-[11px] font-black uppercase tracking-wider text-slate-500 mb-1">Diagnòstic de situació</p>
                        <p className="text-sm font-medium text-slate-300">Últim contacte: <span className="text-white font-bold">{recomanacio.ultim_contacte}</span></p>
                        
                        {recomanacio.blockers && recomanacio.blockers.length > 0 && (
                            <div className="mt-3 space-y-1.5 p-3 bg-red-950/30 border border-red-900/50 rounded-xl">
                                {recomanacio.blockers.map((b:any, i:number) => (
                                    <p key={i} className="text-xs font-bold text-red-400 flex items-start space-x-1.5">
                                        <span>⚠️</span>
                                        <span>{b.descripcio}</span>
                                    </p>
                                ))}
                            </div>
                        )}
                        {!recomanacio.blockers?.length && (
                            <div className="mt-3 p-2 bg-emerald-950/30 border border-emerald-900/50 rounded-lg">
                                <p className="text-xs font-bold text-emerald-400">✅ Cap bloqueig detectat - Tot en ordre</p>
                            </div>
                        )}
                    </div>

                    <div className="bg-blue-950/40 border border-blue-800/50 p-4 rounded-xl shadow-inner relative overflow-hidden">
                        <div className="absolute left-0 top-0 bottom-0 w-1 bg-blue-500"></div>
                        <p className="text-[10px] font-black text-blue-400 mb-1 uppercase tracking-wider flex items-center justify-between">
                            <span>Acció Recomanada</span>
                            <span className="bg-blue-900/60 px-1.5 py-0.5 rounded text-blue-300 border border-blue-700/50">Score: {recomanacio.recomanacio?.score}/100</span>
                        </p>
                        <p className="text-base font-bold text-white mb-2">{recomanacio.recomanacio?.accio_recomanada}</p>
                        <p className="text-xs text-blue-200/70 leading-relaxed font-medium">{recomanacio.recomanacio?.rao}</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 gap-2 mt-auto pt-2">
                    <button onClick={() => setShowEmailModal(true)} className="flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white py-2.5 rounded-xl font-bold text-sm transition-all focus:ring focus:ring-blue-500/50 shadow-lg shadow-blue-900/20">
                        <Mail className="w-4 h-4" />
                        <span>Redactar Email</span>
                    </button>
                    <button onClick={() => setShowTrucadaModal(true)} className="flex items-center justify-center space-x-2 bg-slate-800 hover:bg-slate-700 text-white py-2.5 rounded-xl font-bold text-sm border border-slate-700/50 transition-all focus:ring focus:ring-slate-500/50">
                        <Phone className="w-4 h-4" />
                        <span>Programar Trucada</span>
                    </button>
                    <button onClick={handleMarcarPausa} disabled={pausant} className="flex items-center justify-center space-x-2 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white py-2.5 rounded-xl font-bold text-sm border border-slate-800 hover:border-slate-700 transition-all focus:ring focus:ring-slate-500/50 disabled:opacity-50">
                        {pausant ? <Loader2 className="w-4 h-4 animate-spin" /> : <Pause className="w-4 h-4" />}
                        <span>Marcar Pausa</span>
                    </button>
                </div>
            </div>

            {showEmailModal && <RedactarEmailModal municipiId={municipiId} onClose={() => setShowEmailModal(false)} onSent={() => { setShowEmailModal(false); onActionComplete(); fetchRecomanacio(); }} />}
            {showTrucadaModal && <ProgramarTrucadaModal municipiId={municipiId} contactes={[]} onClose={() => setShowTrucadaModal(false)} onAdded={() => { setShowTrucadaModal(false); onActionComplete(); fetchRecomanacio(); }} />}
        </div>
    );
}
