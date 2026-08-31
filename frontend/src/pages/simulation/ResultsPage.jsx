import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import simulationService from '../../api/simulationService';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import Badge from '../../components/common/Badge';
import { useAuth } from '../../context/AuthContext';
import {
  Award,
  Zap,
  Target,
  Clock,
  ArrowRight,
  RefreshCw,
  LayoutDashboard,
  CheckCircle,
  XCircle,
  BookOpen,
} from 'lucide-react';
import { DIFFICULTY_LABELS, DIFFICULTY_COLORS } from '../../utils/constants';

const ResultsPage = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retrying, setRetrying] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const res = await simulationService.getSessionResult(sessionId);
        if (res?.success) {
          setResult(res.data);
        } else {
          setError(res?.message || 'Failed to load results.');
        }
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to fetch session results.');
      } finally {
        setLoading(false);
      }
    };
    fetchResults();
  }, [sessionId]);

  const handleRetry = async () => {
    if (!result?.scenario_id) return;
    setRetrying(true);
    try {
      const res = await simulationService.startSimulation(result.scenario_id);
      if (res?.success && res?.data?.session_id) {
        navigate(`/simulation/${res.data.session_id}`);
      } else {
        setError(res?.message || 'Failed to start a new simulation session.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to restart simulation.');
    } finally {
      setRetrying(false);
    }
  };

  if (loading) return <Loader fullScreen />;

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full">
          <Alert type="error" message="Results Error" description={error} />
          <div className="mt-4 text-center">
            <Button variant="secondary" onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </Button>
          </div>
        </div>
      </div>
    );
  }

  const {
    scenario_title,
    scenario_id_code,
    category_name,
    difficulty,
    total_xp_earned = 0,
    correct_decisions = 0,
    total_decisions = 0,
    accuracy_percent = 0,
    is_perfect_score = false,
    duration_minutes = 0,
    lessons_learned = '',
    decision_review = [],
    new_badges = [],
  } = result || {};

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4 md:px-8">
      <div className="max-w-4xl mx-auto space-y-8">
        
        {/* Results Header */}
        <div className="text-center bg-white border border-slate-200 rounded-2xl p-6 md:p-8">
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
            Simulation Completed Successfully
          </span>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight mt-1 margin-none leading-tight">
            {scenario_title}
          </h1>
          <p className="text-xs text-slate-500 mt-2">
            Category: {category_name} • Difficulty: {DIFFICULTY_LABELS[difficulty]}
          </p>

          {/* Performance Stats grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 border-t border-slate-100 pt-6">
            <div className="text-center p-3">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                Accuracy
              </span>
              <span className="text-xl font-bold text-slate-800 block mt-1">
                {accuracy_percent}%
              </span>
              <span className="text-[9px] text-slate-400">
                {correct_decisions} / {total_decisions} steps
              </span>
            </div>
            <div className="text-center p-3">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                XP Earned
              </span>
              <span className="text-xl font-bold text-cyan-600 block mt-1">
                +{total_xp_earned} XP
              </span>
              <span className="text-[9px] text-slate-400">added to total</span>
            </div>
            <div className="text-center p-3">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                Duration
              </span>
              <span className="text-xl font-bold text-slate-800 block mt-1">
                {Math.round(duration_minutes)}m
              </span>
              <span className="text-[9px] text-slate-400">elapsed time</span>
            </div>
            <div className="text-center p-3">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                Result Status
              </span>
              <span
                className={`inline-block text-[10px] font-bold px-2 py-0.5 rounded-full border mt-1.5 uppercase ${
                  is_perfect_score
                    ? 'bg-yellow-50 border-yellow-200 text-yellow-700'
                    : 'bg-emerald-50 border-emerald-200 text-emerald-700'
                }`}
              >
                {is_perfect_score ? '🏆 Perfect Score' : '✅ Pass'}
              </span>
            </div>
          </div>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center space-y-3 sm:space-y-0 sm:space-x-4">
            <Button
              variant="primary"
              icon={LayoutDashboard}
              onClick={() => navigate('/dashboard')}
            >
              Return to Dashboard
            </Button>
            <Button
              variant="secondary"
              icon={RefreshCw}
              loading={retrying}
              onClick={handleRetry}
            >
              Retry Simulation
            </Button>
          </div>
        </div>

        {/* Badges Earned Section */}
        {new_badges.length > 0 && (
          <Card
            title="Badges Awarded"
            subtitle="Congratulations! You met the criteria for unlocking the following credentials."
          >
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {new_badges.map((ub) => (
                <Badge
                  key={ub.id}
                  name={ub.badge.name}
                  description={ub.badge.description}
                  badgeType={ub.badge.badge_type}
                  iconName={ub.badge.icon_name}
                  isEarned
                  earnedAt={ub.earned_at}
                />
              ))}
            </div>
          </Card>
        )}

        {/* Lessons Learned */}
        {lessons_learned && (
          <Card
            title="Post-Incident Lessons Learned"
            subtitle="NIST Incident Response recommendations for your remediation log."
          >
            <div className="text-xs text-slate-600 leading-relaxed bg-slate-50 border border-slate-200 rounded-xl p-4 whitespace-pre-line font-medium">
              {lessons_learned}
            </div>
          </Card>
        )}

        {/* Decision Log Review */}
        <Card
          title="Decision Log & Performance Review"
          subtitle="Detailed audit breakdown of your selected choices."
          bodyClassName="p-0"
        >
          {decision_review.length > 0 ? (
            <div className="divide-y divide-slate-100">
              {decision_review.map((item, index) => (
                <div key={index} className="p-6 space-y-3 hover:bg-slate-50/50 transition">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-2 sm:space-y-0 text-xs">
                    <span className="font-bold text-slate-800">
                      Step {item.step_number}: {item.step_title}
                    </span>
                    <div className="flex items-center space-x-2">
                      <span className="font-semibold px-2 py-0.5 rounded-md bg-slate-100 border text-[10px] text-slate-500 capitalize">
                        {item.nist_phase_label}
                      </span>
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                          item.was_correct
                            ? 'bg-emerald-50 border-emerald-200 text-emerald-700'
                            : item.step_type === 'info'
                            ? 'bg-slate-50 border-slate-200 text-slate-600'
                            : 'bg-rose-50 border-rose-200 text-rose-700'
                        }`}
                      >
                        {item.step_type === 'info'
                          ? 'Info Step'
                          : item.was_correct
                          ? 'Correct'
                          : 'Incorrect'}
                      </span>
                    </div>
                  </div>

                  {item.step_type !== 'info' && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs mt-2">
                      <div className="p-3 border border-slate-150 rounded-xl bg-slate-50">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                          Your Choice
                        </span>
                        <p className="mt-1 font-semibold text-slate-700">
                          {item.chosen_option?.option_text || 'No choice submitted'}
                        </p>
                      </div>
                      <div className="p-3 border border-slate-150 rounded-xl bg-slate-50">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                          Correct Response
                        </span>
                        <p className="mt-1 font-semibold text-slate-700">
                          {item.correct_option?.option_text || 'None'}
                        </p>
                      </div>
                    </div>
                  )}

                  {item.step_type !== 'info' && item.chosen_option && (
                    <div
                      className={`text-[11px] leading-relaxed p-3 border rounded-xl font-medium ${
                        item.was_correct
                          ? 'bg-emerald-50/50 border-emerald-100 text-emerald-800'
                          : 'bg-rose-50/50 border-rose-100 text-rose-800'
                      }`}
                    >
                      <span className="font-bold block mb-1">Feedback Explanation:</span>
                      {item.chosen_option.feedback_text}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="p-6">
              <EmptyState title="No decision review logs" icon={BookOpen} />
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default ResultsPage;
