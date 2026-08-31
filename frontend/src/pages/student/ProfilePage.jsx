import React, { useState } from 'react';
import StudentLayout from '../../components/layout/StudentLayout';
import { useAuth } from '../../context/AuthContext';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Alert from '../../components/common/Alert';
import { User, Zap, Mail, Calendar, Edit3 } from 'lucide-react';
import { getDisplayName, getInitials } from '../../utils/formatters';

const ProfilePage = () => {
  const { user, updateProfile } = useAuth();

  const [firstName, setFirstName] = useState(user?.first_name || '');
  const [lastName, setLastName] = useState(user?.last_name || '');
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!firstName.trim() || !lastName.trim()) {
      setError('First name and last name are required.');
      return;
    }

    setUpdating(true);
    const res = await updateProfile({
      first_name: firstName,
      last_name: lastName,
    });
    setUpdating(false);

    if (res.success) {
      setSuccess('Profile updated successfully.');
    } else {
      setError(res.message);
    }
  };

  return (
    <StudentLayout>
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
          My Account Profile
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Manage your personal details and view platform metrics.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Info card */}
        <div className="space-y-6">
          <Card title="Student Card" bodyClassName="p-6 text-center">
            <div className="w-20 h-20 rounded-full bg-cyan-100 text-cyan-800 border-2 border-cyan-200 flex items-center justify-center font-bold text-3xl mx-auto mb-4">
              {getInitials(user)}
            </div>
            <h3 className="text-lg font-bold text-slate-800">{getDisplayName(user)}</h3>
            <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider mt-0.5">
              Role: {user?.role}
            </p>

            <div className="border-t border-slate-100 mt-6 pt-6 text-xs text-left space-y-4">
              <div className="flex items-center space-x-3 text-slate-500">
                <Zap className="w-4 h-4 text-cyan-600" />
                <div>
                  <span className="font-semibold block text-slate-700">Total Score</span>
                  <span className="text-[11px] font-bold text-slate-500">{user?.total_xp || 0} XP</span>
                </div>
              </div>
              <div className="flex items-center space-x-3 text-slate-500">
                <Mail className="w-4 h-4 text-slate-400" />
                <div>
                  <span className="font-semibold block text-slate-700">Email Address</span>
                  <span className="text-[11px]">{user?.email}</span>
                </div>
              </div>
              <div className="flex items-center space-x-3 text-slate-500">
                <Calendar className="w-4 h-4 text-slate-400" />
                <div>
                  <span className="font-semibold block text-slate-700">Joined Platform</span>
                  <span className="text-[11px]">
                    {user?.date_joined ? new Date(user.date_joined).toLocaleDateString() : '—'}
                  </span>
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Update Card */}
        <div className="lg:col-span-2">
          <Card
            title="Edit Profile Details"
            subtitle="Update your name as it will display on completions and earned certificates."
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              {error && <Alert type="error" message={error} onClose={() => setError(null)} />}
              {success && <Alert type="success" message={success} onClose={() => setSuccess(null)} />}

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="firstName" className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                    First Name
                  </label>
                  <input
                    id="firstName"
                    type="text"
                    required
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-400 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label htmlFor="lastName" className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                    Last Name
                  </label>
                  <input
                    id="lastName"
                    type="text"
                    required
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-400 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wide">
                  Username (Immutable)
                </label>
                <input
                  type="text"
                  disabled
                  value={user?.username || ''}
                  className="mt-1.5 block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-slate-500 cursor-not-allowed sm:text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wide">
                  Email Address (Immutable)
                </label>
                <input
                  type="text"
                  disabled
                  value={user?.email || ''}
                  className="mt-1.5 block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-slate-500 cursor-not-allowed sm:text-sm"
                />
              </div>

              <div className="flex justify-end border-t border-slate-100 pt-6">
                <Button type="submit" loading={updating} icon={Edit3}>
                  Save Changes
                </Button>
              </div>
            </form>
          </Card>
        </div>
      </div>
    </StudentLayout>
  );
};

export default ProfilePage;
