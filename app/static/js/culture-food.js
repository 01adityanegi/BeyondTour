/**
 * Beyond Tour — Himalayan Food & Pahadi Cuisine Controller
 * Synchronizes selected culinary region with browser session storage.
 */
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const regionParam = urlParams.get('region');
  if (regionParam) {
    sessionStorage.setItem('beyond_tour_region', regionParam);
  } else {
    const saved = sessionStorage.getItem('beyond_tour_region');
    if (saved && saved !== 'all' && ['kumaon', 'garhwal'].includes(saved)) {
      window.location.href = window.location.pathname + '?region=' + encodeURIComponent(saved);
    }
  }
});
