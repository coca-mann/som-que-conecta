// src/services/api.js
import axios from 'axios';

// NENHUMA importação do auth.store aqui no topo

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    headers: {
    'Content-Type': 'application/json',
    },
});

// Interceptor de REQUEST: Esta parte está perfeita e não precisa mudar.
// Ele lê o token do localStorage, que não cria dependência com o store.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de RESPONSE: Aqui faremos o ajuste.
api.interceptors.response.use(
  (response) => {
    // Se a resposta for bem-sucedida, não fazemos nada.
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // Verificamos se o erro é 401 e se ainda não tentamos o refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // A lógica de tentar o refresh do token está perfeita.
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
            // Se não houver refresh token, não há como continuar. Deslogue.
            throw new Error("No refresh token found");
        }
        const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', {
          refresh: refreshToken,
        });

        const newAccessToken = response.data.access;
        localStorage.setItem('accessToken', newAccessToken);
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;

        return api(originalRequest);

      } catch (refreshError) {
        // --- AQUI ESTÁ A MUDANÇA ---
        // Se a atualização do token falhar (ex: refresh token expirado ou inválido),
        // deslogamos o usuário usando o store de forma centralizada.
        console.error("Refresh token is invalid or expired. Logging out.", refreshError);
        
        // 1. Importa o store dinamicamente para quebrar o ciclo de dependência
        const { useAuthStore } = await import('@/stores/auth.store');
        const authStore = useAuthStore();

        // 2. Chama a ação de logout centralizada
        authStore.logout();

        // 3. As linhas antigas que faziam isso manualmente são removidas
        // localStorage.removeItem('accessToken');
        // localStorage.removeItem('refreshToken');
        // window.location.href = '/login'; 

        return Promise.reject(refreshError);
      }
    }

    // Para todos os outros erros, apenas os rejeita.
    return Promise.reject(error);
  }
);


export default api;