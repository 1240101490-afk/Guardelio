import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import simulationService from '../../api/simulationService';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import {
  Shield,
  Clock,
  ArrowLeft,
  ChevronRight,
  HelpCircle,
  Award,
  BookOpen,
} from 'lucide-react';
import { NIST_PHASE_LABELS } from '../../utils/constants';

const SimulationPage = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();

  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const [selectedOption, setSelectedOption] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [confirmExit, setConfirmExit] = useState(false);

  // For tracking which next_step and status is queued up next
  const [queuedNextStep, setQueuedNextStep] = useState(null);
  const [queuedStatus, setQueuedStatus] = useState(null);

  useEffect(() => {
    const fetchSession = async () => {
      try {
        const res = await simulationService.getSessionState(sessionId);
        if (res?.success) {
          const sessionData = res.data;
          
          // If already finished, direct to results page
          if (sessionData.status === 'completed' || sessionData.status === 'failed') {
            navigate(`/simulation/${sessionId}/results`, { replace: true });
            return;
          }
          
          setSession(sessionData);
        } else {
          setError(res?.message || 'Failed to load simulation session.');
        }
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to connect to the server.');
      } finally {
        setLoading(false);
      }
    };
    fetchSession();
  }, [sessionId, navigate]);

  const handleOptionSelect = (optionId) => {
    if (feedback) return; // Disallow changing choice once feedback is shown
    setSelectedOption(optionId);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (session?.current_step?.step_type === 'decision' && !selectedOption) {
      setError('Please select an option to submit.');
      return;
    }

    setError(null);
    setSubmitting(true);

    try {
      const optionId = session?.current_step?.step_type === 'decision' ? selectedOption : null;
      const res = await simulationService.respondToStep(sessionId, optionId);

      if (res?.success && res?.data) {
        const { feedback: fbData, next_step, session_status } = res.data;

        if (session?.current_step?.step_type === 'info') {
          // Info step has no feedback, advance immediately
          if (session_status === 'completed' || session_status === 'failed') {
            navigate(`/simulation/${sessionId}/results`, { replace: true });
          } else if (next_step) {
            setSession({
              ...session,
              current_step: next_step,
              status: session_status,
            });
            setSelectedOption(null);
            setFeedback(null);
          }
        } else {
          // Decision step: show feedback card first, queue the next step
          setFeedback(fbData);
          setQueuedNextStep(next_step);
          setQueuedStatus(session_status);
        }
      } else {
        setError(res?.message || 'Failed to record response.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to submit response.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleContinue = () => {
    if (queuedStatus === 'completed' || queuedStatus === 'failed') {
      navigate(`/simulation/${sessionId}/results`, { replace: true });
      return;
    }

    if (queuedNextStep) {
      setSession({
        ...session,
        current_step: queuedNextStep,
        status: queuedStatus,
      });
    }

    // Reset interaction states
    setSelectedOption(null);
    setFeedback(null);
    setQueuedNextStep(null);
    setQueuedStatus(null);
  };

  const handleExitSimulation = () => {
    setConfirmExit(true);
  };

  const confirmExitAction = () => {
    navigate('/dashboard');
  };

  if (loading) return <Loader fullScreen />;

  if (error && !feedback) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full">
          <Alert
            type="error"
            message="Simulation Error"
            description={error}
            onClose={() => setError(null)}
          />
          <div className="mt-4 text-center">
            <Button variant="secondary" onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </Button>
          </div>
        </div>
      </div>
    );
  }

  const { scenario, current_step } = session || {};
  const progressPercent = scenario
    ? Math.round(((current_step?.step_number || 1) / (scenario.total_steps || 1)) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Immersive Header */}
      <header className="bg-white border-b border-slate-200 h-16 flex items-center justify-between px-6 sticky top-0 z-40">
        <div className="flex items-center space-x-3">
          <div className="bg-cyan-600 text-white p-2 rounded-lg">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs text-slate-400 font-bold uppercase tracking-wider block">
              Simulation Session
            </span>
            <span className="text-sm font-bold text-slate-800 line-clamp-1">
              {scenario?.title}
            </span>
          </div>
        </div>

        <Button variant="outline" size="sm" icon={ArrowLeft} onClick={handleExitSimulation}>
          Exit
        </Button>
      </header>

      {/* Main Container */}
      <main className="flex-1 flex flex-col max-w-3xl w-full mx-auto px-4 py-8 justify-center">
        {/* Progress Tracker */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2 text-xs font-semibold text-slate-500">
            <span>
              Step {current_step?.step_number} of {scenario?.total_steps}
            </span>
            <span>{progressPercent}% Complete</span>
          </div>
          <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-cyan-600 h-full rounded-full transition-all duration-350"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>

        {/* Dynamic Step View */}
        <Card
          title={current_step?.title}
          subtitle={`Operational Phase: ${NIST_PHASE_LABELS[current_step?.nist_phase]}`}
          headerClassName="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50"
          bodyClassName="p-6 space-y-6"
        >
          {/* Situation Text */}
          <div className="text-sm text-slate-700 leading-relaxed whitespace-pre-line bg-slate-50/50 p-4 border border-slate-150 rounded-xl font-medium">
            {current_step?.situation_text}
          </div>

          {/* Form wrapper */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Options List */}
            {current_step?.step_type === 'decision' && (
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                  Select your operational response
                </h4>
                {current_step?.options.map((option) => (
                  <div
                    key={option.id}
                    onClick={() => handleOptionSelect(option.id)}
                    className={`border rounded-xl p-4 cursor-pointer transition flex items-start space-x-3 ${
                      selectedOption === option.id
                        ? 'border-cyan-500 bg-cyan-50/45 ring-1 ring-cyan-500'
                        : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/40'
                    } ${feedback ? 'pointer-events-none' : ''}`}
                  >
                    <input
                      type="radio"
                      name="decision_option"
                      checked={selectedOption === option.id}
                      onChange={() => {}}
                      className="mt-1 h-4 w-4 border-slate-300 text-cyan-600 focus:ring-cyan-500 flex-shrink-0"
                    />
                    <span className="text-xs text-slate-700 font-semibold leading-relaxed">
                      {option.option_text}
                    </span>
                  </div>
                ))}
              </div>
            )}

            {/* Error handling inside page context */}
            {error && <Alert type="error" message={error} onClose={() => setError(null)} />}

            {/* Response actions block */}
            {!feedback ? (
              <div className="pt-2 flex justify-end">
                <Button
                  type="submit"
                  loading={submitting}
                  disabled={current_step?.step_type === 'decision' && !selectedOption}
                  icon={ChevronRight}
                >
                  {current_step?.step_type === 'decision' ? 'Submit Decision' : 'Continue'}
                </Button>
              </div>
            ) : (
              /* Inline Feedback Card */
              <div
                className={`border rounded-xl p-5 mt-6 ${
                  feedback.is_correct
                    ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
                    : feedback.consequence_type === 'neutral'
                    ? 'bg-amber-50 border-amber-200 text-amber-800'
                    : 'bg-rose-50 border-rose-200 text-rose-800'
                }`}
              >
                <div className="flex items-center space-x-2 font-bold text-sm mb-2">
                  <span>
                    {feedback.is_correct
                      ? '✅ Correct Action'
                      : feedback.consequence_type === 'neutral'
                      ? '⚠️ Partially Correct'
                      : '❌ Incorrect Action'}
                  </span>
                  <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-white border/40">
                    +{feedback.xp_earned} XP
                  </span>
                </div>
                <p className="text-xs leading-relaxed font-medium mb-4">
                  {feedback.feedback_text}
                </p>
                <div className="flex justify-end">
                  <Button
                    variant={feedback.is_correct ? 'primary' : 'secondary'}
                    onClick={handleContinue}
                  >
                    Continue Simulation
                  </Button>
                </div>
              </div>
            )}
          </form>
        </Card>
      </main>

      {/* Confirmation Exit dialog */}
      <ConfirmDialog
        isOpen={confirmExit}
        title="Exit Simulation?"
        message="Are you sure you want to exit? Your progress is saved, and you can resume this session later from the dashboard."
        confirmLabel="Exit to Dashboard"
        cancelLabel="Stay in Simulation"
        onConfirm={confirmExitAction}
        onCancel={() => setConfirmExit(false)}
      />
    </div>
  );
};

export default SimulationPage;
