import api from './api'; // Importamos nossa instância configurada do Axios

const instrumentService = {
  /**
   * Busca a lista de instrumentos do usuário logado.
   * Corresponde ao `list` do seu InstrumentViewSet.
   */
  getInstruments() {
    return api.get('/instruments/');
  },

  /**
   * Cria um novo instrumento.
   * Corresponde ao `create` do seu InstrumentViewSet.
   * @param {object} instrumentData - Os dados do formulário.
   */
  createInstrument(instrumentData) {
    return api.post('/instruments/', instrumentData);
  },

  /**
   * Atualiza um instrumento existente.
   * Corresponde ao `update` do seu InstrumentViewSet.
   * @param {number} id - O ID do instrumento.
   * @param {object} instrumentData - Os dados do formulário.
   */
  updateInstrument(id, instrumentData) {
    return api.put(`/instruments/${id}/`, instrumentData);
  },

  /**
   * Deleta um instrumento.
   * Corresponde ao `destroy` do seu InstrumentViewSet.
   * @param {number} id - O ID do instrumento.
   */
  deleteInstrument(id) {
    return api.delete(`/instruments/${id}/`);
  },
  
  // No futuro, você pode adicionar chamadas para buscar Marcas e Tipos
  // getInstrumentTypes() { ... }
  // getInstrumentBrands() { ... }
};

export default instrumentService;