import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Shield, LogOut, User, Menu, X, ShieldAlert } from 'lucide-react';
import Button from '../common/Button';
import { getDisplayName, getInitials } from '../../utils/formatters';

const Navbar = ({ toggleSidebar, showMenuButton = true }) => {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-200 bg-white/95 backdrop-blur-xs px-4 md:px-6 shadow-xs">
      <div className="flex items-center space-x-3">
        {showMenuButton && (
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-lg text-slate-500 hover:bg-slate-50 focus:outline-none md:hidden"
          >
            <Menu className="w-5 h-5" />
          </button>
        )}
        <Link to="/" className="flex items-center space-x-2">
          <div className="bg-cyan-600 text-white p-2 rounded-lg">
            <Shield className="w-5 h-5" />
          </div>
          <span className="text-xl font-bold tracking-tight text-slate-800">
            Guardelio
          </span>
        </Link>
      </div>

      <div className="flex items-center space-x-4">

        <div className="relative">
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center space-x-3 p-1.5 rounded-lg hover:bg-slate-50 focus:outline-none transition"
          >
            <div className="w-8 h-8 rounded-full bg-cyan-100 text-cyan-800 flex items-center justify-center font-bold text-sm border border-cyan-200">
              {getInitials(user)}
            </div>
            <div className="hidden md:flex flex-col text-left">
              <span className="text-xs font-semibold text-slate-700 leading-tight">
                {getDisplayName(user)}
              </span>
              <span className="text-[10px] text-slate-400 font-medium capitalize leading-tight">
                {user?.role}
              </span>
            </div>
          </button>

          {dropdownOpen && (
            <>
              {/* Overlay background to close */}
              <div
                className="fixed inset-0 z-10"
                onClick={() => setDropdownOpen(false)}
              />
              <div className="absolute right-0 mt-2 w-48 rounded-xl border border-slate-100 bg-white p-1 shadow-lg ring-1 ring-black/5 z-20">
                <Link
                  to="/profile"
                  onClick={() => setDropdownOpen(false)}
                  className="flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
                >
                  <User className="w-4 h-4 text-slate-400" />
                  <span>My Profile</span>
                </Link>

                <div className="h-px bg-slate-100 my-1" />
                <button
                  onClick={() => {
                    setDropdownOpen(false);
                    handleLogout();
                  }}
                  className="w-full flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-medium text-rose-600 hover:bg-rose-50 transition"
                >
                  <LogOut className="w-4 h-4 text-rose-400" />
                  <span>Sign Out</span>
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
