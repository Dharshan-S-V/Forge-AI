"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { chatApi } from "@/lib/api/chat";
import { ChatSidebar } from "@/components/chat/ChatSidebar";
import { ChatInterface } from "@/components/chat/ChatInterface";

export default function ChatPage() {
  const [chats, setChats] = useState<any[]>([]);
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const [activeChatMessages, setActiveChatMessages] = useState<any[]>([]);
  const [isLoadingSidebar, setIsLoadingSidebar] = useState(true);

  useEffect(() => {
    fetchChats();
  }, []);

  useEffect(() => {
    if (activeChatId) {
      loadChat(activeChatId);
    } else {
      setActiveChatMessages([]);
    }
  }, [activeChatId]);

  const fetchChats = async () => {
    setIsLoadingSidebar(true);
    try {
      const data = await chatApi.listChats();
      setChats(data);
    } catch (error) {
      toast.error("Failed to load chat history.");
    } finally {
      setIsLoadingSidebar(false);
    }
  };

  const loadChat = async (id: string) => {
    try {
      const data = await chatApi.getChat(id);
      setActiveChatMessages(data.messages || []);
    } catch (error) {
      toast.error("Failed to load chat details.");
      setActiveChatId(null);
    }
  };

  const handleNewChat = async () => {
    try {
      const title = `New Chat ${new Date().toLocaleTimeString()}`;
      const newChat = await chatApi.createChat(title);
      setChats([newChat, ...chats]);
      setActiveChatId(newChat.id);
    } catch (error) {
      toast.error("Failed to create a new chat.");
    }
  };

  return (
    <div className="flex h-full -mx-6 -my-6 bg-background">
      <ChatSidebar 
        chats={chats}
        activeChatId={activeChatId}
        onSelectChat={setActiveChatId}
        onNewChat={handleNewChat}
        isLoading={isLoadingSidebar}
      />
      <ChatInterface 
        chatId={activeChatId}
        initialMessages={activeChatMessages}
      />
    </div>
  );
}
