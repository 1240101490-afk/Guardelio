import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import categoriesService from '../../api/categoriesService';
import StudentLayout from '../../components/layout/StudentLayout';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import EmptyState from '../../components/common/EmptyState';
import { BookOpen, Clock, Zap, ArrowLeft, Shield } from 'lucide-react';
import { DIFFICULTY_LABELS, DIFFICULTY_COLORS } from '../../utils/constants';

const CategoryDetailPage = () => {
  const { slug } = useParams();
  const [category, setCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategoryDetails = async () => {
      try {
        const res = await categoriesService.getCategoryBySlug(slug);
        if (res?.success) {
          setCategory(res.data);
        } else {
          setError(res?.message || 'Failed to load category details.');
        }
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to connect to the backend server.');
      } finally {
        setLoading(false);
      }
    };
    fetchCategoryDetails();
  }, [slug]);

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
          <Alert type="error" message="Category Detail Error" description={error} />
        </div>
      </StudentLayout>
    );
  }

  const { name, description, scenarios = [] } = category || {};

  return (
    <StudentLayout>
      {/* Back button */}
      <Link to="/categories" className="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-500 hover:text-slate-700 transition mb-6">
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Categories</span>
      </Link>

      {/* Category Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 text-white mb-8">
        <div className="inline-flex items-center space-x-2 px-2.5 py-1 bg-cyan-500/10 border border-cyan-500/20 rounded-full text-cyan-400 text-[10px] font-bold uppercase tracking-wider mb-4">
          <Shield className="w-3.5 h-3.5" />
          <span>NIST Incident Domain</span>
        </div>
        <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight margin-none text-white leading-9">
          {name}
        </h1>
        <p className="mt-4 text-xs text-slate-350 leading-relaxed max-w-3xl">
          {description}
        </p>
      </div>

      <h2 className="text-lg font-bold text-slate-800 mb-6">Available Training Scenarios</h2>

      {scenarios.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {scenarios.map((scenario) => (
            <Card
              key={scenario.id}
              bodyClassName="p-6 flex flex-col justify-between h-full"
              className="hover:shadow-md transition duration-300 border border-slate-200"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[10px] font-bold text-slate-400 tracking-wider">
                    ID: {scenario.scenario_id}
                  </span>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                      DIFFICULTY_COLORS[scenario.difficulty] || 'bg-slate-100'
                    }`}
                  >
                    {DIFFICULTY_LABELS[scenario.difficulty]}
                  </span>
                </div>
                <h3 className="font-bold text-slate-800 text-base mb-2">{scenario.title}</h3>
                <p className="text-slate-500 text-xs leading-relaxed mb-6 line-clamp-3">
                  {scenario.overview || 'No overview available.'}
                </p>
              </div>

              <div className="border-t border-slate-100 pt-4 flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-4 sm:space-y-0 text-xs">
                <div className="flex items-center space-x-4 text-slate-400 font-semibold">
                  <div className="flex items-center space-x-1">
                    <Clock className="w-4 h-4" />
                    <span>{scenario.estimated_duration_minutes}m</span>
                  </div>
                  <div className="flex items-center space-x-1 text-cyan-600">
                    <Zap className="w-4 h-4" />
                    <span>+{scenario.xp_completion_bonus} XP</span>
                  </div>
                </div>
                <Link to={`/scenarios/${scenario.id}`} className="w-full sm:w-auto">
                  <Button size="sm" className="w-full sm:w-auto">
                    View Details
                  </Button>
                </Link>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No scenarios found"
          description="There are no scenarios currently available in this category."
          icon={BookOpen}
        />
      )}
    </StudentLayout>
  );
};

export default CategoryDetailPage;
