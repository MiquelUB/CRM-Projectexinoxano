"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { format } from "date-fns";
import { Button } from "@/components/ui/button";

export default function EmailsPendentsPage() {
  const [emails, setEmails] = useState<any[]>([]);
  const [deals, setDeals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [emailsRes, dealsRes] = await Promise.all([
        api.emails.pendents(),
        api.municipis.llistar({ limit: "200" })
      ]);
      setEmails(emailsRes.items || []);
      setDeals(dealsRes.items || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const assignarDeal = async (emailId: string, dealId: string) => {
    if (!dealId) return;
    try {
      await api.emails.vincular(emailId, dealId);
      fetchData(); // Refresh after assignment
    } catch (err) {
      alert("Error a l'assignar");
    }
  };

  if (loading) return <div>Carregant pendents...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-[#1B3A6B]">Emails sense vincular (Pendents)</h1>
        <p className="text-gray-500 mt-2">Aquests emails no s'han pogut vincular automàticament a cap deal actiu.</p>
      </div>

      <div className="grid gap-4">
        {emails.map((email) => (
          <div key={email.id} className="bg-white p-4 rounded-lg shadow flex flex-col md:flex-row justify-between md:items-center space-y-4 md:space-y-0">
            <div className="flex-1 mr-4">
              <div className="flex items-center space-x-2">
                <span className="font-semibold">{email.direccio === 'IN' ? 'DE:' : 'PER A:'}</span>
                <span>{email.direccio === 'IN' ? email.from_address : email.to_address}</span>
              </div>
              <h3 className="font-bold text-lg mt-1">{email.assumpte}</h3>
              <p className="text-sm text-gray-500 mt-1">{format(new Date(email.data_email), "dd MMM yyyy")}</p>
            </div>
            <div className="flex flex-col space-y-2 min-w-[300px]">
              <label className="text-sm font-medium">Vincular a:</label>
              <select 
                title="Vincular a deal"
                className="border p-2 rounded-md"
                onChange={(e) => assignarDeal(email.id, e.target.value)}
                defaultValue=""
              >
                <option value="" disabled>Selecciona un Deal...</option>
                {deals.filter(d => d.etapa_actual !== "perdut").map(deal => (
                  <option key={deal.id} value={deal.id}>
                    {deal.nom} ({deal.etapa_actual})
                  </option>
                ))}
              </select>
            </div>
          </div>
        ))}
        {emails.length === 0 && (
          <div className="text-center p-8 bg-gray-50 rounded-lg text-gray-500">Tot al dia! No hi ha emails pendents.</div>
        )}
      </div>
    </div>
  );
}
