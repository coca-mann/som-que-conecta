// services/profileService.js
import api from './api';

export const getProfile = () => {
  return api.get('/profile/');
};

export const updateProfile = (profileData) => {
  // Para upload de imagem, precisamos usar 'multipart/form-data'
  return api.patch('/profile/', profileData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const getInProgressCourses = () => {
  return api.get('/profile/in-progress-courses/');
};

export const getMyInstruments = () => {
  return api.get('/profile/my-instruments/');
};

export const getRecentActivity = () => {
  return api.get('/profile/recent-activity/');
};

export const getGoals = () => {
  return api.get('/goals/');
};

export const createGoal = (goalData) => {
  // O backend espera 'to_do_date'
  const payload = {
    title: goalData.title,
    description: goalData.description,
    to_do_date: goalData.deadline,
  };
  return api.post('/goals/', payload);
};

export const deleteGoal = (goalId) => {
  // Faz uma requisição DELETE para a URL específica da meta, ex: /api/goals/5/
  return api.delete(`/goals/${goalId}/`);
};
