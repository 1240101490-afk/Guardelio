import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Award, User, BookOpen, ChevronRight } from 'lucide-react';

const Sidebar = ({ isOpen, onClose }) => {
  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Categories', path: '/categories', icon: BookOpen },
    { name: 'Progress & Badges', path: '/progress', icon: Award },
    { name: 'Profile', path: '/profile', icon: User },
  ];

  const sidebarContent = (
    <div className="flex flex-col h-full border-r border-slate-800 text-slate-400" style={{ background: 'linear-gradient(180deg, #0d1b2a 0%, #1a2744 100%)' }}>
      <div className="flex-1 py-6 px-4 space-y-1.5 overflow-y-auto">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center justify-between px-4 py-3 rounded-lg text-xs font-semibold tracking-wide uppercase transition ${
                  isActive
                    ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-900/40'
                    : 'hover:bg-white/5 hover:text-slate-200'
                }`
              }
            >
              <div className="flex items-center space-x-3">
                <Icon className="w-4 h-4" />
                <span>{item.name}</span>
              </div>
              <ChevronRight className="w-3.5 h-3.5 opacity-60" />
            </NavLink>
          );
        })}
      </div>
    </div>
  );

  return (
    <>
      {/* Mobile Drawer Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs md:hidden"
          onClick={onClose}
        />
      )}

      {/* Drawer Container */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-40 w-64 transform transition-transform duration-300 md:translate-x-0 md:static md:h-[calc(100vh-4rem)] md:z-auto ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {sidebarContent}
      </aside>
    </>
  );
};

export default Sidebar;
