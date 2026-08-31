import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import adminService from '../../api/adminService';
import AdminLayout from '../../components/layout/AdminLayout';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import EmptyState from '../../components/common/EmptyState';
import Modal from '../../components/common/Modal';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import {
  Plus,
  Edit2,
  Trash2,
  FileSpreadsheet,
  ListCollapse,
  CheckCircle,
  XCircle,
} from 'lucide-react';
import { DIFFICULTY_LABELS, DIFFICULTY_COLORS } from '../../utils/constants';

const ScenariosManagePage = () => {
  const navigate = useNavigate();

  const [scenarios, setScenarios] = useState([]);
  const [categories, setCategories] = useState([]);
  const [filterCategory, setFilterCategory] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Form Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingScenario, setEditingScenario] = useState(null);
  const [modalFormData, setModalFormData] = useState({
    scenario_id: '',
    category: '',
    title: '',
    student_role: '',
    overview: '',
    difficulty: 'beginner',
    estimated_duration_minutes: 20,
    xp_completion_bonus: 30,
    xp_perfect_score_bonus: 40,
    version: '1.0',
    is_active: true,
  });

  // Delete Confirm Dialog State
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [scenarioToDelete, setScenarioToDelete] = useState(null);

  const fetchInitialData = async () => {
    setLoading(true);
    try {
      const catRes = await adminService.getCategories();
      if (catRes?.success) {
        setCategories(catRes.data);
      }
      
      const scRes = await adminService.getScenarios(
        filterCategory ? { category: filterCategory } : {}
      );
      if (scRes?.success) {
        setScenarios(scRes.data);
      } else {
        setError(scRes?.message || 'Failed to fetch scenarios.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to connect to the server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInitialData();
  }, [filterCategory]);

  const handleOpenCreateModal = () => {
    setEditingScenario(null);
    setModalFormData({
      scenario_id: '',
      category: categories[0]?.id || '',
      title: '',
      student_role: '',
      overview: '',
      difficulty: 'beginner',
      estimated_duration_minutes: 20,
      xp_completion_bonus: 30,
      xp_perfect_score_bonus: 40,
      version: '1.0',
      is_active: true,
    });
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (scen) => {
    setEditingScenario(scen);
    setModalFormData({
      scenario_id: scen.scenario_id,
      category: scen.category || '',
      title: scen.title,
      student_role: scen.student_role || '',
      overview: scen.overview || '',
      difficulty: scen.difficulty || 'beginner',
      estimated_duration_minutes: scen.estimated_duration_minutes || 20,
      xp_completion_bonus: scen.xp_completion_bonus || 30,
      xp_perfect_score_bonus: scen.xp_perfect_score_bonus || 40,
      version: scen.version || '1.0',
      is_active: scen.is_active,
    });
    setIsModalOpen(true);
  };

  const handleModalFormSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (
      !modalFormData.scenario_id.trim() ||
      !modalFormData.title.trim() ||
      !modalFormData.category
    ) {
      setError('Please fill in all required fields.');
      return;
    }

    try {
      if (editingScenario) {
        // Edit
        const res = await adminService.updateScenario(editingScenario.id, modalFormData);
        if (res?.success) {
          setSuccess(`Scenario "${res.data.title}" updated.`);
          setIsModalOpen(false);
          fetchInitialData();
        } else {
          setError(res?.message || 'Failed to update scenario.');
        }
      } else {
        // Create
        const res = await adminService.createScenario(modalFormData);
        if (res?.success) {
          setSuccess(`Scenario "${res.data.title}" created.`);
          setIsModalOpen(false);
          fetchInitialData();
        } else {
          setError(res?.message || 'Failed to create scenario.');
        }
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to submit form.');
    }
  };

  const handleOpenDeleteConfirm = (scen) => {
    setScenarioToDelete(scen);
    setDeleteConfirmOpen(true);
  };

  const handleDeleteConfirmAction = async () => {
    if (!scenarioToDelete) return;
    setError(null);
    setSuccess(null);
    try {
      const res = await adminService.deleteScenario(scenarioToDelete.id);
      if (res?.success) {
        setSuccess(res.message || 'Scenario deleted/deactivated.');
        setDeleteConfirmOpen(false);
        fetchInitialData();
      } else {
        setError(res?.message || 'Failed to delete scenario.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete scenario.');
    }
  };

  return (
    <AdminLayout>
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 mb-8">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
            Scenario Management
          </h1>

        </div>
        <Button size="sm" icon={Plus} onClick={handleOpenCreateModal}>
          Create Scenario
        </Button>
      </div>

      {/* Filter and Message Blocks */}
      {success && <Alert type="success" message={success} className="mb-6" onClose={() => setSuccess(null)} />}
      {error && <Alert type="error" message={error} className="mb-6" onClose={() => setError(null)} />}

      <div className="flex items-center space-x-3 mb-6">
        <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
          Filter Category:
        </label>
        <select
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          className="rounded-lg border border-slate-300 px-3 py-1.5 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-1 focus:ring-cyan-500 bg-white"
        >
          <option value="">All Categories</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      {/* Main Grid */}
      <Card title="Database Scenarios Index" subtitle="List of training scripts." bodyClassName="p-0">
        {loading ? (
          <Loader size="lg" className="my-12" />
        ) : scenarios.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-150">
              <thead className="bg-slate-50 text-[10px] font-bold uppercase tracking-wider text-slate-500 text-left">
                <tr>
                  <th className="px-6 py-3">ID Code</th>
                  <th className="px-6 py-3">Scenario Title</th>
                  <th className="px-6 py-3">Category</th>
                  <th className="px-6 py-3">Difficulty</th>
                  <th className="px-6 py-3">Version</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs text-slate-600">
                {scenarios.map((scen) => (
                  <tr key={scen.id} className="hover:bg-slate-50/50 transition">
                    <td className="px-6 py-4 font-bold text-slate-800">{scen.scenario_id}</td>
                    <td className="px-6 py-4">
                      <div className="font-semibold text-slate-800">{scen.title}</div>
                      <div className="text-[10px] text-slate-400 max-w-sm truncate mt-0.5">
                        Role: {scen.student_role}
                      </div>
                    </td>
                    <td className="px-6 py-4 font-medium">{scen.category_name || '—'}</td>
                    <td className="px-6 py-4">
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                          DIFFICULTY_COLORS[scen.difficulty] || 'bg-slate-100'
                        }`}
                      >
                        {DIFFICULTY_LABELS[scen.difficulty]}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-slate-500 font-semibold">v{scen.version}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-1.5 font-bold">
                        {scen.is_active ? (
                          <>
                            <CheckCircle className="w-4 h-4 text-emerald-500" />
                            <span className="text-emerald-700 text-[10px] uppercase">Active</span>
                          </>
                        ) : (
                          <>
                            <XCircle className="w-4 h-4 text-rose-500" />
                            <span className="text-rose-700 text-[10px] uppercase">Inactive</span>
                          </>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right space-x-2">
                      <Link to={`/admin/scenarios/${scen.id}/steps`}>
                        <Button variant="ghost" size="sm" icon={ListCollapse}>
                          Steps
                        </Button>
                      </Link>
                      <Button
                        variant="ghost"
                        size="sm"
                        icon={Edit2}
                        onClick={() => handleOpenEditModal(scen)}
                      >
                        Edit
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        icon={Trash2}
                        className="text-rose-600 hover:bg-rose-50"
                        onClick={() => handleOpenDeleteConfirm(scen)}
                      >
                        Delete
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-6">
            <EmptyState
              title="No scenarios found"
              description="Platform database contains zero scenario definitions."
              icon={FileSpreadsheet}
              action={<Button onClick={handleOpenCreateModal}>Add Scenario</Button>}
            />
          </div>
        )}
      </Card>

      {/* Form Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingScenario ? `Edit Scenario: ${editingScenario.title}` : 'Create Scenario'}
        size="lg"
      >
        <form onSubmit={handleModalFormSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                Scenario ID Code *
              </label>
              <input
                type="text"
                required
                value={modalFormData.scenario_id}
                onChange={(e) => setModalFormData({ ...modalFormData, scenario_id: e.target.value })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
                placeholder="e.g. S-MAL-02"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                Category Domain *
              </label>
              <select
                value={modalFormData.category}
                onChange={(e) => setModalFormData({ ...modalFormData, category: e.target.value })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              >
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
              Scenario Title *
            </label>
            <input
              type="text"
              required
              value={modalFormData.title}
              onChange={(e) => setModalFormData({ ...modalFormData, title: e.target.value })}
              className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="e.g. Supply Chain Trogan compromised workstation"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
              Operational Role *
            </label>
            <input
              type="text"
              required
              value={modalFormData.student_role}
              onChange={(e) => setModalFormData({ ...modalFormData, student_role: e.target.value })}
              className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="e.g. Junior Security Operations Analyst at GlobalTech"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
              Overview Context *
            </label>
            <textarea
              required
              rows={3}
              value={modalFormData.overview}
              onChange={(e) => setModalFormData({ ...modalFormData, overview: e.target.value })}
              className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="Brief briefing context shown to student before beginning..."
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                Difficulty *
              </label>
              <select
                value={modalFormData.difficulty}
                onChange={(e) => setModalFormData({ ...modalFormData, difficulty: e.target.value })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                Duration (minutes) *
              </label>
              <input
                type="number"
                required
                value={modalFormData.estimated_duration_minutes}
                onChange={(e) =>
                  setModalFormData({
                    ...modalFormData,
                    estimated_duration_minutes: parseInt(e.target.value) || 20,
                  })
                }
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                Completion XP *
              </label>
              <input
                type="number"
                required
                value={modalFormData.xp_completion_bonus}
                onChange={(e) =>
                  setModalFormData({
                    ...modalFormData,
                    xp_completion_bonus: parseInt(e.target.value) || 0,
                  })
                }
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                Perfect XP *
              </label>
              <input
                type="number"
                required
                value={modalFormData.xp_perfect_score_bonus}
                onChange={(e) =>
                  setModalFormData({
                    ...modalFormData,
                    xp_perfect_score_bonus: parseInt(e.target.value) || 0,
                  })
                }
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                Version *
              </label>
              <input
                type="text"
                required
                value={modalFormData.version}
                onChange={(e) => setModalFormData({ ...modalFormData, version: e.target.value })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              />
            </div>
          </div>

          <div className="flex items-center space-x-3 pt-2">
            <input
              type="checkbox"
              id="scen_is_active"
              checked={modalFormData.is_active}
              onChange={(e) => setModalFormData({ ...modalFormData, is_active: e.target.checked })}
              className="h-4 w-4 border-slate-300 text-cyan-600 focus:ring-cyan-500 rounded-sm"
            />
            <label htmlFor="scen_is_active" className="text-xs font-semibold text-slate-750">
              Active (Visible on student portal)
            </label>
          </div>

          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-100">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit">
              {editingScenario ? 'Save Changes' : 'Create Scenario'}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete/Deactivate Confirmation */}
      <ConfirmDialog
        isOpen={deleteConfirmOpen}
        onCancel={() => setDeleteConfirmOpen(false)}
        onConfirm={handleDeleteConfirmAction}
        title="Confirm Deletion"
        message={`Are you sure you want to delete "${scenarioToDelete?.title}"? If students have active sessions on this scenario, it will be deactivated instead.`}
      />
    </AdminLayout>
  );
};

export default ScenariosManagePage;
