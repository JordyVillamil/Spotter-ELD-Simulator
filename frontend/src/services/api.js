import axios from 'axios';

// Base URL apuntando a producción en Render
const API_BASE_URL = 'https://spotter-eld-simulator.onrender.com/api/v1';
// const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const calculateELD = async (data) => {
  try {
    // Usamos template literals (comillas invertidas) para unir la base con la ruta final
    const response = await axios.post(`${API_BASE_URL}/calculate-eld/`, data);
    return response.data;
  } catch (error) {
    console.error("Error calling ELD API:", error);
    throw error;
  }
};