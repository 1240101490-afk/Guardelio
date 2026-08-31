import React from 'react';

const Loader = ({ fullScreen = false, size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-6 h-6 border-2',
    md: 'w-10 h-10 border-4',
    lg: 'w-16 h-16 border-4',
  };

  const spinner = (
    <div
      className={`animate-spin rounded-full border-slate-200 border-t-cyan-600 ${sizeClasses[size]} ${className}`}
      role="status"
    >
      <span className="sr-only">Loading...</span>
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex flex-col items-center justify-center bg-slate-50/70 z-50">
        {spinner}
        <p className="mt-4 text-slate-500 font-medium animate-pulse">Loading Guardelio...</p>
      </div>
    );
  }

  return <div className="flex items-center justify-center p-4">{spinner}</div>;
};

export default Loader;
