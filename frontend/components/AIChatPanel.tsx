"use client";

import React, { useState, useEffect, useRef } from "react";
import { 
  MessageSquare, 
  X, 
  Send, 
  Minus, 
  Maximize2, 
  Bot, 
  User, 
  Loader2, 
  Sparkles,
  Link as LinkIcon,
  ChevronRight
} from "lucide-react";
import { useChatContext } from "@/contexts/ChatContext";
import api from "@/lib/api";
import { format } from "date-fns";
import { ca } from "date-fns/locale";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  accions_suggerides?: string[];
}

export function AIChatPanel() {
  const { dealContext, isChatOpen, setIsChatOpen, clearDealContext } = useChatContext();
  const [isExpanded, setIsExpanded] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Carregar historial quan canvia el dealContext
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const res = await api.agent.getMemory({ 
          deal_id: dealContext?.id 
        });
        
        if (res && res.history) {
          const formattedMessages = res.history.map((m: any) => ({
            ...m,
            timestamp: m.timestamp ? new Date(m.timestamp) : new Date()
          }));
          setMessages(formattedMessages);
        } else {
          // Missatge de benvinguda si no hi ha historial
          const welcomeMsg = dealContext 
            ? `Hola! Soc l'agent Kimi K2. Estic analitzant el deal **${dealContext.titol}**. En què et puc ajudar?`
            : "Hola! Soc l'agent Kimi K2, el teu assistent d'estratègia CRM. Com et puc ajudar avui?";
          
          setMessages([{
            role: "assistant",
            content: welcomeMsg,
            timestamp: new Date()
          }]);
        }
      } catch (err) {
        console.error("Error carregant historial:", err);
      }
    };

    loadHistory();
  }, [dealContext]);

  // Scroll automàtic al final
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading, isExpanded]);

  const handleSendMessage = async (e?: React.FormEvent, customText?: string) => {
    if (e) e.preventDefault();
    const text = customText || inputValue;
    if (!text.trim() || isLoading) return;

    const userMsg: Message = {
      role: "user",
      content: text,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await api.agent.chat({
        message: text,
        deal_id: dealContext?.id
      });

      const assistantMsg: Message = {
        role: "assistant",
        content: response.response,
        timestamp: new Date(),
        accions_suggerides: response.accions_suggerides
      };

      setMessages(prev => [...prev, assistantMsg]);
    } catch (err) {
      console.error("Error en el xat:", err);
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Ho sento, hi ha hagut un error en processar la teva petició. Torna-ho a provar en un moment.",
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const togglePanel = () => {
    setIsExpanded(!isExpanded);
    if (!isExpanded) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  if (!isExpanded) {
    return (
      <div 
        onClick={togglePanel}
        className="fixed bottom-6 right-6 z-50 group transition-all duration-300 transform hover:scale-105"
      >
        <div className="relative">
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
          <button className="relative flex items-center space-x-3 bg-white px-5 py-3.5 rounded-2xl shadow-xl border border-blue-50">
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-tr from-blue-600 to-indigo-700 rounded-xl flex items-center justify-center text-white shadow-lg">
                <Bot className="w-6 h-6" />
              </div>
              <div className="absolute -top-1 -right-1 w-3.5 h-3.5 bg-green-500 border-2 border-white rounded-full"></div>
            </div>
            <div className="flex flex-col items-start pr-2">
              <span className="text-sm font-bold text-slate-800">Kimi K2</span>
              <span className="text-[10px] text-slate-400 font-medium uppercase tracking-wider tabular-nums">Online</span>
            </div>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 w-[400px] h-[600px] flex flex-col bg-white rounded-3xl shadow-2xl border border-blue-100/50 overflow-hidden animate-in slide-in-from-bottom-4 duration-300">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-5 flex items-center justify-between text-white shrink-0">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center backdrop-blur-md border border-white/20">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold tracking-tight">Agent Kimi K2</h3>
              <Sparkles className="w-3.5 h-3.5 text-blue-200 fill-blue-200" />
            </div>
            {dealContext ? (
              <div className="flex items-center space-x-1.5 bg-white/10 px-2 py-0.5 rounded-md mt-0.5 border border-white/5">
                <LinkIcon className="w-2.5 h-2.5 text-blue-200" />
                <span className="text-[10px] font-semibold text-blue-50 truncate max-w-[150px]">
                  {dealContext.titol}
                </span>
              </div>
            ) : (
              <p className="text-[10px] text-blue-200 font-medium uppercase tracking-widest">Global CRM Assistant</p>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-1">
          <button 
            onClick={togglePanel}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <Minus className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-5 space-y-4 bg-slate-50/50 scroll-smooth"
      >
        {messages.map((msg, i) => (
          <div 
            key={i} 
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div className={`max-w-[85%] flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}>
              <div className={`
                p-4 rounded-2xl text-sm leading-relaxed shadow-sm
                ${msg.role === "user" 
                  ? "bg-blue-600 text-white rounded-tr-none" 
                  : "bg-white text-slate-700 border border-blue-50 rounded-tl-none"}
              `}>
                <div className="whitespace-pre-wrap">{msg.content}</div>
                
                {msg.accions_suggerides && msg.accions_suggerides.length > 0 && (
                  <div className="mt-4 flex flex-wrap gap-2 pt-3 border-t border-slate-100">
                    {msg.accions_suggerides.map((action, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSendMessage(undefined, action)}
                        className="text-[10px] font-bold bg-blue-50 text-blue-600 px-3 py-1.5 rounded-full border border-blue-100 hover:bg-blue-600 hover:text-white transition-all flex items-center space-x-1"
                      >
                        <span>{action}</span>
                        <ChevronRight className="w-3 h-3" />
                      </button>
                    ))}
                  </div>
                )}
              </div>
              <span className="text-[10px] text-slate-400 mt-1.5 font-medium px-1 uppercase tracking-tighter tabular-nums">
                {format(msg.timestamp, "HH:mm", { locale: ca })}
              </span>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-blue-50 p-4 rounded-2xl rounded-tl-none shadow-sm">
              <div className="flex space-x-1">
                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce"></div>
                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 bg-white border-t border-slate-100 shrink-0">
        <form 
          onSubmit={handleSendMessage}
          className="relative flex items-center bg-slate-100/50 rounded-2xl border border-slate-200 p-1.5 focus-within:border-blue-400 focus-within:ring-2 focus-within:ring-blue-100 transition-all"
        >
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
            placeholder={dealContext ? "Pregunta sobre aquest deal..." : "Pregunta a Kimi..."}
            className="flex-1 bg-transparent border-none focus:ring-0 text-sm py-2 px-3 text-slate-700 placeholder:text-slate-400"
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className={`
              p-2.5 rounded-xl transition-all
              ${!inputValue.trim() || isLoading 
                ? "text-slate-300 bg-transparent" 
                : "text-white bg-blue-600 hover:bg-blue-700 hover:scale-105 active:scale-95 shadow-md shadow-blue-200"}
            `}
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
          </button>
        </form>
        <p className="text-[9px] text-center text-slate-400 mt-2.5 font-medium uppercase tracking-widest opacity-70">
          Powered by Kimi K2 Doctrine
        </p>
      </div>
    </div>
  );
}
