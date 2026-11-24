"use client";

import { useState } from "react";
import { UploadDocument } from "@/components/documents/UploadDocument";
import { DocumentList } from "@/components/documents/DocumentList";

export default function DocumentsPage() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadSuccess = () => {
    // Increment to trigger a re-fetch in the DocumentList component
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Documents</h1>
        <p className="text-muted-foreground">
          Upload and manage documents. The AI will answer questions based only on these documents.
        </p>
      </div>

      <UploadDocument onUploadSuccess={handleUploadSuccess} />
      
      <div>
        <h2 className="text-xl font-semibold mb-4">Uploaded Documents</h2>
        <DocumentList refreshTrigger={refreshTrigger} />
      </div>
    </div>
  );
}
