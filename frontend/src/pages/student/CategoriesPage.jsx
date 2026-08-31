import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import categoriesService from '../../api/categoriesService';
import StudentLayout from '../../components/layout/StudentLayout';
import Card from '../../components/common/Card';
import Loader from '../../components/common/Loader';
import Alert from '../../components/common/Alert';
import EmptyState from '../../components/common/EmptyState';
import * as LucideIcons from 'lucide-react';
import { BookOpen } from 'lucide-react';

const CategoriesPage = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await categoriesService.getCategories();
        if (res?.success) {
          setCategories(res.data);
        } else {
          setError(res?.message || 'Failed to load categories.');
        }
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to connect to the backend server.');
      } finally {
        setLoading(false);
      }
    };
    fetchCategories();
  }, []);

  const toPascalCase = (str) => {
    if (!str) return 'BookOpen';
    return str
      .split('-')
      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
      .join('');
  };

  const getThemeClasses = (color) => {
    const themes = {
      red: 'bg-rose-50 text-rose-600 border-rose-100 ring-rose-500/10',
      amber: 'bg-amber-50 text-amber-600 border-amber-100 ring-amber-500/10',
      blue: 'bg-blue-50 text-blue-600 border-blue-100 ring-blue-500/10',
      purple: 'bg-purple-50 text-purple-600 border-purple-100 ring-purple-500/10',
      orange: 'bg-orange-50 text-orange-600 border-orange-100 ring-orange-500/10',
      emerald: 'bg-emerald-50 text-emerald-600 border-emerald-100 ring-emerald-500/10',
    };
    return themes[color] || themes.blue;
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
          <Alert type="error" message="Categories Error" description={error} />
        </div>
      </StudentLayout>
    );
  }

  return (
    <StudentLayout>
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight margin-none leading-9">
          Incident Response Categories
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Explore cybersecurity simulation categories and practice the NIST Incident Response Framework.
        </p>
      </div>

      {categories.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((cat) => {
            const formattedIconName = toPascalCase(cat.icon_name);
            const Icon = LucideIcons[formattedIconName] || LucideIcons.BookOpen;
            const themeClass = getThemeClasses(cat.color_theme);

            return (
              <Link
                key={cat.id}
                to={`/categories/${cat.slug}`}
                className="group block bg-white border border-slate-200 rounded-2xl p-6 transition-all duration-300 hover:shadow-md hover:scale-[1.01] hover:border-slate-300"
              >
                <div className={`p-3 rounded-xl border w-12 h-12 flex items-center justify-center mb-4 transition ${themeClass}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="font-bold text-slate-800 text-base group-hover:text-cyan-600 transition mb-2">
                  {cat.name}
                </h3>
                <p className="text-slate-500 text-xs leading-relaxed mb-6 line-clamp-3">
                  {cat.short_summary || cat.description}
                </p>
                <div className="flex items-center justify-between border-t border-slate-100 pt-4 text-xs font-semibold text-slate-400 group-hover:text-cyan-600 transition">
                  <span>{cat.active_scenario_count || 0} active scenarios</span>
                  <div className="flex items-center text-slate-400 group-hover:text-cyan-600 transition">
                    <span>Explore</span>
                    <LucideIcons.ChevronRight className="w-4 h-4 ml-1 transition group-hover:translate-x-0.5" />
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      ) : (
        <EmptyState
          title="No categories found"
          description="Platform content seems to be empty. Try seeding the database."
          icon={BookOpen}
        />
      )}
    </StudentLayout>
  );
};

export default CategoriesPage;
