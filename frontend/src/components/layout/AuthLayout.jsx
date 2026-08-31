import React from 'react';
import { Shield } from 'lucide-react';
import { Link } from 'react-router-dom';
import Footer from './Footer';

const AuthLayout = ({ children, title, subtitle }) => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <div className="flex-1 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
          <Link to="/" className="inline-flex items-center space-x-2">
            <div className="bg-cyan-600 text-white p-2 rounded-lg">
              <Shield className="w-6 h-6" />
            </div>
            <span className="text-2xl font-bold text-slate-800 tracking-tight">
              Guardelio
            </span>
          </Link>
          {title && (
            <h2 className="mt-6 text-center text-2xl font-bold tracking-tight text-slate-800">
              {title}
            </h2>
          )}
          {subtitle && (
            <p className="mt-2 text-center text-xs text-slate-500 max-w-xs mx-auto">
              {subtitle}
            </p>
          )}
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 border border-slate-200 shadow-sm sm:rounded-xl sm:px-10">
            {children}
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default AuthLayout;
