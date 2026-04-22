"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/lib/api";
import { 
    X, Mail, CreditCard, Trash2, Save, Euro, Building2, User, Loader2, 
    History, ArrowLeft, Calendar
} from "lucide-react";
import { format } from "date-fns";
import { EmailComposer } from "@/components/EmailComposer";
import { Button } from "@/components/ui/button";

export default function MunicipiDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  // Editable fields (Copy from DealDrawer)
  const [nom, setNom] = useState("");
  const [valorSetup, setValorSetup] = useState("0");
  const [valorLlicencia, setValorLlicencia] = useState("0");
  const [prioritat, setPrioritat] = useState("mitjana");
  const [properPas, setProperPas] = useState("");
  const [dataSeguiment, setDataSeguiment] = useState("");
  const [notesHumanes, setNotesHumanes] = useState("");
  
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [activitats, setActivitats] = useState<any[]>([]);
  const [llicencia, setLlicencia] = useState<any>(null);

  // Email states
  const [isComposerOpen, setIsComposerOpen] = useState(false);
  const [composerConfig, setComposerConfig] = useState({ to: "", subject: "", contacteId: "" });

  useEffect(() => {
    if (id) {
      fetchData();
    }
  }, [id]);

  const fetchData = async () => {
    try {
      const res = await api.municipis.detall(id as string);
      setData(res);
      
      // Initialize editable fields
      setNom(res.nom || "");
      setValorSetup(res.valor_setup?.toString() || "0");
      setValorLlicencia(res.valor_llicencia?.toString() || "0");
      setPrioritat(res.prioritat || "mitjana");
      setProperPas(res.proper_pas || "");
      setDataSeguiment(res.data_seguiment ? new Date(res.data_seguiment).toISOString().split('T')[0] : "");
      setNotesHumanes(res.notes_humanes || "");

      // Fetch related data
      const [activities, llicenciaRes] = await Promise.all([
        api.municipis.get_activitats(id as string),
        api.municipis.get_llicencia(id as string)
      ]);
      setActivitats(Array.isArray(activities) ? activities : (activities.items || []));
      setLlicencia(llicenciaRes);

    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveAll = async () => {
    setSaving(true);
    try {
      await api.municipis.editar(id as string, {
        nom,
        valor_setup: parseFloat(valorSetup),
        valor_llicencia: parseFloat(valorLlicencia),
        prioritat,
        proper_pas: properPas || null,
        data_seguiment: dataSeguiment || null,
        notes_humanes: notesHumanes
      });
      alert("Municipi actualitzat correctament.");
      fetchData();
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
      await api.municipis.eliminar(id as string);
      router.push("/pipeline");
    } catch (e: any) {
      alert(`Error al eliminar: ${e.message}`);
    } finally {
      setDeleting(false);
    }
  };

  const handleOpenComposer = (to = data?.actor_principal?.email || "", subject = `Seguiment PXX — ${data?.nom || 'Ajuntament'}`) => {
    setComposerConfig({ to, subject, contacteId: data?.actor_principal_id || "" });
    setIsComposerOpen(true);
  };

  if (loading) return (
    <div className="p-20 flex flex-col items-center justify-center space-y-4">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-400 font-bold uppercase tracking-widest text-xs">Carregant dades del municipi...</p>
    </div>
  );
  
  if (!data) return (
    <div className="p-20 text-center">
        <div className="text-6xl mb-4">📍</div>
        <h2 className="text-2xl font-black text-slate-800">Municipi no trobat</h2>
        <p className="text-slate-500 mt-2">No hem pogut trobar la fitxa que busques.</p>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Header - Aligned with DealDrawer style but as absolute top */}
      <div className="bg-[#0f172a] text-white p-10 rounded-3xl shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl -mr-48 -mt-48" />
        
        <div className="flex flex-col md:flex-row justify-between items-start relative z-10">
          <div className="flex items-center space-x-6">
            <div className="w-20 h-20 bg-blue-500/20 rounded-2x flex items-center justify-center border border-blue-500/30">
                <Building2 className="w-10 h-10 text-blue-400" />
            </div>
            <div>
              <div className="flex items-center space-x-3 mb-2">
                <span className="px-3 py-1 bg-blue-500/20 text-blue-300 text-[10px] font-black uppercase tracking-widest rounded-full border border-blue-500/30">
                    {data.tipus}
                </span>
                <span className="text-slate-500 font-bold">•</span>
                <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">{data.provincia}</span>
              </div>
              <h1 className="text-5xl font-black tracking-tighter mb-2">{nom}</h1>
              <p className="text-slate-400 font-bold uppercase tracking-[0.2em] text-[10px]">{data.comarca} • {data.poblacio?.toLocaleString() || '0'} HAB.</p>
            </div>
          </div>
          
          <div className="mt-8 md:mt-0 grid grid-cols-3 gap-3">
             <div className="bg-white/5 rounded-2xl p-4 border border-white/10 flex flex-col items-center min-w-[120px]">
                <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Temperatura</span>
                <span className="text-sm font-bold mt-1">
                  {data.temperatura === 'fred' ? '🧊 Fred' : 
                   data.temperatura === 'templat' ? '⚡ Templat' : 
                   data.temperatura === 'calent' ? '🔥 Calent' : '☀️ Bullent'}
                </span>
             </div>
             <div className="bg-white/5 rounded-2xl p-4 border border-white/10 flex flex-col items-center min-w-[120px]">
                <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Etapa</span>
                <span className="text-sm font-bold mt-1 text-blue-400 uppercase">
                  {data.etapa_actual?.replace('_', ' ')}
                </span>
             </div>
             <div className="bg-white/5 rounded-2xl p-4 border border-white/10 flex flex-col items-center min-w-[120px]">
                <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Prioritat</span>
                <span className={`text-sm font-bold mt-1 uppercase ${data.prioritat === 'alta' ? 'text-rose-400' : 'text-slate-300'}`}>
                  {data.prioritat || 'MITJANA'}
                </span>
             </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Data and History */}
        <div className="lg:col-span-7 space-y-8">
          
          {/* Economic Section */}
          <div className="glass-card p-8 border-white/60 bg-blue-50/30">
             <h3 className="text-xs font-black text-blue-600 uppercase tracking-widest mb-6 flex items-center">
                <Euro className="w-4 h-4 mr-2" /> Valors de l'Acord (PXX)
             </h3>
             <div className="grid grid-cols-2 gap-8">
                <div>
                    <label className="block text-[10px] font-extrabold text-blue-400 uppercase mb-2">Set Up (€)</label>
                    <input 
                        type="number"
                        value={valorSetup} 
                        onChange={e => setValorSetup(e.target.value)}
                        className="w-full bg-white border border-blue-100 rounded-2xl px-6 py-4 font-black text-slate-800 outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-400 text-xl transition-all"
                    />
                </div>
                <div>
                    <label className="block text-[10px] font-extrabold text-blue-400 uppercase mb-2">Manteniment (€)</label>
                    <input 
                        type="number"
                        value={valorLlicencia} 
                        onChange={e => setValorLlicencia(e.target.value)}
                        className="w-full bg-white border border-blue-100 rounded-2xl px-6 py-4 font-black text-slate-800 outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-400 text-xl transition-all"
                    />
                </div>
                <div className="col-span-2 flex justify-between items-center pt-6 border-t border-blue-100/50">
                    <span className="text-xs font-black text-blue-400 uppercase tracking-widest">Total Pipeline Projectat</span>
                    <span className="text-3xl font-black text-blue-700 tracking-tighter">
                        {(Number(valorSetup) + Number(valorLlicencia)).toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })}
                    </span>
                </div>
             </div>
          </div>

          {/* Activity Timeline */}
          <div className="glass-card p-10 border-white/60">
              <div className="flex justify-between items-center mb-8">
                <h3 className="text-2xl font-black text-slate-800 tracking-tighter flex items-center">
                    <History className="w-6 h-6 mr-3 text-slate-400" />
                    Timeline Universal
                </h3>
                <Button 
                    onClick={() => handleOpenComposer()}
                    className="bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold flex items-center space-x-2"
                >
                    <Mail className="w-4 h-4" />
                    <span>Nou Email</span>
                </Button>
              </div>
              
              {activitats.length > 0 ? (
                <div className="space-y-6 relative before:absolute before:left-4 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-100">
                    {activitats.map((a, i) => (
                        <div key={a.id} className="relative pl-12">
                            <div className={`absolute left-0 top-1 w-8 h-8 rounded-full border-4 border-white shadow-sm flex items-center justify-center text-xs z-10 ${
                                a.tipus_activitat === 'email_enviat' ? 'bg-blue-500 text-white' :
                                a.tipus_activitat === 'email_rebut' ? 'bg-indigo-500 text-white' :
                                a.tipus_activitat === 'canvi_etapa' ? 'bg-purple-500 text-white' :
                                'bg-slate-400 text-white'
                            }`}>
                                {a.tipus_activitat === 'email_enviat' ? '📧' :
                                 a.tipus_activitat === 'email_rebut' ? '📥' :
                                 a.tipus_activitat === 'canvi_etapa' ? '⚙️' : '📝'}
                            </div>
                            <div className="bg-white p-6 rounded-2xl border border-slate-100 hover:border-blue-100 transition-colors shadow-sm">
                                <div className="flex justify-between items-start mb-2">
                                    <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                                        {a.tipus_activitat?.replace('_', ' ')}
                                        {a.generat_per_ia && <span className="ml-2 text-blue-500">IA</span>}
                                    </span>
                                    <span className="text-[10px] font-bold text-slate-300">{format(new Date(a.data_activitat), "dd/MM/yyyy HH:mm")}</span>
                                </div>
                                <div className="text-slate-700 text-sm font-medium leading-relaxed">
                                    {a.tipus_activitat?.includes('email') ? (
                                        <>
                                            <p className="font-black text-slate-900 mb-1">{a.contingut?.assumpte}</p>
                                            <p className="text-slate-500 line-clamp-3 italic">"{a.contingut?.cos || a.notes_comercial}"</p>
                                        </>
                                    ) : (
                                        <p>{a.notes_comercial}</p>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
              ) : (
                <div className="py-12 bg-slate-50/50 rounded-3xl border border-dashed border-slate-200 text-center">
                    <p className="text-slate-400 font-bold italic text-sm">No s'ha registrat cap activitat encara.</p>
                </div>
              )}
          </div>
        </div>

        {/* Right Column: Settings and Controls */}
        <div className="lg:col-span-5 space-y-8">
            
            {/* Proper Pas i Agenda */}
            <div className="glass-card p-8 border-white/60">
                <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest mb-6 flex items-center">
                    <Calendar className="w-4 h-4 mr-2" /> Proper Pas de Seguiment
                </h3>
                <div className="space-y-4">
                    <input 
                        type="text"
                        value={properPas}
                        onChange={e => setProperPas(e.target.value)}
                        placeholder="Què cal fer a continuació?"
                        className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-6 py-4 font-bold text-slate-800 outline-none focus:border-blue-400"
                    />
                    <input 
                        type="date"
                        value={dataSeguiment}
                        onChange={e => setDataSeguiment(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-6 py-4 font-bold text-slate-800 outline-none focus:border-blue-400"
                    />
                </div>
            </div>

            {/* Notes Section */}
            <div className="glass-card p-8 border-white/60 flex flex-col">
                <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest mb-6">Diari d'Abord / Notes</h3>
                <textarea 
                    value={notesHumanes}
                    onChange={e => setNotesHumanes(e.target.value)}
                    placeholder="Detalls de la negociació, contactes clau, pors del client..."
                    className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-6 py-4 font-medium text-slate-700 outline-none focus:border-blue-400 min-h-[150px] flex-1"
                />
            </div>

            {/* License management (if applicable) */}
            {data.etapa_actual === 'client' && (
                <div className="glass-card p-8 border-white/60 bg-emerald-50/30 border-emerald-100">
                    <h3 className="text-xs font-black text-emerald-600 uppercase tracking-widest mb-6 flex items-center">
                        <CreditCard className="w-4 h-4 mr-2" /> Gestió de Llicència Activa
                    </h3>
                    {llicencia ? (
                        <div className="space-y-4">
                            <div className="flex justify-between items-center">
                                <span className="text-xs font-bold text-slate-400 uppercase">Estat</span>
                                <span className="px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full font-black text-[10px] uppercase">{llicencia.estat}</span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-xs font-bold text-slate-400 uppercase">Renovació</span>
                                <span className="font-black text-rose-500">{format(new Date(llicencia.data_renovacio), "dd/MM/yyyy")}</span>
                            </div>
                        </div>
                    ) : (
                        <p className="text-sm text-slate-500 italic">No s'ha detectat cap llicència activa vinculada.</p>
                    )}
                </div>
            )}

            {/* Global Actions - Identical to Footer of Drawer */}
            <div className="flex flex-col space-y-4 pt-4">
                <Button 
                    onClick={handleSaveAll}
                    disabled={saving}
                    className="w-full h-16 bg-slate-900 hover:bg-black text-white rounded-2xl font-black text-lg shadow-xl"
                >
                    {saving ? <Loader2 className="w-6 h-6 animate-spin" /> : (
                        <>
                            <Save className="w-5 h-5 mr-3" />
                            <span>GUARDAR TOTA LA FITXA</span>
                        </>
                    )}
                </Button>
                <button 
                    onClick={handleDelete}
                    disabled={deleting}
                    className="w-full py-4 text-rose-600 hover:text-white hover:bg-rose-600 border border-rose-200 rounded-2xl font-black text-[10px] uppercase tracking-[0.3em] transition-all"
                >
                    {deleting ? 'Eliminant...' : 'Esborrar Municipi Definitivament'}
                </button>
            </div>
        </div>
      </div>

    {isComposerOpen && (
      <EmailComposer 
        onClose={() => {
            setIsComposerOpen(false);
            fetchData();
        }}
        initialTo={composerConfig.to}
        initialSubject={composerConfig.subject}
        municipiId={id as string}
        onSent={() => alert("Email enviat manualment")}
      />
    )}
    </div>
  );
}
