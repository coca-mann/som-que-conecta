import api from './api'; // Usando sua instância do Axios

const articleService = {
  // Para a página de lista de artigos
  getArticles(params) {
    // params pode ser { category: 'Teoria', search: 'piano', ordering: '-created_at' }
    return api.get('/articles/', { params });
  },

  // Para a página de detalhes
  getArticleDetail(articleId) {
    return api.get(`/articles/${articleId}/`);
  },

  // Para a página de criação
  createArticle(formData) {
    // Usamos FormData por causa do upload de imagem
    return api.post('/articles/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  // Para a página de edição
  updateArticle(articleId, formData) {
    return api.patch(`/articles/${articleId}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  // Para os comentários
  addComment(articleId, comment) {
    return api.post(`/articles/${articleId}/add_comment/`, { comment });
  },
  
  // Para as categorias (usado no filtro)
  getCategories() {
    // Assumindo que você criará um endpoint para categorias
    return api.get('/article-categories/');
  },

  // Para favoritos
  checkFavorite(articleId) {
    return api.get(`/articles/${articleId}/check_favorite/`);
  },

  addFavorite(articleId) {
    return api.post(`/articles/${articleId}/favorite/`);
  },

  unfavorite(articleId) {
    return api.delete(`/articles/${articleId}/unfavorite/`);
  },

  async getComments(articleId) {
    return await api.get(`/articles/${articleId}/comments/`);
  },

  async rateArticle(articleId, rating) {
    return await api.post(`/articles/${articleId}/rate/`, { rating });
  },

  async checkRating(articleId) {
    return await api.get(`/articles/${articleId}/check_rating/`);
  },

  async removeRating(articleId) {
    return await api.delete(`/articles/${articleId}/remove_rating/`);
  }
};

export default articleService;