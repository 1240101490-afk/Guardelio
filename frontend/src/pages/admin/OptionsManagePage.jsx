import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import adminService from '../../api/adminService';
import AdminLayout from '../../components/layout/AdminLayout';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import EmptyState from '../../components/common/EmptyState';
import Modal from '../../components/common/Modal';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import { Plus, Edit2, Trash2, ArrowLeft, HelpCircle, CheckCircle, XCircle } from 'lucide-react';

const OptionsManagePage = () => {
  const { id: stepId } = useParams();
  const navigate = useNavigate();

  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Form Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingOption, setEditingOption] = useState(null);
  const [modalFormData, setModalFormData] = useState({
    option_text: '',
    is_correct: false,
    xp_awarded: 20,
    feedback_text: '',
    consequence_type: 'positive',
    next_step: '',
    display_order: 1,
  });

  // Delete Confirm State
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [optionToDelete, setOptionToDelete] = useState(null);

  const fetchOptions = async () => {
    setLoading(true);
    try {
      const res = await adminService.getOptions(stepId);
      if (res?.success) {
        setOptions(res.data);
      } else {
        setError(res?.message || 'Failed to fetch options.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to connect to server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOptions();
  }, [stepId]);

  const handleOpenCreateModal = () => {
    setEditingOption(null);
    setModalFormData({
      option_text: '',
      is_correct: false,
      xp_awarded: 20,
      feedback_text: '',
      consequence_type: 'positive',
      next_step: '',
      display_order: options.length + 1,
    });
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (opt) => {
    setEditingOption(opt);
    setModalFormData({
      option_text: opt.option_text,
      is_correct: opt.is_correct,
      xp_awarded: opt.xp_awarded || 0,
      feedback_text: opt.feedback_text || '',
      consequence_type: opt.consequence_type || 'positive',
      next_step: opt.next_step || '',
      display_order: opt.display_order || 1,
    });
    setIsModalOpen(true);
  };

  const handleModalFormSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!modalFormData.option_text.trim() || !modalFormData.feedback_text.trim()) {
      setError('Please fill in all required fields.');
      return;
    }

    try {
      // If next_step is empty string, make it null
      const payload = {
        ...modalFormData,
        next_step: modalFormData.next_step ? parseInt(modalFormData.next_step) : null,
      };

      if (editingOption) {
        const res = await adminService.updateOption(editingOption.id, payload);
        if (res?.success) {
          setSuccess('Decision option updated.');
          setIsModalOpen(false);
          fetchOptions();
        } else {
          setError(res?.message || 'Failed to update option.');
        }
      } else {
        const res = await adminService.createOption(stepId, payload);
        if (res?.success) {
          setSuccess('Decision option created.');
          setIsModalOpen(false);
          fetchOptions();
        } else {
          setError(res?.message || 'Failed to create option.');
        }
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to submit form.');
    }
  };

  const handleOpenDeleteConfirm = (opt) => {
    setOptionToDelete(opt);
    setDeleteConfirmOpen(true);
  };

  const handleDeleteConfirmAction = async () => {
    if (!optionToDelete) return;
    setError(null);
    setSuccess(null);
    try {
      const res = await adminService.deleteOption(optionToDelete.id);
      if (res?.success) {
        setSuccess('Option deleted successfully.');
        setDeleteConfirmOpen(false);
        fetchOptions();
      } else {
        setError(res?.message || 'Failed to delete option.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete option.');
    }
  };

  return (
    <AdminLayout>
      {/* Back button */}
      <button
        onClick={() => navigate(-1)}
        className="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-500 hover:text-slate-700 transition mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Steps</span>
      </button>

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 mb-8">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
            Decision Options
          </h1>

        </div>
        <Button size="sm" icon={Plus} onClick={handleOpenCreateModal}>
          Create Option
        </Button>
      </div>

      {success && <Alert type="success" message={success} className="mb-6" onClose={() => setSuccess(null)} />}
      {error && <Alert type="error" message={error} className="mb-6" onClose={() => setError(null)} />}

      <Card title="Available Step Choices" subtitle="List of responses students can choose." bodyClassName="p-0">
        {loading ? (
          <Loader size="lg" className="my-12" />
        ) : options.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-150">
              <thead className="bg-slate-50 text-[10px] font-bold uppercase tracking-wider text-slate-500 text-left">
                <tr>
                  <th className="px-6 py-3">Order</th>
                  <th className="px-6 py-3">Option Text</th>
                  <th className="px-6 py-3">Is Correct</th>
                  <th className="px-6 py-3">XP Awarded</th>
                  <th className="px-6 py-3">Consequence</th>
                  <th className="px-6 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs text-slate-600">
                {options.map((opt) => (
                  <tr key={opt.id} className="hover:bg-slate-50/50 transition">
                    <td className="px-6 py-4 font-bold text-slate-800">{opt.display_order}</td>
                    <td className="px-6 py-4">
                      <div className="font-semibold text-slate-800">{opt.option_text}</div>
                      <div className="text-[10px] text-slate-400 max-w-sm truncate mt-0.5">
                        Feedback: {opt.feedback_text}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-1.5 font-bold">
                        {opt.is_correct ? (
                          <>
                            <CheckCircle className="w-4 h-4 text-emerald-500" />
                            <span className="text-emerald-700 text-[10px] uppercase">Yes</span>
                          </>
                        ) : (
                          <>
                            <XCircle className="w-4 h-4 text-rose-500" />
                            <span className="text-rose-700 text-[10px] uppercase">No</span>
                          </>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 font-bold text-cyan-600">+{opt.xp_awarded} XP</td>
                    <td className="px-6 py-4 font-semibold capitalize text-[10px]">
                      <span className={`px-2 py-0.5 rounded-full border ${opt.consequence_type === 'positive' ? 'bg-emerald-50 border-emerald-200 text-emerald-750' : opt.consequence_type === 'negative' ? 'bg-rose-50 border-rose-200 text-rose-750' : 'bg-slate-50 border-slate-200 text-slate-700'}`}>
                        {opt.consequence_type}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right space-x-2">
                      <Button variant="ghost" size="sm" icon={Edit2} onClick={() => handleOpenEditModal(opt)}>
                        Edit
                      </Button>
                      <Button variant="ghost" size="sm" icon={Trash2} className="text-rose-600 hover:bg-rose-50" onClick={() => handleOpenDeleteConfirm(opt)}>
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
              title="No options found"
              description="This step does not have any decision options configured."
              icon={HelpCircle}
              action={<Button onClick={handleOpenCreateModal}>Add Option</Button>}
            />
          </div>
        )}
      </Card>

      {/* Form Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingOption ? 'Edit Decision Option' : 'Create Option'}
        size="lg"
      >
        <form onSubmit={handleModalFormSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Option Text *</label>
            <input
              type="text"
              required
              value={modalFormData.option_text}
              onChange={(e) => setModalFormData({ ...modalFormData, option_text: e.target.value })}
              className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="e.g. Isolate the network segment by disabling port..."
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Educational Feedback *</label>
            <textarea
              required
              rows={4}
              value={modalFormData.feedback_text}
              onChange={(e) => setModalFormData({ ...modalFormData, feedback_text: e.target.value })}
              className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="Explain why this option is correct or incorrect..."
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">XP Awarded *</label>
              <input
                type="number"
                required
                value={modalFormData.xp_awarded}
                onChange={(e) => setModalFormData({ ...modalFormData, xp_awarded: parseInt(e.target.value) || 0 })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Consequence Type *</label>
              <select
                value={modalFormData.consequence_type}
                onChange={(e) => setModalFormData({ ...modalFormData, consequence_type: e.target.value })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              >
                <option value="positive">Positive</option>
                <option value="neutral">Neutral</option>
                <option value="negative">Negative</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Display Order *</label>
              <input
                type="number"
                required
                value={modalFormData.display_order}
                onChange={(e) => setModalFormData({ ...modalFormData, display_order: parseInt(e.target.value) || 1 })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Next Step (ID) - Optional</label>
              <input
                type="number"
                value={modalFormData.next_step}
                onChange={(e) => setModalFormData({ ...modalFormData, next_step: e.target.value })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
                placeholder="Leave blank for linear flow"
              />
            </div>
          </div>

          <div className="flex items-center space-x-3 pt-2">
            <input
              type="checkbox"
              id="is_correct"
              checked={modalFormData.is_correct}
              onChange={(e) => setModalFormData({ ...modalFormData, is_correct: e.target.checked })}
              className="h-4 w-4 border-slate-300 text-cyan-600 focus:ring-cyan-500 rounded-sm"
            />
            <label htmlFor="is_correct" className="text-xs font-semibold text-slate-755">Is Correct Key Response</label>
          </div>

          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-100">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit">
              {editingOption ? 'Save Changes' : 'Create Option'}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation */}
      <ConfirmDialog
        isOpen={deleteConfirmOpen}
        onCancel={() => setDeleteConfirmOpen(false)}
        onConfirm={handleDeleteConfirmAction}
        title="Confirm Delete"
        message={`Are you sure you want to permanently delete this option?`}
      />
    </AdminLayout>
  );
};

export default OptionsManagePage;
