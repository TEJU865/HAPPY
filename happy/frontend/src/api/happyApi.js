import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export async function sendCommand(command) {
  try {
    const response = await axios.post(`${API_BASE_URL}/command`, {
      command,
    });
    return response.data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}
