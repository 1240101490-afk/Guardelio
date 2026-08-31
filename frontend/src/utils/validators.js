export const validateEmail = (email) => {
  if (!email) return 'Email is required.';
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!re.test(email)) return 'Please enter a valid email address.';
  return null;
};

export const validatePassword = (password) => {
  if (!password) return 'Password is required.';
  if (password.length < 8) return 'Password must be at least 8 characters long.';
  
  // Complexity checks (optional, but standard for FYP security alignment)
  const hasUpper = /[A-Z]/.test(password);
  const hasLower = /[a-z]/.test(password);
  const hasDigit = /[0-9]/.test(password);
  
  if (!hasUpper || !hasLower || !hasDigit) {
    return 'Password must contain uppercase letters, lowercase letters, and numbers.';
  }
  
  return null;
};

export const validateUsername = (username) => {
  if (!username) return 'Username is required.';
  if (username.length < 3) return 'Username must be at least 3 characters long.';
  const re = /^[a-zA-Z0-9_.-]+$/;
  if (!re.test(username)) {
    return 'Username can only contain alphanumeric characters, underscores, hyphens, and dots.';
  }
  return null;
};
