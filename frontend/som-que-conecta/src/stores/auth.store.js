// src/stores/auth.store.js
import { defineStore } from 'pinia';
import authService from '@/services/authService';
import router from '@/router';

// Usamos `jwt-decode` para extrair informações do token, como o nome do usuário.
// Instale com: npm install jwt-decode
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        // Inicializamos o estado a partir do localStorage para manter o login ao recarregar a página
        accessToken: localStorage.getItem('accessToken'),
        refreshToken: localStorage.getItem('refreshToken'),
        user: JSON.parse(localStorage.getItem('user')),
    }),
    getters: {
        // Um getter para facilmente verificar se o usuário está autenticado
        isAuthenticated: (state) => !!state.accessToken,
    },
    actions: {
        async login(credentials) {
            try {
                const response = await authService.login(credentials);
                const token = response.data.access;
                
                // Decodifica o token para pegar os dados do usuário
                const userData = jwtDecode(token);

                // Atualiza o estado da store
                this.accessToken = token;
                this.refreshToken = response.data.refresh;
                this.user = { 
                    id: userData.user_id,
                    email: userData.email,
                    firstName: userData.first_name 
                };

                // Armazena no localStorage para persistência
                localStorage.setItem('accessToken', this.accessToken);
                localStorage.setItem('refreshToken', this.refreshToken);
                localStorage.setItem('user', JSON.stringify(this.user));

                // Redireciona para a página principal
                router.push('/');

            } catch (error) {
                // Relança o erro para que o componente possa tratá-lo (ex: mostrar uma mensagem)
                throw error;
            }
        },
        logout() {
            // Limpa o estado
            this.accessToken = null;
            this.refreshToken = null;
            this.user = null;

            // Limpa o localStorage
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('user');

            // Redireciona para a página de login
            router.push('/auth');
        }
    }
});