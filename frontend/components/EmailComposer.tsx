"use client";

import { useState } from "react";
import { X, Mail, Sparkles, Bot, Loader2, Send } from "lucide-react";
import api from "@/lib/api";

interface EmailComposerProps {
  onClose: () => void;
  onSent?: () => void;
  initialTo?: string;
  initialSubject?: string;
  dealId?: string;
  contacteId?: string;
  initialBody?: string;
}

export function EmailComposer({ 
    onClose, 
    onSent, 
    initialTo = "", 
    initialSubject = "", 
    initialBody = "",
    dealId,
    contacteId
}: EmailComposerProps) {
  const [to, setTo] = useState(initialTo);
  const [subject, setSubject] = useState(initialSubject);
  const [body, setBody] = useState(initialBody);
  const [instruccionsIA, setInstruccionsIA] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [selectedModel, setSelectedModel] = useState("anthropic/claude-3.5-sonnet");

  const handleRedactarIA = async () => {
    setAiLoading(true);
    try {
      const res = await api.agent.redactarEmail({
        deal_id: dealId || null,
        contacte_id: contacteId || null,
        instruccions: instruccionsIA,
        model: selectedModel,
        to_address: to
      });
      if (res.assumpte) setSubject(res.assumpte);
      if (res.cos_text) setBody(res.cos_text);
    } catch (error) {
      console.error("Error redactant amb IA", error);
    } finally {
      setAiLoading(false);
    }
  };

  const handleSend = async () => {
    setSending(true);
    try {
      await api.emails.enviar({
        to,
        assumpte: subject,
        cos: body, // For now sending as plain text or simple HTML
        deal_id: dealId || null,
        contacte_id: contacteId || null
      });
      if (onSent) onSent();
      onClose();
    } catch (error) {
      console.error("Error enviant email", error);
      alert("Error enviant el correu. Revisa la configuració SMTP.");
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4 overflow-hidden">
      <div className="bg-white w-full max-w-3xl rounded-3xl shadow-2xl flex flex-col max-h-[90vh] animate-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="p-6 border-b flex justify-between items-center bg-slate-50 rounded-t-3xl">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-slate-900 rounded-xl flex items-center justify-center text-white">
              <Mail className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-black text-slate-800 tracking-tight">Nou Correu Electrònic</h2>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Plataforma de Comunicació PXX</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-slate-200 rounded-full transition-colors">
            <X className="w-6 h-6 text-slate-400" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-8 space-y-6">
          <div className="space-y-4">
            <div className="grid grid-cols-12 gap-4 items-center">
              <label className="col-span-2 text-[10px] font-black text-slate-400 uppercase tracking-widest">Per a:</label>
              <input 
                type="email"
                value={to}
                onChange={e => setTo(e.target.value)}
                placeholder="destinatari@ajuntament.cat"
                className="col-span-10 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 font-bold text-slate-700 outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-all"
              />
            </div>
            <div className="grid grid-cols-12 gap-4 items-center">
              <label className="col-span-2 text-[10px] font-black text-slate-400 uppercase tracking-widest">Assumpte:</label>
              <input 
                value={subject}
                onChange={e => setSubject(e.target.value)}
                placeholder="Assumpte del correu"
                className="col-span-10 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 font-bold text-slate-700 outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-all"
              />
            </div>
          </div>

          {/* IA Section */}
          <div className="bg-blue-50/50 p-5 rounded-2xl border border-blue-100 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-blue-600">
                <Sparkles className="w-4 h-4" />
                <span className="text-[10px] font-black uppercase tracking-widest">Redactar amb IA</span>
              </div>
              <select 
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="bg-white/80 text-[10px] font-bold px-3 py-1 rounded-lg border border-blue-200 outline-none text-blue-700"
              >
                  <option value="anthropic/claude-3.5-sonnet">Claude 3.5 Sonnet</option>
                  <option value="openai/gpt-4o">GPT-4o (Premium)</option>
                  <option value="openai/gpt-4o-mini">GPT-4o mini (Ràpid)</option>
                  <option value="google/gemini-pro-1.5">Gemini 1.5 Pro</option>
                  <option value="mistralai/mistral-small-3.1-24b-instruct">Mistral Small</option>
                  <option value="meta-llama/llama-3.1-70b-instruct">Llama 3.1 70B</option>
              </select>
            </div>
            <textarea 
              placeholder="Instruccions per a la IA... (Ex: 'Demana una cita per presentar el projecte')"
              value={instruccionsIA}
              onChange={e => setInstruccionsIA(e.target.value)}
              className="w-full bg-white/80 border border-blue-100 rounded-xl px-4 py-3 text-sm font-medium text-slate-700 outline-none focus:border-blue-300 min-h-[80px] placeholder:text-blue-300"
            />
            <button 
              onClick={handleRedactarIA}
              disabled={aiLoading || !instruccionsIA}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-black uppercase tracking-widest transition-all disabled:opacity-50 flex items-center justify-center space-x-2 shadow-lg shadow-blue-200"
            >
              {aiLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Bot className="w-4 h-4" />}
              <span>{body ? 'Regenerar Versió' : 'Generar Esborrany Professional'}</span>
            </button>
          </div>

          <textarea 
            value={body}
            onChange={e => setBody(e.target.value)}
            placeholder="Escriu el missatge aquí..."
            className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-6 py-4 font-medium text-slate-700 outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 min-h-[250px] leading-relaxed"
          />
        </div>

        {/* Footer */}
        <div className="p-6 border-t bg-slate-50 flex space-x-4 rounded-b-3xl">
          <button 
            onClick={onClose}
            className="px-8 py-3 text-slate-400 hover:text-slate-600 font-bold text-sm transition-colors"
          >
            Cancel·lar
          </button>
          <button 
            onClick={handleSend}
            disabled={sending || !to || !subject || !body}
            className="flex-1 h-14 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl font-black text-sm transition-all disabled:opacity-50 flex items-center justify-center space-x-3 shadow-xl shadow-slate-200"
          >
            {sending ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            <span>ENVIAR CORREU ARA</span>
          </button>
        </div>
      </div>
    </div>
  );
}
