import axiosInstance from './axiosInstance';

export const simulationService = {
  async startSimulation(scenarioId) {
    const response = await axiosInstance.post('/simulation/start/', { scenario_id: scenarioId });
    return response.data; // { success, data: { session_id, ... } }
  },

  async getSessionState(sessionId) {
    const response = await axiosInstance.get(`/simulation/${sessionId}/`);
    return response.data;
  },

  async respondToStep(sessionId, optionId) {
    const response = await axiosInstance.post(`/simulation/${sessionId}/respond/`, { option_id: optionId });
    return response.data; // { success, data: { was_correct, ... } }
  },

  async getSessionResult(sessionId) {
    const response = await axiosInstance.get(`/simulation/${sessionId}/result/`);
    return response.data;
  }
};

export default simulationService;
