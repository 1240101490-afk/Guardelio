import React, { createContext, useState, useContext } from 'react';
import simulationService from '../api/simulationService';

const SimulationContext = createContext(null);

export const SimulationProvider = ({ children }) => {
  const [activeSession, setActiveSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const startSession = async (scenarioId) => {
    setLoading(true);
    setError(null);
    try {
      const res = await simulationService.startSimulation(scenarioId);
      if (res?.success && res?.data) {
        setActiveSession(res.data);
        return { success: true, sessionId: res.data.session_id };
      }
      return { success: false, message: res?.message || 'Failed to start simulation.' };
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to start simulation.';
      setError(msg);
      return { success: false, message: msg };
    } finally {
      setLoading(false);
    }
  };

  const loadSession = async (sessionId) => {
    setLoading(true);
    setError(null);
    try {
      const res = await simulationService.getSessionState(sessionId);
      if (res?.success && res?.data) {
        setActiveSession(res.data);
        return { success: true, session: res.data };
      }
      return { success: false, message: res?.message || 'Failed to load session.' };
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to load session.';
      setError(msg);
      return { success: false, message: msg };
    } finally {
      setLoading(false);
    }
  };

  const submitResponse = async (sessionId, optionId) => {
    setLoading(true);
    setError(null);
    try {
      const res = await simulationService.respondToStep(sessionId, optionId);
      if (res?.success && res?.data) {
        // Option response yields feedback, consequence, XP, and optionally the updated session or next step
        // We can reload session state afterwards, or merge the response
        return { success: true, responseData: res.data };
      }
      return { success: false, message: res?.message || 'Failed to submit response.' };
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to submit response.';
      setError(msg);
      return { success: false, message: msg };
    } finally {
      setLoading(false);
    }
  };

  const clearSession = () => {
    setActiveSession(null);
    setError(null);
  };

  const value = {
    activeSession,
    loading,
    error,
    startSession,
    loadSession,
    submitResponse,
    clearSession,
    setActiveSession
  };

  return <SimulationContext.Provider value={value}>{children}</SimulationContext.Provider>;
};

export const useSimulation = () => {
  const context = useContext(SimulationContext);
  if (!context) {
    throw new Error('useSimulation must be used within a SimulationProvider');
  }
  return context;
};
