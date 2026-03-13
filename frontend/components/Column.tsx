import { useDroppable } from "@dnd-kit/core";
import { SortableContext, verticalListSortingStrategy } from "@dnd-kit/sortable";
import { DealCard, SortableDealCard } from "./DealCard";

export function Column({ stage, deals, totalValue, onCardClick }: any) {
  const { setNodeRef } = useDroppable({
    id: stage.id,
  });

  return (
    <div 
      ref={setNodeRef}
      className={`flex-none w-[320px] glass-card p-4 flex flex-col border-t-4 transition-all duration-300`}
      style={{ borderTopColor: stage.id === 'prospecte' ? '#3b82f6' : 
                               stage.id === 'contacte_inicial' ? '#6366f1' :
                               stage.id === 'demo_feta' ? '#a855f7' :
                               stage.id === 'proposta_enviada' ? '#f59e0b' :
                               stage.id === 'tramitacio_admin' ? '#64748b' :
                               stage.id === 'tancat_guanyat' ? '#10b981' : '#ef4444' }}
    >
      <div className="flex justify-between items-start mb-5">
        <div>
            <h3 className="font-black text-slate-800 text-xs uppercase tracking-widest">{stage.title}</h3>
            <p className="text-[10px] font-bold text-slate-400 mt-0.5">
                {deals.length} DEALS
            </p>
        </div>
        <div className="text-right">
          <span className="text-xs font-black text-slate-800 bg-white/50 px-2 py-1 rounded-lg border border-slate-100 shadow-sm">
            {totalValue.toLocaleString('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })}
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 custom-scrollbar pr-1 pb-4">
        <SortableContext items={deals.map((d: any) => d.id)} strategy={verticalListSortingStrategy}>
          {deals.map((deal: any) => (
            <SortableDealCard key={deal.id} deal={deal} onClick={() => onCardClick(deal)} />
          ))}
        </SortableContext>
      </div>
    </div>
  );
}
