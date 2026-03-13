---
name: nextjs-frontend
description: Guides creation of Next.js 14 pages, React components, and API calls for the CRM PXX frontend. Use when creating or editing any frontend TypeScript/TSX file, including pages, components, hooks, or API client code.
---

# Next.js Frontend — Convencions CRM PXX

Aplica aquest skill sempre que treballis en qualsevol fitxer del frontend.

## Principis de Disseny

- **Estètica:** Professional, sobri, orientat a eficiència. No colorista ni "startup".
- **Colors principals:** Blau fosc #1B3A6B (primari), #2E6DA4 (secundari), blanc #FFFFFF (fons)
- **Font:** Sistema (Inter o equivalent). No Google Fonts (sobirania).
- **Components UI:** shadcn/ui com a base. Tailwind per a ajustos específics.
- **No emojis a la UI de producció** — només icones de lucide-react.

## Estructura de Pàgines (App Router)

```typescript
// app/municipis/page.tsx — patró estàndard
"use client"

import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"

export default function MunicipisPage() {
  const [cerca, setCerca] = useState("")

  const { data, isLoading, error } = useQuery({
    queryKey: ["municipis", cerca],
    queryFn: () => api.municipis.llistar({ cerca }),
  })

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage error={error} />

  return (
    <div className="p-6">
      {/* contingut */}
    </div>
  )
}
```

## Client API (lib/api.ts)

Totes les crides al backend passen per aquest client centralitzat:

```typescript
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function fetchAPI(endpoint: string, options?: RequestInit) {
  const token = getToken() // des de cookie httpOnly o store
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    ...options,
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export const api = {
  municipis: {
    llistar: (params?) => fetchAPI(`/municipis?${new URLSearchParams(params)}`),
    detall: (id: string) => fetchAPI(`/municipis/${id}`),
    crear: (data) => fetchAPI("/municipis", { method: "POST", body: JSON.stringify(data) }),
    editar: (id, data) => fetchAPI(`/municipis/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    eliminar: (id) => fetchAPI(`/municipis/${id}`, { method: "DELETE" }),
  },
  // ... rest of modules
}
```

## Component KanbanBoard

El component més crític de la Fase 1. Regles:

- Usa `@dnd-kit/core` per al drag & drop (no react-beautiful-dnd)
- Actualització **optimista**: canvia la UI abans de la resposta del servidor
- Si el servidor retorna error: reverteix el canvi i mostra toast d'error
- Les columnes no es poden reordenar, només les targetes entre columnes

```typescript
// Ordre fix de columnes (mai canviar)
const ETAPES = [
  { id: "prospecte", label: "Prospecte" },
  { id: "contacte_inicial", label: "Contacte Inicial" },
  { id: "demo_feta", label: "Demo Feta" },
  { id: "proposta_enviada", label: "Proposta Enviada" },
  { id: "tramitacio_admin", label: "Tramitació Admin" },
  { id: "tancat_guanyat", label: "Tancat Guanyat" },
]
```

## Gestió d'Estat

- **Servidor:** @tanstack/react-query (cache, revalidació automàtica)
- **UI local:** useState de React (modals, drawers, formularis)
- **No Redux, no Zustand** en Fase 1 — innecessari per a 1 usuari

## Formularis

Usa `react-hook-form` + `zod` per a validació:

```typescript
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const schema = z.object({
  nom: z.string().min(2, "El nom ha de tenir mínim 2 caràcters"),
  email: z.string().email("Format d'email invàlid"),
})
```

## Missatges i Feedback

- **Toast notifications:** sonner (inclòs a shadcn/ui)
- **Loading states:** Skeleton de shadcn/ui (no spinners genèrics)
- **Errors:** Missatge descriptiu en català sota el camp afectat

## Checklist Frontend

- [ ] Tots els texts de la UI en català
- [ ] Cap crida directa a fetch() — sempre via api.ts
- [ ] Loading i error states gestionats a totes les pàgines
- [ ] Formularis amb validació zod
- [ ] Actualització optimista al Kanban
