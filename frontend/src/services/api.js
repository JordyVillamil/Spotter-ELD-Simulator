import axios from 'axios';

const API_BASE_URL = 'https://spotter-eld-simulator.onrender.com/api/v1';


export const calculateELD = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/calculate-eld/`, data);
    return response.data;
  } catch (error) {
    console.error("Error calling ELD API:", error);
    throw error;
  }
};