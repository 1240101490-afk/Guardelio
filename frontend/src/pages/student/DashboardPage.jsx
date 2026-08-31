import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import progressService from '../../api/progressService';
import StudentLayout from '../../components/layout/StudentLayout';
import StatCard from '../../components/common/StatCard';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import EmptyState from '../../components/common/EmptyState';
import {
  Award,
  Zap,
  Target,
  CheckCircle,
  Play,
  ArrowRight,
  BookOpen,
  History,
} from 'lucide-react';
import { DIFFICULTY_LABELS } from '../../utils/constants';
import { getDisplayName } from '../../utils/formatters';

const DashboardPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await progressService.getDashboard();
        if (res?.success) {
          setData(res.data);
        } else {
          setError(res?.message || 'Failed to load dashboard data.');
        }
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to connect to the backend server.');
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <StudentLayout>
        <Loader fullScreen />
      </StudentLayout>
    );
  }

  if (error) {
    return (
      <StudentLayout>
        <div className="max-w-3xl mx-auto mt-8">
          <Alert type="error" message="Dashboard Error" description={error} />
        </div>
      </StudentLayout>
    );
  }

  const {
    total_xp = 0,
    completed_count = 0,
    badge_count = 0,
    average_accuracy = 0,
    recent_sessions = [],
    recent_badges = [],
    in_progress_sessions = [],
  } = data || {};

  return (
    <StudentLayout>
      {/* Welcome Banner */}
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
          Welcome back, {getDisplayName(user)}!
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Track your metrics, view earned credentials, and resume active simulations.
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Total XP" value={`${total_xp} XP`} icon={Zap} />
        <StatCard
          title="Completions"
          value={completed_count}
          icon={CheckCircle}
          colorClass="text-emerald-600 bg-emerald-50 border-emerald-100"
        />
        <StatCard
          title="Accuracy"
          value={`${average_accuracy}%`}
          icon={Target}
          colorClass="text-amber-600 bg-amber-50 border-amber-100"
        />
        <StatCard
          title="Badges Earned"
          value={badge_count}
          icon={Award}
          colorClass="text-purple-600 bg-purple-50 border-purple-100"
        />
      </div>

      {/* Active / Continue Learning */}
      <div className="mb-8">
        <Card
          title="Resume Learning"
          subtitle="Continue where you left off in your ongoing simulations."
          action={
            <Link to="/categories">
              <Button size="sm" variant="ghost">
                Browse All <ArrowRight className="w-4 h-4 ml-1" />
              </Button>
            </Link>
          }
        >
          {in_progress_sessions.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {in_progress_sessions.map((session) => (
                <div
                  key={session.id}
                  className="flex items-center justify-between p-4 border border-slate-200 rounded-xl bg-slate-50 hover:bg-slate-100/75 transition"
                >
                  <div className="min-w-0 pr-4">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide block">
                      {session.category_name}
                    </span>
                    <h4 className="font-semibold text-slate-800 text-sm truncate mt-0.5">
                      {session.scenario_title}
                    </h4>
                    <span className="text-[10px] text-slate-500 block mt-1">
                      Started: {new Date(session.started_at).toLocaleDateString()}
                    </span>
                  </div>
                  <Button
                    size="sm"
                    icon={Play}
                    onClick={() => navigate(`/simulation/${session.id}`)}
                  >
                    Resume
                  </Button>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState
              title="No active simulations"
              description="Start a new scenario in any of the categories to test your skills."
              icon={BookOpen}
              action={
                <Link to="/categories">
                  <Button size="sm">Explore Scenarios</Button>
                </Link>
              }
            />
          )}
        </Card>
      </div>

      {/* Split List View: Recent Sessions / Recent Badges */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent History */}
        <div className="lg:col-span-2">
          <Card
            title="Recent Simulations"
            subtitle="Your latest incident response exercise logs."
            bodyClassName="p-0"
          >
            {recent_sessions.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-150">
                  <thead className="bg-slate-50 text-[10px] font-bold uppercase tracking-wider text-slate-500 text-left">
                    <tr>
                      <th className="px-6 py-3">Scenario</th>
                      <th className="px-6 py-3">Accuracy</th>
                      <th className="px-6 py-3">XP</th>
                      <th className="px-6 py-3">Completed</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-xs text-slate-600">
                    {recent_sessions.map((session) => (
                      <tr key={session.id} className="hover:bg-slate-50/50 transition">
                        <td className="px-6 py-4 font-semibold text-slate-800">
                          {session.scenario_title}
                        </td>
                        <td className="px-6 py-4">
                          <span className="font-bold text-slate-700">
                            {session.accuracy_percent}%
                          </span>
                        </td>
                        <td className="px-6 py-4 text-cyan-600 font-bold">
                          +{session.total_xp_earned} XP
                        </td>
                        <td className="px-6 py-4">
                          {session.completed_at
                            ? new Date(session.completed_at).toLocaleDateString()
                            : 'In Progress'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="p-6">
                <EmptyState
                  title="No sessions completed yet"
                  description="Your completed incident simulation records will appear here."
                  icon={History}
                />
              </div>
            )}
          </Card>
        </div>

        {/* Recent Badges */}
        <div>
          <Card title="Latest Badges" subtitle="Newly unlocked accomplishments." bodyClassName="p-6">
            {recent_badges.length > 0 ? (
              <div className="grid grid-cols-2 gap-4">
                {recent_badges.slice(0, 4).map((ub) => {
                  const toPascalCase = (str) => {
                    if (!str) return 'Award';
                    return str
                      .split('-')
                      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
                      .join('');
                  };
                  return (
                    <div
                      key={ub.id}
                      className="flex flex-col items-center p-3 border border-slate-150 rounded-xl text-center bg-slate-50 hover:bg-slate-100/50 transition"
                    >
                      <div className="p-2 bg-white rounded-full border border-slate-200/50 mb-2">
                        {/* Dynamic resolve fallback */}
                        <Award className="w-5 h-5 text-cyan-600" />
                      </div>
                      <span className="font-bold text-slate-800 text-[11px] leading-tight block">
                        {ub.badge?.name}
                      </span>
                      <span className="text-[9px] text-slate-400 font-semibold uppercase block mt-1">
                        {ub.badge?.badge_type}
                      </span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <EmptyState
                title="No badges earned"
                description="Complete scenarios with high accuracy to earn credentials."
                icon={Award}
              />
            )}
          </Card>
        </div>
      </div>
    </StudentLayout>
  );
};

export default DashboardPage;
