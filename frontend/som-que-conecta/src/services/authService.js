console.log("Executando services/authService.js");
import api from './api';

/**
 * Criamos um objeto `authService` que agrupará todas as funções
 * relacionadas à autenticação.
 */
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
  }

  // No futuro, você pode adicionar outras funções aqui:
  //
  // register(userData) {
  //   return api.post('/register/', userData);
  // },
  //
  // logout() {
  //   // ...
  // }
};

/**
 * Exportamos o objeto authService para que ele possa ser importado
 * e utilizado em qualquer componente da nossa aplicação.
 */
export default authService;