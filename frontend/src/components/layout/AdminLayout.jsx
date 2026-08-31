import React, { useState } from 'react';
import Navbar from './Navbar';
import AdminSidebar from './AdminSidebar';
import Footer from './Footer';

const AdminLayout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex flex-col min-h-screen bg-slate-50">
      <Navbar toggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
      <div className="flex flex-1 overflow-hidden">
        <AdminSidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <main className="flex-1 overflow-y-auto px-4 py-8 md:px-8 max-w-7xl mx-auto w-full">
          {children}
        </main>
      </div>
      <Footer />
    </div>
  );
};

export default AdminLayout;
