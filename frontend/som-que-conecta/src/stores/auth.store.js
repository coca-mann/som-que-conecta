console.log("Executando stores/auth.store.js");
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
                const response = await authService.login(credentials);
                const token = response.data.access;
                const userData = jwtDecode(token);

                this.accessToken = token;
                this.refreshToken = response.data.refresh;
                this.user = { 
                    id: userData.user_id,
                    email: userData.email,
                    firstName: userData.first_name 
                };

                localStorage.setItem('accessToken', this.accessToken);
                localStorage.setItem('refreshToken', this.refreshToken);
                localStorage.setItem('user', JSON.stringify(this.user));
            } catch (error) {
                // --- AQUI ESTÁ A MUDANÇA ---
                // Em vez de chamar this.logout(), limpamos o estado diretamente
                // para evitar problemas de referência interna na inicialização.
                this.accessToken = null;
                this.refreshToken = null;
                this.user = null;
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                localStorage.removeItem('user');
                
                // Relança o erro para que o componente que chamou possa tratá-lo.
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