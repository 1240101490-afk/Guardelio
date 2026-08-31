import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import adminService from '../../api/adminService';
import { useAuth } from '../../context/AuthContext';
import AdminLayout from '../../components/layout/AdminLayout';
import StatCard from '../../components/common/StatCard';
import Card from '../../components/common/Card';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import {
  Users,
  FolderTree,
  FileSpreadsheet,
  History,
  CheckCircle,
  Target,
  Award,
  ArrowRight,
  BarChart3,
} from 'lucide-react';
import { getDisplayName } from '../../utils/formatters';

const AdminDashboardPage = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAdminStats = async () => {
      try {
        const res = await adminService.getStats();
        if (res?.success) {
          setStats(res.data);
        } else {
          setError(res?.message || 'Failed to load platform statistics.');
        }
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to connect to the backend server.');
      } finally {
        setLoading(false);
      }
    };
    fetchAdminStats();
  }, []);

  if (loading) {
    return (
      <AdminLayout>
        <Loader fullScreen />
      </AdminLayout>
    );
  }

  if (error) {
    return (
      <AdminLayout>
        <div className="max-w-3xl mx-auto mt-8">
          <Alert type="error" message="Admin Statistics Error" description={error} />
        </div>
      </AdminLayout>
    );
  }

  const {
    total_users = 0,
    active_students = 0,
    total_categories = 0,
    total_scenarios = 0,
    total_sessions = 0,
    completed_sessions = 0,
    average_accuracy = 0,
    top_scenario_title = '—',
  } = stats || {};

  return (
    <AdminLayout>
      {/* Title */}
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
          Welcome, {getDisplayName(user)}
        </h1>

      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Total Users" value={total_users} icon={Users} description={`${active_students} active students`} />
        <StatCard title="Categories" value={total_categories} icon={FolderTree} colorClass="text-emerald-600 bg-emerald-50 border-emerald-100" />
        <StatCard title="Scenarios" value={total_scenarios} icon={FileSpreadsheet} colorClass="text-amber-600 bg-amber-50 border-amber-100" />
        <StatCard title="Total Sessions" value={total_sessions} icon={History} colorClass="text-purple-600 bg-purple-50 border-purple-100" description={`${completed_sessions} completions`} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Core summary widgets */}
        <div className="lg:col-span-2 space-y-6">
          <Card title="Quick Console Links" subtitle="Manage Guardelio educational resources.">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Link
                to="/admin/categories"
                className="flex items-center justify-between p-4 border border-slate-200 rounded-xl hover:bg-slate-50 transition"
              >
                <div className="flex items-center space-x-3">
                  <div className="bg-red-50 text-red-600 p-2 rounded-lg">
                    <FolderTree className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="font-bold text-slate-800 text-xs block">Category Management</span>
                    <span className="text-[10px] text-slate-400">Add, edit, or deactivate categories</span>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-400" />
              </Link>

              <Link
                to="/admin/scenarios"
                className="flex items-center justify-between p-4 border border-slate-200 rounded-xl hover:bg-slate-50 transition"
              >
                <div className="flex items-center space-x-3">
                  <div className="bg-amber-50 text-amber-600 p-2 rounded-lg">
                    <FileSpreadsheet className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="font-bold text-slate-800 text-xs block">Scenario Management</span>
                    <span className="text-[10px] text-slate-400">Configure branching simulations and steps</span>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-400" />
              </Link>

              <Link
                to="/admin/users"
                className="flex items-center justify-between p-4 border border-slate-200 rounded-xl hover:bg-slate-50 transition"
              >
                <div className="flex items-center space-x-3">
                  <div className="bg-blue-50 text-blue-600 p-2 rounded-lg">
                    <Users className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="font-bold text-slate-800 text-xs block">User Directory</span>
                    <span className="text-[10px] text-slate-400">View logs and update student states</span>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-400" />
              </Link>

              <Link
                to="/admin/reports"
                className="flex items-center justify-between p-4 border border-slate-200 rounded-xl hover:bg-slate-50 transition"
              >
                <div className="flex items-center space-x-3">
                  <div className="bg-purple-50 text-purple-600 p-2 rounded-lg">
                    <BarChart3 className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="font-bold text-slate-800 text-xs block">Reports & Analytics</span>
                    <span className="text-[10px] text-slate-400">Export accuracy levels and summaries</span>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-400" />
              </Link>
            </div>
          </Card>
        </div>

        {/* Sidebar Highlight stats */}
        <div className="space-y-6">
          <Card title="Activity Analytics" bodyClassName="p-6 space-y-4">
            <div className="flex items-start justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-slate-400 text-[10px] font-bold uppercase tracking-wider block">
                  Top Scenario
                </span>
                <span className="font-bold text-slate-800 text-xs block mt-0.5 `max-w-[180px]` truncate">
                  {top_scenario_title}
                </span>
              </div>
              <div className="p-2 bg-yellow-50 text-yellow-600 rounded-lg">
                <Award className="w-4 h-4" />
              </div>
            </div>

            <div className="flex items-start justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-slate-400 text-[10px] font-bold uppercase tracking-wider block">
                  Completions Rate
                </span>
                <span className="font-bold text-slate-800 text-xs block mt-0.5">
                  {total_sessions > 0 ? Math.round((completed_sessions / total_sessions) * 100) : 0}%
                </span>
              </div>
              <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg">
                <CheckCircle className="w-4 h-4" />
              </div>
            </div>

            <div className="flex items-start justify-between">
              <div>
                <span className="text-slate-400 text-[10px] font-bold uppercase tracking-wider block">
                  Global Accuracy
                </span>
                <span className="font-bold text-slate-800 text-xs block mt-0.5">
                  {average_accuracy}%
                </span>
              </div>
              <div className="p-2 bg-cyan-50 text-cyan-600 rounded-lg">
                <Target className="w-4 h-4" />
              </div>
            </div>
          </Card>
        </div>
      </div>
    </AdminLayout>
  );
};

export default AdminDashboardPage;
