
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
  console.log(`[fetchAPI] Unified Call:`, fullUrl, `| Method:`, options?.method || "GET");

  const headers: Record<string, string> = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  if (!(options?.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  try {
    const res = await fetch(fullUrl, {
      ...options,
      headers: {
        ...headers,
        ...options?.headers as Record<string, string>,
      },
    });
    
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: "Error desconegut" }));
      throw new Error(error.detail || "Error del servidor");
    }
    return res.json();
  } catch (err) {
    console.error("[fetchAPI] Error: ", err);
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
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
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
    canviarEtapa: (id: string, etapa: string) =>
      fetchAPI(`/municipis/${id}/etapa`, { method: "PATCH", body: JSON.stringify({ etapa }) }),
    getTimeline: (id: string) => fetchAPI(`/municipis/${id}/activitats`),
    kpis: () => fetchAPI("/municipis/kpis"),
    eliminar: (id: string) => fetchAPI(`/municipis/${id}`, { method: "DELETE" }),
  },
  contactes: {
    llistar: (params?: Record<string, string>) =>
      fetchAPI(`/contactes?${new URLSearchParams(params || {})}`),
    crear: (data: unknown) => fetchAPI("/contactes", { method: "POST", body: JSON.stringify(data) }),
    editar: (id: string, data: unknown) => fetchAPI(`/contactes/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    eliminar: (id: string) => fetchAPI(`/contactes/${id}`, { method: "DELETE" }),
  },
  emails: {
    llistar: (params?: Record<string, string>) => 
      fetchAPI(`/emails?${new URLSearchParams(params || {})}`),
    vincular: (id: string, dealId: string) => 
      fetchAPI(`/emails/${id}/deal`, { method: "PATCH", body: JSON.stringify({ deal_id: dealId }) }),
    sync: () => fetchAPI("/emails/sync", { method: "POST" }),
    eliminar: (id: string) => fetchAPI(`/emails/${id}`, { method: "DELETE" }),
    enviar: (data: any) => {
      if (data instanceof FormData) {
        const mid = data.get("municipi_id") || data.get("deal_id");
        return fetchAPI(`/emails/enviar_manual/${mid}`, { method: "POST", body: data });
      }
      return fetchAPI(`/emails/enviar_manual/${data.municipi_id}`, { method: "POST", body: JSON.stringify(data) });
    },
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
  agent: {
    chat: (data: any) => fetchAPI("/agent/chat", { method: "POST", body: JSON.stringify(data) }),
    getMemory: (params?: { deal_id?: string; municipi_id?: string }) => {
      const cleanParams: Record<string, string> = {};
      if (params) {
        Object.entries(params).forEach(([key, value]) => {
          if (value) cleanParams[key] = value;
        });
      }
      return fetchAPI(`/agent/memory?${new URLSearchParams(cleanParams)}`);
    },
  },
};

// Aliases for compatibility during transition
api.municipis_v2 = api.municipis;
api.contactes_v2 = api.contactes;
api.emails_v2 = api.emails;

export default api;
