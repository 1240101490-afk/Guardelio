import React from 'react';
import { HelpCircle } from 'lucide-react';

const EmptyState = ({
  title = 'No records found',
  description = 'There are no items matching your criteria at this moment.',
  icon: Icon = HelpCircle,
  action,
  className = '',
}) => {
  return (
    <div className={`flex flex-col items-center justify-center p-8 text-center bg-slate-50/50 border border-dashed border-slate-200 rounded-xl ${className}`}>
      <div className="p-3 bg-slate-100 text-slate-400 rounded-full mb-4">
        <Icon className="w-8 h-8" />
      </div>
      <h3 className="text-base font-semibold text-slate-800 mb-1">{title}</h3>
      <p className="text-xs text-slate-500 max-w-sm mb-6 leading-5">{description}</p>
      {action && <div className="flex-shrink-0">{action}</div>}
    </div>
  );
};

export default EmptyState;
