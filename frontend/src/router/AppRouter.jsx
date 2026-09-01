import React from 'react';
import { Routes, Route, Navigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Loader from '../components/common/Loader';

// Lazy load page components or import directly (directly is faster to bundle in development)
import LandingPage from '../pages/LandingPage';
import LoginPage from '../pages/auth/LoginPage';
import RegisterPage from '../pages/auth/RegisterPage';

import DashboardPage from '../pages/student/DashboardPage';
import CategoriesPage from '../pages/student/CategoriesPage';
import CategoryDetailPage from '../pages/student/CategoryDetailPage';
import ScenarioOverviewPage from '../pages/student/ScenarioOverviewPage';
import SimulationPage from '../pages/simulation/SimulationPage';
import ResultsPage from '../pages/simulation/ResultsPage';
import ProgressPage from '../pages/student/ProgressPage';
import ProfilePage from '../pages/student/ProfilePage';

import AdminDashboardPage from '../pages/admin/AdminDashboardPage';
import CategoriesManagePage from '../pages/admin/CategoriesManagePage';
import ScenariosManagePage from '../pages/admin/ScenariosManagePage';
import StepsManagePage from '../pages/admin/StepsManagePage';
import OptionsManagePage from '../pages/admin/OptionsManagePage';
import UsersManagePage from '../pages/admin/UsersManagePage';
import ReportsPage from '../pages/admin/ReportsPage';
import SettingsPage from '../pages/admin/SettingsPage';

// Simple Not Found Page
const NotFoundPage = () => (
  <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
    <h1 className="text-6xl font-bold text-slate-800 mb-4">404</h1>
    <h2 className="text-2xl font-semibold text-slate-600 mb-6">Page Not Found</h2>
    <p className="text-slate-500 mb-8 max-w-md">
      The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
    </p>
    <Link
      to="/dashboard"
      className="px-6 py-3 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 transition font-medium"
    >
      Back to Dashboard
    </Link>
  </div>
);

// Protected Route Guard for logged-in users (students or admins)
export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) return <Loader fullScreen />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  
  return children;
};

// Admin Route Guard
export const AdminRoute = ({ children }) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();
  
  if (loading) return <Loader fullScreen />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (!isAdmin) return <Navigate to="/dashboard" replace />;
  
  return children;
};

const AppRouter = () => {
  const { isAuthenticated, isAdmin } = useAuth();

  return (
    <Routes>
      {/* Public Routes */}
      <Route
        path="/"
        element={
          isAuthenticated ? (
            isAdmin ? <Navigate to="/admin" replace /> : <Navigate to="/dashboard" replace />
          ) : (
            <LandingPage />
          )
        }
      />
      <Route
        path="/login"
        element={
          isAuthenticated ? (
            isAdmin ? <Navigate to="/admin" replace /> : <Navigate to="/dashboard" replace />
          ) : (
            <LoginPage />
          )
        }
      />
      <Route
        path="/register"
        element={
          isAuthenticated ? (
            isAdmin ? <Navigate to="/admin" replace /> : <Navigate to="/dashboard" replace />
          ) : (
            <RegisterPage />
          )
        }
      />

      {/* Student Protected Routes */}
      <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
      <Route path="/categories" element={<ProtectedRoute><CategoriesPage /></ProtectedRoute>} />
      <Route path="/categories/:slug" element={<ProtectedRoute><CategoryDetailPage /></ProtectedRoute>} />
      <Route path="/scenarios/:id" element={<ProtectedRoute><ScenarioOverviewPage /></ProtectedRoute>} />
      <Route path="/simulation/:sessionId" element={<ProtectedRoute><SimulationPage /></ProtectedRoute>} />
      <Route path="/simulation/:sessionId/results" element={<ProtectedRoute><ResultsPage /></ProtectedRoute>} />
      <Route path="/progress" element={<ProtectedRoute><ProgressPage /></ProtectedRoute>} />
      <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />

      {/* Admin Protected Routes */}
      <Route path="/admin" element={<AdminRoute><AdminDashboardPage /></AdminRoute>} />
      <Route path="/admin/categories" element={<AdminRoute><CategoriesManagePage /></AdminRoute>} />
      <Route path="/admin/scenarios" element={<AdminRoute><ScenariosManagePage /></AdminRoute>} />
      <Route path="/admin/scenarios/:id/steps" element={<AdminRoute><StepsManagePage /></AdminRoute>} />
      <Route path="/admin/steps/:id/options" element={<AdminRoute><OptionsManagePage /></AdminRoute>} />
      <Route path="/admin/users" element={<AdminRoute><UsersManagePage /></AdminRoute>} />
      <Route path="/admin/reports" element={<AdminRoute><ReportsPage /></AdminRoute>} />
      <Route path="/admin/settings" element={<AdminRoute><SettingsPage /></AdminRoute>} />

      {/* Fallback */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};

export default AppRouter;
