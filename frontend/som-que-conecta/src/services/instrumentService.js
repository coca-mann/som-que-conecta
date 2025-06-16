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
   * ATUALIZAÇÃO PARCIAL: Usado para alterar apenas campos específicos,
   * como o status 'is_active'.
   * @param {number} id O ID do instrumento.
   * @param {object} data Os dados a serem atualizados. Ex: { is_active: false }
   */
  patchInstrument(id, data) {
    return api.patch(`/instruments/${id}/`, data);
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

  getPublicInstruments() {
    return api.get('/instruments-public-list/');
  },

  createBooking(bookingData) {
    // A URL agora aponta para a raiz do ViewSet, como definido pelo DefaultRouter
    return api.post('/bookings/', bookingData);
  },

  getBookings() {
    return api.get('/bookings/');
  },
  
  updateBookingStatus(bookingId, status, reason = '') {
    // O serializer de update espera um objeto com o status
    const payload = { 
      status: status,
      reservation_refusal_reason: reason
    };
    return apiClient.patch(`/bookings/${bookingId}/`, payload);
  }
  
};


export default instrumentService;