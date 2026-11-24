"use client";

import { MessageSquare, Plus, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { formatDistanceToNow } from "date-fns";

interface ChatSidebarProps {
  chats: any[];
  activeChatId: string | null;
  onSelectChat: (id: string) => void;
  onNewChat: () => void;
  isLoading: boolean;
}

export function ChatSidebar({ chats, activeChatId, onSelectChat, onNewChat, isLoading }: ChatSidebarProps) {
  return (
    <div className="w-64 border-r bg-muted/20 flex flex-col h-[calc(100vh-4rem)]">
      <div className="p-4">
        <Button onClick={onNewChat} className="w-full justify-start gap-2" variant="outline">
          <Plus className="h-4 w-4" />
          New Chat
        </Button>
      </div>
      <Separator />
      <ScrollArea className="flex-1">
        {isLoading ? (
          <div className="flex justify-center p-4">
            <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <div className="p-2 space-y-1">
            {chats.length === 0 ? (
              <p className="text-sm text-center text-muted-foreground p-4">No chats yet</p>
            ) : (
              chats.map((chat) => (
                <Button
                  key={chat.id}
                  variant={activeChatId === chat.id ? "secondary" : "ghost"}
                  className="w-full justify-start font-normal text-left h-auto py-3"
                  onClick={() => onSelectChat(chat.id)}
                >
                  <div className="flex flex-col items-start gap-1 w-full overflow-hidden">
                    <div className="flex items-center gap-2 w-full">
                      <MessageSquare className="h-4 w-4 shrink-0" />
                      <span className="truncate">{chat.title}</span>
                    </div>
                    <span className="text-xs text-muted-foreground pl-6">
                      {formatDistanceToNow(new Date(chat.updated_at), { addSuffix: true })}
                    </span>
                  </div>
                </Button>
              ))
            )}
          </div>
        )}
      </ScrollArea>
    </div>
  );
}
