import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, BookOpen, Award, ChevronRight } from 'lucide-react';
import Button from '../components/common/Button';
import Footer from '../components/layout/Footer';

const LandingPage = () => {
  return (
    <div className="bg-slate-50 min-h-screen flex flex-col">
      {/* Navbar */}
      <header className="bg-white border-b border-slate-200 h-16 flex items-center justify-between px-6 sticky top-0 z-50">
        <Link to="/" className="flex items-center space-x-2">
          <div className="bg-cyan-600 text-white p-2 rounded-lg">
            <Shield className="w-5 h-5" />
          </div>
          <span className="text-xl font-bold tracking-tight text-slate-800">Guardelio</span>
        </Link>
        <div className="flex items-center space-x-4">
          <Link to="/login" className="text-xs font-semibold text-slate-600 hover:text-slate-800 transition">
            Sign In
          </Link>
          <Link to="/register">
            <Button size="sm">Get Started</Button>
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-6 max-w-5xl mx-auto text-center flex-1 flex flex-col items-center justify-center">
        <div className="inline-flex items-center space-x-2 px-3 py-1 bg-cyan-50 border border-cyan-200 rounded-full text-cyan-800 text-[10px] font-bold uppercase tracking-wider mb-6">
          <span>University Final Year Project</span>
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-800 max-w-3xl leading-tight">
          Interactive Security Incident Training & Branching Simulation
        </h1>
        <p className="mt-4 text-sm md:text-base text-slate-500 max-w-2xl leading-relaxed">
          Master the NIST SP 800-61 Incident Response Lifecycle. Guardelio simulates real-world security incidents, allowing you to practice critical decision-making under fire.
        </p>
        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center space-y-3 sm:space-y-0 sm:space-x-4">
          <Link to="/register">
            <Button size="lg" className="w-full sm:w-auto">
              Create Student Account <ChevronRight className="w-4 h-4 ml-1" />
            </Button>
          </Link>
          <Link to="/login">
            <Button size="lg" variant="secondary" className="w-full sm:w-auto">
              Guardelio Login
            </Button>
          </Link>
        </div>

        {/* Feature Grid */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-4xl text-left">
          <div className="bg-white border border-slate-200 rounded-2xl p-6">
            <div className="bg-blue-50 text-blue-600 p-3 rounded-xl inline-block mb-4 border border-blue-100">
              <BookOpen className="w-6 h-6" />
            </div>
            <h3 className="font-semibold text-slate-800 text-lg mb-2">30 IR Scenarios</h3>
            <p className="text-xs text-slate-500 leading-5">
              Practice malware outbreaks, phishing campaigns, DDoS mitigation, and advanced persistent threat hunting across 6 domains.
            </p>
          </div>
          <div className="bg-white border border-slate-200 rounded-2xl p-6">
            <div className="bg-emerald-50 text-emerald-600 p-3 rounded-xl inline-block mb-4 border border-emerald-100">
              <Shield className="w-6 h-6" />
            </div>
            <h3 className="font-semibold text-slate-800 text-lg mb-2">NIST Alignment</h3>
            <p className="text-xs text-slate-500 leading-5">
              Work step-by-step through Preparation, Containment, Detection, Eradication, Recovery, and Post-Incident reviews.
            </p>
          </div>
          <div className="bg-white border border-slate-200 rounded-2xl p-6">
            <div className="bg-amber-50 text-amber-600 p-3 rounded-xl inline-block mb-4 border border-amber-100">
              <Award className="w-6 h-6" />
            </div>
            <h3 className="font-semibold text-slate-800 text-lg mb-2">Gamified Badges</h3>
            <p className="text-xs text-slate-500 leading-5">
              Earn XP completion bonuses, climb accuracy ranks, and unlock 18 structured badges for category completions.
            </p>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default LandingPage;
