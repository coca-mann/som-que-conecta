// Em src/services/lessonService.js
import api from './api';

const lessonService = {
  /**
   * Busca a lista de minicursos (lessons).
   * @param {object} params - Parâmetros de filtro (ex: { skill_level: 'BEGINNER' })
   */
  getLessons(params = {}) {
    return api.get('/lessons/', { params });
  },

  /**
   * Busca os detalhes de um minicurso específico.
   * @param {number} lessonId - O ID do minicurso.
   */
  getLesson(id) {
    return api.get(`/lessons/${id}/`);
  },

  getSkillLevels() {
    return api.get('/skill-levels/');
  },

  getInstrumentTypes() {
    return api.get('/instrument-types/');
  },

  /**
   * Marca uma tarefa como concluída.
   * @param {number} taskId - O ID da tarefa.
   */
  completeTask(taskId) {
    return api.post(`/tasks/${taskId}/complete/`);
  },

  /**
   * Desmarca uma tarefa como concluída.
   * @param {number} taskId - O ID da tarefa.
   */
  uncompleteTask(taskId) {
    return api.post(`/tasks/${taskId}/uncomplete/`);
  },

  /**
   * Busca os detalhes de um minicurso específico.
   * @param {number} lessonId - O ID do minicurso.
   */
  getLessonDetail(lessonId) {
    return api.get(`/lessons/${lessonId}/`);
  },
};

export default lessonService;