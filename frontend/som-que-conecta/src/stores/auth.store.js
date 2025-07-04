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
        },
        async loginWithGoogle(googleResponse) {
            try {
                // ETAPA 1: Envia o token do Google e obtém os tokens da NOSSA aplicação
                const tokenResponse = await authService.loginWithGoogle({
                    access_token: googleResponse.access_token,
                });

                // Salva os tokens no estado e no localStorage.
                // Usamos 'access' e 'refresh' para manter a consistência com o login local.
                this.accessToken = tokenResponse.data.access;
                this.refreshToken = tokenResponse.data.refresh;
                localStorage.setItem('accessToken', this.accessToken);
                localStorage.setItem('refreshToken', this.refreshToken);

                // ETAPA 2: Com os tokens salvos, busca os dados completos do usuário.
                // Este passo é idêntico ao do login local e garante que tenhamos o objeto 'user' completo.
                const userResponse = await authService.getMe();

                this.user = userResponse.data;
                localStorage.setItem('user', JSON.stringify(this.user));

            } catch (error) {
                this.logout();
                throw error;
            }
        },
        async requestPasswordReset(payload) {
            // Apenas repassa a chamada para o serviço
            return authService.requestPasswordReset(payload);
        },
        async confirmPasswordReset(payload) {
            // Apenas repassa a chamada para o serviço
            return authService.confirmPasswordReset(payload);
        },
        /**
         * Envia o formulário de ajuda/contato para o backend.
         * @param {FormData} formData - Os dados do formulário, incluindo o anexo.
         */
        sendHelpRequest(formData) {
            // A action apenas repassa a chamada para o serviço. 
            // O componente que a chamou usará 'await' com 'try/catch'
            // para lidar com o sucesso ou o erro da promessa retornada.
            return authService.sendHelpRequest(formData);
        }
    }
});