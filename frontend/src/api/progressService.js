import axiosInstance from './axiosInstance';

export const progressService = {
  async getDashboard() {
    const response = await axiosInstance.get('/progress/dashboard/');
    return response.data;
  },

  async getSessions() {
    const response = await axiosInstance.get('/progress/sessions/');
    return response.data;
  },

  async getBadges() {
    const response = await axiosInstance.get('/progress/badges/');
    return response.data;
  },

  async getAllBadges() {
    const response = await axiosInstance.get('/progress/all-badges/');
    return response.data;
  },

  async getXPHistory() {
    const response = await axiosInstance.get('/progress/xp-history/');
    return response.data;
  },

  async getLearningStats() {
    const response = await axiosInstance.get('/progress/stats/');
    return response.data;
  }
};

export default progressService;
