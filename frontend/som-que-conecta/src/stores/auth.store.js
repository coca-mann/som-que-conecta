import { defineStore } from 'pinia';
import authService from '@/services/authService';

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        accessToken: localStorage.getItem('accessToken'),
        refreshToken: localStorage.getItem('refreshToken'),
        user: JSON.parse(localStorage.getItem('user')),
    }),
    getters: {
        isAuthenticated: (state) => !!state.accessToken,
        canManageInstrumentDetails: (state) => {
            // Garante que o usuário existe antes de tentar ler a 'role'
            if (!state.user || !state.user.role) {
                return false;
            }
            const restrictedRoles = ['student', 'normal'];
            return !restrictedRoles.includes(state.user.role);
        },
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
        /**
         * --- NOVA AÇÃO DE REGISTRO ---
         * @param {object} userData - Dados do formulário de registro
         */
        async register(userData) {
            try {
                // A resposta agora contém os dados do usuário + tokens
                const response = await authService.register(userData);
                
                // Extraímos os dados e tokens da resposta
                const { access, refresh, ...user } = response.data;

                // Atualizamos o estado e o localStorage, assim como no login
                this.accessToken = access;
                this.refreshToken = refresh;
                this.user = user;

                localStorage.setItem('accessToken', this.accessToken);
                localStorage.setItem('refreshToken', this.refreshToken);
                localStorage.setItem('user', JSON.stringify(this.user));

            } catch (error) {
                // Se der erro, limpa tudo para garantir
                this.logout();
                throw error;
            }
        },
        /**
         * --- NOVA AÇÃO PARA ATUALIZAR O USUÁRIO ---
         * Atualiza os dados do usuário no estado da store e no localStorage.
         * @param {object} newUserData - O objeto de usuário atualizado vindo da API.
         */
        updateUser(newUserData) {
            this.user = newUserData;
            localStorage.setItem('user', JSON.stringify(this.user));
            console.log('Dados do usuário atualizados na store Pinia.');
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