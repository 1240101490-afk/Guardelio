import React from 'react';
import * as LucideIcons from 'lucide-react';

const Badge = ({
  name,
  description,
  badgeType = 'bronze',
  iconName = 'Award',
  isEarned = false,
  earnedAt,
  className = '',
}) => {
  // Resolve Lucide Icon dynamically
  // Transform kebab-case or lowercase icon name to PascalCase
  const toPascalCase = (str) => {
    if (!str) return 'Award';
    return str
      .split('-')
      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
      .join('');
  };

  const formattedIconName = toPascalCase(iconName);
  const Icon = LucideIcons[formattedIconName] || LucideIcons.Award;

  const bgClasses = {
    bronze: isEarned
      ? 'bg-amber-50 border-amber-200 text-amber-700'
      : 'bg-slate-50 border-slate-200 text-slate-400 grayscale',
    silver: isEarned
      ? 'bg-slate-100 border-slate-300 text-slate-700'
      : 'bg-slate-50 border-slate-200 text-slate-400 grayscale',
    gold: isEarned
      ? 'bg-yellow-50 border-yellow-200 text-yellow-700'
      : 'bg-slate-50 border-slate-200 text-slate-400 grayscale',
  };

  const iconBgClasses = {
    bronze: isEarned ? 'bg-amber-100' : 'bg-slate-100',
    silver: isEarned ? 'bg-slate-200' : 'bg-slate-100',
    gold: isEarned ? 'bg-yellow-100' : 'bg-slate-100',
  };

  return (
    <div
      className={`relative group flex flex-col items-center p-4 border rounded-xl transition-all duration-300 ${
        isEarned
          ? 'hover:shadow-md hover:scale-[1.02] bg-white'
          : 'bg-slate-50/55 opacity-70'
      } ${className}`}
    >
      <div className={`p-3 rounded-full mb-3 ${iconBgClasses[badgeType]} ${bgClasses[badgeType]}`}>
        <Icon className="w-6 h-6" />
      </div>
      <h4 className="font-semibold text-sm text-slate-800 text-center mb-1">{name}</h4>
      <span
        className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${
          isEarned
            ? badgeType === 'gold'
              ? 'bg-yellow-100 border-yellow-300 text-yellow-800'
              : badgeType === 'silver'
              ? 'bg-slate-200 border-slate-400 text-slate-800'
              : 'bg-amber-100 border-amber-300 text-amber-800'
            : 'bg-slate-100 border-slate-300 text-slate-500'
        }`}
      >
        {isEarned ? badgeType : 'locked'}
      </span>
      {isEarned && earnedAt && (
        <p className="text-[10px] text-slate-400 mt-2">
          Earned: {new Date(earnedAt).toLocaleDateString()}
        </p>
      )}

      {/* Tooltip on hover */}
      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-48 bg-slate-800 text-white text-xs text-center rounded-lg py-2 px-3 opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity duration-200 z-10 shadow-lg">
        {description}
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-width border-t-8 border-t-slate-800 border-x-8 border-x-transparent" />
      </div>
    </div>
  );
};

export default Badge;
