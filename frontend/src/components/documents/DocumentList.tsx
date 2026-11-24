"use client";

import { useEffect, useState } from "react";
import { FileText, Trash2, Loader2, AlertCircle } from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import { toast } from "sonner";

import { documentsApi } from "@/lib/api/documents";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function DocumentList({ refreshTrigger }: { refreshTrigger: number }) {
  const [documents, setDocuments] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDocuments();
  }, [refreshTrigger]);

  const fetchDocuments = async () => {
    setIsLoading(true);
    try {
      const data = await documentsApi.listDocuments();
      setDocuments(data.documents);
    } catch (error) {
      toast.error("Failed to fetch documents.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this document?")) return;
    
    try {
      await documentsApi.deleteDocument(id);
      toast.success("Document deleted.");
      fetchDocuments();
    } catch (error) {
      toast.error("Failed to delete document.");
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return <Badge className="bg-green-500">Processed</Badge>;
      case "processing":
        return <Badge variant="secondary" className="animate-pulse">Processing</Badge>;
      case "failed":
        return <Badge variant="destructive">Failed</Badge>;
      default:
        return <Badge variant="outline">Uploaded</Badge>;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  if (isLoading) {
    return (
      <div className="flex justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-center border rounded-md bg-muted/20">
        <AlertCircle className="h-10 w-10 text-muted-foreground mb-4" />
        <h3 className="text-lg font-medium">No documents yet</h3>
        <p className="text-sm text-muted-foreground mt-1">
          Upload your first document above to get started.
        </p>
      </div>
    );
  }

  return (
    <div className="border rounded-md">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Filename</TableHead>
            <TableHead>Size</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Uploaded</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {documents.map((doc) => (
            <TableRow key={doc.id}>
              <TableCell className="font-medium flex items-center gap-2">
                <FileText className="h-4 w-4 text-muted-foreground" />
                {doc.original_filename}
              </TableCell>
              <TableCell className="text-muted-foreground">
                {formatFileSize(doc.file_size)}
              </TableCell>
              <TableCell>{getStatusBadge(doc.status)}</TableCell>
              <TableCell className="text-muted-foreground">
                {formatDistanceToNow(new Date(doc.created_at), { addSuffix: true })}
              </TableCell>
              <TableCell className="text-right">
                <Button
                  variant="ghost"
                  size="icon"
                  className="text-destructive hover:bg-destructive/10 hover:text-destructive"
                  onClick={() => handleDelete(doc.id)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
