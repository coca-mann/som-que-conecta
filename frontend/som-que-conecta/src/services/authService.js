console.log("Executando services/authService.js");
import api from './api';

const authService = {
  /**
   * Função para realizar o login.
   * Ela recebe um objeto `credentials` que deve conter o email e a senha.
   * @param {object} credentials - As credenciais do usuário. Ex: { email: 'user@test.com', password: '123' }
   * @returns {Promise} - Retorna a promessa da chamada da API.
   */
  login(credentials) {
    // Faz a requisição POST para o endpoint de token.
    // O segundo argumento (`credentials`) é o corpo (body) da requisição.
    return api.post('/token/', credentials);
  },
  register(userData) {
    // Assumindo que seu endpoint de registro está em /register/
    // O DRF espera snake_case (first_name), então mapeamos aqui se necessário.
    return api.post('/register/', userData);
  },
  getMe() {
    return api.get('/profile/');
  },
  /**
   * Envia o access_token do Google para o backend para login/registro.
   * @param {object} payload - Objeto contendo o token. Ex: { access_token: '...' }
   */
  loginWithGoogle(payload) {
    // O endpoint deve corresponder ao seu urls.py
    return api.post('/auth/social/login/', payload);
  },
  requestPasswordReset(payload) {
    // dj-rest-auth fornece este endpoint por padrão
    return api.post('/auth/password/reset/', payload);
  },
  confirmPasswordReset(payload) {
    // dj-rest-auth fornece este endpoint por padrão
    return api.post('/auth/password/reset/confirm/', payload);
  },
  sendHelpRequest(formData) {
    // A rota /accounts/contact/ vem da combinação da sua URL principal e da URL da app
    return api.post('/contact/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
}
export default authService;