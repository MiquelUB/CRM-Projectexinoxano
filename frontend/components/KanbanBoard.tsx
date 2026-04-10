"use client";

import { useEffect, useState } from "react";
import {
  DndContext,
  DragOverlay,
  closestCorners,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import { SortableContext, horizontalListSortingStrategy } from "@dnd-kit/sortable";
import { Column } from "./Column";
import { DealCard } from "./DealCard";
import DealDrawer from "./DealDrawer";
import api from "@/lib/api";

const STAGES = [
  { id: "research", title: "🔍 Research", color: "bg-slate-50" },
  { id: "contacte", title: "📧 Contacte", color: "bg-blue-50" },
  { id: "demo_pendent", title: "📊 Demo Pendent", color: "bg-purple-50" },
  { id: "demo_ok", title: "✨ Demo OK", color: "bg-purple-100" },
  { id: "oferta", title: "📄 Oferta / Neg.", color: "bg-orange-50" },
  { id: "aprovacio", title: "⚖️ Aprovació", color: "bg-amber-100" },
  { id: "documentacio", title: "📁 Docs / Cont.", color: "bg-slate-100" },
  { id: "contracte", title: "✅ Client", color: "bg-green-50" },
  { id: "pausa", title: "⏸️ Pausa", color: "bg-gray-50" },
  { id: "perdut", title: "❌ Perdut", color: "bg-red-50" },
];

export default function KanbanBoard() {
  const [deals, setDeals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [selectedDeal, setSelectedDeal] = useState<any | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
    useSensor(KeyboardSensor)
  );

  useEffect(() => {
    fetchDeals();
  }, []);

  const fetchDeals = async () => {
    try {
      const response = await api.municipis_v2.llistar({ limit: "200" });
      setDeals(response.items || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const findContainer = (id: string) => {
    if (STAGES.find((s) => s.id === id)) return id;
    const deal = deals.find((d) => d.id === id);
    return deal ? deal.etapa_actual : null;
  };

  const handleDragOver = (event: any) => {
    const { active, over } = event;
    if (!over) return;

    const activeId = active.id;
    const overId = over.id;

    if (activeId === overId) return;

    const overContainer = findContainer(overId);
    if (!overContainer) return;

    const activeDeal = deals.find((d) => d.id === activeId);
    if (activeDeal && activeDeal.etapa_actual !== overContainer) {
      setDeals((prev) =>
        prev.map((d) => (d.id === activeId ? { ...d, etapa_actual: overContainer } : d))
      );
    }
  };

  const handleDragEnd = async (event: any) => {
    const { active } = event;
    const dealId = active.id;

    setActiveId(null);

    // Trobar l'estat final tal com ha quedat a la UI després del DragOver
    const currentDeal = deals.find((d) => d.id === dealId);
    if (!currentDeal) return;

    try {
      // Persistir el canvi a la base de dades V2
      await api.municipis_v2.canviarEtapa(dealId as string, currentDeal.etapa_actual);
    } catch (error) {
      console.error("Error actualitzant etapa:", error);
      fetchDeals(); // Revertir a l'estat del servidor
    }
  };

  const handleCardClick = (deal: any) => {
    setSelectedDeal(deal);
  };

  const handleDragStart = (event: any) => {
    setActiveId(event.active.id);
  };

  if (loading) return <div>Carregant pipeline...</div>;

  return (
    <>
      <DndContext
        sensors={sensors}
        collisionDetection={closestCorners}
        onDragStart={handleDragStart}
        onDragOver={handleDragOver}
        onDragEnd={handleDragEnd}
      >
        <div className="flex gap-4 h-full p-2 items-stretch">
            {STAGES.map((stage) => {
              const stageDeals = deals.filter((d) => d.etapa_actual === stage.id);
              
              // Sort by prioritat
              const priorityWeight: Record<string, number> = { alta: 3, mitjana: 2, baixa: 1 };
              stageDeals.sort((a, b) => (priorityWeight[b.prioritat] || 0) - (priorityWeight[a.prioritat] || 0));

              const stageValue = stageDeals.reduce((sum, d) => sum + (Number(d.valor_setup) + Number(d.valor_llicencia)), 0);

              return (
                <Column 
                  key={stage.id} 
                  stage={stage} 
                  deals={stageDeals} 
                  totalValue={stageValue}
                  onCardClick={handleCardClick}
                />
              );
            })}
        </div>

        <DragOverlay>
          {activeId ? (
             <DealCard deal={deals.find((d) => d.id === activeId)} isOverlay />
          ) : null}
        </DragOverlay>
      </DndContext>

      {/* Drawer */}
      {selectedDeal && (
        <DealDrawer 
          deal={selectedDeal} 
          onClose={() => setSelectedDeal(null)} 
          onUpdate={fetchDeals} 
        />
      )}
    </>
  );
}
