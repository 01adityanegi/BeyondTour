/**
 * BeyondTour - Mountain Guide Booking Modal Controller
 * Handles interactive checklists (experiences & destinations), date validation,
 * smooth AJAX booking request submission, and confirmation views.
 */

function guideBooking() {
  return {
    bookingModalOpen: false,
    selectedGuide: { id: null, name: '', rate: 2400, district: '' },
    startDate: '',
    endDate: '',
    guests: 2,
    message: '',
    selectedExperiences: ['🏡 Village Homestay & Living', '🍲 Kumaoni & Garhwali Food'],
    selectedDestinations: [],
    isSubmitting: false,
    errorMessage: '',
    bookingSuccess: null,

    // Predefined Experience Checklist
    experiencesList: [
      { id: 'homestay', label: '🏡 Village Homestay & Living' },
      { id: 'cuisine', label: '🍲 Kumaoni & Garhwali Food' },
      { id: 'trekking', label: '🥾 High-Altitude Trekking' },
      { id: 'camping', label: '⛺ Mountain Camping & Stargazing' },
      { id: 'temple', label: '🛕 Heritage Temple Trails' },
      { id: 'nature', label: '🦅 Birdwatching & Nature Walk' },
      { id: 'photo', label: '📸 Sunrise & Photography' },
      { id: 'art', label: '🎨 Aipan Art & Folk Workshops' }
    ],

    // Predefined Destination Checklist across Uttarakhand
    destinationsList: [
      { id: 'Almora', label: '🏔️ Almora (Kasar Devi, Jageshwar, Binsar)' },
      { id: 'Nainital', label: '🌊 Nainital (Pangot, Naini Lake, Mukteshwar)' },
      { id: 'Pithoragarh', label: '❄️ Pithoragarh (Munsiyari, Johar, Panchachuli)' },
      { id: 'Uttarkashi', label: '🌲 Uttarkashi (Harsil, Dayara Bugyal, Gangotri)' },
      { id: 'Chamoli', label: '🌸 Chamoli (Valley of Flowers, Auli, Hemkund)' },
      { id: 'Rudraprayag', label: '⛰️ Rudraprayag (Chopta, Tungnath, Kedarnath)' },
      { id: 'Bageshwar', label: '🧊 Bageshwar (Pindari Glacier, Kausani)' },
      { id: 'Dehradun', label: '🌿 Dehradun & Mussoorie (Nag Tibba, Chakrata)' }
    ],

    init() {
      // Default dates: tomorrow to 3 days later
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      this.startDate = tomorrow.toISOString().split('T')[0];

      const afterTomorrow = new Date();
      afterTomorrow.setDate(afterTomorrow.getDate() + 3);
      this.endDate = afterTomorrow.toISOString().split('T')[0];
    },

    openModal(guide) {
      this.selectedGuide = guide || { id: null, name: 'Mountain Guide', rate: 2400, district: '' };
      this.bookingModalOpen = true;
      this.errorMessage = '';
      this.bookingSuccess = null;
      this.isSubmitting = false;

      // Ensure dates are populated
      if (!this.startDate) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        this.startDate = tomorrow.toISOString().split('T')[0];
      }
      if (!this.endDate) {
        const afterTomorrow = new Date();
        afterTomorrow.setDate(afterTomorrow.getDate() + 3);
        this.endDate = afterTomorrow.toISOString().split('T')[0];
      }

      // Auto-select guide's district if available and nothing is selected yet
      if (guide && guide.district && (!this.selectedDestinations || this.selectedDestinations.length === 0)) {
        this.selectedDestinations = [guide.district];
      }

      this.$nextTick(() => {
        if (window.lucide && typeof window.lucide.createIcons === 'function') {
          window.lucide.createIcons();
        }
      });
    },

    closeModal() {
      this.bookingModalOpen = false;
      this.errorMessage = '';
      this.bookingSuccess = null;
    },

    toggleExperience(label) {
      const idx = this.selectedExperiences.indexOf(label);
      if (idx > -1) {
        this.selectedExperiences.splice(idx, 1);
      } else {
        this.selectedExperiences.push(label);
      }
    },

    toggleDestination(label) {
      const idx = this.selectedDestinations.indexOf(label);
      if (idx > -1) {
        this.selectedDestinations.splice(idx, 1);
      } else {
        this.selectedDestinations.push(label);
      }
    },

    calculateDays() {
      if (!this.startDate) return 1;
      const start = new Date(this.startDate);
      const end = this.endDate ? new Date(this.endDate) : start;
      const diffTime = Math.max(0, end - start);
      return Math.max(1, Math.round(diffTime / (1000 * 60 * 60 * 24)) + 1);
    },

    calculateTotal() {
      const days = this.calculateDays();
      const rate = Number(this.selectedGuide.rate) || 2400;
      return days * rate;
    },

    async submitBooking(e) {
      if (e) e.preventDefault();

      if (!this.selectedGuide || !this.selectedGuide.id) {
        this.errorMessage = 'Please select a guide first.';
        return;
      }

      if (!this.startDate) {
        this.errorMessage = 'Please select a start date for your trek or tour.';
        return;
      }

      this.isSubmitting = true;
      this.errorMessage = '';

      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content ||
                        document.querySelector('input[name="csrf_token"]')?.value || '';

      const formData = new FormData();
      formData.append('csrf_token', csrfToken);
      formData.append('start_date', this.startDate);
      formData.append('end_date', this.endDate || this.startDate);
      formData.append('guests', this.guests || 1);
      formData.append('message', this.message || '');

      this.selectedExperiences.forEach(exp => formData.append('experiences', exp));
      this.selectedDestinations.forEach(dest => formData.append('destinations', dest));

      try {
        const res = await fetch('/guides/' + this.selectedGuide.id + '/book', {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: formData
        });

        if (res.status === 401 || res.redirected) {
          this.errorMessage = 'Please sign in to submit a booking request with your verified account.';
          this.isSubmitting = false;
          return;
        }

        const data = await res.json().catch(() => null);

        if (!res.ok) {
          this.errorMessage = data?.error || 'Unable to submit booking request. Please check details and try again.';
          this.isSubmitting = false;
          return;
        }

        this.bookingSuccess = data;
        this.isSubmitting = false;

        this.$nextTick(() => {
          if (window.lucide && typeof window.lucide.createIcons === 'function') {
            window.lucide.createIcons();
          }
        });
      } catch (err) {
        console.error('Booking submission error:', err);
        this.errorMessage = 'Network communication error. Please check your connection and try again.';
        this.isSubmitting = false;
      }
    }
  };
}

window.guideBooking = guideBooking;

function registerGuideBooking() {
  if (window.Alpine) {
    window.Alpine.data('guideBooking', guideBooking);
  } else {
    document.addEventListener('alpine:init', () => {
      window.Alpine.data('guideBooking', guideBooking);
    });
  }
}

registerGuideBooking();
