import axios from "axios";


const API_URL = process.env.EXPO_PUBLIC_API_URL || "http://localhost:5000/api";

export const analyzeResume = async (file: any) => {
  const formData = new FormData();

  formData.append("resume", file);

  const response = await axios.post(`${API_URL}/analyze`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};