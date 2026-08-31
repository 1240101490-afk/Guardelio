import React, { useEffect, useState } from 'react';
import adminService from '../../api/adminService';
import AdminLayout from '../../components/layout/AdminLayout';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import EmptyState from '../../components/common/EmptyState';
import { useAuth } from '../../context/AuthContext';
import { Search, Users, ShieldAlert, CheckCircle, XCircle } from 'lucide-react';

const UsersManagePage = () => {
  const { user: loggedInUser } = useAuth();

  const [users, setUsers] = useState([]);
  const [search, setSearch] = useState('');
  const [role, setRole] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const params = {};
      if (search.trim()) params.search = search;
      if (role) params.role = role;

      const res = await adminService.getUsers(params);
      if (res?.success) {
        setUsers(res.data);
      } else {
        setError(res?.message || 'Failed to fetch users.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to connect to server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [role]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchUsers();
  };

  const handleToggleActive = async (user) => {
    setError(null);
    setSuccess(null);

    if (user.id === loggedInUser.id) {
      setError('You cannot deactivate your own account.');
      return;
    }

    try {
      const res = await adminService.updateUser(user.id, {
        is_active: !user.is_active,
      });
      if (res?.success) {
        setSuccess(`User "${res.data.username}" is_active toggled.`);
        fetchUsers();
      } else {
        setError(res?.message || 'Failed to toggle active state.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update user.');
    }
  };

  const handleRoleChange = async (user, newRole) => {
    setError(null);
    setSuccess(null);

    if (user.id === loggedInUser.id) {
      setError('You cannot change your own role.');
      return;
    }

    try {
      const res = await adminService.updateUser(user.id, {
        role: newRole,
      });
      if (res?.success) {
        setSuccess(`User "${res.data.username}" role updated to ${newRole}.`);
        fetchUsers();
      } else {
        setError(res?.message || 'Failed to update role.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to change role.');
    }
  };

  return (
    <AdminLayout>
      {/* Title */}
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
          User Directory & Management
        </h1>

      </div>

      {success && <Alert type="success" message={success} className="mb-6" onClose={() => setSuccess(null)} />}
      {error && <Alert type="error" message={error} className="mb-6" onClose={() => setError(null)} />}

      {/* Search & Filter Toolbar */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 mb-6 bg-white border border-slate-200 p-4 rounded-xl shadow-xs">
        <form onSubmit={handleSearchSubmit} className="flex-1 max-w-md flex items-center space-x-2">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="block w-full rounded-lg border border-slate-300 px-3 py-1.5 text-xs text-slate-900 placeholder-slate-400 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 bg-white"
            placeholder="Search by username, email, name..."
          />
          <Button type="submit" size="sm" icon={Search}>
            Search
          </Button>
        </form>

        <div className="flex items-center space-x-3 text-xs">
          <label className="font-semibold text-slate-500 uppercase tracking-wide">Role:</label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="rounded-lg border border-slate-300 px-3 py-1.5 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-1 focus:ring-cyan-500 bg-white"
          >
            <option value="">All Roles</option>
            <option value="student">Student</option>
            <option value="admin">Administrator</option>
          </select>
        </div>
      </div>

      <Card title="Active Users Log" subtitle="Directory of registered accounts." bodyClassName="p-0">
        {loading ? (
          <Loader size="lg" className="my-12" />
        ) : users.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-150">
              <thead className="bg-slate-50 text-[10px] font-bold uppercase tracking-wider text-slate-500 text-left">
                <tr>
                  <th className="px-6 py-3">User</th>
                  <th className="px-6 py-3">Email</th>
                  <th className="px-6 py-3">Total XP</th>
                  <th className="px-6 py-3">Role</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs text-slate-600">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50/50 transition">
                    <td className="px-6 py-4">
                      <div className="font-semibold text-slate-800">{u.full_name || u.username}</div>
                      <div className="text-[10px] text-slate-400 mt-0.5">@{u.username}</div>
                    </td>
                    <td className="px-6 py-4 text-slate-500 font-semibold">{u.email}</td>
                    <td className="px-6 py-4 font-bold text-cyan-600">
                      {u.role === 'student' ? `${u.total_xp || 0} XP` : '—'}
                    </td>
                    <td className="px-6 py-4 font-medium uppercase text-[10px]">
                      {u.id === loggedInUser.id ? (
                        <span className="px-2 py-0.5 rounded-full border bg-slate-100 border-slate-300 text-slate-800">
                          {u.role} (You)
                        </span>
                      ) : (
                        <select
                          value={u.role}
                          onChange={(e) => handleRoleChange(u, e.target.value)}
                          className="rounded-lg border border-slate-350 px-2 py-1 text-[10px] font-semibold text-slate-700 bg-white"
                        >
                          <option value="student">student</option>
                          <option value="admin">admin</option>
                        </select>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-1.5 font-bold">
                        {u.is_active ? (
                          <>
                            <CheckCircle className="w-4 h-4 text-emerald-500" />
                            <span className="text-emerald-700 text-[10px] uppercase">Active</span>
                          </>
                        ) : (
                          <>
                            <XCircle className="w-4 h-4 text-rose-500" />
                            <span className="text-rose-700 text-[10px] uppercase">Suspended</span>
                          </>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      {u.id !== loggedInUser.id && (
                        <Button
                          variant="ghost"
                          size="sm"
                          className={u.is_active ? 'text-rose-600 hover:bg-rose-50' : 'text-emerald-600 hover:bg-emerald-50'}
                          onClick={() => handleToggleActive(u)}
                        >
                          {u.is_active ? 'Suspend' : 'Activate'}
                        </Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-6">
            <EmptyState title="No matching users found" icon={Users} />
          </div>
        )}
      </Card>
    </AdminLayout>
  );
};

export default UsersManagePage;
