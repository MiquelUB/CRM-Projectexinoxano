"use client";

import React, { useState, useEffect } from "react";
import { 
  Phone, 
  Mail, 
  Users, 
  StickyNote, 
  CheckCircle2, 
  Clock, 
  Loader2,
  ChevronRight,
  TrendingUp,
  Brain
} from "lucide-react";
import { format } from "date-fns";
import { ca } from "date-fns/locale";
import api from "@/lib/api";

interface ActivitatTimelineProps {
    municipiId: string;
    refreshKey?: number;
}

const ICON_MAP: Record<string, any> = {
    trucada: Phone,
    trucada_programada: Phone,
    email_enviat: Mail,
    email_rebut: Mail,
    reunio: Users,
    nota_manual: StickyNote,
    pagament: TrendingUp,
    canvi_etapa: ChevronRight,
    seguiment: Clock,
    sistema: CheckCircle2
};

const COLOR_MAP: Record<string, string> = {
    trucada: "bg-blue-100 text-blue-600",
    trucada_programada: "bg-emerald-100 text-emerald-600",
    email_enviat: "bg-indigo-100 text-indigo-600",
    email_rebut: "bg-purple-100 text-purple-600",
    reunio: "bg-amber-100 text-amber-600",
    nota_manual: "bg-slate-100 text-slate-600",
    pagament: "bg-emerald-100 text-emerald-600",
    canvi_etapa: "bg-rose-100 text-rose-600",
    seguiment: "bg-cyan-100 text-cyan-600",
    sistema: "bg-slate-50 text-slate-400"
};

export function ActivitatTimeline({ municipiId, refreshKey }: ActivitatTimelineProps) {
    const [activitats, setActivitats] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    const fetchActivitats = async () => {
        try {
            const res = await api.municipis.get_activitats(municipiId);
            setActivitats(res);
        } catch (err) {
            console.error("Error fetching activitats:", err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchActivitats();
    }, [municipiId, refreshKey]);

    if (isLoading) {
        return (
            <div className="flex justify-center p-12">
                <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
            </div>
        );
    }

    if (activitats.length === 0) {
        return (
            <div className="text-center py-20 bg-slate-50 rounded-3xl border-2 border-dashed border-slate-200">
                <Clock className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                <h3 className="text-lg font-bold text-slate-800">Sense activitat encara</h3>
                <p className="text-sm text-slate-500">Registra la primera acció per començar el timeline.</p>
            </div>
        );
    }

    return (
        <div className="relative space-y-8 pl-8 before:absolute before:left-3.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-100">
            {activitats.map((act, idx) => {
                const Icon = ICON_MAP[act.tipus_activitat] || StickyNote;
                const colors = COLOR_MAP[act.tipus_activitat] || "bg-slate-100 text-slate-600";

                return (
                    <div key={act.id || idx} className="relative group">
                        {/* Dot */}
                        <div className={`absolute -left-[32px] w-7 h-7 rounded-full border-4 border-white shadow-sm flex items-center justify-center z-10 transition-transform group-hover:scale-110 ${colors}`}>
                            <Icon className="w-3.5 h-3.5" />
                        </div>

                        {/* Content */}
                        <div className="bg-white rounded-2xl p-5 border border-slate-100 shadow-sm transition-all hover:shadow-md hover:border-blue-100">
                            <div className="flex justify-between items-start mb-3">
                                <div>
                                    <div className="flex items-center gap-2 mb-1">
                                        <h4 className="text-sm font-black text-slate-800 uppercase tracking-tight">
                                            {act.tipus_activitat.replace('_', ' ')}
                                        </h4>
                                    </div>
                                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                                        {format(new Date(act.data_activitat), "PPP 'a les' HH:mm", { locale: ca })}
                                    </p>
                                </div>
                                <div className="text-[10px] font-black text-slate-300 uppercase tracking-widest">
                                    #{activitats.length - idx}
                                </div>
                            </div>
                            
                            <div className="text-sm text-slate-600 leading-relaxed">
                                {act.notes_comercial}
                            </div>

                            {act.etiquetes && act.etiquetes.length > 0 && (
                                <div className="mt-4 flex flex-wrap gap-2">
                                    {act.etiquetes.map((tag: string, i: number) => (
                                        <span key={i} className="px-2 py-0.5 bg-slate-50 text-slate-400 text-[9px] font-bold uppercase tracking-widest rounded-md border border-slate-100">
                                            {tag}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
