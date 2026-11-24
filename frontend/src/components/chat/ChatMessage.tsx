"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { User, Bot, FileText } from "lucide-react";
import { Card } from "@/components/ui/card";

interface ChatMessageProps {
  message: {
    id: string;
    role: string;
    content: string;
    metadata?: any;
  };
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex w-full gap-4 p-4 ${isUser ? "bg-background" : "bg-muted/30"}`}>
      <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border bg-background shadow">
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4 text-primary" />}
      </div>
      <div className="flex-1 space-y-2 overflow-hidden">
        <div className="prose prose-sm dark:prose-invert max-w-none">
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          )}
        </div>
        
        {/* Render Citations / Sources */}
        {!isUser && message.metadata?.sources && message.metadata.sources.length > 0 && (
          <div className="mt-4 pt-4 border-t border-border/50">
            <h4 className="text-xs font-semibold text-muted-foreground mb-2 flex items-center gap-1">
              <FileText className="h-3 w-3" /> Sources
            </h4>
            <div className="flex flex-wrap gap-2">
              {message.metadata.sources.map((source: any, idx: number) => (
                <Card key={idx} className="p-2 text-xs bg-muted/50 border-none inline-flex items-center gap-1">
                  <span className="font-medium text-primary">[{source.id}]</span> {source.filename}
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
