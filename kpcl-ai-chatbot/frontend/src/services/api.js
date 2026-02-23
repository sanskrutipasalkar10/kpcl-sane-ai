import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    headers: { 'Content-Type': 'application/json' }
});

export const sendChatMessage = async (message, userId = 'local_user') => {
    try {
        const response = await api.post('/chat', { 
            message: message, 
            user_id: userId 
        });
        return response.data;
    } catch (error) {
        console.error("API Error:", error);
        throw new Error(error.response?.data?.detail || "Failed to connect to the server.");
    }
};