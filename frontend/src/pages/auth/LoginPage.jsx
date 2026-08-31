import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import AuthLayout from '../../components/layout/AuthLayout';
import Button from '../../components/common/Button';
import Alert from '../../components/common/Alert';

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim() || !password) {
      setError('Please fill in all fields.');
      return;
    }
    setError(null);
    setLoading(true);
    
    const result = await login(username, password);
    setLoading(false);
    
    if (result.success) {
      // Redirect happens automatically or check role again
      const storedUser = JSON.parse(localStorage.getItem('user'));
      if (storedUser?.role === 'admin' || storedUser?.is_staff) {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } else {
      setError(result.message);
    }
  };

  return (
    <AuthLayout
      title="Guardelio Login"
      subtitle="Practice cybersecurity incident response through realistic interactive simulation scenarios."
    >
      <form className="space-y-6" onSubmit={handleSubmit}>
        {error && <Alert type="error" message={error} />}

        <div>
          <label htmlFor="username" className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
            Username or Email
          </label>
          <div className="mt-1.5">
            <input
              id="username"
              name="username"
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-400 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="Enter your username or email"
            />
          </div>
        </div>

        <div>
          <label htmlFor="password" className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
            Password
          </label>
          <div className="mt-1.5">
            <input
              id="password"
              name="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-400 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 sm:text-sm"
              placeholder="••••••••"
            />
          </div>
        </div>

        <div>
          <Button type="submit" loading={loading} className="w-full">
            Sign In
          </Button>
        </div>
      </form>

      <div className="mt-6 text-center text-xs">
        <span className="text-slate-400">Need a student account? </span>
        <Link to="/register" className="font-semibold text-cyan-600 hover:text-cyan-700">
          Register here
        </Link>
      </div>


    </AuthLayout>
  );
};

export default LoginPage;
