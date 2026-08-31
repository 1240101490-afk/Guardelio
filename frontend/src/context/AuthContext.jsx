import React, { createContext, useState, useEffect, useContext } from 'react';
import authService from '../api/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const storedUser = localStorage.getItem('user');
      return storedUser ? JSON.parse(storedUser) : null;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const accessToken = localStorage.getItem('access_token');
      if (accessToken) {
        try {
          const res = await authService.getProfile();
          if (res?.success && res?.data) {
            setUser(res.data);
            localStorage.setItem('user', JSON.stringify(res.data));
          }
        } catch (err) {
          // If fetch fails (e.g. token expired/invalid), axios interceptor handles refresh.
          // If refresh fails too, it logs out.
          console.error('Failed to load profile on mount:', err);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    try {
      const res = await authService.login(username, password);
      if (res?.success && res?.data) {
        const { access, refresh, user: userData } = res.data;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
        return { success: true };
      }
      return { success: false, message: res?.message || 'Login failed' };
    } catch (err) {
      return {
        success: false,
        message: err.response?.data?.message || 'Invalid username or password.',
        errors: err.response?.data?.errors
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        await authService.logout(refreshToken);
      } catch (err) {
        console.error('Logout error on backend:', err);
      }
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  const updateProfile = async (updatedData) => {
    try {
      const res = await authService.updateProfile(updatedData);
      if (res?.success && res?.data) {
        setUser(res.data);
        localStorage.setItem('user', JSON.stringify(res.data));
        return { success: true };
      }
      return { success: false, message: res?.message || 'Update failed' };
    } catch (err) {
      return {
        success: false,
        message: err.response?.data?.message || 'Profile update failed.',
        errors: err.response?.data?.errors
      };
    }
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'admin' || user?.is_staff === true,
    loading,
    login,
    logout,
    updateProfile
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
