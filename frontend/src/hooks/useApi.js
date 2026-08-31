import { useState, useCallback } from 'react';

export const useApi = (apiFunc) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (...args) => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFunc(...args);
      if (res?.success) {
        setData(res.data);
        return { success: true, data: res.data };
      }
      const msg = res?.message || 'Request failed';
      setError(msg);
      return { success: false, message: msg };
    } catch (err) {
      const msg = err.response?.data?.message || 'An unexpected error occurred.';
      setError(msg);
      return { success: false, message: msg };
    } finally {
      setLoading(false);
    }
  }, [apiFunc]);

  return { data, loading, error, execute, setData };
};

export default useApi;
