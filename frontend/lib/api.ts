const isBrowser = typeof window !== "undefined";
const defaultHost = isBrowser ? window.location.hostname : "127.0.0.1";
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || `http://${defaultHost}:8000`;

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return sessionStorage.getItem("token");
}

export function setToken(token: string) {
  sessionStorage.setItem("token", token);
}

export function removeToken() {
  sessionStorage.removeItem("token");
  if (typeof document !== "undefined") {
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT; SameSite=Strict";
  }
}

async function fetchAPI(endpoint: string, options?: RequestInit) {
  const token = getToken();
  const fullUrl = `${BASE_URL}${endpoint}`;
  console.log(`[fetchAPI] Crida a URL:`, fullUrl, `| Method:`, options?.method || "GET", `| isBrowser:`, typeof window !== "undefined");
  try {
    const res = await fetch(fullUrl, {
      headers: {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      ...options,
    });
    
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: "Error desconegut" }));
      const message = typeof error.detail === "object" 
        ? JSON.stringify(error.detail) 
        : (error.detail || "Error del servidor");
      throw new Error(message);
    }
    return res.json();
  } catch (err) {
    console.error("[fetchAPI] Error complet: ", err);
    throw err;
  }
}

const api = {
  auth: {
    login: (email: string, password: string) => {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      
      return fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      }).then(async (res) => {
        if (!res.ok) {
          const error = await res.json().catch(() => ({ detail: "Error desconegut" }));
          throw new Error(error.detail || "Error del servidor");
        }
        return res.json();
      });
    },
    me: () => fetchAPI("/auth/me"),
  },
  municipis: {
    llistar: (params?: Record<string, string>) =>
      fetchAPI(`/municipis?${new URLSearchParams(params || {})}`),
    detall: (id: string) => fetchAPI(`/municipis/${id}`),
    crear: (data: unknown) => fetchAPI("/municipis", { method: "POST", body: JSON.stringify(data) }),
    editar: (id: string, data: unknown) => fetchAPI(`/municipis/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    eliminar: (id: string) => fetchAPI(`/municipis/${id}`, { method: "DELETE" }),
  },
  contactes: {
    llistar: (params?: Record<string, string>) =>
      fetchAPI(`/contactes?${new URLSearchParams(params || {})}`),
    detall: (id: string) => fetchAPI(`/contactes/${id}`),
    crear: (data: unknown) => fetchAPI("/contactes", { method: "POST", body: JSON.stringify(data) }),
    editar: (id: string, data: unknown) => fetchAPI(`/contactes/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    eliminar: (id: string) => fetchAPI(`/contactes/${id}`, { method: "DELETE" }),
  },
  deals: {
    llistar: (params?: Record<string, string>) =>
      fetchAPI(`/deals?${new URLSearchParams(params || {})}`),
    detall: (id: string) => fetchAPI(`/deals/${id}`),
    crear: (data: unknown) => fetchAPI("/deals", { method: "POST", body: JSON.stringify(data) }),
    editar: (id: string, data: unknown) => fetchAPI(`/deals/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    canviarEtapa: (id: string, etapa: string) =>
      fetchAPI(`/deals/${id}/etapa`, { method: "PATCH", body: JSON.stringify({ etapa }) }),
    actualitzarNotes: (id: string, notes: string) =>
      fetchAPI(`/deals/${id}/notes`, { method: "PATCH", body: JSON.stringify({ notes_humanes: notes }) }),
    kpis: () => fetchAPI("/deals/kpis"),
    eliminar: (id: string) => fetchAPI(`/deals/${id}`, { method: "DELETE" }),
  },
  emails: {
    llistar: (params?: Record<string, string>) =>
      fetchAPI(`/emails?${new URLSearchParams(params || {})}`),
    enviar: (data: unknown) => fetchAPI("/emails/enviar", { method: "POST", body: JSON.stringify(data) }),
    vincular: (id: string, dealId: string) =>
      fetchAPI(`/emails/${id}/deal`, { method: "PATCH", body: JSON.stringify({ deal_id: dealId }) }),
    marcarLlegit: (id: string, llegit: boolean) =>
      fetchAPI(`/emails/${id}/llegit`, { method: "PATCH", body: JSON.stringify({ llegit }) }),
    sync: () => fetchAPI("/emails/sync", { method: "POST" }),
    pendents: () => fetchAPI("/emails/pendents"),
    getStats: () => fetchAPI("/emails/stats/obertures"),
    eliminar: (id: string) => fetchAPI(`/emails/${id}`, { method: "DELETE" }),
  },
  llicencies: {
    llistar: (params?: Record<string, string>) =>
      fetchAPI(`/llicencies?${new URLSearchParams(params || {})}`),
    detall: (id: string) => fetchAPI(`/llicencies/${id}`),
    crear: (data: unknown) => fetchAPI("/llicencies", { method: "POST", body: JSON.stringify(data) }),
    editar: (id: string, data: unknown) => fetchAPI(`/llicencies/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  },
  pagaments: {
    llistar: (params?: Record<string, string>) =>
      fetchAPI(`/pagaments?${new URLSearchParams(params || {})}`),
    crear: (data: unknown) => fetchAPI("/pagaments", { method: "POST", body: JSON.stringify(data) }),
    confirmar: (id: string, data: unknown) =>
      fetchAPI(`/pagaments/${id}/confirmar`, { method: "PATCH", body: JSON.stringify(data) }),
    kpis: () => fetchAPI("/pagaments/kpis"),
  },
  usuaris: {
    llistar: () => fetchAPI("/usuaris"),
    crear: (data: unknown) => fetchAPI("/usuaris", { method: "POST", body: JSON.stringify(data) }),
    editar: (id: string, data: unknown) => fetchAPI(`/usuaris/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
    eliminar: (id: string) => fetchAPI(`/usuaris/${id}`, { method: "DELETE" }),
  },
  alertes: {
    totes: () => fetchAPI("/alertes/"),
    count: () => fetchAPI("/alertes/count"),
  },
  agent: {
    redactarEmail: (data: any) => fetchAPI("/agent/redactar-email", { method: "POST", body: JSON.stringify(data) }),
    analitzarDeal: (data: any) => fetchAPI("/agent/analitzar-deal", { method: "POST", body: JSON.stringify(data) }),
    resumirDeal: (data: any) => fetchAPI("/agent/resum-deal", { method: "POST", body: JSON.stringify(data) }),
    chatMunicipi: (data: any) => fetchAPI("/agent/chat_municipi", { method: "POST", body: JSON.stringify(data) }),
  },
  tasques: {
    llistar: (params?: Record<string, string>) =>
      fetchAPI(`/tasques?${new URLSearchParams(params || {})}`),
    crear: (data: any) => fetchAPI("/tasques", { method: "POST", body: JSON.stringify(data) }),
    editar: (id: string, data: any) => fetchAPI(`/tasques/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
    eliminar: (id: string) => fetchAPI(`/tasques/${id}`, { method: "DELETE" }),
  },
  dashboard: {
    diari: () => fetchAPI("/dashboard/diari"),
  },
};

export default api;
