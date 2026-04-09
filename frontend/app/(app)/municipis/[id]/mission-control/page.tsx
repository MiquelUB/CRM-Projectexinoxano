"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ChevronRight, Home, Loader2, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { MunicipiHeader } from "@/components/municipis/MunicipiHeader";
import { KimiRecommendation } from "@/components/municipis/KimiRecommendation";
import { ActivitatTimeline } from "@/components/municipis/ActivitatTimeline";

export default function MissionControlPage() {
    const params = useParams();
    const router = useRouter();
    const municipiId = params?.id as string;
    
    const [municipi, setMunicipi] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [refreshKey, setRefreshKey] = useState(0);

    const fetchMunicipiData = async () => {
        try {
            const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
            const token = sessionStorage.getItem("token") || "";
            const res = await fetch(`${BASE_URL}/municipis_lifecycle/${municipiId}`, {
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setMunicipi(data);
            }
        } catch (e) {
            console.error("Error al carregar municipi", e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (municipiId) {
            fetchMunicipiData();
        }
    }, [municipiId, refreshKey]);

    const handleActionComplete = () => {
        // Incrementar la clau per forçar la recàrrega de dades i timeline
        setRefreshKey(prev => prev + 1);
    };

    if (loading) {
        return (
            <div className="flex-1 flex items-center justify-center min-h-screen bg-slate-50">
                <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
            </div>
        );
    }

    if (!municipi) {
        return (
            <div className="flex-1 p-8 text-center bg-slate-50 min-h-screen">
                <h1 className="text-2xl font-bold text-slate-700">Municipi no trobat</h1>
                <button onClick={() => router.back()} className="mt-4 text-blue-500 underline text-sm">Tornar</button>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto bg-slate-50 min-h-screen">
            {/* Suposem un header de layout genèric però afegim breadcrumbs propis */}
            <div className="bg-white border-b border-slate-200 px-4 sm:px-8 py-4 sticky top-0 z-40 shadow-sm flex items-center space-x-2">
                <button onClick={() => router.push('/municipis')} className="p-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors text-slate-500" aria-label="Tornar a municipis">
                    <ArrowLeft className="w-4 h-4" />
                </button>
                <div className="h-4 w-px bg-slate-300 mx-1 sm:mx-2"></div>
                <div className="flex items-center space-x-1 sm:space-x-2 text-[10px] sm:text-xs font-bold text-slate-500 uppercase tracking-wider overflow-x-auto hide-scrollbar whitespace-nowrap">
                    <Link href="/dashboard" className="hover:text-slate-800 flex items-center space-x-1" aria-label="Anar al Dashboard">
                        <Home className="w-3.5 h-3.5" /> <span className="hidden sm:inline">Dashboard</span>
                    </Link>
                    <ChevronRight className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
                    <Link href="/municipis" className="hover:text-slate-800">Municipis</Link>
                    <ChevronRight className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
                    <span className="text-blue-600 truncate max-w-[100px] sm:max-w-xs">{municipi.nom}</span>
                    <ChevronRight className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
                    <span className="text-slate-800 bg-slate-200 px-2 py-0.5 rounded-md">Mission Control</span>
                </div>
            </div>

            <div className="p-4 sm:p-8 max-w-7xl mx-auto space-y-6">
                
                {/* Header (Top) */}
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <MunicipiHeader municipi={municipi} onUpdated={fetchMunicipiData} />
                </div>

                {/* Grid Layout: Lateral (Recomanació) + Central (Timeline) */}
                <div className="flex flex-col lg:grid lg:grid-cols-3 gap-6 lg:h-[calc(100vh-280px)] min-h-[600px] animate-in fade-in slide-in-from-bottom-8 duration-700">
                    
                    {/* Columna Esquerra: Kimi K2 */}
                    <div className="lg:col-span-1 h-auto lg:h-full">
                        <KimiRecommendation 
                            municipiId={municipiId} 
                            onActionComplete={handleActionComplete} 
                        />
                    </div>

                    {/* Columna Dreta: Timeline */}
                    <div className="lg:col-span-2 h-[500px] lg:h-full" role="region" aria-label="Timeline d'activitats">
                        <ActivitatTimeline 
                            municipiId={municipiId} 
                            refreshKey={refreshKey} 
                        />
                    </div>

                </div>

            </div>
        </div>
    );
}
