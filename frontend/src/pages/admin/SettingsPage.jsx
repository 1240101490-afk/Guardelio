import React from 'react';
import AdminLayout from '../../components/layout/AdminLayout';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Alert from '../../components/common/Alert';
import { useAuth } from '../../context/AuthContext';
import { Save, User, ShieldAlert } from 'lucide-react';

const SettingsPage = () => {
  const { user } = useAuth();

  return (
    <AdminLayout>
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
          Platform Settings
        </h1>

      </div>

      <div className="max-w-2xl space-y-6">
        <Card title="Administrator Account Profile" subtitle="Basic system identifier details.">
          <div className="space-y-4 text-xs">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="font-semibold text-slate-400 block mb-1">First Name</span>
                <span className="font-bold text-slate-800 bg-slate-50 border p-2 rounded-lg block border-slate-200">
                  {user?.first_name || 'Administrator'}
                </span>
              </div>
              <div>
                <span className="font-semibold text-slate-400 block mb-1">Last Name</span>
                <span className="font-bold text-slate-800 bg-slate-50 border p-2 rounded-lg block border-slate-200">
                  {user?.last_name || 'User'}
                </span>
              </div>
            </div>

            <div>
              <span className="font-semibold text-slate-400 block mb-1">Email Address</span>
              <span className="font-bold text-slate-800 bg-slate-50 border p-2 rounded-lg block border-slate-200">
                {user?.email}
              </span>
            </div>

            <div>
              <span className="font-semibold text-slate-400 block mb-1">Operational Role</span>
              <span className="font-bold text-slate-800 bg-slate-50 border p-2 rounded-lg block border-slate-200 uppercase tracking-wide">
                {user?.role}
              </span>
            </div>
          </div>
        </Card>

        <Card title="Operational Parameters" subtitle="Configuration of external servers.">
          <div className="space-y-4">
            <Alert type="info" message="Server connection active" description="The frontend is currently connected to backend Rest APIs via CORS on http://localhost:8000/api/v1/." />
            
            <div className="text-xs space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                  Backend API Base URL
                </label>
                <input
                  type="text"
                  disabled
                  value="http://localhost:8000/api/v1"
                  className="mt-1.5 block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-slate-500 cursor-not-allowed sm:text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
                  Token Expiry Thresholds
                </label>
                <div className="grid grid-cols-2 gap-4 mt-1">
                  <div className="p-3 border rounded-xl bg-slate-50/50">
                    <span className="text-[10px] text-slate-400 font-bold block uppercase">Access JWT</span>
                    <span className="font-bold text-slate-700 block mt-0.5">15 Minutes</span>
                  </div>
                  <div className="p-3 border rounded-xl bg-slate-50/50">
                    <span className="text-[10px] text-slate-400 font-bold block uppercase">Refresh JWT</span>
                    <span className="font-bold text-slate-700 block mt-0.5">7 Days</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </AdminLayout>
  );
};

export default SettingsPage;
