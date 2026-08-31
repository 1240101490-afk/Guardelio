import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import scenariosService from '../../api/scenariosService';
import simulationService from '../../api/simulationService';
import StudentLayout from '../../components/layout/StudentLayout';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import { DIFFICULTY_LABELS, DIFFICULTY_COLORS } from '../../utils/constants';
import {
  Clock,
  Zap,
  ArrowLeft,
  Shield,
  Award,
  User,
  CheckCircle,
} from 'lucide-react';

const ScenarioOverviewPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [scenario, setScenario] = useState(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchScenarioDetails = async () => {
      try {
        const res = await scenariosService.getScenarioById(id);
        if (res?.success) {
          setScenario(res.data);
        } else {
          setError(res?.message || 'Failed to load scenario details.');
        }
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to connect to the backend server.');
      } finally {
        setLoading(false);
      }
    };
    fetchScenarioDetails();
  }, [id]);

  const handleStartSimulation = async () => {
    setStarting(true);
    try {
      const res = await simulationService.startSimulation(id);
      if (res?.success && res?.data?.session_id) {
        navigate(`/simulation/${res.data.session_id}`);
      } else {
        setError(res?.message || 'Failed to start simulation.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to initialize simulation session.');
    } finally {
      setStarting(false);
    }
  };

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
          <Alert type="error" message="Scenario Overview Error" description={error} />
        </div>
      </StudentLayout>
    );
  }

  const {
    title,
    scenario_id,
    difficulty,
    student_role,
    overview,
    estimated_duration_minutes,
    xp_completion_bonus,
    xp_perfect_score_bonus,
    total_xp_available,
    total_steps,
    decision_step_count,
    version,
    category_slug,
    category_name,
    learning_objectives = [],
    nist_phases_in_scenario = [],
  } = scenario || {};

  return (
    <StudentLayout>
      {/* Back button */}
      <Link
        to={`/categories/${category_slug}`}
        className="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-500 hover:text-slate-700 transition mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to {category_name}</span>
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Details (2/3 width) */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 md:p-8">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[10px] font-bold text-slate-400 tracking-wider">
                ID: {scenario_id} • v{version}
              </span>
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                  DIFFICULTY_COLORS[difficulty] || 'bg-slate-100'
                }`}
              >
                {DIFFICULTY_LABELS[difficulty]}
              </span>
            </div>
            <h1 className="text-xl md:text-2xl font-bold tracking-tight text-slate-800 leading-tight margin-none mb-4">
              {title}
            </h1>
            <p className="text-xs text-slate-500 leading-relaxed">{overview}</p>

            {/* Assigned Role */}
            <div className="mt-8 p-4 bg-cyan-50 border border-cyan-100 rounded-xl flex items-start space-x-3">
              <User className="w-5 h-5 text-cyan-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wide">
                  Assigned Operational Role
                </h4>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">{student_role}</p>
              </div>
            </div>
          </div>

          {/* Learning Objectives */}
          <Card title="Learning Objectives" subtitle="Skills you will acquire in this exercise.">
            {learning_objectives.length > 0 ? (
              <ul className="space-y-3.5 text-xs text-slate-600">
                {learning_objectives.map((obj) => (
                  <li key={obj.id} className="flex items-start space-x-3">
                    <CheckCircle className="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{obj.objective_text}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-slate-400">No specific learning objectives listed.</p>
            )}
          </Card>
        </div>

        {/* Action Panel (1/3 width) */}
        <div className="space-y-6">
          <Card title="Exercise Summary" bodyClassName="p-6 space-y-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 text-xs">
                <span className="text-slate-400 font-semibold flex items-center">
                  <Clock className="w-4 h-4 mr-2" /> Duration
                </span>
                <span className="font-bold text-slate-700">{estimated_duration_minutes} Minutes</span>
              </div>
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 text-xs">
                <span className="text-slate-400 font-semibold flex items-center">
                  <Award className="w-4 h-4 mr-2" /> Total Steps
                </span>
                <span className="font-bold text-slate-700">
                  {total_steps} ({decision_step_count} Decisions)
                </span>
              </div>
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 text-xs">
                <span className="text-slate-400 font-semibold flex items-center">
                  <Zap className="w-4 h-4 mr-2" /> Completion Bonus
                </span>
                <span className="font-bold text-cyan-600">+{xp_completion_bonus} XP</span>
              </div>
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 text-xs">
                <span className="text-slate-400 font-semibold flex items-center">
                  <Zap className="w-4 h-4 mr-2" /> Perfect Score Bonus
                </span>
                <span className="font-bold text-amber-600">+{xp_perfect_score_bonus} XP</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 font-semibold flex items-center">
                  <Zap className="w-4 h-4 mr-2" /> Total Potential
                </span>
                <span className="font-extrabold text-cyan-700">+{total_xp_available} XP</span>
              </div>
            </div>

            <Button
              className="w-full justify-center"
              size="lg"
              loading={starting}
              onClick={handleStartSimulation}
            >
              Start Simulation
            </Button>
          </Card>

          {/* NIST Coverage Map */}
          <Card title="NIST IR Framework Coverage" subtitle="Phases covered during this exercise.">
            {nist_phases_in_scenario.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {nist_phases_in_scenario.map((phase) => (
                  <span
                    key={phase.code}
                    className="inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-semibold bg-slate-100 border border-slate-200 text-slate-700 capitalize"
                  >
                    <Shield className="w-3 h-3 mr-1 text-cyan-600" />
                    {phase.label}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-400">No specific NIST phases mapped.</p>
            )}
          </Card>
        </div>
      </div>
    </StudentLayout>
  );
};

export default ScenarioOverviewPage;
