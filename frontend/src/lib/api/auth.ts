import { apiClient } from "./client";

export const authApi = {
  register: async (data: any) => {
    const response = await apiClient.post("/auth/register", data);
    return response.data;
  },
  login: async (data: any) => {
    const response = await apiClient.post("/auth/login", data);
    return response.data;
  },
  logout: async () => {
    const response = await apiClient.post("/auth/logout");
    return response.data;
  },
  getMe: async () => {
    const response = await apiClient.get("/auth/me");
    return response.data;
  },
};
