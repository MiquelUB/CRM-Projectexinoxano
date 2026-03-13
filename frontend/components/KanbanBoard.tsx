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
  { id: "prospecte", title: "🔵 Prospecte", color: "bg-blue-50" },
  { id: "contacte_inicial", title: "📧 Contacte Inicial", color: "bg-indigo-50" },
  { id: "demo_feta", title: "📊 Demo Feta", color: "bg-purple-50" },
  { id: "proposta_enviada", title: "📄 Proposta", color: "bg-orange-50" },
  { id: "tramitacio_admin", title: "⚙️ Tramitació", color: "bg-gray-100" },
  { id: "tancat_guanyat", title: "✅ Tancat", color: "bg-green-50" },
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
      const response = await api.deals.llistar({ limit: "100" });
      setDeals(response.items);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleDragStart = (event: any) => {
    setActiveId(event.active.id);
  };

  const handleDragEnd = async (event: any) => {
    setActiveId(null);
    const { active, over } = event;

    if (!over) return;

    const dealId = active.id;
    const newStage = over.id; // Either hovering a column or another card
    
    // Find dropping stage (could be dropping over a column or another item)
    let targetStage = newStage;
    if (!STAGES.find((s) => s.id === targetStage)) {
       const overDeal = deals.find((d) => d.id === newStage);
       if (overDeal) targetStage = overDeal.etapa;
    }

    const currentDeal = deals.find((d) => d.id === dealId);
    if (!currentDeal || currentDeal.etapa === targetStage) return;

    // Optimistic update
    setDeals(deals.map(d => d.id === dealId ? { ...d, etapa: targetStage } : d));

    try {
      await api.deals.canviarEtapa(dealId, targetStage);
    } catch (e) {
      console.error(e);
      // Revert on error
      fetchDeals();
    }
  };

  const handleCardClick = (deal: any) => {
    setSelectedDeal(deal);
  };

  if (loading) return <div>Carregant pipeline...</div>;

  return (
    <>
      <DndContext
        sensors={sensors}
        collisionDetection={closestCorners}
        onDragStart={handleDragStart}
        onDragEnd={handleDragEnd}
      >
        <div className="flex gap-4 h-full p-2 items-stretch">
          <SortableContext items={STAGES.map(s => s.id)} strategy={horizontalListSortingStrategy}>
            {STAGES.map((stage) => {
              const stageDeals = deals.filter((d) => d.etapa === stage.id);
              
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
          </SortableContext>
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
