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
    return api.post(`/instruments/${id}/update_with_files/`, instrumentData);
  },

  /**
   * Deleta um instrumento.
   * Corresponde ao `destroy` do seu InstrumentViewSet.
   * @param {number} id - O ID do instrumento.
   */
  deleteInstrument(id) {
    return api.delete(`/instruments/${id}/`);
  },
  /**
   * Busca a lista de todos os tipos de instrumentos cadastrados.
   * Corresponde ao `list` do seu InstrumentTypeViewSet.
   */
  getInstrumentTypes() {
    return api.get('/instrumenttype/');
  },

  /**
   * Busca a lista de todas as marcas de instrumentos cadastradas.
   * Corresponde ao `list` do seu InstrumentBrandsViewSet.
   */
  getInstrumentBrands() {
    return api.get('/instrumentbrand/');
  },
};


export default instrumentService;