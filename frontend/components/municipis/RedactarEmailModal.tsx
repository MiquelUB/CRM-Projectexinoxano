"use client";
import { useState, useEffect } from "react";
import { X, Mail, Sparkles, Loader2, Send } from "lucide-react";

export function RedactarEmailModal({ municipiId, onClose, onSent }: { municipiId: string, onClose: () => void, onSent: () => void }) {
    const [tipus, setTipus] = useState("prospeccio");
    const [variants, setVariants] = useState<any[]>([]);
    const [selectedIdx, setSelectedIdx] = useState(0);
    const [generating, setGenerating] = useState(false);
    const [sending, setSending] = useState(false);
    const [body, setBody] = useState("");
    const [subject, setSubject] = useState("");

    const generateVariants = async () => {
        setGenerating(true);
        try {
            const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
            const token = sessionStorage.getItem("token") || "";
            const res = await fetch(`${BASE_URL}/api/v2/municipis/${municipiId}/accions/redactar-email`, {
                method: "POST",
                headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
                body: JSON.stringify({ tipus_template: tipus, contacte_id: null })
            });
            if (res.ok) {
                const data = await res.json();
                setVariants(data.variants || []);
                if (data.variants && data.variants.length > 0) {
                    setSubject(data.draft.subject || "");
                    setBody(data.draft.cos || "");
                    setSelectedIdx(0);
                }
            }
        } catch (e) {
            console.error(e);
        } finally {
            setGenerating(false);
        }
    };

    const handleSelectVariant = (idx: number) => {
        setSelectedIdx(idx);
        setSubject(variants[idx].subject || "");
        setBody(variants[idx].cos || "");
    };

    const handleSend = async () => {
        setSending(true);
        try {
            // Ideally an endpoint for sending, but for Phase 3 UI test, just add a note/activity.
            const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
            const token = sessionStorage.getItem("token") || "";
            // Mock send action via adding notes
            await fetch(`${BASE_URL}/municipis_lifecycle/${municipiId}/accio`, {
                method: "POST",
                headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
                body: JSON.stringify({ accio: "registre_notes", notes: `Email enviat: ${subject}` })
            });
            onSent();
        } catch (e) {
            console.error(e);
        } finally {
            setSending(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
            <div className="bg-white w-full max-w-2xl rounded-2xl shadow-2xl flex flex-col max-h-[90vh] overflow-hidden text-slate-800 animate-in zoom-in-95 duration-200">
                <div className="p-5 border-b flex justify-between items-center bg-slate-50">
                    <div className="flex items-center space-x-2">
                        <Mail className="w-5 h-5 text-blue-600" />
                        <h2 className="text-lg font-black tracking-tight">Redactar Email (Kimi K2)</h2>
                    </div>
                    <button onClick={onClose} className="p-1 hover:bg-slate-200 rounded-full"><X className="w-5 h-5" /></button>
                </div>
                
                <div className="p-6 flex-1 overflow-y-auto space-y-4">
                    {!variants.length ? (
                        <div className="space-y-4">
                            <div>
                                <label className="text-xs font-bold uppercase tracking-wider text-slate-500">Tipus d'Email</label>
                                <select 
                                    value={tipus} 
                                    onChange={e => setTipus(e.target.value)}
                                    className="w-full mt-1 border border-slate-200 rounded-xl px-3 py-2 text-sm font-medium"
                                >
                                    <option value="prospeccio">Prospecció</option>
                                    <option value="seguiment_demo">Seguiment Demo</option>
                                    <option value="compliance">Compliance</option>
                                </select>
                            </div>
                            <button 
                                onClick={generateVariants} 
                                disabled={generating}
                                className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl flex items-center justify-center space-x-2"
                            >
                                {generating ? <Loader2 className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
                                <span>{generating ? "Generant variants..." : "Generar Alternatives"}</span>
                            </button>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            <div className="flex space-x-2 bg-slate-100 p-1.5 rounded-xl overflow-x-auto">
                                {variants.map((v, i) => (
                                    <button 
                                        key={i}
                                        onClick={() => handleSelectVariant(i)}
                                        className={`px-3 py-1.5 text-xs font-bold rounded-lg whitespace-nowrap transition-colors ${selectedIdx === i ? "bg-white text-blue-700 shadow-sm" : "text-slate-500 hover:text-slate-700"}`}
                                    >
                                        Variant {i+1}
                                    </button>
                                ))}
                            </div>
                            
                            <div>
                                <input 
                                    value={subject} 
                                    onChange={e=>setSubject(e.target.value)} 
                                    placeholder="Assumpte"
                                    className="w-full border border-slate-200 rounded-lg px-3 py-2 mb-3 text-sm font-bold" 
                                />
                                <textarea 
                                    value={body} 
                                    onChange={e=>setBody(e.target.value)} 
                                    className="w-full min-h-[250px] border border-slate-200 rounded-lg px-3 py-2 text-sm"
                                    placeholder="Cos de l'email..."
                                />
                            </div>
                        </div>
                    )}
                </div>
                
                {variants.length > 0 && (
                    <div className="p-4 border-t bg-slate-50 flex justify-end space-x-3">
                        <button onClick={onClose} className="px-4 py-2 font-bold text-sm text-slate-500 hover:text-slate-700">Cancel·lar</button>
                        <button 
                            onClick={handleSend}
                            disabled={sending}
                            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl flex items-center space-x-2"
                        >
                            {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                            <span>Enviar (Simulat)</span>
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
