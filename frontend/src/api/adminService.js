import axiosInstance from './axiosInstance';

export const adminService = {
  // Stats
  async getStats() {
    const response = await axiosInstance.get('/admin/stats/');
    return response.data;
  },

  // Categories CRUD
  async getCategories() {
    const response = await axiosInstance.get('/admin/categories/');
    return response.data;
  },
  async createCategory(data) {
    const response = await axiosInstance.post('/admin/categories/', data);
    return response.data;
  },
  async updateCategory(pk, data) {
    const response = await axiosInstance.patch(`/admin/categories/${pk}/`, data);
    return response.data;
  },
  async deleteCategory(pk) {
    const response = await axiosInstance.delete(`/admin/categories/${pk}/`);
    return response.data;
  },

  // Scenarios CRUD
  async getScenarios(params = {}) {
    const response = await axiosInstance.get('/admin/scenarios/', { params });
    return response.data;
  },
  async createScenario(data) {
    const response = await axiosInstance.post('/admin/scenarios/', data);
    return response.data;
  },
  async updateScenario(pk, data) {
    const response = await axiosInstance.patch(`/admin/scenarios/${pk}/`, data);
    return response.data;
  },
  async deleteScenario(pk) {
    const response = await axiosInstance.delete(`/admin/scenarios/${pk}/`);
    return response.data;
  },

  // Steps CRUD
  async getSteps(scenarioPk) {
    const response = await axiosInstance.get(`/admin/scenarios/${scenarioPk}/steps/`);
    return response.data;
  },
  async createStep(scenarioPk, data) {
    const response = await axiosInstance.post(`/admin/scenarios/${scenarioPk}/steps/`, data);
    return response.data;
  },
  async updateStep(pk, data) {
    const response = await axiosInstance.patch(`/admin/steps/${pk}/`, data);
    return response.data;
  },
  async deleteStep(pk) {
    const response = await axiosInstance.delete(`/admin/steps/${pk}/`);
    return response.data;
  },

  // Options CRUD
  async getOptions(stepPk) {
    const response = await axiosInstance.get(`/admin/steps/${stepPk}/options/`);
    return response.data;
  },
  async createOption(stepPk, data) {
    const response = await axiosInstance.post(`/admin/steps/${stepPk}/options/`, data);
    return response.data;
  },
  async updateOption(pk, data) {
    const response = await axiosInstance.patch(`/admin/options/${pk}/`, data);
    return response.data;
  },
  async deleteOption(pk) {
    const response = await axiosInstance.delete(`/admin/options/${pk}/`);
    return response.data;
  },

  // Objectives CRUD
  async getObjectives(scenarioPk) {
    const response = await axiosInstance.get(`/admin/scenarios/${scenarioPk}/objectives/`);
    return response.data;
  },
  async createObjective(scenarioPk, data) {
    const response = await axiosInstance.post(`/admin/scenarios/${scenarioPk}/objectives/`, data);
    return response.data;
  },
  async updateObjective(pk, data) {
    const response = await axiosInstance.patch(`/admin/objectives/${pk}/`, data);
    return response.data;
  },
  async deleteObjective(pk) {
    const response = await axiosInstance.delete(`/admin/objectives/${pk}/`);
    return response.data;
  },

  // User Management
  async getUsers(params = {}) {
    const response = await axiosInstance.get('/admin/users/', { params });
    return response.data;
  },
  async updateUser(pk, data) {
    const response = await axiosInstance.patch(`/admin/users/${pk}/`, data);
    return response.data;
  },

  // Reports
  async getScenarioReport() {
    const response = await axiosInstance.get('/admin/reports/scenarios/');
    return response.data;
  },
  async getUserReport() {
    const response = await axiosInstance.get('/admin/reports/users/');
    return response.data;
  }
};

export default adminService;
