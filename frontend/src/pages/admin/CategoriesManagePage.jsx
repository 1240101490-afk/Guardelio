import React, { useEffect, useState } from 'react';
import adminService from '../../api/adminService';
import AdminLayout from '../../components/layout/AdminLayout';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import EmptyState from '../../components/common/EmptyState';
import Modal from '../../components/common/Modal';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import { Plus, Edit2, Trash2, FolderTree, Power, CheckCircle, XCircle } from 'lucide-react';

const CategoriesManagePage = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [modalFormData, setModalFormData] = useState({
    name: '',
    short_summary: '',
    description: '',
    icon_name: 'book-open',
    color_theme: 'blue',
    display_order: 1,
    is_active: true,
  });

  // Delete Confirm Dialog State
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [categoryToDelete, setCategoryToDelete] = useState(null);

  const fetchCategories = async () => {
    setLoading(true);
    try {
      const res = await adminService.getCategories();
      if (res?.success) {
        setCategories(res.data);
      } else {
        setError(res?.message || 'Failed to fetch categories.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to connect to the backend server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleOpenCreateModal = () => {
    setEditingCategory(null);
    setModalFormData({
      name: '',
      short_summary: '',
      description: '',
      icon_name: 'book-open',
      color_theme: 'blue',
      display_order: categories.length + 1,
      is_active: true,
    });
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (cat) => {
    setEditingCategory(cat);
    setModalFormData({
      name: cat.name,
      short_summary: cat.short_summary || '',
      description: cat.description || '',
      icon_name: cat.icon_name || 'book-open',
      color_theme: cat.color_theme || 'blue',
      display_order: cat.display_order || 1,
      is_active: cat.is_active,
    });
    setIsModalOpen(true);
  };

  const handleModalFormSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!modalFormData.name.trim() || !modalFormData.description.trim()) {
      setError('Please fill in all required fields.');
      return;
    }

    try {
      if (editingCategory) {
        // Edit
        const res = await adminService.updateCategory(editingCategory.id, modalFormData);
        if (res?.success) {
          setSuccess(`Category "${res.data.name}" updated successfully.`);
          setIsModalOpen(false);
          fetchCategories();
        } else {
          setError(res?.message || 'Failed to update category.');
        }
      } else {
        // Create
        const res = await adminService.createCategory(modalFormData);
        if (res?.success) {
          setSuccess(`Category "${res.data.name}" created successfully.`);
          setIsModalOpen(false);
          fetchCategories();
        } else {
          setError(res?.message || 'Failed to create category.');
        }
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to submit form.');
    }
  };

  const handleOpenDeleteConfirm = (cat) => {
    setCategoryToDelete(cat);
    setDeleteConfirmOpen(true);
  };

  const handleDeleteConfirmAction = async () => {
    if (!categoryToDelete) return;
    setError(null);
    setSuccess(null);
    try {
      const res = await adminService.deleteCategory(categoryToDelete.id);
      if (res?.success) {
        setSuccess(res.message || 'Category deleted/deactivated successfully.');
        setDeleteConfirmOpen(false);
        fetchCategories();
      } else {
        setError(res?.message || 'Failed to delete category.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete category.');
    }
  };

  return (
    <AdminLayout>
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 mb-8">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
            Category Management
          </h1>

        </div>
        <Button size="sm" icon={Plus} onClick={handleOpenCreateModal}>
          Create Category
        </Button>
      </div>

      {success && <Alert type="success" message={success} className="mb-6" onClose={() => setSuccess(null)} />}
      {error && <Alert type="error" message={error} className="mb-6" onClose={() => setError(null)} />}

      <Card title="Database Domains Catalog" subtitle="Platform categories grid." bodyClassName="p-0">
        {loading ? (
          <Loader size="lg" className="my-12" />
        ) : categories.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-150">
              <thead className="bg-slate-50 text-[10px] font-bold uppercase tracking-wider text-slate-500 text-left">
                <tr>
                  <th className="px-6 py-3">Order</th>
                  <th className="px-6 py-3">Category Name</th>
                  <th className="px-6 py-3">Icon & Theme</th>
                  <th className="px-6 py-3">Slug</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs text-slate-600">
                {categories.map((cat) => (
                  <tr key={cat.id} className="hover:bg-slate-50/50 transition">
                    <td className="px-6 py-4 font-bold text-slate-800">{cat.display_order}</td>
                    <td className="px-6 py-4">
                      <div className="font-semibold text-slate-800">{cat.name}</div>
                      <div className="text-[10px] text-slate-400 max-w-sm truncate mt-0.5">
                        {cat.short_summary || cat.description}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="font-semibold">{cat.icon_name}</span> ({cat.color_theme})
                    </td>
                    <td className="px-6 py-4 font-semibold text-slate-500">{cat.slug}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-1.5 font-bold">
                        {cat.is_active ? (
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
                      <Button variant="ghost" size="sm" icon={Edit2} onClick={() => handleOpenEditModal(cat)}>
                        Edit
                      </Button>
                      <Button variant="ghost" size="sm" icon={Trash2} className="text-rose-600 hover:bg-rose-50" onClick={() => handleOpenDeleteConfirm(cat)}>
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
              title="No categories found"
              description="Platform database contains zero category definitions."
              icon={FolderTree}
              action={<Button onClick={handleOpenCreateModal}>Add Category</Button>}
            />
          </div>
        )}
      </Card>

      {/* Create / Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingCategory ? `Edit Category: ${editingCategory.name}` : 'Create Category'}
        size="lg"
      >
        <form onSubmit={handleModalFormSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Category Name *</label>
            <input
              type="text"
              required
              value={modalFormData.name}
              onChange={(e) => setModalFormData({ ...modalFormData, name: e.target.value })}
              className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="e.g. Malware Infection Response"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Short Summary *</label>
            <input
              type="text"
              required
              value={modalFormData.short_summary}
              onChange={(e) => setModalFormData({ ...modalFormData, short_summary: e.target.value })}
              className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="Detect and contain active malware."
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Full Description *</label>
            <textarea
              required
              rows={4}
              value={modalFormData.description}
              onChange={(e) => setModalFormData({ ...modalFormData, description: e.target.value })}
              className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="Detailed explanation of the category's learning scope..."
            />
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Icon Name *</label>
              <input
                type="text"
                required
                value={modalFormData.icon_name}
                onChange={(e) => setModalFormData({ ...modalFormData, icon_name: e.target.value })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">Color Theme *</label>
              <select
                value={modalFormData.color_theme}
                onChange={(e) => setModalFormData({ ...modalFormData, color_theme: e.target.value })}
                className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              >
                <option value="red">Red</option>
                <option value="amber">Amber</option>
                <option value="blue">Blue</option>
                <option value="purple">Purple</option>
                <option value="orange">Orange</option>
                <option value="emerald">Emerald</option>
              </select>
            </div>
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
          </div>

          <div className="flex items-center space-x-3 pt-2">
            <input
              type="checkbox"
              id="is_active"
              checked={modalFormData.is_active}
              onChange={(e) => setModalFormData({ ...modalFormData, is_active: e.target.checked })}
              className="h-4 w-4 border-slate-300 text-cyan-600 focus:ring-cyan-500 rounded-sm"
            />
            <label htmlFor="is_active" className="text-xs font-semibold text-slate-750">
              Active (Visible on student portal)
            </label>
          </div>

          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-100">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit">
              {editingCategory ? 'Save Changes' : 'Create Category'}
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
        message={`Are you sure you want to delete "${categoryToDelete?.name}"? If there are scenarios associated with this category, it will be deactivated (soft-deleted) instead to protect integrity.`}
      />
    </AdminLayout>
  );
};

export default CategoriesManagePage;
