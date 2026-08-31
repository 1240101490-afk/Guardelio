import React, { useState, useEffect } from 'react';
import adminService from '../../api/adminService';
import AdminLayout from '../../components/layout/AdminLayout';
import Card from '../../components/common/Card';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import EmptyState from '../../components/common/EmptyState';
import { BarChart3, Users, FileSpreadsheet, Percent, Trophy } from 'lucide-react';
import { DIFFICULTY_LABELS } from '../../utils/constants';

const ReportsPage = () => {
  const [activeTab, setActiveTab] = useState('scenarios');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // States
  const [scenariosReport, setScenariosReport] = useState([]);
  const [studentsReport, setStudentsReport] = useState([]);

  useEffect(() => {
    const loadReport = async () => {
      setLoading(true);
      setError(null);
      try {
        if (activeTab === 'scenarios') {
          const res = await adminService.getScenarioReport();
          if (res?.success) setScenariosReport(res.data);
        } else if (activeTab === 'users') {
          const res = await adminService.getUserReport();
          if (res?.success) setStudentsReport(res.data);
        }
      } catch (err) {
        setError(err.response?.data?.message || `Failed to fetch report for ${activeTab}.`);
      } finally {
        setLoading(false);
      }
    };
    loadReport();
  }, [activeTab]);

  return (
    <AdminLayout>
      {/* Title */}
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
          Platform Reports & Analytics
        </h1>

      </div>

      {/* Tabs */}
      <div className="border-b border-slate-200 mb-6">
        <nav className="flex space-x-6" aria-label="Tabs">
          <button
            onClick={() => setActiveTab('scenarios')}
            className={`flex items-center space-x-2 py-4 px-1 border-b-2 text-xs font-semibold uppercase tracking-wider focus:outline-none transition ${
              activeTab === 'scenarios'
                ? 'border-red-700 text-red-700'
                : 'border-transparent text-slate-400 hover:text-slate-600 hover:border-slate-300'
            }`}
          >
            <FileSpreadsheet className="w-4 h-4" />
            <span>Scenario Performance</span>
          </button>
          <button
            onClick={() => setActiveTab('users')}
            className={`flex items-center space-x-2 py-4 px-1 border-b-2 text-xs font-semibold uppercase tracking-wider focus:outline-none transition ${
              activeTab === 'users'
                ? 'border-red-700 text-red-700'
                : 'border-transparent text-slate-400 hover:text-slate-600 hover:border-slate-300'
            }`}
          >
            <Users className="w-4 h-4" />
            <span>Student Performance</span>
          </button>
        </nav>
      </div>

      {error && (
        <div className="mb-6">
          <Alert type="error" message="Reports Load Error" description={error} />
        </div>
      )}

      {loading ? (
        <Loader size="lg" className="my-12" />
      ) : (
        <div>
          {/* Scenarios Analytics Tab */}
          {activeTab === 'scenarios' && (
            <Card
              title="Scenario Operations Summary"
              subtitle="Completion analytics grouped by category and scenario codes."
              bodyClassName="p-0"
            >
              {scenariosReport.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-slate-150">
                    <thead className="bg-slate-50 text-[10px] font-bold uppercase tracking-wider text-slate-500 text-left">
                      <tr>
                        <th className="px-6 py-3">Code</th>
                        <th className="px-6 py-3">Scenario</th>
                        <th className="px-6 py-3">Difficulty</th>
                        <th className="px-6 py-3">Attempts</th>
                        <th className="px-6 py-3">Completions</th>
                        <th className="px-6 py-3">Abandon Rate</th>
                        <th className="px-6 py-3">Avg Accuracy</th>
                        <th className="px-6 py-3">Avg XP</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 text-xs text-slate-600">
                      {scenariosReport.map((row) => (
                        <tr key={row.scenario_id} className="hover:bg-slate-50/50 transition">
                          <td className="px-6 py-4 font-bold text-slate-800">{row.scenario_id}</td>
                          <td className="px-6 py-4">
                            <div className="font-semibold text-slate-800">{row.scenario_title}</div>
                            <div className="text-[10px] text-slate-400 mt-0.5">{row.category_name}</div>
                          </td>
                          <td className="px-6 py-4 capitalize">{DIFFICULTY_LABELS[row.difficulty] || row.difficulty}</td>
                          <td className="px-6 py-4 font-semibold text-slate-705">{row.total_attempts}</td>
                          <td className="px-6 py-4 font-semibold text-slate-705">{row.completions}</td>
                          <td className="px-6 py-4 text-rose-600 font-bold">{row.abandonment_rate}%</td>
                          <td className="px-6 py-4 text-cyan-600 font-bold">{row.average_accuracy}%</td>
                          <td className="px-6 py-4 font-semibold text-slate-700">{row.average_xp} XP</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="p-6">
                  <EmptyState title="No scenario data logs found" icon={FileSpreadsheet} />
                </div>
              )}
            </Card>
          )}

          {/* Student Report Tab */}
          {activeTab === 'users' && (
            <Card
              title="Student Standings Ledger"
              subtitle="Overview of learning history and total experience scores."
              bodyClassName="p-0"
            >
              {studentsReport.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-slate-150">
                    <thead className="bg-slate-50 text-[10px] font-bold uppercase tracking-wider text-slate-500 text-left">
                      <tr>
                        <th className="px-6 py-3">Student</th>
                        <th className="px-6 py-3">Email</th>
                        <th className="px-6 py-3">Total XP</th>
                        <th className="px-6 py-3">Completions</th>
                        <th className="px-6 py-3">Total Attempts</th>
                        <th className="px-6 py-3">Avg Accuracy</th>
                        <th className="px-6 py-3">Last Logged In</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 text-xs text-slate-600">
                      {studentsReport.map((row) => (
                        <tr key={row.student_id} className="hover:bg-slate-50/50 transition">
                          <td className="px-6 py-4">
                            <div className="font-semibold text-slate-800">{row.full_name || row.username}</div>
                            <div className="text-[10px] text-slate-400 mt-0.5">@{row.username}</div>
                          </td>
                          <td className="px-6 py-4 text-slate-500 font-semibold">{row.email}</td>
                          <td className="px-6 py-4 font-extrabold text-cyan-600">+{row.total_xp} XP</td>
                          <td className="px-6 py-4 font-semibold text-slate-700">{row.completed_scenarios}</td>
                          <td className="px-6 py-4 font-semibold text-slate-700">{row.total_sessions}</td>
                          <td className="px-6 py-4 text-emerald-600 font-bold">{row.average_accuracy}%</td>
                          <td className="px-6 py-4">
                            {row.last_login ? new Date(row.last_login).toLocaleString() : 'Never'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="p-6">
                  <EmptyState title="No student data logs found" icon={Users} />
                </div>
              )}
            </Card>
          )}
        </div>
      )}
    </AdminLayout>
  );
};

export default ReportsPage;
