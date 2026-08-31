import React from 'react';

const Card = ({
  children,
  title,
  subtitle,
  action,
  className = '',
  bodyClassName = 'p-6',
  headerClassName = 'px-6 py-4 border-b border-slate-100 flex items-center justify-between',
}) => {
  return (
    <div className={`bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden ${className}`}>
      {(title || subtitle || action) && (
        <div className={headerClassName}>
          <div>
            {title && <h3 className="font-semibold text-slate-800 text-lg leading-6">{title}</h3>}
            {subtitle && <p className="text-slate-400 text-xs mt-1">{subtitle}</p>}
          </div>
          {action && <div className="flex-shrink-0">{action}</div>}
        </div>
      )}
      <div className={bodyClassName}>
        {children}
      </div>
    </div>
  );
};

export default Card;
