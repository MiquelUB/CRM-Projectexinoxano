"use client";

import { useEffect, useState } from "react";
import { X, Mail, Sparkles, Loader2, Send, Check, Phone } from "lucide-react";

interface EmailDraftModalProps {
  onClose: () => void;
  onSent?: () => void;
  municipiId: string;
  tipus?: string; 
  initialTo?: string;
  contacteId?: string;
  accioRecomanada?: string;
  rao?: string;
}

export function EmailDraftModal({ 
    onClose, 
    onSent, 
    municipiId,
    tipus = "email_1_prospeccio",
    initialTo = "", 
    contacteId,
    accioRecomanada,
    rao
}: EmailDraftModalProps) {
  const [to, setTo] = useState(initialTo);
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [variants, setVariants] = useState<any[]>([]);
  const [selectedVariantIdx, setSelectedVariantIdx] = useState(0);
  const [draftId, setDraftId] = useState<string | null>(null);
  
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isLogSaving, setIsLogSaving] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const [anglePersonalitzacio, setAnglePersonalitzacio] = useState("");
  const [notesActuacio, setNotesActuacio] = useState("");
  const [municipiData, setMunicipiData] = useState<any>(null);

  const [chatMessages, setChatMessages] = useState<{ role: string; content: string }[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);

  const handleSendChat = async () => {
       if (!chatInput.trim()) return;
       const userMsg = { role: "user", content: chatInput };
       const updatedMessages = [...chatMessages, userMsg];
       setChatMessages(updatedMessages);
       setChatInput("");
       setChatLoading(true);
       try {
            const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
            const token = sessionStorage.getItem("token");
            const res = await fetch(`${BASE_URL}/agent/chat_municipi`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    ...(token && { Authorization: `Bearer ${token}` })
                },
                body: JSON.stringify({ municipi_id: municipiId, messages: updatedMessages })
            });
            const data = await res.json();
            setChatMessages(prev => [...prev, data]);
       } catch (error) {
            console.error(error);
       } finally {
            setChatLoading(false);
       }
  };

  const fetchMunicipiData = async () => {
    setLoading(true);
    try {
      const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const token = sessionStorage.getItem("token");
      const res = await fetch(`${BASE_URL}/municipis_lifecycle/${municipiId}`, {
        headers: { ...(token && { Authorization: `Bearer ${token}` }) }
      });
      if (!res.ok) throw new Error("Error detall");
      const data = await res.json();
      setMunicipiData(data);
      setAnglePersonalitzacio(data.angle_personalitzacio || "");

      // Mapejar correctament el destinatari
      const contacte = data.contactes?.find((c: any) => c.id === contacteId) 
                     || data.contactes?.find((c: any) => c.principal);
      if (contacte?.email && !to) {
          setTo(contacte.email);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const fetchDraftVariants = async () => {
    setIsGenerating(true);
    try {
      const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const token = sessionStorage.getItem("token");
      const res = await fetch(`${BASE_URL}/emails_v2/drafts/nou/${municipiId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...(token && { Authorization: `Bearer ${token}` })
        },
        body: JSON.stringify({ tipus, contacte_id: contacteId || null })
      });
      if (!res.ok) throw new Error("Error generant variants");
      
      const data = await res.json();
      setDraftId(data.draft_id);
      setVariants(data.variants || []);
      
      if (data.variants && data.variants.length > 0) {
          setSubject(data.subject_inicial || "");
          setBody(data.cos_inicial || "");
          
          const idx = data.variants.findIndex((v: any) => v.subject === data.subject_inicial);
          if (idx !== -1) setSelectedVariantIdx(idx);
      }
    } catch (error) {
      console.error("Error carregant variants", error);
      alert("No s'han pogut generar variants.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleUpdateContext = async () => {
    setIsSaving(true);
    try {
      const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const token = sessionStorage.getItem("token");
      await fetch(`${BASE_URL}/municipis_lifecycle/${municipiId}/notes`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...(token && { Authorization: `Bearer ${token}` }) },
        body: JSON.stringify({ angle_personalitzacio: anglePersonalitzacio })
      });
      alert("Anotacions del Deal desades!");
      if (onSent) onSent(); // Actualitzar fons dashboard
    } catch (e) {
      console.error(e);
    } finally {
      setIsSaving(false);
    }
  };

  const handleSaveActuacio = async () => {
    if (!notesActuacio.trim()) return;
    setIsLogSaving(true);
    try {
      const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const token = sessionStorage.getItem("token");
      await fetch(`${BASE_URL}/municipis_lifecycle/${municipiId}/accio`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...(token && { Authorization: `Bearer ${token}` }) },
        body: JSON.stringify({ accio: "registre_notes", notes: notesActuacio })
      });
      alert("Actuació registrada correctament!");
      setNotesActuacio("");
      if (onSent) onSent(); // Actualitzar fons dashboard
    } catch (e) {
         console.error(e);
    } finally {
         setIsLogSaving(false);
    }
  };

  const handleSelectVariant = async (idx: number) => {
    setSelectedVariantIdx(idx);
    const v = variants[idx];
    setSubject(v.subject || "");
    setBody(v.cos || "");
    // ... opcionalment guardar variant seleccionada ...
  };

  const handleSend = async () => {
    setSending(true);
    try {
      const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const token = sessionStorage.getItem("token");

      if (draftId) {
          // 1. Desar canvis si hi ha draft actualment activa
          await fetch(`${BASE_URL}/emails_v2/drafts/${draftId}/editar`, {
              method: "POST",
              headers: { "Content-Type": "application/json", ...(token && { Authorization: `Bearer ${token}` }) },
              body: JSON.stringify({ subject, cos: body })
          });

          // 2. Enviar draft
          const res = await fetch(`${BASE_URL}/emails_v2/drafts/${draftId}/enviar`, {
            method: "POST",
            headers: { "Content-Type": "application/json", ...(token && { Authorization: `Bearer ${token}` }) },
            body: JSON.stringify({ mode: "immediat" })
          });
          if (!res.ok) throw new Error("Error enviant draft");
      } else {
          // 3. Enviar manualment si no hem usat la IA (Variants buides)
          const res = await fetch(`${BASE_URL}/emails_v2/enviar_manual/${municipiId}`, {
              method: "POST",
              headers: { "Content-Type": "application/json", ...(token && { Authorization: `Bearer ${token}` }) },
              body: JSON.stringify({ subject, cos: body })
          });
          if (!res.ok) throw new Error("Error enviant correu manual");
      }
      
      if (onSent) onSent();
      onClose();
    } catch (error) {
       console.error("Error enviant email", error);
       alert("No s'ha pogut enviar el correu.");
    } finally {
       setSending(false);
    }
  };

  useEffect(() => {
    fetchMunicipiData();
  }, [municipiId]);

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4 overflow-hidden">
      <div className="bg-white w-full max-w-3xl rounded-3xl shadow-2xl flex flex-col max-h-[90vh] animate-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="p-6 border-b flex justify-between items-center bg-slate-50 rounded-t-3xl">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-slate-800 rounded-xl flex items-center justify-center text-white">
              <Mail className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-black text-slate-800 tracking-tight">
                <span>{municipiData?.nom || "Carregant..."}</span> 
              </h2>
              <div className="flex items-center space-x-2 text-[10px] font-bold text-slate-500">
                  <span className="uppercase tracking-widest text-slate-400">Control d'Acció</span>
                  {(() => {
                      // Trobar el contacte actiu/principal
                      const contacte = municipiData?.contactes?.find((c: any) => c.id === contacteId) 
                                     || municipiData?.contactes?.find((c: any) => c.principal);
                      if (!contacte) return null;
                      return (
                          <span className="bg-slate-200/80 px-2 py-0.5 rounded-full text-slate-700 flex items-center space-x-1">
                              <span>{contacte.nom} ({contacte.carrec})</span>
                              {contacte.email && <span> | ✉️ {contacte.email}</span>}
                              {contacte.telefon && <span> | 📞 {contacte.telefon}</span>}
                          </span>
                      );
                  })()}
              </div>
            </div>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-slate-200 rounded-full transition-colors">
            <X className="w-6 h-6 text-slate-400" />
          </button>
        </div>

        {loading ? (
             <div className="flex-1 flex items-center justify-center p-8"><Loader2 className="w-8 h-8 animate-spin text-slate-400" /></div>
        ) : (
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
             
             {/* Bloc 0: Raonament de la IA */}
             {rao && (
                 <div className="bg-blue-50/40 p-4 rounded-xl border border-blue-100/60 flex items-start space-x-3 mb-4">
                     <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600 mt-1">
                         <Sparkles className="w-4 h-4" />
                     </div>
                     <div className="flex-1">
                         <p className="text-xs font-black text-blue-700 uppercase tracking-wider">Recomanació de l'Agent d'IA</p>
                         <p className="text-sm font-bold text-slate-800 mt-0.5">{accioRecomanada}</p>
                         <p className="text-xs text-slate-600 mt-1">{rao}</p>
                     </div>
                 </div>
             )}

              {/* Bloc 0.5: Xat Estratègic amb l'Agent */}
              <div className="bg-slate-50/70 p-4 rounded-xl border border-slate-100 flex flex-col space-y-3">
                  <div className="flex items-center space-x-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                      <p className="text-xs font-black text-slate-500 uppercase tracking-wider">Xat amb l'Agent (Estratègia i Dubtes)</p>
                  </div>
                  
                  <div className="max-h-[180px] overflow-y-auto space-y-2 flex flex-col p-2 bg-white/50 rounded-lg border border-slate-100/80">
                      {chatMessages.length === 0 && (
                          <p className="text-[11px] text-slate-400 italic">No hi ha missatges. Pregunta quelcom sobre el deal...</p>
                      )}
                      {chatMessages.map((m, i) => (
                          <div 
                              key={i} 
                              className={`p-2.5 rounded-2xl max-w-[85%] text-xs ${
                                  m.role === 'user' 
                                  ? 'bg-blue-600 text-white self-end rounded-br-none' 
                                  : 'bg-slate-100 text-slate-800 self-start rounded-bl-none border border-slate-200/40'
                              }`}
                          >
                              {m.content}
                          </div>
                      ))}
                      {chatLoading && (
                          <div className="self-start bg-slate-100 text-slate-400 p-2.5 rounded-2xl rounded-bl-none text-xs italic flex items-center space-x-1 border border-slate-200/40">
                              <Loader2 className="w-3 h-3 animate-spin" />
                              <span>L'Agent està escrivint...</span>
                          </div>
                      )}
                  </div>

                  <div className="flex space-x-2">
                      <input 
                          type="text" 
                          value={chatInput} 
                          onChange={e => setChatInput(e.target.value)} 
                          onKeyDown={e => e.key === 'Enter' && handleSendChat()}
                          placeholder="Pregunta dubtes, objeccions, argumentació..." 
                          className="flex-1 text-xs border border-slate-200 rounded-xl px-3 py-2.5 focus:ring-1 focus:ring-blue-500 outline-none bg-white"
                      />
                      <button 
                          onClick={handleSendChat} 
                          disabled={chatLoading}
                          className="bg-blue-600 text-white px-3.5 py-2.5 rounded-xl text-xs font-bold hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center"
                      >
                          <Send className="w-3.5 h-3.5" />
                      </button>
                  </div>
              </div>

             {/* Bloc 1: Anotacions del Deal */}
             <div className="bg-slate-50 p-5 rounded-2xl border border-slate-100 space-y-3">
                 <label className="text-xs font-black text-slate-500 uppercase tracking-wider">Anotacions del Deal (Llegit per la IA)</label>
                 <textarea 
                     value={anglePersonalitzacio}
                     onChange={e => setAnglePersonalitzacio(e.target.value)}
                     className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium text-slate-700 outline-none focus:ring-1 focus:ring-blue-500/20 min-h-[70px]"
                 />
                 <button 
                     onClick={handleUpdateContext}
                     disabled={isSaving}
                     className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-bold transition-all shadow-sm flex items-center space-x-1"
                 >
                     {isSaving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4" />}
                     <span>Desa Anotacions</span>
                 </button>
             </div>

             {/* Bloc 2: Registrar Actuació */}
             <div className="bg-slate-50 p-5 rounded-2xl border border-slate-100 space-y-3">
                 <div className="flex items-center space-x-2">
                     <Phone className="w-4 h-4 text-emerald-600" />
                     <label className="text-xs font-black text-slate-500 uppercase tracking-wider">Registrar Actuació (Trucada, Demo, Visita...)</label>
                 </div>
                 <textarea 
                     value={notesActuacio}
                     onChange={e => setNotesActuacio(e.target.value)}
                     placeholder="Afegeix què ha passat a la trucada o reunió..."
                     className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium text-slate-700 outline-none focus:ring-1 focus:ring-emerald-500/20 min-h-[70px]"
                 />
                 <button 
                     onClick={handleSaveActuacio}
                     disabled={isLogSaving || !notesActuacio.trim()}
                     className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition-all shadow-sm flex items-center space-x-1 disabled:opacity-50"
                 >
                     {isLogSaving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4" />}
                     <span>Registra Actuació</span>
                 </button>
             </div>

             {/* Bloc 3: Redactar Email */}
             <div className="border-t pt-6 space-y-4">
                 <div className="flex items-center justify-between">
                     <p className="text-xs font-black text-slate-500 uppercase tracking-wider">Redacció de correu</p>
                     {!isGenerating && (
                         <button 
                             onClick={fetchDraftVariants}
                             className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-black transition-all flex items-center space-x-2 shadow-md shadow-blue-100"
                         >
                             <Sparkles className="w-4 h-4" />
                             <span>{variants.length > 0 ? "RE-GENERA AMB IA" : "REDACTA AMB IA"}</span>
                         </button>
                     )}
                 </div>

                 {isGenerating && (
                     <div className="flex flex-col items-center justify-center p-8 space-y-3 bg-blue-50/50 rounded-2xl border border-blue-100">
                         <Loader2 className="w-7 h-7 text-blue-600 animate-spin" />
                         <p className="text-xs font-bold text-blue-700 uppercase tracking-wider">Generant variants amb Kimi K2...</p>
                     </div>
                 )}

                 {variants.length > 0 && !isGenerating && (
                     <div className="bg-blue-50/40 p-3 border border-blue-100 rounded-xl flex items-center space-x-2">
                         <span className="text-xs font-bold text-blue-700 mx-2"><Sparkles className="w-3 h-3 inline mr-1" /> Variants:</span>
                         {variants.map((v: any, idx: number) => (
                             <button 
                                 key={idx}
                                 onClick={() => handleSelectVariant(idx)}
                                 className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                                     selectedVariantIdx === idx 
                                       ? 'bg-blue-600 text-white shadow-md' 
                                       : 'bg-white border border-blue-100 text-blue-600 hover:bg-blue-100/50'
                                 }`}
                             >
                                 # {idx+1} {v.angle ? `(${v.angle})` : ""}
                             </button>
                         ))}
                     </div>
                 )}

                 {/* Sempre visible el formulari d'email */}
                 <div className="space-y-3 bg-white border border-slate-200 p-5 rounded-2xl">
                     <input 
                         type="email"
                         value={to}
                         onChange={e => setTo(e.target.value)}
                         placeholder="Per a: destinatari@ajuntament.cat"
                         className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-xs font-bold text-slate-700 outline-none focus:ring-1 focus:ring-blue-500/20"
                     />
                     <input 
                         value={subject}
                         onChange={e => setSubject(e.target.value)}
                         placeholder="Assumpte del correu"
                         className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 font-bold text-slate-700 outline-none focus:ring-1 focus:ring-blue-500/20"
                     />
                     <textarea 
                         value={body}
                         onChange={e => setBody(e.target.value)}
                         placeholder="El missatge de l'email..."
                         className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium text-slate-700 outline-none focus:ring-1 focus:ring-blue-500/20 min-h-[180px]"
                     />
                     <div className="flex justify-end space-x-3 pt-2">
                         <button 
                             onClick={handleSend}
                             disabled={sending || !subject || !body}
                             className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold text-xs transition-all flex items-center space-x-2 shadow-xl shadow-blue-200"
                         >
                             {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                             <span>Envia Ara</span>
                         </button>
                     </div>
                 </div>
             </div>
          </div>
        )}
      </div>
    </div>
  );
}
