/**
 * Beyond Tour — Homepage Controller
 * Manages Hero AI prompt form submission and loading indicator state.
 */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('hero-ai-form');
  const btn = document.getElementById('hero-plan-btn');
  const text = document.getElementById('hero-plan-text');
  const icon = document.getElementById('hero-plan-icon');

  if (form && btn) {
    form.addEventListener('submit', () => {
      btn.disabled = true;
      btn.classList.add('opacity-90', 'cursor-wait');
      if (text) text.textContent = 'Crafting Itinerary...';
      if (icon) {
        icon.outerHTML = '<svg class="w-5 h-5 animate-spin text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>';
      }
    });
  }
});
