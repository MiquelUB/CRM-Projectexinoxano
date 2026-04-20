"use client";

import React, { useState, useEffect } from "react";
import { Sparkles, Brain, ArrowRight, Loader2, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";

interface KimiRecommendationProps {
    municipiId: string;
    onActionComplete?: () => void;
}

export function KimiRecommendation({ municipiId, onActionComplete }: KimiRecommendationProps) {
    const [recommendation, setRecommendation] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isRefreshing, setIsRefreshing] = useState(false);

    const fetchRecommendation = async () => {
        try {
            setIsRefreshing(true);
            const res = await api.agent.recomanarAccio(municipiId);
            setRecommendation(res);
        } catch (err) {
            console.error("Error fetching recommendation:", err);
        } finally {
            setIsLoading(false);
            setIsRefreshing(false);
        }
    };

    useEffect(() => {
        fetchRecommendation();
    }, [municipiId]);

    if (isLoading) {
        return (
            <div className="bg-white rounded-3xl p-8 border-2 border-dashed border-blue-100 flex flex-col items-center justify-center space-y-4">
                <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
                <p className="text-sm font-bold text-slate-400 uppercase tracking-widest">Analitzant context...</p>
            </div>
        );
    }

    return (
        <div className="bg-gradient-to-br from-indigo-900 to-slate-900 rounded-3xl p-8 text-white relative overflow-hidden shadow-xl">
            <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -mr-32 -mt-32" />
            
            <div className="relative z-10">
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
                            <Sparkles className="w-6 h-6" />
                        </div>
                        <div>
                            <h3 className="text-lg font-black tracking-tight">Kimi Recommendation</h3>
                            <p className="text-[10px] text-blue-300 font-bold uppercase tracking-widest">IA Strategic Insight</p>
                        </div>
                    </div>
                    <button 
                        onClick={fetchRecommendation}
                        disabled={isRefreshing}
                        className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                    >
                        <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                    </button>
                </div>

                <div className="bg-white/5 rounded-2xl p-6 border border-white/10 mb-8 blur-overlay">
                    <div className="flex items-start gap-4">
                        <div className="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center shrink-0">
                            <Brain className="w-4 h-4 text-blue-300" />
                        </div>
                        <div>
                            <p className="text-blue-100 leading-relaxed mb-4">
                                {recommendation?.rao || "No s'ha pogut generar una recomanació específica en aquest moment."}
                            </p>
                            <div className="flex items-center gap-3">
                                <span className="text-[10px] font-black text-blue-400 uppercase tracking-widest">Score de prioritat:</span>
                                <div className="flex-1 h-1.5 bg-white/10 rounded-full overflow-hidden">
                                    <div 
                                        className="h-full bg-blue-500" 
                                        style={{ width: `${recommendation?.score || 0}%` }}
                                    />
                                </div>
                                <span className="text-xs font-bold">{recommendation?.score || 0}%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex flex-col sm:flex-row items-center gap-4">
                    <Button 
                        className="w-full sm:w-auto h-12 px-8 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold shadow-lg shadow-blue-600/20 group translate-y-0 active:translate-y-0.5 transition-all"
                        onClick={() => {/* handle action */}}
                    >
                        <span>{recommendation?.accio || "Revisar Manualment"}</span>
                        <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                    </Button>
                </div>
            </div>
        </div>
    );
}
