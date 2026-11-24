import { apiClient } from "./client";

export const documentsApi = {
  uploadDocument: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    
    const response = await apiClient.post("/documents/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },
  
  listDocuments: async () => {
    const response = await apiClient.get("/documents");
    return response.data;
  },
  
  deleteDocument: async (id: string) => {
    const response = await apiClient.delete(`/documents/${id}`);
    return response.data;
  },
};
