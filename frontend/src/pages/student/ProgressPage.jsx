import React, { useState, useEffect } from 'react';
import StudentLayout from '../../components/layout/StudentLayout';
import progressService from '../../api/progressService';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import Card from '../../components/common/Card';
import Badge from '../../components/common/Badge';
import EmptyState from '../../components/common/EmptyState';
import { Award, History, Zap, BarChart3, Clock, CheckCircle } from 'lucide-react';
import { DIFFICULTY_LABELS } from '../../utils/constants';

const ProgressPage = () => {
  const [activeTab, setActiveTab] = useState('history');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // States for each section
  const [sessions, setSessions] = useState([]);
  const [badgesData, setBadgesData] = useState({ badges: [], total_earned: 0, total_badges: 0 });
  const [xpHistory, setXpHistory] = useState([]);
  const [stats, setStats] = useState({ category_breakdown: {}, nist_phase_breakdown: {}, total_xp: 0, total_completed: 0 });

  useEffect(() => {
    const loadTabData = async () => {
      setLoading(true);
      setError(null);
      try {
        if (activeTab === 'history') {
          const res = await progressService.getSessions();
          if (res?.success) setSessions(res.data);
        } else if (activeTab === 'badges') {
          const res = await progressService.getAllBadges();
          if (res?.success) setBadgesData(res.data);
        } else if (activeTab === 'xp') {
          const res = await progressService.getXPHistory();
          if (res?.success) setXpHistory(res.data);
        } else if (activeTab === 'stats') {
          const res = await progressService.getLearningStats();
          if (res?.success) setStats(res.data);
        }
      } catch (err) {
        setError(err.response?.data?.message || `Failed to fetch data for ${activeTab}.`);
      } finally {
        setLoading(false);
      }
    };
    loadTabData();
  }, [activeTab]);

  return (
    <StudentLayout>
      {/* Title */}
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
          My Learning Progress
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Review your operational simulation logs, unlocked badges, XP transactions, and skill summaries.
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-slate-200 mb-6">
        <nav className="flex space-x-6" aria-label="Tabs">
          {[
            { id: 'history', label: 'History', icon: History },
            { id: 'badges', label: 'Badges Catalog', icon: Award },
            { id: 'xp', label: 'XP Log', icon: Zap },
            { id: 'stats', label: 'Skill Analytics', icon: BarChart3 },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 text-xs font-semibold uppercase tracking-wider focus:outline-none transition ${
                  activeTab === tab.id
                    ? 'border-cyan-600 text-cyan-600'
                    : 'border-transparent text-slate-400 hover:text-slate-600 hover:border-slate-300'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Context wrapper */}
      {error && (
        <div className="mb-6">
          <Alert type="error" message="Error loading tab data" description={error} />
        </div>
      )}

      {loading ? (
        <Loader size="lg" className="my-12" />
      ) : (
        <div className="space-y-6">
          {/* History Tab */}
          {activeTab === 'history' && (
            <Card
              title="Simulation Sessions History"
              subtitle="Every incident simulation session completed or in progress."
              bodyClassName="p-0"
            >
              {sessions.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-slate-150">
                    <thead className="bg-slate-50 text-[10px] font-bold uppercase tracking-wider text-slate-500 text-left">
                      <tr>
                        <th className="px-6 py-3">ID Code</th>
                        <th className="px-6 py-3">Scenario</th>
                        <th className="px-6 py-3">Difficulty</th>
                        <th className="px-6 py-3">XP Earned</th>
                        <th className="px-6 py-3">Accuracy</th>
                        <th className="px-6 py-3">Status</th>
                        <th className="px-6 py-3">Completed At</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 text-xs text-slate-600">
                      {sessions.map((session) => (
                        <tr key={session.id} className="hover:bg-slate-50/50 transition">
                          <td className="px-6 py-4 font-bold text-slate-400">
                            {session.scenario_id_code}
                          </td>
                          <td className="px-6 py-4 font-semibold text-slate-800">
                            {session.scenario_title}
                          </td>
                          <td className="px-6 py-4 capitalize">{session.difficulty}</td>
                          <td className="px-6 py-4 text-cyan-600 font-bold">
                            +{session.total_xp_earned} XP
                          </td>
                          <td className="px-6 py-4 font-bold">{session.accuracy_percent}%</td>
                          <td className="px-6 py-4">
                            <span
                              className={`px-2 py-0.5 rounded-full border text-[10px] font-bold uppercase ${
                                session.status === 'completed'
                                  ? 'bg-emerald-50 border-emerald-200 text-emerald-700'
                                  : 'bg-amber-50 border-amber-200 text-amber-700'
                              }`}
                            >
                              {session.status}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            {session.completed_at
                              ? new Date(session.completed_at).toLocaleDateString()
                              : '—'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="p-6">
                  <EmptyState
                    title="No simulation history"
                    description="You have not participated in any incident response simulations yet."
                    icon={History}
                  />
                </div>
              )}
            </Card>
          )}

          {/* Badges Tab */}
          {activeTab === 'badges' && (
            <div className="space-y-6">
              <div className="bg-slate-100 border border-slate-200 rounded-xl p-4 text-xs font-semibold text-slate-600 flex items-center justify-between">
                <span>Total Badges Earned:</span>
                <span className="bg-cyan-600 text-white px-3 py-1 rounded-full text-xs font-extrabold">
                  {badgesData.total_earned} of {badgesData.total_badges}
                </span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {badgesData.badges.map((badge) => (
                  <Badge
                    key={badge.id}
                    name={badge.name}
                    description={badge.description}
                    badgeType={badge.badge_type}
                    iconName={badge.icon_name}
                    isEarned={badge.is_earned}
                    earnedAt={badge.earned_at}
                  />
                ))}
              </div>
            </div>
          )}

          {/* XP Log Tab */}
          {activeTab === 'xp' && (
            <Card
              title="XP Transaction History"
              subtitle="Every point earned from decision submissions and completion bonuses."
              bodyClassName="p-0"
            >
              {xpHistory.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-slate-150">
                    <thead className="bg-slate-50 text-[10px] font-bold uppercase tracking-wider text-slate-500 text-left">
                      <tr>
                        <th className="px-6 py-3">Activity</th>
                        <th className="px-6 py-3">Details</th>
                        <th className="px-6 py-3">XP Change</th>
                        <th className="px-6 py-3">Balance After</th>
                        <th className="px-6 py-3">Timestamp</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 text-xs text-slate-600">
                      {xpHistory.map((log) => (
                        <tr key={log.id} className="hover:bg-slate-50/50 transition">
                          <td className="px-6 py-4 font-semibold text-slate-800 capitalize">
                            {log.transaction_type_label}
                          </td>
                          <td className="px-6 py-4 text-slate-500">{log.description}</td>
                          <td className="px-6 py-4 text-cyan-600 font-bold">+{log.amount} XP</td>
                          <td className="px-6 py-4 text-slate-700 font-bold">
                            {log.balance_after} XP
                          </td>
                          <td className="px-6 py-4">
                            {new Date(log.earned_at).toLocaleString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="p-6">
                  <EmptyState
                    title="No XP logs"
                    description="Perform actions in active scenarios to start generating XP logs."
                    icon={Zap}
                  />
                </div>
              )}
            </Card>
          )}

          {/* Skill Analytics Tab */}
          {activeTab === 'stats' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Category Breakdown */}
              <Card
                title="Category Completion Stats"
                subtitle="Completions by security domain categories."
              >
                <div className="space-y-4">
                  {Object.keys(stats.category_breakdown || {}).length > 0 ? (
                    Object.entries(stats.category_breakdown).map(([name, catData]) => {
                      const completed = catData.completed || 0;
                      const total = catData.total || 0;
                      const percent = total > 0 ? Math.round((completed / total) * 100) : 0;
                      return (
                        <div key={name} className="space-y-1 text-xs">
                          <div className="flex justify-between font-semibold text-slate-700">
                            <span>{name}</span>
                            <span>
                              {completed}/{total} ({percent}%)
                            </span>
                          </div>
                          <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden border border-slate-200/50">
                            <div
                              className="bg-cyan-600 h-full rounded-full transition-all duration-350"
                              style={{ width: `${percent}%` }}
                            />
                          </div>
                        </div>
                      );
                    })
                  ) : (
                    <p className="text-xs text-slate-400 text-center py-4">
                      No category stats available yet.
                    </p>
                  )}
                </div>
              </Card>

              {/* NIST Phase Breakdown */}
              <Card
                title="Incident Response Phase Performance"
                subtitle="Accuracy metrics aligned with the NIST SP 800-61 framework."
              >
                <div className="space-y-4">
                  {Object.keys(stats.nist_phase_breakdown || {}).length > 0 ? (
                    Object.entries(stats.nist_phase_breakdown).map(([phase, phaseData]) => {
                      const correct = phaseData.correct || 0;
                      const total = phaseData.total || 0;
                      const percent = total > 0 ? Math.round((correct / total) * 100) : 0;
                      return (
                        <div key={phase} className="space-y-1 text-xs">
                          <div className="flex justify-between font-semibold text-slate-700">
                            <span className="capitalize">{phase.replace('_', ' ')}</span>
                            <span>{percent}% Accuracy</span>
                          </div>
                          <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden border border-slate-200/50">
                            <div
                              className="bg-emerald-600 h-full rounded-full transition-all duration-350"
                              style={{ width: `${percent}%` }}
                            />
                          </div>
                          <span className="text-[10px] text-slate-400 block font-semibold">
                            {correct} correct decisions out of {total} attempts
                          </span>
                        </div>
                      );
                    })
                  ) : (
                    <p className="text-xs text-slate-400 text-center py-4">
                      No incident phase stats available. Complete scenarios containing decision points.
                    </p>
                  )}
                </div>
              </Card>
            </div>
          )}
        </div>
      )}
    </StudentLayout>
  );
};

export default ProgressPage;
