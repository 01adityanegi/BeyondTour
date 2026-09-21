/**
 * Beyond Tour — Core Site-wide JavaScript
 * Manages Lucide icons, HTMX integration, scroll reveals, service worker,
 * network status monitoring, deferred image loading, and emergency SOS alerts.
 */

// Initialize Lucide stroke-based icons site-wide
function initLucide() {
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    try {
      window.lucide.createIcons({
        attrs: {
          'stroke-width': 1.5
        }
      });
    } catch (err) {
      console.debug('Lucide icon init notice:', err);
    }
  }
}
window.initLucide = initLucide;
document.addEventListener('DOMContentLoaded', initLucide);

// Intersection Observer for scroll animations
let revealObserver = null;
if (typeof IntersectionObserver !== 'undefined') {
  revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((el) => {
      if (el.isIntersecting) {
        el.target.classList.add('visible');
      }
    });
  }, { threshold: 0.05 });
}

function initReveals(scope) {
  if (!revealObserver) return;
  const root = scope && scope.querySelectorAll ? scope : document;
  root.querySelectorAll('.reveal:not(.visible)').forEach((el) => revealObserver.observe(el));
}
window.initReveals = initReveals;

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => initReveals(document));
} else {
  initReveals(document);
}

// HTMX Lifecycle & CSRF Configuration
if (window.htmx) {
  htmx.onLoad((target) => {
    initLucide();
    initReveals(target);
  });
  document.addEventListener('htmx:configRequest', (event) => {
    const token = document.querySelector('meta[name=csrf-token]')?.content;
    if (token) {
      event.detail.headers['X-CSRFToken'] = token;
    }
  });
}

// Service Worker Registration for Offline & 2G Resilient Himalayan Travel
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch((err) => {
      console.debug('ServiceWorker notice:', err);
    });
  });
}

// Online / Offline Status Detection for Himalayan Travel Resilience
function updateOnlineStatus() {
  const banner = document.getElementById('offline-status-banner');
  if (!banner) return;
  if (!navigator.onLine) {
    banner.classList.remove('-translate-y-full');
    banner.classList.add('translate-y-0');
    initLucide();
  } else {
    banner.classList.add('-translate-y-full');
    banner.classList.remove('translate-y-0');
  }
}
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);
document.addEventListener('DOMContentLoaded', updateOnlineStatus);

// Lazy load deferred images and iframes with data-lazy-src
document.addEventListener('DOMContentLoaded', () => {
  if (typeof IntersectionObserver !== 'undefined') {
    const lazyObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          if (entry.target.dataset.lazySrc) {
            entry.target.src = entry.target.dataset.lazySrc;
          }
          obs.unobserve(entry.target);
        }
      });
    });
    document.querySelectorAll('[data-lazy-src]').forEach((el) => lazyObserver.observe(el));
  }
});

// SOS Widget (Alpine.js component for emergency floating action button)
function sosWidget() {
  return {
    loading: false,
    confirmed: false,
    confirmMsg: 'Your location has been logged. Please call 112 immediately for rescue services.',

    async triggerSos() {
      if (!confirm('Send SOS Alert?\n\nThis will log your location as a distress signal. For immediate danger, call 112 directly.')) return;
      this.loading = true;

      let lat = null, lng = null, district = 'Unknown';
      try {
        const pos = await new Promise((res, rej) =>
          navigator.geolocation.getCurrentPosition(res, rej, { timeout: 8000 })
        );
        lat = pos.coords.latitude;
        lng = pos.coords.longitude;
      } catch (e) { /* geolocation unavailable */ }

      try {
        const resp = await fetch('/safety/sos', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name=csrf-token]')?.content || ''
          },
          body: JSON.stringify({ lat, lng, district })
        });
        const data = await resp.json();
        if (data.ok) {
          this.confirmMsg = `SOS logged at ${lat ? lat.toFixed(4) : 'unknown'}, ${lng ? lng.toFixed(4) : 'unknown'}. ` +
            `${data.contacts_notified} emergency contact(s) notified. Call 112 for immediate help.`;
        } else {
          this.confirmMsg = data.error || 'Error. Please call 112 directly.';
        }
      } catch (e) {
        this.confirmMsg = 'Could not reach server. Please call 112 immediately.';
      }
      this.loading = false;
      this.confirmed = true;
      setTimeout(() => { this.confirmed = false; }, 20000);
    }
  };
}
window.sosWidget = sosWidget;
