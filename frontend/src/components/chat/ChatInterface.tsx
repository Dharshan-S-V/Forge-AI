"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2 } from "lucide-react";
import { toast } from "sonner";

import { chatApi } from "@/lib/api/chat";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ChatMessage } from "./ChatMessage";

interface ChatInterfaceProps {
  chatId: string | null;
  initialMessages: any[];
}

export function ChatInterface({ chatId, initialMessages }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<any[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMessages(initialMessages);
  }, [initialMessages]);

  useEffect(() => {
    // Scroll to bottom on new messages
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isSending]);

  const handleSend = async () => {
    if (!input.trim() || !chatId || isSending) return;

    const userMessage = {
      id: "temp-" + Date.now(),
      role: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsSending(true);

    try {
      const aiResponse = await chatApi.sendMessage(chatId, userMessage.content);
      
      setMessages((prev) => [
        // replace temp message with real one if needed, or just append AI response
        // In a real app we'd fetch the whole chat or replace temp with server response for user msg.
        ...prev,
        aiResponse
      ]);
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || "Failed to send message.");
      // Remove the temp message on failure
      setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!chatId) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-muted-foreground p-8 text-center">
        <div className="max-w-md space-y-4">
          <h3 className="text-2xl font-semibold text-foreground">Welcome to ForgeAI Copilot</h3>
          <p>
            Select a chat from the sidebar or create a new one to start interacting with your enterprise knowledge base.
          </p>
          <p className="text-sm">
            Answers are generated strictly from the documents you have uploaded in the Documents tab.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-4rem)]">
      <ScrollArea className="flex-1 p-4" ref={scrollRef}>
        <div className="max-w-3xl mx-auto space-y-4 pb-20">
          {messages.length === 0 ? (
            <div className="text-center text-muted-foreground mt-20">
              No messages yet. Send a message to start the conversation!
            </div>
          ) : (
            messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))
          )}
          {isSending && (
            <div className="flex w-full gap-4 p-4 bg-muted/30">
              <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border bg-background shadow">
                <Loader2 className="h-4 w-4 animate-spin text-primary" />
              </div>
              <div className="flex-1 space-y-2">
                <p className="text-sm text-muted-foreground animate-pulse">
                  Analyzing documents...
                </p>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>
      
      <div className="border-t bg-background p-4">
        <div className="max-w-3xl mx-auto flex items-end gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your documents..."
            className="min-h-[60px] max-h-[200px] resize-none"
            disabled={isSending}
          />
          <Button 
            size="icon" 
            className="h-[60px] w-[60px] shrink-0" 
            onClick={handleSend}
            disabled={!input.trim() || isSending}
          >
            <Send className="h-5 w-5" />
            <span className="sr-only">Send message</span>
          </Button>
        </div>
      </div>
    </div>
  );
}
