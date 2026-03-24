import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { Clock } from "lucide-react";

export function DealCard({ deal, isOverlay = false }: any) {
  if (!deal) return null;

  const priorityStyles: Record<string, string> = {
    alta: "bg-rose-50 text-rose-600 border-rose-100",
    mitjana: "bg-amber-50 text-amber-600 border-amber-100",
    baixa: "bg-emerald-50 text-emerald-600 border-emerald-100",
  };

  const totalValue = Number(deal.valor_setup) + Number(deal.valor_llicencia);

  // Calcula dies en etapa actual
  const updateDate = new Date(deal.updated_at);
  const now = new Date();
  const diffDays = Math.floor((now.getTime() - updateDate.getTime()) / (1000 * 3600 * 24));

  return (
    <div
      className={`bg-white rounded-xl border border-slate-100 p-4 cursor-grab active:cursor-grabbing hover:shadow-xl hover:shadow-slate-200/50 hover:border-blue-100 transition-all z-10 ${
        isOverlay ? "opacity-90 scale-105 shadow-2xl ring-2 ring-blue-500/20" : ""
      }`}
    >
      <div className="flex justify-between items-start mb-3 gap-2">
        <div className="flex-1">
          <h4 className="font-extrabold text-slate-800 text-[14px] leading-snug tracking-tight mb-1" title={deal.titol}>
            {deal.titol}
          </h4>
          {deal.municipi?.nom && (
            <p className="text-[10px] font-black text-blue-600 uppercase tracking-widest">
              {deal.municipi.nom}
            </p>
          )}
        </div>
        <div className={`text-[9px] font-black uppercase tracking-tighter px-1.5 py-0.5 rounded-md border shrink-0 ${priorityStyles[deal.prioritat] || priorityStyles.baixa}`}>
            {deal.prioritat}
        </div>
      </div>
      
      <div className="flex items-center space-x-2 mb-4">
          <div className="w-5 h-5 rounded-full bg-slate-100 flex items-center justify-center text-[10px] font-black text-slate-400">
            {deal.contacte?.nom?.charAt(0) || '?'}
          </div>
          <p className="text-[11px] font-bold text-slate-500 truncate">
            {deal.contacte?.nom || 'Sense assignar'}
          </p>
      </div>
      
      <div className="flex justify-between items-end border-t border-slate-50 pt-3 mt-1">
        <div>
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-0.5">Valor</p>
            <span className="font-extrabold text-slate-800 text-sm">
            {totalValue.toLocaleString('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })}
            </span>
        </div>
        
        <div className="flex flex-col items-end">
             <div className="flex items-center text-slate-400 gap-1" title={`${diffDays} dies en aquesta etapa`}>
                <Clock className="w-2.5 h-2.5" />
                <span className="text-[10px] font-bold">{diffDays}d</span>
             </div>
        </div>
      </div>
    </div>
  );
}

export function SortableDealCard({ deal, onClick }: any) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: deal.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.4 : 1,
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners} onClick={onClick}>
      <DealCard deal={deal} />
    </div>
  );
}
