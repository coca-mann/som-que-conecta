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