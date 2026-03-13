"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";
import { CalendarWidget } from "@/components/CalendarWidget";
import { TaskModal } from "@/components/TaskModal";
import DealDrawer from "@/components/DealDrawer";

export default function DashboardPage() {
  const [isClient, setIsClient] = useState(false);
  const [kpis, setKpis] = useState<any>(null);
  const [alertes, setAlertes] = useState<any>(null);
  const [emailStats, setEmailStats] = useState<any>(null);
  const [tasques, setTasques] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showTaskModal, setShowTaskModal] = useState(false);
  const [selectedTaskDate, setSelectedTaskDate] = useState<Date | undefined>(undefined);
  const [selectedDeal, setSelectedDeal] = useState<any>(null);
  const [selectedTaskForEdit, setSelectedTaskForEdit] = useState<any>(null);
  const [dealLoading, setDealLoading] = useState(false);

  const fetchDashboardData = async () => {
    try {
      const [kpisData, alertesData, statsData, tasquesData] = await Promise.all([
        api.deals.kpis(),
        api.alertes.totes(),
        api.emails.getStats(),
        api.tasques.llistar({ estat: "pendent" })
      ]);
      setKpis(kpisData);
      setAlertes(alertesData);
      setEmailStats(statsData);
      setTasques(tasquesData.items || []);
    } catch (error) {
      console.error("Failed to load dashboard data", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTask = async (task: any) => {
    // If it's a real task, open TaskModal to edit
    if (task.id && task.is_pseudo === false) {
      setSelectedTaskForEdit(task);
      setShowTaskModal(true);
      return;
    }

    // If it's a pseudo-task or we want to see the deal
    if (!task.deal_id) return;
    
    setDealLoading(true);
    try {
      const deal = await api.deals.detall(task.deal_id);
      setSelectedDeal(deal);
    } catch (error) {
      console.error("Error fetching deal", error);
    } finally {
      setDealLoading(false);
    }
  };

  const handleTaskModalClose = () => {
    setShowTaskModal(false);
    setSelectedTaskForEdit(null);
    setSelectedTaskDate(undefined);
  };

  const handleDrawerClose = () => {
    setSelectedDeal(null);
    fetchDashboardData();
  };

  useEffect(() => {
    setIsClient(true);
    fetchDashboardData();
  }, []);

  if (loading) return (
    <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center space-y-4">
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-slate-500 font-medium animate-pulse">Carregant dashboard...</p>
        </div>
    </div>
  );

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-end">
        <div>
            <h1 className="text-4xl font-extrabold premium-gradient-text tracking-tight">Dashboard</h1>
            <p className="text-slate-500 mt-1">Benvingut de nou, Albert. Aquí tens el resum d'avui.</p>
        </div>
        <div className="text-right hidden sm:block">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Data d'avui</p>
            {isClient && (
                <p className="text-sm font-medium text-slate-600">
                    {new Date().toLocaleDateString('ca-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                </p>
            )}
        </div>
      </div>
      
      {/* Bloc 1 — KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-card p-6 border-l-4 border-l-blue-500 group hover:scale-[1.02] transition-transform cursor-default">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Deals Actius</h3>
          <div className="flex items-baseline space-x-2">
            <p className="text-4xl font-black text-slate-800 tracking-tight">{kpis?.total_deals || 0}</p>
            <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">+2%</span>
          </div>
        </div>
        <div className="glass-card p-6 border-l-4 border-l-emerald-500 group hover:scale-[1.02] transition-transform cursor-default">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Valor Pipeline</h3>
          <p className="text-3xl font-black text-slate-800 tracking-tight">
            {kpis?.valor_total_pipeline?.toLocaleString('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }) || '0 €'}
          </p>
        </div>
        <div className="glass-card p-6 border-l-4 border-l-amber-500 group hover:scale-[1.02] transition-transform cursor-default">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Cicles Mes</h3>
          <p className="text-4xl font-black text-slate-800 tracking-tight">{kpis?.deals_per_tancar_aquest_mes || 0}</p>
        </div>
        
        {/* Emails del sistema */}
        <div className="glass-card p-6 border-l-4 border-l-indigo-500 group hover:scale-[1.02] transition-transform cursor-default col-span-1 md:col-span-1">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Emails del sistema</h3>
          <div className="flex items-baseline space-x-2">
            <p className="text-4xl font-black text-indigo-600 tracking-tight">{(emailStats as any)?.total_emails || 0}</p>
            <span className="text-[9px] font-bold text-slate-400 uppercase truncate">Sincronitzats</span>
          </div>
          <div className="mt-2 flex items-center text-[10px] font-bold text-slate-400">
            <span className="text-indigo-500 mr-1">{(emailStats as any)?.taxa_obertura || 0}%</span>
            <span>obertures (30d)</span>
          </div>
        </div>
      </div>

      {/* Agenda & Calendari Section */}
      <CalendarWidget 
        tasques={tasques} 
        onNewTask={(date) => {
          setSelectedTaskDate(date);
          setShowTaskModal(true);
        }}
        onSelectTask={handleSelectTask}
      />
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Bloc 2 — Alertes Renovacions + Pagaments */}
        <div className="lg:col-span-2 glass-card p-8 flex flex-col min-h-[400px]">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-black text-slate-800 tracking-tight">Alertes Crítiques</h2>
            <span className="text-xs font-bold text-slate-400 bg-slate-100 px-3 py-1 rounded-full uppercase">Acció Requerida</span>
          </div>
          
          <div className="flex-1 space-y-4">
            {alertes?.renovacions?.length > 0 ? (
              alertes.renovacions.map((ren: any) => (
                <div key={ren.id} className="p-4 bg-white border border-slate-100 rounded-xl flex items-center shadow-sm hover:shadow-md transition-shadow">
                  <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center mr-4">
                    <span className="text-blue-600 font-bold text-xs">RE</span>
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-bold text-slate-800">
                      Renovació: {ren.nom_municipi}
                    </p>
                    <p className="text-xs text-slate-500">Llicència expira el {new Date(ren.data_renovacio).toLocaleDateString()}</p>
                  </div>
                  <button 
                    onClick={() => handleSelectTask({ deal_id: ren.deal_id })}
                    className="text-xs font-bold text-blue-600 hover:text-blue-700 decoration-dotted hover:underline"
                  >
                    Gestionar
                  </button>
                </div>
              ))
            ) : null}
            
            {alertes?.pagaments_vencuts?.length > 0 ? (
              alertes.pagaments_vencuts.map((pag: any) => (
                <div key={pag.id} className="p-4 bg-white border border-slate-100 rounded-xl flex items-center shadow-sm hover:shadow-md transition-shadow">
                  <div className="w-10 h-10 rounded-full bg-rose-50 flex items-center justify-center mr-4 text-rose-600 italic font-black">!</div>
                  <div className="flex-1">
                    <p className="text-sm font-bold text-slate-800">
                      Impagat: {pag.nom_municipi}
                    </p>
                    <p className="text-xs text-slate-500">{Number(pag.import).toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })} • des de {new Date(pag.data_limit).toLocaleDateString()}</p>
                  </div>
                  <button 
                    onClick={() => handleSelectTask({ deal_id: pag.deal_id })}
                    className="text-xs font-bold text-rose-600 hover:text-rose-700 decoration-dotted hover:underline"
                  >
                    Reclamar
                  </button>
                </div>
              ))
            ) : null}

            {alertes?.tasques_urgents?.length > 0 ? (
              alertes.tasques_urgents.map((t: any) => (
                <div key={t.id} className="p-4 bg-amber-50 border border-amber-100 rounded-xl flex items-center shadow-sm hover:shadow-md transition-shadow">
                  <div className="w-10 h-10 rounded-full bg-amber-500 flex items-center justify-center mr-4 text-white font-black">!</div>
                  <div className="flex-1">
                    <p className="text-sm font-bold text-slate-800">
                      {t.titol}
                    </p>
                    <p className="text-xs text-slate-500">{t.nom_municipi}</p>
                  </div>
                  <button 
                    onClick={() => handleSelectTask(t)}
                    className="text-xs font-bold text-amber-600 hover:text-amber-700 decoration-dotted hover:underline"
                  >
                    Gestionar
                  </button>
                </div>
              ))
            ) : null}
            
            {(alertes?.renovacions?.length === 0 && alertes?.pagaments_vencuts?.length === 0) && (
              <div className="flex flex-col items-center justify-center h-full text-center space-y-2 opacity-50">
                <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center text-2xl">✨</div>
                <p className="text-sm text-slate-500 font-medium italic">Tot en ordre. No hi ha alertes pendents.</p>
              </div>
            )}
          </div>
        </div>
        
        {/* Bloc 3 — Emails Pendents */}
        <div className="glass-card p-8 flex flex-col">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-black text-slate-800 tracking-tight">Correus</h2>
            <div className="w-8 h-8 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 font-bold text-xs ring-4 ring-indigo-50/50">
                {alertes?.emails_pendents?.length || 0}
            </div>
          </div>
          
          <div className="flex-1 space-y-4">
             {alertes?.emails_pendents?.length > 0 ? (
                <>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Pendents de vincular</p>
                {alertes.emails_pendents.slice(0, 4).map((em: any) => (
                  <div key={em.id} className="p-4 bg-slate-50 border border-transparent hover:border-indigo-100 hover:bg-white rounded-xl transition-all group cursor-pointer">
                     <p className="text-sm font-bold text-slate-800 truncate group-hover:text-indigo-600 transition-colors">{em.assumpte}</p>
                     <p className="text-[10px] text-slate-400 font-medium mt-1 uppercase tracking-tighter truncate">De: {em.from}</p>
                  </div>
                ))}
                </>
             ) : (
                <div className="flex flex-col items-center justify-center h-full text-center space-y-4 py-8">
                    <div className="w-20 h-20 bg-emerald-50 rounded-2xl flex items-center justify-center text-4xl rotate-3 transform transition-transform hover:rotate-0">✅</div>
                    <p className="text-sm text-slate-600 font-bold">Safata d'entrada neta</p>
                    <p className="text-xs text-slate-400 px-4">Tots els correus estan vinculats correctament als seus deals.</p>
                </div>
             )}
             
             {alertes?.emails_pendents?.length > 4 && (
                <Link href="/emails/pendents" className="block text-center p-3 text-xs font-black text-indigo-600 hover:bg-indigo-50 rounded-xl transition-colors border-2 border-indigo-50 mt-4">
                   VEURE TOTS ({alertes.emails_pendents.length})
                </Link>
             )}
          </div>
        </div>
      </div>

      {showTaskModal && (
        <TaskModal 
          initialDate={selectedTaskDate}
          task={selectedTaskForEdit}
          onClose={handleTaskModalClose}
          onSaved={fetchDashboardData}
        />
      )}

      {selectedDeal && (
        <DealDrawer 
          deal={selectedDeal} 
          onClose={handleDrawerClose} 
          onUpdate={fetchDashboardData}
        />
      )}

      {dealLoading && (
        <div className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-3xl shadow-xl flex flex-col items-center space-y-4">
             <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
             <p className="text-xs font-bold text-slate-600 uppercase tracking-widest">Obrint Deal...</p>
          </div>
        </div>
      )}

       {/* Bloc 4 — Activitat recente / Footer */}
       <div className="glass-card p-6 border-dashed border-2 border-slate-200 bg-slate-50/30 flex items-center justify-between">
          <p className="text-sm font-bold text-slate-400 uppercase tracking-widest flex items-center">
            <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
            Sistema Operatiu
          </p>
          <p className="text-xs font-medium text-slate-500 italic">PXX CRM Engine v2.0-2026</p>
       </div>
    </div>
  );
}
