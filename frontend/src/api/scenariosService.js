import axiosInstance from './axiosInstance';

export const scenariosService = {
  async getScenarios(params = {}) {
    const response = await axiosInstance.get('/scenarios/', { params });
    return response.data;
  },

  async getScenarioById(id) {
    const response = await axiosInstance.get(`/scenarios/${id}/`);
    return response.data;
  }
};

export default scenariosService;
