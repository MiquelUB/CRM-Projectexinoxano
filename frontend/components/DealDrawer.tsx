import { useState, useEffect } from "react";
import api from "@/lib/api";
import { format } from "date-fns";
import { X, Mail, CreditCard, Trash2, Save, Euro, Building2, User, Loader2 } from "lucide-react";

export default function DealDrawer({ deal, onClose, onUpdate }: any) {
  // State per a camps editables
  // State per a camps editables (V2 MunicipiLifecycle)
  const safeFormatDate = (dateStr: string | null | undefined, formatStr: string = "dd/MM/yyyy") => {
    if (!dateStr) return "N/A";
    try {
      const d = new Date(dateStr);
      if (isNaN(d.getTime())) return "Invalid";
      return format(d, formatStr);
    } catch (e) {
      return "Error";
    }
  };

  const [nom, setNom] = useState(deal.nom || "");
  const [valorSetup, setValorSetup] = useState(deal.valor_setup?.toString() || "0");
  const [valorLlicencia, setValorLlicencia] = useState(deal.valor_llicencia?.toString() || "0");
  const [prioritat, setPrioritat] = useState(deal.prioritat || "mitjana");
  const [properPas, setProperPas] = useState(deal.proper_pas || "");
  const [dataSeguiment, setDataSeguiment] = useState(() => {
    if (!deal.data_seguiment) return "";
    try {
      const d = new Date(deal.data_seguiment);
      return isNaN(d.getTime()) ? "" : d.toISOString().split('T')[0];
    } catch { return ""; }
  });
  const [notesHumanes, setNotesHumanes] = useState(deal.notes_humanes || "");
  
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [activitats, setActivitats] = useState<any[]>([]);
  const [llicencia, setLlicencia] = useState<any>(null);


  // Email Composer State
  const [showEmailComposer, setShowEmailComposer] = useState(false);
  const [composerData, setComposerData] = useState({ to: "", subject: "", body: "", instruccionsIA: "" });
  const [sendingEmail, setSendingEmail] = useState(false);

  const handleOpenComposer = (to = deal.actor_principal?.email || "", subject = `Seguiment PXX — ${deal.nom || 'Ajuntament'}`, body = "") => {
    setComposerData({ to, subject, body, instruccionsIA: "" });
    setShowEmailComposer(true);
  };

  const handleSendEmail = async () => {
    setSendingEmail(true);
    try {
      await api.emails.enviar({
        municipi_id: deal.id,
        to: composerData.to,
        assumpte: composerData.subject,
        cos: composerData.body
      });
      setShowEmailComposer(false);
      // Refresh activities
      fetchActivitats();
    } catch (e: any) {
      alert(`Error enviant email: ${e.message}`);
    } finally {
      setSendingEmail(false);
    }
  };


  const fetchActivitats = async () => {
    try {
      const res = await api.municipis.get_activitats(deal.id);
      setActivitats(Array.isArray(res) ? res : (res.items || []));
    } catch (e) {
      console.error("Error carregant activitats", e);
    }
  };

  useEffect(() => {
    if (deal.id) {
      fetchActivitats();
      api.municipis.get_llicencia(deal.id).then((l: any) => setLlicencia(l));
    }
  }, [deal.id]);

  const handleSaveAll = async () => {
    setSaving(true);
    try {
      await api.municipis.editar(deal.id, {
        nom,
        valor_setup: parseFloat(valorSetup),
        valor_llicencia: parseFloat(valorLlicencia),
        prioritat,
        proper_pas: properPas || null,
        data_seguiment: dataSeguiment || null,
        notes_humanes: notesHumanes
      });
      if (onUpdate) onUpdate();
      alert("Municipi actualitzat correctament.");
    } catch (e: any) {
      alert(`Error al guardar: ${e.message}`);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Estàs segur que vols eliminar aquest municipi?")) return;
    setDeleting(true);
    try {
      await api.municipis.eliminar(deal.id);
      if (onUpdate) onUpdate();
      onClose();
    } catch (e: any) {
      alert(`Error al eliminar: ${e.message}`);
    } finally {
      setDeleting(false);
    }
  };

  const handleCrearLlicencia = async () => {
    try {
      const data_inici = new Date().toISOString().split('T')[0];
      const nextYear = new Date();
      nextYear.setFullYear(nextYear.getFullYear() + 1);
      const data_renovacio = nextYear.toISOString().split('T')[0];
      
      await api.llicencies.crear({
          deal_id: deal.id,
          data_inici,
          data_renovacio,
          estat: "activa"
      });
      api.llicencies.llistar({ deal_id: deal.id }).then((res: any) => {
         if (res.items && res.items.length > 0) setLlicencia(res.items[0]);
      });
      if (onUpdate) onUpdate();
    } catch (e) {
      alert("Error creant llicència.");
    }
  };

  const handleConfirmarPagament = async (pagamentId: string) => {
    try {
      await api.pagaments.confirmar(pagamentId, { estat: "pagat", data_confirmacio: new Date().toISOString().split('T')[0] });
      // Refresh license to get updated payments list
      api.llicencies.llistar({ deal_id: deal.id }).then((res: any) => {
         if (res.items && res.items.length > 0) setLlicencia(res.items[0]);
      });
      if (onUpdate) onUpdate();
    } catch (e) {
      alert("Error confirmant pagament.");
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/40 flex justify-end backdrop-blur-sm">
      <div className="w-[550px] h-full bg-white shadow-2xl flex flex-col translate-x-0 transition-transform overflow-hidden relative">
        {/* Header - NOU ESTIL CARBONI (DIFERENT) */}
        <div className="bg-[#0f172a] text-white p-7 sticky top-0 z-10 shrink-0 border-b border-white/5 shadow-2xl">
          <div className="flex justify-between items-start mb-6">
            <div className="flex items-center space-x-4">
              <div className="w-14 h-14 bg-blue-500/20 rounded-2xl flex items-center justify-center border border-blue-500/30 shadow-inner">
                <Building2 className="w-7 h-7 text-blue-400" />
              </div>
              <div>
                <h2 className="text-2xl font-black tracking-tighter text-white leading-none">{deal.nom}</h2>
                <div className="flex items-center gap-2 text-slate-400 text-[10px] font-black uppercase tracking-[0.2em] mt-2">
                   <span>{deal.comarca}</span>
                   <span className="opacity-30">•</span>
                   <span>{deal.poblacio?.toLocaleString() || '0'} hab.</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-2">
                <button onClick={onClose} className="p-2 text-slate-400 hover:text-white transition-colors bg-white/5 rounded-xl border border-white/10">
                  <X className="w-5 h-5" />
                </button>
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-2">
             <div className="bg-white/5 rounded-xl p-2 border border-white/10 flex flex-col items-center">
                <span className="text-[9px] font-black text-slate-500 uppercase">Temperatura</span>
                <span className="text-sm font-bold mt-0.5">
                  {deal.temperatura === 'fred' ? '🧊 Fred' : 
                   deal.temperatura === 'templat' ? '⚡ Templat' : 
                   deal.temperatura === 'calent' ? '🔥 Calent' : '☀️ Bullent'}
                </span>
             </div>
             <div className="bg-white/5 rounded-xl p-2 border border-white/10 flex flex-col items-center">
                <span className="text-[9px] font-black text-slate-500 uppercase">Etapa</span>
                <span className="text-sm font-bold mt-0.5 text-blue-400">
                  {deal.etapa_actual?.replace('_', ' ').toUpperCase()}
                </span>
             </div>
             <div className="bg-white/5 rounded-xl p-2 border border-white/10 flex flex-col items-center">
                <span className="text-[9px] font-black text-slate-500 uppercase">Prioritat</span>
                <span className={`text-sm font-bold mt-0.5 ${deal.prioritat === 'alta' ? 'text-rose-400' : 'text-slate-300'}`}>
                  {deal.prioritat?.toUpperCase()}
                </span>
             </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-8 space-y-8 flex-1 overflow-y-auto custom-scrollbar pb-32">
          {/* Secció Informació General */}
          <section className="grid grid-cols-2 gap-6">
            <div className="col-span-2 md:col-span-1">
                <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Territori</label>
                <div className="flex items-center space-x-2 text-slate-700 font-bold bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <Building2 className="w-4 h-4 text-slate-400" />
                    <span>{deal.comarca} ({deal.provincia})</span>
                </div>
            </div>
            <div className="col-span-2 md:col-span-1">
                <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Actor Principal</label>
                <div className="flex items-center space-x-2 text-slate-700 font-bold bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <User className="w-4 h-4 text-slate-400" />
                    <span>{deal.actor_principal?.nom || "Sense assignar"}</span>
                </div>
            </div>
          </section>

          {/* Secció Econòmica */}
          <section className="bg-blue-50/50 p-6 rounded-2xl border border-blue-100">
            <h3 className="text-xs font-black text-blue-600 uppercase tracking-widest mb-4 flex items-center">
                <Euro className="w-3 h-3 mr-2" /> Valors de l'Acord
            </h3>
            <div className="grid grid-cols-2 gap-6">
                <div>
                    <label className="block text-[10px] font-extrabold text-blue-400 uppercase mb-1">Set Up (€)</label>
                   <input 
                        type="number"
                        value={valorSetup} 
                        onChange={e => setValorSetup(e.target.value)}
                        className="w-full bg-white border border-blue-100 rounded-xl px-4 py-2 font-bold text-slate-700 outline-none focus:border-blue-400"
                   />
                </div>
                <div>
                    <label className="block text-[10px] font-extrabold text-blue-400 uppercase mb-1">Manteniment (€)</label>
                   <input 
                        type="number"
                        value={valorLlicencia} 
                        onChange={e => setValorLlicencia(e.target.value)}
                        className="w-full bg-white border border-blue-100 rounded-xl px-4 py-2 font-bold text-slate-700 outline-none focus:border-blue-400"
                   />
                </div>
                <div className="col-span-2 flex justify-between items-center pt-2 border-t border-blue-100">
                    <span className="text-[10px] font-black text-blue-400 uppercase">Total Pipeline</span>
                    <span className="text-lg font-black text-blue-700">
                        {(Number(valorSetup) + Number(valorLlicencia)).toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })}
                    </span>
                </div>
            </div>
          </section>

          {/* Secció Prioritat i Etapa */}
          <section className="grid grid-cols-2 gap-6">
            <div>
                <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Prioritat</label>
                <select 
                    value={prioritat} 
                    onChange={e => setPrioritat(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 font-bold text-slate-700 outline-none focus:border-blue-400"
                >
                    <option value="alta">Alta 🔥</option>
                    <option value="mitjana">Mitjana ⚡</option>
                    <option value="baixa">Baixa 🧊</option>
                </select>
            </div>
            <div>
                <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Etapa Actual</label>
                <div className="px-4 py-2 rounded-xl bg-slate-100 text-slate-500 font-bold text-sm border border-slate-200">
                    {deal.etapa_actual.replace('_', ' ').toUpperCase()}
                </div>
            </div>
          </section>

          {/* Secció Proper Pas */}
          <section>
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest mb-4">Proper Pas</h3>
            <div className="space-y-4">
              <input
                type="text"
                value={properPas}
                onChange={(e) => setProperPas(e.target.value)}
                placeholder="Ex: Trucar a l'alcalde"
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400"
              />
              <div className="relative">
                <input
                  type="date"
                  value={dataSeguiment}
                  onChange={(e) => setDataSeguiment(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400"
                />
              </div>
            </div>
          </section>

          <section>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest">Diari d'Abord / Notes de Seguiment</h3>
            </div>
            <textarea
                value={notesHumanes}
                onChange={(e) => setNotesHumanes(e.target.value)}
                placeholder="Escriu aquí qualsevol detall de la negociació..."
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-700 outline-none focus:border-blue-400 min-h-[120px]"
            />
          </section>


          {/* Secció Llicència (visible només a client) */}
          {deal.etapa_actual === "client" && (
            <section className="bg-emerald-50 p-6 rounded-2xl border border-emerald-100">
               <h3 className="text-xs font-black text-emerald-600 uppercase tracking-widest mb-4 flex items-center">
                 <CreditCard className="w-4 h-4 mr-2" /> Gestió de Llicència
               </h3>
               {llicencia ? (
                 <div className="text-sm space-y-2">
                     <p className="flex justify-between">
                         <span className="text-emerald-600 font-bold uppercase text-[10px]">Estat</span>
                         <span className="font-black text-emerald-700">{llicencia.estat.toUpperCase()}</span>
                     </p>
                     <p className="flex justify-between">
                         <span className="text-emerald-600 font-bold uppercase text-[10px]">Inici</span>
                         <span className="font-bold">{safeFormatDate(llicencia.data_inici)}</span>
                     </p>
                     <p className="flex justify-between">
                         <span className="text-emerald-600 font-bold uppercase text-[10px]">Renovació</span>
                         <span className="font-black text-rose-500">{safeFormatDate(llicencia.data_renovacio)}</span>
                     </p>

                     {llicencia.pagaments?.length > 0 && (
                       <div className="mt-4 pt-4 border-t border-emerald-100">
                         <label className="text-[10px] font-black text-emerald-600 uppercase mb-2 block">Pagaments Recents</label>
                         <div className="space-y-2">
                           {llicencia.pagaments.map((p: any) => (
                             <div key={p.id} className="flex items-center justify-between bg-white/50 p-2 rounded-lg border border-emerald-100/50">
                               <div>
                                 <p className="text-[10px] font-black text-slate-700">{p.tipus.toUpperCase()}</p>
                                 <p className="text-[9px] font-bold text-slate-400">{safeFormatDate(p.data_emisio, "dd/MM/yy")} • {Number(p.import).toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })}</p>
                               </div>
                               <div className="flex items-center gap-2">
                                  <span className={`text-[8px] font-black px-1.5 py-0.5 rounded-md uppercase ${p.estat === 'pagat' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>
                                    {p.estat}
                                  </span>
                                  {p.estat !== 'pagat' && (
                                    <button 
                                      onClick={() => handleConfirmarPagament(p.id)}
                                      className="text-[10px] font-black text-blue-600 hover:underline px-1"
                                    >
                                      CONFIRMAR
                                    </button>
                                  )}
                               </div>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}
                 </div>
               ) : (
                 <div>
                   <p className="text-xs text-emerald-600 font-medium mb-4">Aquest deal està guanyat però encara no té llicència activa.</p>
                   <button onClick={handleCrearLlicencia} className="w-full bg-emerald-600 hover:bg-emerald-700 text-white py-3 rounded-xl font-bold text-sm transition-colors">
                     Activar Llicència Ara
                   </button>
                 </div>
               )}
            </section>
          )}

          <section>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                 ⚡ Timeline Universal
              </h3>
              <button 
                onClick={() => handleOpenComposer()}
                className="flex items-center space-x-1 px-3 py-1 bg-blue-500/10 hover:bg-blue-500/20 text-blue-600 rounded-lg text-[10px] font-black tracking-widest uppercase transition-colors"
              >
                <Mail className="w-3 h-3" />
                <span>Nou Email</span>
              </button>
            </div>
            
            {activitats.length === 0 ? (
              <p className="text-xs text-slate-400 italic bg-slate-50 p-4 rounded-xl border border-dashed border-slate-200">No hi ha activitat registrada encara.</p>
            ) : (
              <div className="space-y-4 relative before:absolute before:left-3 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-100">
                 {activitats.map(a => (
                    <div key={a.id} className="relative pl-8">
                       <div className={`absolute left-0 top-1 w-6 h-6 rounded-full border-2 border-white shadow-sm flex items-center justify-center text-[10px] z-10 ${
                         a.tipus_activitat === 'email_enviat' ? 'bg-blue-100 text-blue-600' :
                         a.tipus_activitat === 'email_rebut' ? 'bg-indigo-100 text-indigo-600' :
                         a.tipus_activitat === 'canvi_etapa' ? 'bg-purple-100 text-purple-600' :
                         'bg-slate-100 text-slate-600'
                       }`}>
                          {a.tipus_activitat === 'email_enviat' ? '📧' :
                           a.tipus_activitat === 'email_rebut' ? '📥' :
                           a.tipus_activitat === 'canvi_etapa' ? '⚙️' : '📝'}
                       </div>
                       
                       <div className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm hover:border-blue-100 transition-colors">
                          <div className="flex justify-between items-start mb-2">
                             <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                                {a.tipus_activitat.replace('_', ' ')}
                                {a.generat_per_ia && <span className="ml-2 text-blue-500">✨ IA-GEN</span>}
                             </span>
                             <span className="text-[10px] text-slate-400 font-bold">{safeFormatDate(a.data_activitat, "dd MMM, HH:mm")}</span>
                          </div>
                          
                          {/* Contingut específic basat en tipus */}
                          <div className="text-sm">
                             {a.tipus_activitat.includes('email') ? (
                                <>
                                   <p className="font-extrabold text-slate-800 mb-1">{a.contingut.assumpte}</p>
                                   <p className="text-slate-500 line-clamp-3 text-xs leading-relaxed italic">"{a.contingut.cos}"</p>
                                </>
                             ) : a.tipus_activitat === 'canvi_etapa' ? (
                                <p className="font-bold text-slate-700">
                                   Canvi d'etapa a <span className="text-purple-600 uppercase italic">{(a.contingut.etapa_nova || 'desconeguda').replace('_', ' ')}</span>
                                </p>
                             ) : (
                                <p className="text-slate-600">{a.notes_comercial}</p>
                             )}
                          </div>
                       </div>
                    </div>
                 ))}
              </div>
            )}
          </section>
        </div>

        {/* Footer d'accions del Drawer - RELATIU PER SEGURETAT */}
        <div className="p-6 bg-white/80 backdrop-blur-md border-t flex space-x-3 z-20 shrink-0">
          <button 
              onClick={handleDelete} 
              disabled={deleting}
              className="flex items-center space-x-2 px-6 h-14 bg-rose-50 hover:bg-rose-600 text-rose-600 hover:text-white rounded-2xl transition-all disabled:opacity-50 border border-rose-200 group"
              title="Eliminar aquest deal per sempre"
          >
              {deleting ? <Loader2 className="w-5 h-5 animate-spin" /> : <Trash2 className="w-5 h-5 group-hover:scale-110" />}
              <span className="text-xs font-black uppercase tracking-widest">Esborrar Deal</span>
          </button>
          <button 
              onClick={handleSaveAll} 
              disabled={saving}
              className="flex-1 h-14 bg-slate-900 hover:bg-black text-white rounded-2xl font-black shadow-xl transition-all flex items-center justify-center space-x-2"
          >
              {saving ? <Loader2 className="w-5 h-5 animate-spin" /> : (
                  <>
                      <Save className="w-4 h-4" />
                      <span>Guardar Canvis</span>
                  </>
              )}
          </button>
        </div>

        {/* Email Composer Modal */}
        {showEmailComposer && (
          <div className="fixed inset-0 z-[60] bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-6">
            <div className="bg-white w-full max-w-2xl rounded-3xl shadow-2xl overflow-hidden animate-in zoom-in duration-200 flex flex-col max-h-[90vh]">
              <div className="bg-slate-900 p-6 flex justify-between items-center">
                <div className="flex items-center space-x-2 text-white">
                  <Mail className="w-5 h-5 text-blue-400" />
                  <span className="font-black text-sm uppercase tracking-widest">Nou Missatge</span>
                </div>
                <button onClick={() => setShowEmailComposer(false)} className="text-slate-400 hover:text-white transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>
              
              <div className="p-8 space-y-4 overflow-y-auto">
                <div className="grid grid-cols-12 gap-4 items-center">
                   <label className="col-span-2 text-[10px] font-black text-slate-400 uppercase">Per a:</label>
                   <input 
                    value={composerData.to}
                    onChange={e => setComposerData({...composerData, to: e.target.value})}
                    className="col-span-10 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 font-bold text-slate-700 outline-none focus:border-blue-400"
                   />
                </div>
                <div className="grid grid-cols-12 gap-4 items-center">
                   <label className="col-span-2 text-[10px] font-black text-slate-400 uppercase">Assumpte:</label>
                   <input 
                    value={composerData.subject}
                    onChange={e => setComposerData({...composerData, subject: e.target.value})}
                    className="col-span-10 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 font-bold text-slate-700 outline-none focus:border-blue-400"
                   />
                </div>


                <textarea 
                  value={composerData.body}
                  onChange={e => setComposerData({...composerData, body: e.target.value})}
                  placeholder="Escriu el missatge aquí..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 font-medium text-slate-700 outline-none focus:border-blue-400 min-h-[200px]"
                />
              </div>

              <div className="p-6 bg-slate-50 border-t flex space-x-3">
                <button 
                  onClick={() => setShowEmailComposer(false)}
                  className="px-6 py-3 text-slate-500 font-bold text-sm hover:text-slate-700"
                >
                  Cancel·lar
                </button>
                <button 
                  onClick={handleSendEmail}
                  disabled={sendingEmail || !composerData.to || !composerData.subject || !composerData.body}
                  className="flex-1 bg-slate-900 hover:bg-slate-800 text-white rounded-xl font-black text-sm transition-all disabled:opacity-50 flex items-center justify-center space-x-2 shadow-lg"
                >
                  {sendingEmail ? <Loader2 className="w-4 h-4 animate-spin" /> : <Mail className="w-4 h-4" />}
                  <span>Enviar Email ara</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
