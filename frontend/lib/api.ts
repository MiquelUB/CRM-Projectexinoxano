const isBrowser = typeof window !== "undefined";
const defaultHost = isBrowser ? window.location.host : "127.0.0.1:8000";
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || (isBrowser ? `${window.location.protocol}//${window.location.host}` : `http://${defaultHost}`);
// Si estem al backend de EasyPanel, la URL ja ve sense port o amb el protocol correcte.

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
  console.log(`🚀 [API UNIFIED]`, fullUrl, `| Method:`, options?.method || "GET");

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

const auth = {
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
};

const municipis = {
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
  get_activitats: (id: string) => fetchAPI(`/municipis/${id}/activitats`),
  get_llicencia: (id: string) => fetchAPI(`/llicencies?deal_id=${id}`),
};

const contactes = {
  llistar: (params?: Record<string, string>) =>
    fetchAPI(`/contactes?${new URLSearchParams(params || {})}`),
  crear: (data: unknown) => fetchAPI("/contactes", { method: "POST", body: JSON.stringify(data) }),
  editar: (id: string, data: unknown) => fetchAPI(`/contactes/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  eliminar: (id: string) => fetchAPI(`/contactes/${id}`, { method: "DELETE" }),
};

const emails = {
  llistar: (params?: Record<string, string>) => 
    fetchAPI(`/emails?${new URLSearchParams(params || {})}`),
  pendents: () => fetchAPI("/emails?sense_vincular=true"),
  vincular: (id: string, dealId: string) => 
    fetchAPI(`/emails/${id}/deal`, { method: "PATCH", body: JSON.stringify({ deal_id: dealId }) }),
  sync: () => fetchAPI("/emails/sync", { method: "POST" }),
  eliminar: (id: string) => fetchAPI(`/emails/${id}`, { method: "DELETE" }),
  enviar: (data: any) => {
    const mid = data.municipi_id || data.deal_id;
    return fetchAPI(`/emails/enviar_manual/${mid}`, { 
      method: "POST", 
      body: JSON.stringify({
        to: data.to,
        assumpte: data.assumpte,
        cos: data.cos
      }) 
    });
  },
  marcarLlegit: (id: string, llegit: boolean) => 
    fetchAPI(`/emails/${id}/llegit`, { method: "PATCH", body: JSON.stringify({ llegit }) }),
};

const llicencies = {
  llistar: (params?: Record<string, string>) =>
    fetchAPI(`/llicencies?${new URLSearchParams(params || {})}`),
  crear: (data: any) => fetchAPI("/llicencies", { method: "POST", body: JSON.stringify(data) }),
  detall: (id: string) => fetchAPI(`/llicencies/${id}`),
};

const pagaments = {
  llistar: (params?: Record<string, string>) =>
    fetchAPI(`/pagaments?${new URLSearchParams(params || {})}`),
  confirmar: (id: string, data: any) =>
    fetchAPI(`/pagaments/${id}/confirmar`, { method: "PATCH", body: JSON.stringify(data) }),
};

const tasques = {
  llistar: (params?: Record<string, string>) =>
    fetchAPI(`/tasques?${new URLSearchParams(params || {})}`),
  crear: (data: any) => fetchAPI("/tasques", { method: "POST", body: JSON.stringify(data) }),
  editar: (id: string, data: any) => fetchAPI(`/tasques/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  eliminar: (id: string) => fetchAPI(`/tasques/${id}`, { method: "DELETE" }),
};

const dashboard = {
  diari: () => fetchAPI("/dashboard/diari"),
};

const alertes = {
  totes: () => fetchAPI("/alertes"),
  count: () => fetchAPI("/alertes/count"),
};

const usuaris = {
  llistar: () => fetchAPI("/usuaris"),
  crear: (data: any) => fetchAPI("/usuaris", { method: "POST", body: JSON.stringify(data) }),
  editar: (id: string, data: any) => fetchAPI(`/usuaris/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  eliminar: (id: string) => fetchAPI(`/usuaris/${id}`, { method: "DELETE" }),
};


const api = {
  auth,
  municipis,
  contactes,
  emails,
  llicencies,
  pagaments,
  tasques,
  dashboard,
  alertes,
  usuaris
};

export { auth, municipis, contactes, emails, llicencies, pagaments, tasques, dashboard, alertes, usuaris };
export default api;
