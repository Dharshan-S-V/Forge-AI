import { apiClient } from "./client";

export const chatApi = {
  createChat: async (title: string) => {
    const response = await apiClient.post("/chats", { title });
    return response.data;
  },
  
  listChats: async () => {
    const response = await apiClient.get("/chats");
    return response.data;
  },
  
  getChat: async (chatId: string) => {
    const response = await apiClient.get(`/chats/${chatId}`);
    return response.data;
  },
  
  sendMessage: async (chatId: string, content: string) => {
    const response = await apiClient.post(`/chats/${chatId}/messages`, { content });
    return response.data;
  },
};
