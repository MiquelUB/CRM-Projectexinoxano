"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { format } from "date-fns";
import { Mail, MailOpen, ArrowRightLeft, ArrowDownRight, ArrowUpRight, Eye, Plus, Send, X, Bot, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { EmailComposer } from "@/components/EmailComposer";

export default function EmailsPage() {
  const [isClient, setIsClient] = useState(false);
  const [emails, setEmails] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("ALL"); // ALL, IN, OUT, UNREAD
  const [showComposer, setShowComposer] = useState(false);
  const [selectedEmail, setSelectedEmail] = useState<any>(null);
  const [composerConfig, setComposerConfig] = useState<any>({ to: "", subject: "", dealId: "" });
  const [search, setSearch] = useState("");

  useEffect(() => {
    setIsClient(true);
    const timer = setTimeout(() => {
        fetchEmails();
    }, 300);
    return () => clearTimeout(timer);
  }, [filter, search]);

  const fetchEmails = async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = { page: "1" };
      if (filter === "IN" || filter === "OUT") params.direccio = filter;
      if (filter === "UNREAD") params.llegit = "false";
      if (search) params.cerca = search;
      
      const res = await api.emails.llistar(params);
      const sanitizedEmails = (res.items || []).map((em: any) => ({
        ...em,
        data_enviament: em.data_enviament || em.created_at || new Date().toISOString()
      }));
      setEmails(sanitizedEmails);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleManualSync = async () => {
    try {
      await api.emails.sync();
      fetchEmails();
    } catch (err) {
      alert("Error durant la sincronització manual.");
    }
  };

  const handleDeleteEmail = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!window.confirm("Estàs segur que vols eliminar aquest correu? Aquesta acció és permanent.")) return;
    
    try {
      await api.emails.eliminar(id);
      fetchEmails();
    } catch (err) {
      alert("Error eliminant el correu.");
    }
  };

  const markAsRead = async (email: any) => {
    if (!email.llegit) {
        try {
            await api.emails.marcarLlegit(email.id, true);
            setEmails(prev => prev.map(e => e.id === email.id ? {...e, llegit: true} : e));
        } catch (err) {
            console.error(err);
        }
    }
  };

  if (loading && !selectedEmail && !showComposer) return (
    <div className="p-20 flex flex-col items-center justify-center space-y-4">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px]">Llegint la teva safata d'entrada...</p>
    </div>
  );

  const safeFormatDate = (dateStr: string | null | undefined) => {
    if (!dateStr) return "N/A";
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return "N/A";
    return d.toLocaleDateString('ca-ES') + " " + d.toLocaleTimeString('ca-ES', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-start">
        <div>
            <h1 className="text-4xl font-extrabold premium-gradient-text tracking-tight">Comunicacions</h1>
            <p className="text-slate-500 mt-1">Plataforma integrada per a la gestió del correu corporatiu.</p>
        </div>
        <div className="flex space-x-3">
            <Button 
                onClick={() => {
                    setComposerConfig({ to: "", subject: "", dealId: "" });
                    setShowComposer(true);
                }}
                className="h-12 px-6 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-bold shadow-lg shadow-blue-100 transition-all active:scale-[0.95] flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>Nou Correu</span>
            </Button>
            <Button 
                onClick={handleManualSync} 
                variant="outline"
                className="h-12 px-6 bg-white hover:bg-slate-50 text-slate-700 rounded-2xl font-bold border-slate-200 transition-all flex items-center space-x-2"
            >
              <ArrowRightLeft className="w-4 h-4 text-blue-500" />
              <span>Sincronitzar IMAP</span>
            </Button>
        </div>
      </div>
      
      <div className="flex items-center justify-between">
          <div className="flex bg-slate-100 p-1.5 rounded-2xl space-x-1 border border-slate-200/50">
            {[
                { id: "ALL", label: "Tots" },
                { id: "IN", label: "Rebuts" },
                { id: "OUT", label: "Enviats" },
                { id: "UNREAD", label: "No Llegits" }
            ].map(f => (
              <button 
                key={f.id} 
                className={`px-5 py-2.5 rounded-xl text-xs font-black transition-all ${
                    filter === f.id 
                    ? "bg-white text-slate-900 shadow-sm" 
                    : "text-slate-400 hover:text-slate-600"
                }`}
                onClick={() => setFilter(f.id)}
              >
                {f.label.toUpperCase()}
              </button>
            ))}
          </div>
          
          <div className="text-right">
             <p className="text-[10px] font-black text-slate-300 uppercase tracking-widest">Sincronitzat fa poc</p>
             {isClient && <p className="text-xs font-bold text-slate-500">{format(new Date(), "HH:mm:ss")}</p>}
          </div>
      </div>

      <div className="glass-card p-4 flex items-center space-x-4 border-white/60 shadow-lg shadow-slate-200/40">
        <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center">
            {/* Using Eye Icon or similar as eye but let's just use Mail for general searches or search icon */}
            <Eye className="text-slate-400 w-5 h-5" />
        </div>
        <input 
          type="text" 
          placeholder="Cerca per assumpte, cos o destinatari..." 
          className="flex-1 bg-transparent outline-none font-bold text-slate-700 placeholder:text-slate-300"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="glass-card overflow-hidden border-white/60 shadow-xl shadow-slate-200/30">
        <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50 border-b border-slate-100">
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Direccio</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Contacte</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Assumpte</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Estat Deal</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Data</th>
                <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] text-right">Accions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 bg-white/40">
            {emails.map((email) => (
              <tr 
                key={email.id} 
                className={`hover:bg-blue-50/30 transition-colors group cursor-pointer ${!email.llegit ? "bg-blue-50/50" : ""}`}
                onClick={() => {
                    setSelectedEmail(email);
                    markAsRead(email);
                }}
              >
                <td className="px-8 py-5">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${email.direccio === "IN" ? "bg-blue-50 text-blue-600" : "bg-emerald-50 text-emerald-600"}`}>
                    {email.direccio === "IN" ? (
                      <ArrowDownRight className="w-4 h-4" />
                    ) : (
                      <ArrowUpRight className="w-4 h-4" />
                    )}
                  </div>
                </td>
                <td className="px-8 py-5">
                  <div className="flex flex-col space-y-1">
                    <p className={`text-sm tracking-tight ${!email.llegit ? "font-black text-slate-800" : "font-semibold text-slate-500"}`}>
                      {email.direccio === "IN" ? (email.from_address || "Desconegut") : (email.to_address || "Desconegut")}
                    </p>
                    {email.direccio === "OUT" && (
                      <div className="flex items-center space-x-2" title={email.obert ? `Obert ${email.nombre_obertures} vegades.` : "No obert encara"}>
                        <Eye className={`w-3 h-3 ${email.obert ? 'text-emerald-500' : 'text-slate-300'}`} />
                        {email.obert && <span className="text-[10px] text-emerald-600 font-black">{email.nombre_obertures}</span>}
                      </div>
                    )}
                  </div>
                </td>
                <td className="px-8 py-5">
                  <p className={`text-sm truncate max-w-md ${!email.llegit ? "font-black text-slate-900" : "font-medium text-slate-600"}`} title={email.assumpte}>
                    {email.assumpte}
                  </p>
                </td>
                <td className="px-8 py-5">
                  {email.deal_id ? (
                    <span className="bg-emerald-100 text-emerald-700 text-[10px] font-black px-2 py-1 rounded-md uppercase tracking-tighter">Vinculat</span>
                  ) : (
                    <span className="bg-rose-100 text-rose-700 text-[10px] font-black px-2 py-1 rounded-md uppercase tracking-tighter">Sense deal</span>
                  )}
                </td>
                <td className="px-8 py-5">
                  <p className="text-[11px] font-bold text-slate-400">
                    {safeFormatDate(email.data_enviament || email.data_email)}
                  </p>
                </td>
                <td className="px-8 py-5 text-right">
                    <button 
                        onClick={(e) => handleDeleteEmail(email.id, e)}
                        className="p-2 text-slate-300 hover:text-rose-500 transition-colors bg-transparent rounded-lg hover:bg-rose-50"
                        title="Eliminar correu"
                    >
                        <Trash2 className="w-4 h-4" />
                    </button>
                </td>
              </tr>
            ))}
            {emails.length === 0 && (
              <tr>
                <td colSpan={6} className="px-8 py-20 text-center">
                    <div className="flex flex-col items-center opacity-40">
                        <div className="text-4xl mb-4">Inbox Neta ✨</div>
                        <p className="text-slate-400 font-bold uppercase tracking-widest text-xs">No hi ha comunicacions per mostrar</p>
                    </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* MODALS */}
      {showComposer && (
        <EmailComposer 
            initialTo={composerConfig.to}
            initialSubject={composerConfig.subject}
            municipiId={composerConfig.dealId}
            onClose={() => setShowComposer(false)} 
            onSent={() => fetchEmails()}
        />
      )}

      {selectedEmail && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-4xl rounded-3xl shadow-2xl flex flex-col max-h-[90vh] animate-in zoom-in-95 duration-200">
            <div className="p-6 border-b flex justify-between items-center bg-slate-50 rounded-t-3xl">
              <div className="flex items-center space-x-3">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-white ${selectedEmail.direccio === "IN" ? "bg-blue-600" : "bg-emerald-600"}`}>
                   {selectedEmail.direccio === "IN" ? <ArrowDownRight className="w-5 h-5" /> : <ArrowUpRight className="w-5 h-5" />}
                </div>
                <div>
                   <h2 className="text-xl font-black text-slate-800 truncate max-w-xl">{selectedEmail.assumpte}</h2>
                   <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                     {selectedEmail.direccio === "IN" ? `Rebut de: ${selectedEmail.from_address}` : `Enviat a: ${selectedEmail.to_address}`}
                   </p>
                </div>
              </div>
              <button onClick={() => setSelectedEmail(null)} className="p-2 hover:bg-slate-200 rounded-full transition-colors">
                <X className="w-6 h-6 text-slate-400" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-10 bg-[#fdfdfd]">
               <div className="max-w-none prose prose-blue">
                  <div className="text-slate-700 whitespace-pre-wrap leading-relaxed font-medium" dangerouslySetInnerHTML={{ __html: selectedEmail.cos || "No hi ha contingut disponible." }} />
               </div>
            </div>
            <div className="p-6 border-t bg-slate-50 rounded-b-3xl flex justify-between items-center">
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                  Data: {safeFormatDate(selectedEmail.data_enviament || selectedEmail.data_email)}
                </div>
                <div className="flex space-x-2">
                    {selectedEmail.direccio === "IN" && (
                        <Button 
                            onClick={() => {
                                const sub = selectedEmail.assumpte.startsWith("Re:") ? selectedEmail.assumpte : `Re: ${selectedEmail.assumpte}`;
                                setComposerConfig({ 
                                    to: selectedEmail.from_address, 
                                    subject: sub, 
                                    dealId: selectedEmail.deal_id || "" 
                                });
                                setSelectedEmail(null);
                                setShowComposer(true);
                            }}
                            className="bg-slate-900 text-white rounded-xl font-bold px-6"
                        >
                            Respondre
                        </Button>
                    )}
                    <Button 
                        variant="ghost"
                        onClick={() => setSelectedEmail(null)}
                        className="text-slate-400 font-bold"
                    >
                        Tancar
                    </Button>
                </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
