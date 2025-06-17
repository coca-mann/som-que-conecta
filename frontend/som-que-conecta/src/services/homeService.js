import api from './api';

const homeService = {
  /**
   * Busca os dados da página inicial de forma concorrente
   */
  getHomePageData() {
    return Promise.all([
      api.get('/articles/latest/'),
      api.get('/lessons/latest/')
    ]);
  },

  /**
   * Constrói a URL completa para uma imagem
   * @param {string} imagePath - Caminho relativo ou URL completa da imagem
   * @returns {string} URL completa da imagem
   */
  getImageUrl(imagePath) {
    if (!imagePath) return null;
    // Se a URL já começa com http, retorna ela mesma
    if (imagePath.startsWith('http')) return imagePath;
    // Caso contrário, constrói a URL completa
    return `${api.defaults.baseURL.replace('/api/', '')}${imagePath}`;
  }
};

export default homeService;