import { defineStore } from 'pinia';
import authService from '@/services/authService';
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        accessToken: localStorage.getItem('accessToken'),
        refreshToken: localStorage.getItem('refreshToken'),
        user: JSON.parse(localStorage.getItem('user')),
    }),
    getters: {
        isAuthenticated: (state) => !!state.accessToken,
    },
    actions: {
        async login(credentials) {
            try {
                // ETAPA 1: Obter os tokens
                const tokenResponse = await authService.login(credentials);

                this.accessToken = tokenResponse.data.access;
                this.refreshToken = tokenResponse.data.refresh;
                localStorage.setItem('accessToken', this.accessToken);
                localStorage.setItem('refreshToken', this.refreshToken);

                // ETAPA 2: Buscar os dados do usuário
                const userResponse = await authService.getMe();

                this.user = userResponse.data;
                localStorage.setItem('user', JSON.stringify(this.user));

            } catch (error) {
                this.logout(); 
                throw error;
            }
        },
        logout() {
            this.accessToken = null;
            this.refreshToken = null;
            this.user = null;
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('user');
        }
    }
});