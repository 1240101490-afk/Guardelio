import React from 'react';

const ProgressBar = ({
  value = 0,
  max = 100,
  label,
  showValue = false,
  color = 'bg-cyan-600',
  className = '',
}) => {
  const percent = Math.min(Math.max(Math.round((value / max) * 100), 0), 100);

  return (
    <div className={className}>
      {(label || showValue) && (
        <div className="flex justify-between items-center mb-1.5">
          {label && <span className="text-xs font-semibold text-slate-700">{label}</span>}
          {showValue && <span className="text-xs font-semibold text-slate-500">{percent}%</span>}
        </div>
      )}
      <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden border border-slate-200/50">
        <div
          className={`h-full rounded-full transition-all duration-500 ease-out ${color}`}
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
