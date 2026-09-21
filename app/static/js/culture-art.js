/**
 * Beyond Tour — Traditional Arts & Handicrafts Controller
 * Manages craft gallery modals, high-res previews, and regional filtering.
 */

function initArtHub() {
  if (typeof Alpine === 'undefined') return;

  const artsElem = document.getElementById('traditional-arts-data');
  const artsList = artsElem ? JSON.parse(artsElem.textContent || '[]') : [];

  Alpine.data('artHub', () => ({
    arts: artsList,
    selectedArt: null,
    modalImg: '',

    init() {
      const urlParams = new URLSearchParams(window.location.search);
      const regionParam = urlParams.get('region');
      if (regionParam) {
        sessionStorage.setItem('beyond_tour_region', regionParam);
      } else {
        const savedRegion = sessionStorage.getItem('beyond_tour_region');
        if (savedRegion && savedRegion !== 'all' && ['kumaon', 'garhwal'].includes(savedRegion)) {
          window.location.href = window.location.pathname + '?region=' + encodeURIComponent(savedRegion);
          return;
        }
      }

      const craftParam = urlParams.get('craft');
      if (craftParam) {
        this.openModal(craftParam);
      }
    },

    setRegion(reg) {
      sessionStorage.setItem('beyond_tour_region', reg);
    },

    openModal(artId, initialImg = null) {
      const found = this.arts.find((a) => a.id === artId);
      if (found) {
        this.selectedArt = found;
        this.modalImg = initialImg || found.cover_image || (found.gallery && found.gallery[0]);
        document.body.style.overflow = 'hidden';

        setTimeout(() => {
          if (window.lucide) {
            lucide.createIcons();
          }
        }, 50);
      }
    },

    closeModal() {
      this.selectedArt = null;
      document.body.style.overflow = '';
    }
  }));
}

if (window.Alpine) {
  initArtHub();
} else {
  document.addEventListener('alpine:init', initArtHub);
}
