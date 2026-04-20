"use client";

import { Building2, MapPin, Users, ThermometerSun, Calendar, Edit3 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface MunicipiHeaderProps {
    municipi: any;
    onUpdated?: () => void;
}

export function MunicipiHeader({ municipi, onUpdated }: MunicipiHeaderProps) {
    if (!municipi) return null;

    return (
        <div className="bg-[#0f172a] text-white p-8 rounded-3xl shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl -mr-48 -mt-48" />
            
            <div className="flex flex-col md:flex-row justify-between items-start relative z-10 gap-6">
                <div className="flex items-center space-x-6">
                    <div className="w-20 h-20 bg-blue-500/20 rounded-2xl flex items-center justify-center border border-blue-500/30">
                        <Building2 className="w-10 h-10 text-blue-400" />
                    </div>
                    <div>
                        <div className="flex items-center space-x-3 mb-2">
                            <span className="px-3 py-1 bg-blue-500/20 text-blue-300 text-[10px] font-black uppercase tracking-widest rounded-full border border-blue-500/30">
                                {municipi.tipus || 'AJUNTAMENT'}
                            </span>
                            <span className="text-slate-500 font-bold">•</span>
                            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">{municipi.provincia}</span>
                        </div>
                        <h1 className="text-4xl sm:text-5xl font-black tracking-tighter mb-2">{municipi.nom}</h1>
                        <div className="flex flex-wrap items-center gap-4 text-slate-400 text-[10px] font-bold uppercase tracking-wider">
                            <span className="flex items-center gap-1.5">
                                <MapPin className="w-3 h-3" /> {municipi.comarca}
                            </span>
                            <span className="flex items-center gap-1.5">
                                <Users className="w-3 h-3" /> {municipi.poblacio?.toLocaleString() || '0'} HAB.
                            </span>
                             <span className="flex items-center gap-1.5">
                                <Calendar className="w-3 h-3" /> CREAT: {new Date(municipi.created_at).toLocaleDateString()}
                            </span>
                        </div>
                    </div>
                </div>
                
                <div className="flex flex-wrap items-center gap-3">
                    <div className="bg-white/5 rounded-2xl p-4 border border-white/10 flex flex-col items-center min-w-[100px]">
                        <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Estat</span>
                        <span className="text-sm font-bold text-blue-400 uppercase">
                            {municipi.etapa_actual?.replace('_', ' ')}
                        </span>
                    </div>
                    <div className="bg-white/5 rounded-2xl p-4 border border-white/10 flex flex-col items-center min-w-[100px]">
                        <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Temperatura</span>
                        <div className="flex items-center gap-1.5">
                            <ThermometerSun className={`w-3.5 h-3.5 ${
                                municipi.temperatura === 'fred' ? 'text-blue-400' :
                                municipi.temperatura === 'templat' ? 'text-amber-400' :
                                'text-rose-400'
                            }`} />
                            <span className="text-sm font-bold">
                                {municipi.temperatura?.toUpperCase()}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
