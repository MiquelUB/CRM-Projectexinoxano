"use client";
import React, { useEffect, useState, useRef } from "react";
import { Mail, Phone, Users, FileText, ChevronDown, Calendar, Search, Loader2 } from "lucide-react";
import { ActivitatDetallModal } from "./ActivitatDetallModal";

export function ActivitatTimeline({ municipiId, refreshKey }: { municipiId: string, refreshKey: number }) {
    const [activitats, setActivitats] = useState<any[]>([]);
    const [page, setPage] = useState(1);
    const [loading, setLoading] = useState(true);
    const loadingRef = useRef(false);
    const [hasMore, setHasMore] = useState(true);
    const [filters, setFilters] = useState<string[]>(['email_enviat', 'email_rebut', 'trucada', 'reunio', 'nota_manual', 'sistema']);
    const [searchTerm, setSearchTerm] = useState("");
    
    const [selectedAct, setSelectedAct] = useState<any>(null);

    const filterTypes = [
        { id: 'email_enviat', label: 'Emails' }, // inclou rebut i enviat
        { id: 'trucada', label: 'Trucades' },
        { id: 'reunio', label: 'Reunions' },
        { id: 'nota_manual', label: 'Notes' },
    ];

    const loadActivitats = async (p: number, reset: boolean = false) => {
        setLoading(true);
        loadingRef.current = true;
        try {
            const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
            const token = sessionStorage.getItem("token") || "";
            const params = new URLSearchParams({ limit: "50", offset: ((p - 1) * 50).toString() });
            
            filters.forEach(f => {
                params.append('tipus', f);
                if(f === 'email_enviat') params.append('tipus', 'email_rebut');
            });
            
            const res = await fetch(`${BASE_URL}/api/v2/municipis/${municipiId}/timeline?${params.toString()}`, {
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                if (reset) setActivitats(data.timeline || []);
                else setActivitats(prev => [...prev, ...(data.timeline || [])]);
                
                if (data.timeline?.length < 50) setHasMore(false);
                else setHasMore(true);
            }
        } catch(e) {
            console.error(e);
        } finally {
            setLoading(false);
            loadingRef.current = false;
        }
    };

    useEffect(() => {
        setPage(1);
        loadActivitats(1, true);
    }, [municipiId, refreshKey, filters]);

    const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
        const { scrollTop, scrollHeight, clientHeight } = e.currentTarget;
        if (scrollHeight - scrollTop <= clientHeight * 1.5 && !loadingRef.current && hasMore) {
            setPage(p => p + 1);
            loadActivitats(page + 1);
        }
    };

    const getIcon = (type: string) => {
        if (type.includes("email")) return <Mail className="w-4 h-4 text-white" />;
        if (type === "trucada") return <Phone className="w-4 h-4 text-white" />;
        if (type === "reunio") return <Users className="w-4 h-4 text-white" />;
        if (type === "nota_manual") return <FileText className="w-4 h-4 text-white" />;
        return <Calendar className="w-4 h-4 text-white" />;
    };

    const getIconColor = (type: string) => {
        if (type.includes("email")) return "bg-blue-500";
        if (type === "trucada") return "bg-emerald-500";
        if (type === "reunio") return "bg-purple-500";
        if (type === "nota_manual") return "bg-yellow-500";
        return "bg-slate-400";
    };

    const filteredActivitats = activitats.filter(a => {
        if (!searchTerm) return true;
        const search = searchTerm.toLowerCase();
        const contentStr = JSON.stringify(a.contingut || {}).toLowerCase();
        const notesStr = (a.notes_comercial || "").toLowerCase();
        return contentStr.includes(search) || notesStr.includes(search);
    });

    return (
        <div className="bg-white rounded-2xl shadow-xl border border-slate-200 flex flex-col h-full overflow-hidden w-full max-w-full relative">
            <div className="p-5 border-b border-slate-100 bg-slate-50 flex flex-col space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <h2 className="text-lg font-black text-slate-800 tracking-tight flex items-center">
                        <span className="w-2 h-2 rounded-full bg-blue-600 mr-2"></span>
                        Timeline d'Activitats
                    </h2>
                    <div className="relative flex-1 max-w-xs">
                        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                        <input 
                            type="text" 
                            placeholder="Cerca anotacions..." 
                            value={searchTerm}
                            onChange={e => setSearchTerm(e.target.value)}
                            className="w-full bg-white border border-slate-200 rounded-full pl-9 pr-4 py-2 text-xs font-bold focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all shadow-sm"
                        />
                    </div>
                </div>
                <div className="flex flex-wrap gap-2">
                    {filterTypes.map(f => (
                        <label key={f.id} className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-full text-xs font-bold cursor-pointer transition-all active:scale-95 ${
                            filters.includes(f.id) ? "bg-slate-800 text-white shadow-sm" : "bg-white text-slate-500 border border-slate-200 hover:bg-slate-50"
                        }`}>
                            <input 
                                type="checkbox" 
                                className="hidden" 
                                checked={filters.includes(f.id)} 
                                onChange={(e) => {
                                    if (e.target.checked) setFilters([...filters, f.id]);
                                    else setFilters(filters.filter(x => x !== f.id));
                                }}
                            />
                            {filters.includes(f.id) && <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>}
                            <span>{f.label}</span>
                        </label>
                    ))}
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-5 relative bg-slate-50/50" onScroll={handleScroll}>
                <div className="absolute left-9 top-0 bottom-0 w-0.5 bg-slate-200 z-0"></div>
                
                {filteredActivitats.map((act, idx) => (
                    <div key={act.id || idx} className="relative z-10 flex items-start space-x-4 mb-6 group">
                        <div className={`mt-1.5 flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center shadow-lg border-2 border-white ring-4 ring-slate-50 ${getIconColor(act.tipus_activitat)} group-hover:scale-110 transition-transform`}>
                            {getIcon(act.tipus_activitat)}
                        </div>
                        <div className="flex-1 bg-white rounded-2xl border border-slate-200/80 p-4 shadow-sm hover:shadow-md transition-shadow group-hover:border-blue-100">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-[10px] font-black text-slate-700 bg-slate-100 px-2 py-0.5 rounded-md uppercase tracking-wider">
                                    {act.actor?.substring(0, 30)}{act.actor?.length > 30 ? "..." : ""}
                                </span>
                                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest bg-slate-50 px-2 py-0.5 rounded border border-slate-100">
                                    {new Date(act.data_activitat).toLocaleString(undefined, {
                                        month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit'
                                    })}
                                </span>
                            </div>
                            <div className="mb-3 text-sm font-medium text-slate-600 line-clamp-3">
                                {act.notes_comercial ? act.notes_comercial :
                                    act.tipus_activitat.includes('email') ? (act.contingut?.subject || '📨 Sense assumpte específic') : 
                                    (act.tipus_activitat === 'trucada' ? `📞 Trucada de ${act.contingut?.duracio_minuts || 0} minuts` : 
                                    "✨ Registre del sistema")}
                            </div>
                            <button onClick={() => setSelectedAct(act)} className="text-[11px] font-black uppercase text-blue-600 hover:text-blue-800 flex items-center space-x-1 group-hover:underline decoration-blue-200 underline-offset-4 transition-all">
                                <span>Veure més detalls</span>
                                <ChevronDown className="w-3 h-3 group-hover:translate-y-0.5 transition-transform" />
                            </button>
                        </div>
                    </div>
                ))}
                
                {loading && (
                    <div className="flex justify-center p-6">
                        <Loader2 className="w-6 h-6 animate-spin text-slate-400" />
                    </div>
                )}
                {!loading && filteredActivitats.length === 0 && (
                    <div className="flex flex-col items-center justify-center py-12 text-slate-400 space-y-3">
                        <Search className="w-8 h-8 opacity-20" />
                        <p className="text-sm font-bold opacity-50">Cap activitat trobada.</p>
                    </div>
                )}
            </div>

            {selectedAct && <ActivitatDetallModal activitat={selectedAct} onClose={() => setSelectedAct(null)} />}
        </div>
    );
}
