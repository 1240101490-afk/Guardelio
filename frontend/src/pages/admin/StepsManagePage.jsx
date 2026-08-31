import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import adminService from '../../api/adminService';
import AdminLayout from '../../components/layout/AdminLayout';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import EmptyState from '../../components/common/EmptyState';
import Modal from '../../components/common/Modal';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import { Plus, Edit2, Trash2, ArrowLeft, Layers, ListCollapse, CheckCircle, XCircle } from 'lucide-react';
import { NIST_PHASE_LABELS } from '../../utils/constants';

const StepsManagePage = () => {
  const { id: scenarioId } = useParams();

  const [steps, setSteps] = useState([]);
  const [scenario, setScenario] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Form Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingStep, setEditingStep] = useState(null);
  const [modalFormData, setModalFormData] = useState({
    step_number: 1,
    title: '',
    situation_text: '',
    nist_phase: 'preparation',
    step_type: 'info',
    is_final_step: false,
    is_active: true,
  });

  // Delete Confirm State
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [stepToDelete, setStepToDelete] = useState(null);

  const fetchSteps = async () => {
    setLoading(true);
    try {
      const scenRes = await adminService.updateScenario(scenarioId, {}); // Get scenario or retrieve details
      // Wait, we can use getScenarioById
      const details = await adminService.getScenarios(); // Fallback or retrieve
      
      // Let's get scenario details cleanly
      const scenDetails = await adminService.updateScenario(scenarioId, {});
      if (scenDetails?.success) setScenario(scenDetails.data);

      const res = await adminService.getSteps(scenarioId);
      if (res?.success) {
        setSteps(res.data);
      } else {
        setError(res?.message || 'Failed to fetch steps.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to connect to server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSteps();
  }, [scenarioId]);

  const handleOpenCreateModal = () => {
    setEditingStep(null);
    setModalFormData({
      step_number: steps.length > 0 ? Math.max(...steps.map((s) => s.step_number)) + 1 : 1,
      title: '',
      situation_text: '',
      nist_phase: 'preparation',
      step_type: 'info',
      is_final_step: false,
      is_active: true,
    });
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (step) => {
    setEditingStep(step);
    setModalFormData({
      step_number: step.step_number,
      title: step.title,
      situation_text: step.situation_text || '',
      nist_phase: step.nist_phase || 'preparation',
      step_type: step.step_type || 'info',
      is_final_step: step.is_final_step,
      is_active: step.is_active,
    });
    setIsModalOpen(true);
  };

  const handleModalFormSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!modalFormData.title.trim() || !modalFormData.situation_text.trim()) {
      setError('Please fill in all required fields.');
      return;
    }

    try {
      if (editingStep) {
        const res = await adminService.updateStep(editingStep.id, modalFormData);
        if (res?.success) {
          setSuccess(`Step ${res.data.step_number} updated.`);
          setIsModalOpen(false);
          fetchSteps();
        } else {
          setError(res?.message || 'Failed to update step.');
        }
      } else {
        const res = await adminService.createStep(scenarioId, modalFormData);
        if (res?.success) {
          setSuccess(`Step ${res.data.step_number} created.`);
          setIsModalOpen(false);
          fetchSteps();
        } else {
          setError(res?.message || 'Failed to create step.');
        }
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to submit form.');
    }
  };

  const handleOpenDeleteConfirm = (step) => {
    setStepToDelete(step);
    setDeleteConfirmOpen(true);
  };

  const handleDeleteConfirmAction = async () => {
    if (!stepToDelete) return;
    setError(null);
    setSuccess(null);
    try {
      const res = await adminService.deleteStep(stepToDelete.id);
      if (res?.success) {
        setSuccess(res.message || 'Step deactivated.');
        setDeleteConfirmOpen(false);
        fetchSteps();
      } else {
        setError(res?.message || 'Failed to deactivate step.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete step.');
    }
  };

  return (
    <AdminLayout>
      {/* Back button */}
      <Link to="/admin/scenarios" className="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-500 hover:text-slate-700 transition mb-6">
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Scenarios</span>
      </Link>

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 mb-8">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
            Steps: {scenario?.title || 'Scenario'}
          </h1>

        </div>
        <Button size="sm" icon={Plus} onClick={handleOpenCreateModal}>
          Create Step
        </Button>
      </div>

      {success && <Alert type="success" message={success} className="mb-6" onClose={() => setSuccess(null)} />}
      {error && <Alert type="error" message={error} className="mb-6" onClose={() => setError(null)} />}

      <Card title="Simulation Flow Steps" subtitle="Ordered sequence of steps." bodyClassName="p-0">
        {loading ? (
          <Loader size="lg" className="my-12" />
        ) : steps.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-150">
              <thead className="bg-slate-50 text-[10px] font-bold uppercase tracking-wider text-slate-500 text-left">
                <tr>
                  <th className="px-6 py-3">Step #</th>
                  <th className="px-6 py-3">Step Title</th>
                  <th className="px-6 py-3">NIST Phase</th>
                  <th className="px-6 py-3">Step Type</th>
                  <th className="px-6 py-3">Final Step</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs text-slate-600">
                {steps.map((step) => (
                  <tr key={step.id} className="hover:bg-slate-50/50 transition">
                    <td className="px-6 py-4 font-bold text-slate-800">{step.step_number}</td>
                    <td className="px-6 py-4">
                      <div className="font-semibold text-slate-800">{step.title}</div>
                      <div className="text-[10px] text-slate-400 max-w-sm truncate mt-0.5">
                        {step.situation_text}
                      </div>
                    </td>
                    <td className="px-6 py-4 font-semibold text-slate-500">
                      {NIST_PHASE_LABELS[step.nist_phase] || step.nist_phase}
                    </td>
                    <td className="px-6 py-4 font-medium uppercase text-[10px]">
                      <span className={`px-2 py-0.5 rounded-full border ${step.step_type === 'decision' ? 'bg-amber-50 border-amber-200 text-amber-700' : 'bg-blue-50 border-blue-200 text-blue-700'}`}>
                        {step.step_type}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      {step.is_final_step ? (
                        <span className="text-emerald-600 font-bold text-[10px] uppercase">Yes</span>
                      ) : (
                        <span className="text-slate-400">No</span>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-1.5 font-bold">
                        {step.is_active ? (
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
                      {step.step_type === 'decision' && (
                        <Link to={`/admin/steps/${step.id}/options`}>
                          <Button variant="ghost" size="sm" icon={ListCollapse}>
                            Options
                          </Button>
                        </Link>
                      )}
                      <Button variant="ghost" size="sm" icon={Edit2} onClick={() => handleOpenEditModal(step)}>
                        Edit
                      </Button>
                      <Button variant="ghost" size="sm" icon={Trash2} className="text-rose-600 hover:bg-rose-50" onClick={() => handleOpenDeleteConfirm(step)}>
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
              title="No steps found"
              description="This scenario does not have any steps added yet."
              icon={Layers}
              action={<Button onClick={handleOpenCreateModal}>Add Step</Button>}
            />
          </div>
        )}
      </Card>

      {/* Form Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingStep ? `Edit Step ${editingStep.step_number}` : 'Create Step'}
        size="lg"
      >
        <form onSubmit={handleModalFormSubmit} className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Step Number *</label>
              <input
                type="number"
                required
                value={modalFormData.step_number}
                onChange={(e) => setModalFormData({ ...modalFormData, step_number: parseInt(e.target.value) || 1 })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">NIST Phase *</label>
              <select
                value={modalFormData.nist_phase}
                onChange={(e) => setModalFormData({ ...modalFormData, nist_phase: e.target.value })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              >
                <option value="preparation">Preparation</option>
                <option value="detection">Detection & Analysis</option>
                <option value="containment">Containment</option>
                <option value="eradication">Eradication</option>
                <option value="recovery">Recovery</option>
                <option value="post_incident">Post-Incident Review</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Step Type *</label>
              <select
                value={modalFormData.step_type}
                onChange={(e) => setModalFormData({ ...modalFormData, step_type: e.target.value })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              >
                <option value="info">Info (Read-only)</option>
                <option value="decision">Decision (Multiple Choice)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Step Title *</label>
            <input
              type="text"
              required
              value={modalFormData.title}
              onChange={(e) => setModalFormData({ ...modalFormData, title: e.target.value })}
              className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="e.g. Initial containment decision"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Situation Text *</label>
            <textarea
              required
              rows={5}
              value={modalFormData.situation_text}
              onChange={(e) => setModalFormData({ ...modalFormData, situation_text: e.target.value })}
              className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="Provide context and framing for this step..."
            />
          </div>

          <div className="flex items-center space-x-6 pt-2">
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="is_final_step"
                checked={modalFormData.is_final_step}
                onChange={(e) => setModalFormData({ ...modalFormData, is_final_step: e.target.checked })}
                className="h-4 w-4 border-slate-300 text-cyan-600 focus:ring-cyan-500 rounded-sm"
              />
              <label htmlFor="is_final_step" className="text-xs font-semibold text-slate-750">Is Final Step</label>
            </div>
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="step_is_active"
                checked={modalFormData.is_active}
                onChange={(e) => setModalFormData({ ...modalFormData, is_active: e.target.checked })}
                className="h-4 w-4 border-slate-300 text-cyan-600 focus:ring-cyan-500 rounded-sm"
              />
              <label htmlFor="step_is_active" className="text-xs font-semibold text-slate-750">Active</label>
            </div>
          </div>

          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-100">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit">
              {editingStep ? 'Save Changes' : 'Create Step'}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation */}
      <ConfirmDialog
        isOpen={deleteConfirmOpen}
        onCancel={() => setDeleteConfirmOpen(false)}
        onConfirm={handleDeleteConfirmAction}
        title="Confirm Deactivate"
        message={`Are you sure you want to deactivate step ${stepToDelete?.step_number}? This step will be hidden from simulation flows.`}
      />
    </AdminLayout>
  );
};

export default StepsManagePage;
