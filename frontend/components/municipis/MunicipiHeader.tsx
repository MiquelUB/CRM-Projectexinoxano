"use client";
import { useState } from "react";
import { Users, CreditCard, Edit, MapPin } from "lucide-react";
import { EditarMunicipiModal } from "./EditarMunicipiModal";

export function MunicipiHeader({ municipi, onUpdated }: { municipi: any, onUpdated?: () => void }) {
    const [isEditing, setIsEditing] = useState(false);

    if (!municipi) return null;

    const temperatureIcons = {
        "fred": "❄️",
        "templat": "🌤️",
        "calent": "🔥"
    } as any;
    
    const etapaColors = {
        "research": "bg-slate-100 text-slate-700",
        "contacte": "bg-blue-100 text-blue-700",
        "demo_pendent": "bg-yellow-100 text-yellow-700",
        "demo_ok": "bg-emerald-100 text-emerald-700",
        "oferta": "bg-purple-100 text-purple-700",
        "documentacio": "bg-indigo-100 text-indigo-700",
        "aprovacio": "bg-orange-100 text-orange-700",
        "contracte": "bg-green-100 text-green-700",
        "client": "bg-teal-100 text-teal-700",
        "pausa": "bg-red-100 text-red-700",
        "perdut": "bg-gray-200 text-gray-800"
    } as any;

    return (
        <div className="bg-white rounded-2xl shadow border border-slate-200 p-6 flex flex-col md:flex-row justify-between items-start md:items-center relative z-10">
            <div className="flex flex-col space-y-2">
                <div className="flex items-center space-x-3">
                    <h1 className="text-2xl font-black tracking-tight text-slate-800">{municipi.nom}</h1>
                    <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${etapaColors[municipi.etapa_actual] || "bg-slate-100 text-slate-700"}`}>
                        {municipi.etapa_actual?.toUpperCase() || "SENSE ETAPA"}
                    </span>
                    <span className="text-xl inline-block" title={`Temperatura: ${municipi.temperatura || 'No'}`}>
                        {temperatureIcons[municipi.temperatura] || "❓"}
                    </span>
                </div>
                <div className="flex items-center space-x-4 text-sm text-slate-500 font-medium tracking-tight">
                    <span className="flex items-center space-x-1">
                        <Users className="w-4 h-4 text-slate-400" />
                        <span>{municipi.poblacio?.toLocaleString() || "---"} Hab.</span>
                    </span>
                    <span className="flex items-center space-x-1">
                        <MapPin className="w-4 h-4 text-slate-400" />
                        <span>Geografia: {municipi.geografia || "No definida"}</span>
                    </span>
                </div>
                <div className="flex items-center space-x-2 pt-1">
                    {municipi.plans_contractats?.map((p: string) => (
                        <span key={p} className="bg-indigo-50 border border-indigo-100 text-indigo-700 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">
                            {p}
                        </span>
                    ))}
                    {municipi.estat_pagament && (
                        <span className="bg-green-50 border border-green-200 text-green-700 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider flex items-center space-x-1">
                            <CreditCard className="w-3 h-3" />
                            <span>Pagament: {municipi.estat_pagament}</span>
                        </span>
                    )}
                </div>
            </div>
            
            <div className="mt-4 md:mt-0">
                <button onClick={() => setIsEditing(true)} className="flex items-center justify-center space-x-2 bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-sm font-bold transition-all">
                    <Edit className="w-4 h-4" />
                    <span>Editar municipi</span>
                </button>
            </div>

            {isEditing && (
                <EditarMunicipiModal 
                    municipi={municipi} 
                    onClose={() => setIsEditing(false)} 
                    onUpdated={() => {
                        setIsEditing(false);
                        if (onUpdated) onUpdated();
                    }} 
                />
            )}
        </div>
    );
}
