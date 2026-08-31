import React from 'react';
import { AlertCircle, CheckCircle2, Info, XCircle } from 'lucide-react';

const Alert = ({
  type = 'info',
  message,
  description,
  onClose,
  className = '',
}) => {
  const styles = {
    info: {
      bg: 'bg-blue-50 border-blue-200',
      text: 'text-blue-800',
      iconText: 'text-blue-500',
      icon: Info,
    },
    success: {
      bg: 'bg-emerald-50 border-emerald-200',
      text: 'text-emerald-800',
      iconText: 'text-emerald-500',
      icon: CheckCircle2,
    },
    warning: {
      bg: 'bg-amber-50 border-amber-200',
      text: 'text-amber-800',
      iconText: 'text-amber-500',
      icon: AlertCircle,
    },
    error: {
      bg: 'bg-rose-50 border-rose-200',
      text: 'text-rose-800',
      iconText: 'text-rose-500',
      icon: XCircle,
    },
  };

  const style = styles[type] || styles.info;
  const Icon = style.icon;

  return (
    <div className={`p-4 border rounded-xl flex items-start space-x-3 ${style.bg} ${className}`} role="alert">
      <Icon className={`w-5 h-5 flex-shrink-0 mt-0.5 ${style.iconText}`} />
      <div className="flex-1">
        {message && <h4 className={`font-semibold text-sm leading-5 ${style.text}`}>{message}</h4>}
        {description && <p className={`text-xs mt-1 leading-4 opacity-90 ${style.text}`}>{description}</p>}
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="text-slate-400 hover:text-slate-600 focus:outline-none flex-shrink-0"
        >
          <span className="sr-only">Close</span>
          <XCircle className="w-5 h-5" />
        </button>
      )}
    </div>
  );
};

export default Alert;
