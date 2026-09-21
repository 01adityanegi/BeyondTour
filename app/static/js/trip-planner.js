/**
 * Beyond Tour — AI Trip Planner Controller
 * Manages planner form interactions, HTMX swap transitions, Lucide/Alpine re-initialization,
 * and smooth scroll into newly generated itineraries.
 */

document.addEventListener('DOMContentLoaded', () => {
  if (!window.location.hash) {
    window.scrollTo({ top: 0, behavior: 'instant' });
  }
});

document.body.addEventListener('htmx:afterSwap', () => {
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    try {
      window.lucide.createIcons();
    } catch (e) {
      console.debug('Lucide icon refresh notice:', e);
    }
  }

  const resultElem = document.getElementById('planner-result');
  if (resultElem) {
    resultElem.querySelectorAll('.reveal').forEach((el) => el.classList.add('visible'));
  }

  if (window.Alpine && resultElem) {
    try {
      Alpine.initTree(resultElem);
    } catch (e) {
      console.debug('Alpine tree init notice:', e);
    }
  }

  if (resultElem && resultElem.children.length > 0) {
    resultElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});
