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

