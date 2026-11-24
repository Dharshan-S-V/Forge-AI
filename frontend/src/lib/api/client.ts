import axios from "axios";
import { createClient } from "@/lib/supabase/client";

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL + "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(async (config) => {
  const supabase = createClient();
  const { data } = await supabase.auth.getSession();
  if (data?.session?.access_token) {
    config.headers.Authorization = `Bearer ${data.session.access_token}`;
  }
  return config;
});
