import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import authService from '../../api/authService';
import AuthLayout from '../../components/layout/AuthLayout';
import Button from '../../components/common/Button';
import Alert from '../../components/common/Alert';

// Maps backend field names (including Django-style) to friendly UI labels
const FIELD_LABELS = {
  first_name: 'First Name',
  last_name: 'Last Name',
  username: 'Username',
  email: 'Email Address',
  password: 'Password',
  password2: 'Confirm Password',
  confirm_password: 'Confirm Password',
  non_field_errors: '',
};

const getFriendlyError = (fieldKey, message) => {
  const label = FIELD_LABELS[fieldKey];
  if (label === undefined) {
    // Unknown field — still show it but without the raw key prefix
    return message;
  }
  if (label === '') {
    // non_field_errors — show the message as-is
    return message;
  }
  // Replace generic "This field is required." with label-prefixed version
  const cleaned = message
    .replace(/^This field may not be blank\.?$/i, `${label} is required.`)
    .replace(/^This field is required\.?$/i, `${label} is required.`)
    .replace(/^This field must be unique\.?$/i, `${label} is already in use.`);
  // If the message already starts with the label, return as-is to avoid duplication
  if (cleaned.toLowerCase().startsWith(label.toLowerCase())) return cleaned;
  return `${label}: ${cleaned}`;
};

const RegisterPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    password: '',
    confirm_password: '',
  });

  // Track which fields the user has interacted with (for blur-based validation)
  const [touched, setTouched] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear the top-level error when the user edits a field after a failed submit
    if (error) setError(null);
  };

  const handleBlur = (e) => {
    setTouched((prev) => ({ ...prev, [e.target.name]: true }));
  };

  // Pure helper — checks a single field given an explicit touched map and submitted flag.
  // This allows the submit handler to call it eagerly before React state batches settle.
  const computeFieldError = (name, data, touchedMap, isSubmitted) => {
    if (!touchedMap[name] && !isSubmitted) return null;
    const value = data[name];
    if (!value || !String(value).trim()) {
      return `${FIELD_LABELS[name] || name} is required.`;
    }
    if (name === 'confirm_password' && data.password && value !== data.password) {
      return 'Passwords do not match.';
    }
    return null;
  };

  // Returns an inline error message for a field based on current React state.
  const getFieldError = (name) => computeFieldError(name, formData, touched, submitted);

  const inputClass = (name) => {
    const hasError = getFieldError(name);
    return `mt-1.5 block w-full rounded-lg border px-3 py-2 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-1 sm:text-sm ${
      hasError
        ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500'
        : 'border-slate-300 focus:border-cyan-500 focus:ring-cyan-500'
    }`;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    // Build the "all touched" map eagerly — don't wait for React to batch setTouched
    const allTouched = {
      first_name: true,
      last_name: true,
      username: true,
      email: true,
      password: true,
      confirm_password: true,
    };

    // Flush touched + submitted into React state so the UI re-renders with errors
    setSubmitted(true);
    setTouched(allTouched);

    // Client-side guard — use formData directly (not state) to avoid stale closure
    const hasEmptyField = Object.keys(allTouched).some(
      (name) => computeFieldError(name, formData, allTouched, true) !== null
    );
    if (hasEmptyField) {
      setError('Please fill in all required fields.');
      return;
    }

    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match. Please re-enter your password.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        first_name: formData.first_name,
        last_name: formData.last_name,
        username: formData.username,
        email: formData.email,
        password: formData.password,
        password2: formData.confirm_password,
      };

      const res = await authService.register(payload);
      if (res?.success) {
        setSuccess('Registration successful! Redirecting you to login page...');
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      } else {
        setError(res?.message || 'Registration failed.');
      }
    } catch (err) {
      const fieldErrors = err.response?.data?.errors;
      if (fieldErrors && typeof fieldErrors === 'object') {
        // Translate the first backend field error into a friendly message
        const firstKey = Object.keys(fieldErrors)[0];
        const rawMsg = fieldErrors[firstKey];
        const message = Array.isArray(rawMsg) ? rawMsg[0] : rawMsg;
        setError(getFriendlyError(firstKey, message));
      } else {
        setError(err.response?.data?.message || 'An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Create Student Account"
      subtitle="Register below to join Guardelio simulations and start tracking your incident response progress."
    >
      <form className="space-y-4" onSubmit={handleSubmit} noValidate>
        {error && <Alert type="error" message={error} />}
        {success && <Alert type="success" message={success} />}

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="first_name" className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
              First Name
            </label>
            <input
              id="first_name"
              name="first_name"
              type="text"
              value={formData.first_name}
              onChange={handleChange}
              onBlur={handleBlur}
              className={inputClass('first_name')}
              placeholder="First name"
            />
            {getFieldError('first_name') && (
              <p className="mt-1 text-[11px] text-rose-600 font-medium">{getFieldError('first_name')}</p>
            )}
          </div>
          <div>
            <label htmlFor="last_name" className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
              Last Name
            </label>
            <input
              id="last_name"
              name="last_name"
              type="text"
              value={formData.last_name}
              onChange={handleChange}
              onBlur={handleBlur}
              className={inputClass('last_name')}
              placeholder="Last name"
            />
            {getFieldError('last_name') && (
              <p className="mt-1 text-[11px] text-rose-600 font-medium">{getFieldError('last_name')}</p>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="username" className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
            Username
          </label>
          <input
            id="username"
            name="username"
            type="text"
            value={formData.username}
            onChange={handleChange}
            onBlur={handleBlur}
            className={inputClass('username')}
            placeholder="Username"
          />
          {getFieldError('username') && (
            <p className="mt-1 text-[11px] text-rose-600 font-medium">{getFieldError('username')}</p>
          )}
        </div>

        <div>
          <label htmlFor="email" className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
            Email Address
          </label>
          <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            onBlur={handleBlur}
            className={inputClass('email')}
            placeholder="Email address"
          />
          {getFieldError('email') && (
            <p className="mt-1 text-[11px] text-rose-600 font-medium">{getFieldError('email')}</p>
          )}
        </div>

        <div>
          <label htmlFor="password" className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            onBlur={handleBlur}
            className={inputClass('password')}
            placeholder="••••••••"
          />
          {getFieldError('password') && (
            <p className="mt-1 text-[11px] text-rose-600 font-medium">{getFieldError('password')}</p>
          )}
        </div>

        <div>
          <label htmlFor="confirm_password" className="block text-xs font-semibold text-slate-700 uppercase tracking-wide">
            Confirm Password
          </label>
          <input
            id="confirm_password"
            name="confirm_password"
            type="password"
            value={formData.confirm_password}
            onChange={handleChange}
            onBlur={handleBlur}
            className={inputClass('confirm_password')}
            placeholder="••••••••"
          />
          {getFieldError('confirm_password') && (
            <p className="mt-1 text-[11px] text-rose-600 font-medium">{getFieldError('confirm_password')}</p>
          )}
        </div>

        <div className="pt-2">
          <Button type="submit" loading={loading} className="w-full">
            Register Account
          </Button>
        </div>
      </form>

      <div className="mt-6 text-center text-xs">
        <span className="text-slate-400">Already registered? </span>
        <Link to="/login" className="font-semibold text-cyan-600 hover:text-cyan-700">
          Sign in instead
        </Link>
      </div>
    </AuthLayout>
  );
};

export default RegisterPage;

