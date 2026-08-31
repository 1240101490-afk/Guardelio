export const formatDate = (dateString) => {
  if (!dateString) return '—';
  try {
    const d = new Date(dateString);
    return d.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return '—';
  }
};

export const formatDateTime = (dateString) => {
  if (!dateString) return '—';
  try {
    const d = new Date(dateString);
    return d.toLocaleString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return '—';
  }
};

export const formatDuration = (minutes) => {
  if (minutes === undefined || minutes === null) return '0m';
  const mins = Math.round(minutes);
  if (mins < 60) return `${mins}m`;
  const hrs = Math.floor(mins / 60);
  const remainingMins = mins % 60;
  return remainingMins > 0 ? `${hrs}h ${remainingMins}m` : `${hrs}h`;
};

export const formatXP = (xp) => {
  if (xp === undefined || xp === null) return '0';
  return xp.toLocaleString();
};

export const capitalize = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
};

/**
 * Returns the best available display name for a user object.
 * Priority: full_name → first_name + last_name → username → role → 'User'
 */
export const getDisplayName = (user) => {
  if (!user) return 'User';
  if (user.full_name && user.full_name.trim()) return user.full_name.trim();
  const parts = [user.first_name, user.last_name].filter(Boolean).map((s) => s.trim()).filter(Boolean);
  if (parts.length > 0) return parts.join(' ');
  if (user.username && user.username.trim()) return user.username.trim();
  if (user.role) return capitalize(user.role);
  return 'User';
};

/**
 * Returns the initials (1–2 chars) for an avatar, derived from getDisplayName.
 */
export const getInitials = (user) => {
  const name = getDisplayName(user);
  const words = name.split(/\s+/).filter(Boolean);
  if (words.length === 1) return words[0].charAt(0).toUpperCase();
  return (words[0].charAt(0) + words[words.length - 1].charAt(0)).toUpperCase();
};

