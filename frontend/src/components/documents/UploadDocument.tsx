"use client";

import { useState } from "react";
import { UploadCloud, File, X, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { documentsApi } from "@/lib/api/documents";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function UploadDocument({ onUploadSuccess }: { onUploadSuccess: () => void }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const allowedTypes = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ];

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => setIsDragging(false);

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files?.[0];
    if (file) {
      await uploadFile(file);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await uploadFile(file);
    }
  };

  const uploadFile = async (file: File) => {
    if (!allowedTypes.includes(file.type)) {
      toast.error("Unsupported file type. Please upload PDF, DOCX, TXT, or XLSX.");
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      toast.error("File is too large. Maximum size is 50MB.");
      return;
    }

    setIsUploading(true);
    try {
      await documentsApi.uploadDocument(file);
      toast.success("Document uploaded successfully.");
      onUploadSuccess();
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || "Failed to upload document.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-10 text-center transition-colors ${
        isDragging ? "border-primary bg-primary/5" : "border-muted-foreground/25"
      }`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <div className="flex flex-col items-center justify-center gap-4">
        {isUploading ? (
          <Loader2 className="h-10 w-10 animate-spin text-primary" />
        ) : (
          <UploadCloud className="h-10 w-10 text-muted-foreground" />
        )}
        
        <div>
          <h3 className="font-semibold text-lg">
            {isUploading ? "Uploading..." : "Click or drag file to this area to upload"}
          </h3>
          <p className="text-sm text-muted-foreground mt-1">
            Support for a single PDF, DOCX, TXT, or XLSX file. Max size 50MB.
          </p>
        </div>

        <div className="mt-4">
          <input
            type="file"
            id="file-upload"
            className="hidden"
            accept=".pdf,.docx,.txt,.xlsx"
            onChange={handleFileChange}
            disabled={isUploading}
          />
          <label
            htmlFor="file-upload"
            className={cn(
              buttonVariants({ variant: "outline" }),
              "cursor-pointer",
              isUploading && "pointer-events-none opacity-50"
            )}
          >
            Select File
          </label>
        </div>
      </div>
    </div>
  );
}
