"use client";

import { useState } from "react";
import { X, Mail, Send, Loader2 } from "lucide-react";
import api from "@/lib/api";

interface EmailComposerProps {
  municipiId: string;
  onClose: () => void;
  onSent: () => void;
  initialTo?: string;
  initialSubject?: string;
}

export function EmailComposer({ municipiId, onClose, onSent, initialTo = "", initialSubject = "" }: EmailComposerProps) {
  const [to, setTo] = useState(initialTo);
  const [assumpte, setAssumpte] = useState(initialSubject);
  const [cos, setCos] = useState("");
  const [sending, setSending] = useState(false);

  const handleSend = async () => {
    if (!assumpte || !cos) {
      alert("L'assumpte i el cos de l'email són obligatoris.");
      return;
    }

    setSending(true);
    try {
      await api.emails.enviar({
        municipi_id: municipiId,
        to,
        assumpte,
        cos
      });
      onSent();
      onClose();
    } catch (e) {
      console.error(e);
      alert("Hi ha hagut un error enviant l'email.");
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
            <h2 className="text-lg font-black tracking-tight">Redactar Email Manual</h2>
          </div>
          <button onClick={onClose} className="p-1 hover:bg-slate-200 rounded-full transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 flex-1 overflow-y-auto space-y-4">
          <div>
            <label className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1 block">Per a (opcional, per defecte contacte principal)</label>
            <input
              value={to}
              onChange={e => setTo(e.target.value)}
              placeholder="email@destinacio.com"
              className="w-full border border-slate-200 rounded-xl px-4 py-2 text-sm font-medium focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            />
          </div>
          <div>
            <label className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1 block">Assumpte</label>
            <input
              value={assumpte}
              onChange={e => setAssumpte(e.target.value)}
              placeholder="Assumpte de l'email"
              className="w-full border border-slate-200 rounded-xl px-4 py-2 text-sm font-bold focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            />
          </div>
          <div>
            <label className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1 block">Missatge</label>
            <textarea
              value={cos}
              onChange={e => setCos(e.target.value)}
              className="w-full min-h-[250px] border border-slate-200 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all resize-y"
              placeholder="Escriu el teu missatge aquí..."
            />
          </div>
        </div>

        <div className="p-4 border-t bg-slate-50 flex justify-end space-x-3">
          <button onClick={onClose} className="px-4 py-2 font-bold text-sm text-slate-500 hover:text-slate-700 transition-colors">
            Cancel·lar
          </button>
          <button
            onClick={handleSend}
            disabled={sending}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl flex items-center space-x-2 shadow-sm hover:shadow transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            <span>{sending ? 'Enviant...' : 'Enviar'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
