import axiosInstance from './axiosInstance';

export const categoriesService = {
  async getCategories() {
    const response = await axiosInstance.get('/categories/');
    return response.data;
  },

  async getCategoryBySlug(slug) {
    const response = await axiosInstance.get(`/categories/${slug}/`);
    return response.data;
  }
};

export default categoriesService;
