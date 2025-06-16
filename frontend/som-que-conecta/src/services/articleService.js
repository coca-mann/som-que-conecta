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
  addComment(payload) {
    // payload: { article: articleId, comment: '...' }
    return api.post('/comments/', payload);
  },
  
  // Para as categorias (usado no filtro)
  getCategories() {
    // Assumindo que você criará um endpoint para categorias
    return api.get('/article-categories/');
  }
};

export default articleService;