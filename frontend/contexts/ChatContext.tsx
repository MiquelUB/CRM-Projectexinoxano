"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";

interface DealContext {
  id: string;
  titol: string;
  municipiNom?: string;
}

interface ChatContextType {
  dealContext: DealContext | null;
  setDealContext: (context: DealContext) => void;
  clearDealContext: () => void;
  isChatOpen: boolean;
  setIsChatOpen: (open: boolean) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export function ChatProvider({ children }: { children: ReactNode }) {
  const [dealContext, setDealContextState] = useState<DealContext | null>(null);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const setDealContext = (context: DealContext) => {
    setDealContextState(context);
    // Podríem voler obrir el xat automàticament quan s'obre un deal
    // setIsChatOpen(true);
  };

  const clearDealContext = () => {
    setDealContextState(null);
  };

  return (
    <ChatContext.Provider
      value={{
        dealContext,
        setDealContext,
        clearDealContext,
        isChatOpen,
        setIsChatOpen,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChatContext() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error("useChatContext must be used within a ChatProvider");
  }
  return context;
}
