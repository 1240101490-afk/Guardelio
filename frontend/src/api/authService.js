import axiosInstance from './axiosInstance';

export const authService = {
  async login(username, password) {
    const response = await axiosInstance.post('/auth/login/', { username, password });
    return response.data; // { success, data: { access, refresh, user } }
  },

  async register(data) {
    const response = await axiosInstance.post('/auth/register/', data);
    return response.data; // { success, data: { ...user }, message }
  },

  async logout(refreshToken) {
    const response = await axiosInstance.post('/auth/logout/', { refresh: refreshToken });
    return response.data;
  },

  async getProfile() {
    const response = await axiosInstance.get('/auth/me/');
    return response.data;
  },

  async updateProfile(data) {
    const response = await axiosInstance.patch('/auth/me/', data);
    return response.data;
  }
};

export default authService;
