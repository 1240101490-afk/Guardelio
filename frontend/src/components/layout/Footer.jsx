import React from 'react';

const Footer = ({ className = '' }) => {
  return (
    <footer className={`bg-white border-t border-slate-200 py-5 text-center ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-xs font-semibold text-slate-500">Guardelio: Learn &amp; Practice Web Security.</p>
        <p className="mt-1 text-[11px] text-slate-400">&copy; 2026. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
