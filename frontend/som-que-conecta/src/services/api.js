// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Sua URL base
});

// Interceptor para adicionar o ACCESS TOKEN em cada requisição
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      // Padrão JWT é usar o prefixo 'Bearer'
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Lógica mais avançada para atualizar o token (opcional, mas recomendado)
// O interceptor de resposta lida com o caso de um access token expirado.
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    // Se o erro for 401 (Não Autorizado) e ainda não tentamos atualizar o token
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', {
          refresh: refreshToken,
        });

        const newAccessToken = response.data.access;
        localStorage.setItem('accessToken', newAccessToken);

        // Atualiza o cabeçalho da requisição original com o novo token
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;

        // Tenta a requisição original novamente
        return api(originalRequest);

      } catch (refreshError) {
        // Se a atualização falhar, deslogue o usuário
        console.error("Refresh token is invalid. Logging out.", refreshError);
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        // Redireciona para a página de login
        window.location.href = '/login'; 
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);


export default api;