"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Users, UserSquare2, BriefcaseIcon, LogOut, Mail, MailOpen, CreditCard, Shield } from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();

  const handleLogout = () => {
    sessionStorage.removeItem("token");
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT";
    window.location.href = "/login";
  };

  const menu = [
    { name: "Dashboard", icon: LayoutDashboard, href: "/dashboard" },
    { name: "Municipis", icon: Users, href: "/municipis" },
    { name: "Contactes", icon: UserSquare2, href: "/contactes" },
    { name: "Deals", icon: BriefcaseIcon, href: "/deals" },
    { name: "Emails", icon: Mail, href: "/emails" },
    { name: "Pendents", icon: MailOpen, href: "/emails/pendents" },
    { name: "Pagaments", icon: CreditCard, href: "/pagaments" },
    { name: "Configuració", icon: Shield, href: "/configuracio" },
  ];

  return (
    <div className="w-72 premium-sidebar min-h-screen flex flex-col fixed left-0 top-0 z-50">
      <div className="p-8">
        <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm border border-white/10">
                <span className="text-xl font-bold">P</span>
            </div>
            <div>
                <h2 className="text-xl font-bold tracking-tight">CRM PXX</h2>
                <p className="text-[10px] uppercase tracking-widest text-blue-300 font-semibold">Admin Panel</p>
            </div>
        </div>
      </div>

      <nav className="flex-1 px-4 space-y-1.5 mt-4">
        {menu.map((item) => {
          const isActive = item.href === "/emails" 
            ? pathname === "/emails" 
            : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center space-x-3 px-4 py-3.5 rounded-xl transition-all duration-200 group ${
                isActive 
                  ? "nav-item-active text-white" 
                  : "text-blue-100/70 hover:bg-white/5 hover:text-white"
              }`}
            >
              <item.icon className={`w-5 h-5 transition-transform group-hover:scale-110 ${isActive ? "text-white" : "text-blue-200/50"}`} />
              <span className="font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-6 mt-auto border-t border-white/10 space-y-4">
        <div className="flex items-center space-x-3 px-2">
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-400 to-indigo-500 border-2 border-white/20 shadow-inner" />
            <div className="flex-1 overflow-hidden">
                <p className="text-sm font-bold text-white truncate">Albert Martí</p>
                <p className="text-xs text-blue-300 truncate">Administrador</p>
            </div>
        </div>
        <button
          onClick={handleLogout}
          className="flex items-center space-x-3 px-4 py-3 w-full text-blue-100 hover:bg-red-500/20 hover:text-red-300 rounded-xl transition-all duration-200 group"
        >
          <LogOut className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
          <span className="font-medium text-sm">Tancar Sessió</span>
        </button>
      </div>
    </div>
  );
}
