import React from 'react';

const StatCard = ({
  title,
  value,
  icon: Icon,
  description,
  colorClass = 'text-cyan-600 bg-cyan-50 border-cyan-100',
  className = '',
}) => {
  return (
    <div className={`bg-white border border-slate-200 rounded-xl p-5 flex items-start justify-between shadow-xs ${className}`}>
      <div className="flex-1">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-1">
          {title}
        </span>
        <span className="text-2xl font-bold text-slate-800 leading-8 block">
          {value}
        </span>
        {description && (
          <span className="text-[11px] text-slate-400 font-medium block mt-1">
            {description}
          </span>
        )}
      </div>
      {Icon && (
        <div className={`p-3 rounded-xl border flex-shrink-0 ml-3 ${colorClass}`}>
          <Icon className="w-6 h-6" />
        </div>
      )}
    </div>
  );
};

export default StatCard;
