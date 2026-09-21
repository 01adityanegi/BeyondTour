/**
 * Beyond Tour — Culture Hub & Living Directory Controller
 * Manages regional festival filtering, Google Maps & Leaflet layer switcher,
 * Nanda Devi Raj Jat trail polylines, peak markers, and modal views.
 */

function initLivingCultureDirectory() {
  if (typeof Alpine === 'undefined') return;

  const festElem = document.getElementById('featured-festivals-data');
  const festivalsList = festElem ? JSON.parse(festElem.textContent || '[]') : [];

  const cultElem = document.getElementById('living-culture-data');
  const livingCultureList = cultElem ? JSON.parse(cultElem.textContent || '[]') : [];

  const yatraElem = document.getElementById('nanda-yatra-data');
  const nandaYatraData = yatraElem ? JSON.parse(yatraElem.textContent || '{}') : {};

  const mapElem = document.getElementById('map-locations-data');
  const mapLocationsList = mapElem ? JSON.parse(mapElem.textContent || '[]') : [];

  const cfgElem = document.getElementById('initial-config-data');
  const cfg = cfgElem ? JSON.parse(cfgElem.textContent || '{}') : {};

  const urlParams = new URLSearchParams(window.location.search);

  Alpine.data('livingCultureDirectory', () => ({
    festivals: festivalsList,
    livingCulture: livingCultureList,
    nandaYatra: nandaYatraData,
    mapLocations: mapLocationsList,

    // Filter states
    region: sessionStorage.getItem('beyond_tour_region') || urlParams.get('region') || cfg.selectedRegion || 'all',
    activeTab: urlParams.get('tab') || 'all',
    selectedSeason: 'all',
    selectedMonth: urlParams.get('month') || cfg.selectedMonth || 'all',
    selectedCategory: urlParams.get('category') || cfg.selectedCategory || 'all',
    happeningSoon: urlParams.get('soon') === '1' || cfg.happeningSoon || false,
    selectedMapPin: null,
    mapFilterMode: 'all',
    searchQuery: cfg.searchQuery || urlParams.get('q') || '',

    // Google Map & Leaflet state
    mapInstance: null,
    tileLayers: {},
    activeTileLayerKey: 'terrain',
    mapMarkers: {},
    trailPolyline: null,
    trailGlow: null,
    peaksGroup: null,

    // Yatra stage selection state
    activeYatraStageNumber: (nandaYatraData.live_yatra_status && nandaYatraData.live_yatra_status.active_stage_number) || 9,
    yatraRulesOpen: false,

    // Modals state
    activeModal: null,
    modalOpen: false,
    calendarModalOpen: false,
    activeArtModal: null,
    activeArtImageIndex: 0,
    artModalOpen: false,

    init() {
      this.$watch('region', (val) => {
        sessionStorage.setItem('beyond_tour_region', val);
        const url = new URL(window.location);
        if (val === 'all') url.searchParams.delete('region');
        else url.searchParams.set('region', val);
        window.history.pushState({}, '', url);
        this.onFilterChange();
      });
      this.$watch('activeTab', () => this.onFilterChange());
      this.$watch('selectedSeason', () => this.onFilterChange());
      this.$watch('selectedMonth', () => this.onFilterChange());
      this.$watch('selectedCategory', () => this.onFilterChange());
      this.$watch('happeningSoon', () => this.onFilterChange());
      this.$watch('selectedMapPin', () => this.onFilterChange());
      this.$watch('searchQuery', () => this.onFilterChange());
      this.$watch('mapFilterMode', () => {
        this.onFilterChange();
        this.updateMarkerVisibility();
      });

      this.$nextTick(() => {
        if (window.lucide) lucide.createIcons();
        this.initGoogleMap();
      });
    },

    onFilterChange() {
      this.$nextTick(() => {
        if (window.lucide) lucide.createIcons();
      });
    },

    setRegion(reg) {
      this.region = reg;
    },

    setTab(tab) {
      this.activeTab = tab;
      this.selectedMapPin = null;
    },

    initGoogleMap() {
      if (this.mapInstance || !document.getElementById('uttarakhand-google-map')) return;
      if (typeof L === 'undefined') {
        setTimeout(() => this.initGoogleMap(), 250);
        return;
      }

      // Initialize map centered over Uttarakhand
      const map = L.map('uttarakhand-google-map', {
        center: [30.08, 79.40],
        zoom: 8,
        minZoom: 7,
        maxZoom: 16,
        scrollWheelZoom: false
      });
      this.mapInstance = map;

      // Google Maps Tile Layers
      this.tileLayers = {
        terrain: L.tileLayer('https://mt{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', {
          subdomains: ['0', '1', '2', '3'],
          attribution: 'Map data &copy; Google Maps',
          maxZoom: 18
        }),
        satellite: L.tileLayer('https://mt{s}.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
          subdomains: ['0', '1', '2', '3'],
          attribution: 'Imagery &copy; Google Maps',
          maxZoom: 18
        }),
        road: L.tileLayer('https://mt{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
          subdomains: ['0', '1', '2', '3'],
          attribution: 'Map data &copy; Google Maps',
          maxZoom: 18
        })
      };

      // Add default Google Terrain Layer
      this.tileLayers[this.activeTileLayerKey].addTo(map);

      // High Himalayan Snow Peaks
      const peaks = [
        { name: 'Nanda Devi (7,816m)', lat: 30.3756, lng: 79.9708, tag: 'Highest Peak in Uttarakhand' },
        { name: 'Trishul (7,120m)', lat: 30.3167, lng: 79.7667, tag: 'Sacred Trident of Lord Shiva' },
        { name: 'Chaukhamba (7,138m)', lat: 30.7469, lng: 79.2839, tag: 'Four-Pillared Crest of Garhwal' },
        { name: 'Panchachuli (6,334m)', lat: 30.2194, lng: 80.4283, tag: 'Five Chariots of Pandavas' },
        { name: 'Bandarpunch (6,316m)', lat: 31.1044, lng: 78.5528, tag: 'Sacred Monkey Tail Crest' }
      ];

      this.peaksGroup = L.layerGroup();
      peaks.forEach((peak) => {
        const peakIcon = L.divIcon({
          className: 'custom-peak-pin',
          html: `<div class="peak-marker-label">
                   <span class="text-amber-300">▲</span>
                   <span>${peak.name}</span>
                 </div>`,
          iconSize: [150, 26],
          iconAnchor: [75, 13]
        });
        const m = L.marker([peak.lat, peak.lng], { icon: peakIcon });
        m.bindPopup(`
          <div class="p-3 text-xs">
            <div class="text-[10px] uppercase font-bold text-amber-400 tracking-wider">High Himalayan Crest</div>
            <div class="text-sm font-serif font-bold text-white mt-0.5">${peak.name}</div>
            <div class="text-white/80 text-[11px] mt-1">${peak.tag}</div>
          </div>
        `);
        this.peaksGroup.addLayer(m);
      });
      this.peaksGroup.addTo(map);

      // 280-km Sacred Nanda Devi Raj Jat Yatra Trail
      const trailWaypoints = [
        [30.2520, 79.2310], // Stage 1: Nauti Village
        [30.2300, 79.2800], // Stage 2: Idabhadani
        [30.2100, 79.3100], // Stage 3: Chandpur Garhi
        [30.1500, 79.3900], // Stage 4: Kulsari
        [30.1100, 79.4500], // Stage 5: Chepdyun
        [30.0700, 79.5200], // Stage 6: Nandkeshari (Kumaon/Garhwal union)
        [30.0900, 79.5700], // Stage 7: Faldiya Gaon
        [30.1100, 79.6000], // Stage 8: Mundoli
        [30.1347, 79.6231], // Stage 9: Wan Village
        [30.1700, 79.6500], // Stage 10: Gairoli Patal
        [30.1982, 79.6823], // Stage 11: Bedni Bugyal
        [30.2200, 79.7000], // Stage 12: Pather Nachauni
        [30.2450, 79.7150], // Stage 13: Baguabasa
        [30.2644, 79.7322], // Stage 14: Roopkund
        [30.2720, 79.7450], // Stage 15: Jurangali Pass (4,850m)
        [30.2750, 79.7520], // Stage 16: Shila Samudra
        [30.2770, 79.7570], // Stage 17: Chandaniya Ghat
        [30.2790, 79.7620]  // Stage 18: Homkund (Final Destination)
      ];

      // Outer glow line
      this.trailGlow = L.polyline(trailWaypoints, {
        color: '#f59e0b',
        weight: 7,
        opacity: 0.5,
        lineCap: 'round',
        lineJoin: 'round'
      }).addTo(map);

      // Main dashed trail
      this.trailPolyline = L.polyline(trailWaypoints, {
        color: '#b45309',
        weight: 3.5,
        opacity: 0.95,
        dashArray: '6, 8',
        lineCap: 'round',
        lineJoin: 'round'
      }).addTo(map);

      this.trailPolyline.bindPopup(`
        <div class="p-3.5 text-xs max-w-xs">
          <div class="flex items-center gap-1.5 text-amber-400 font-bold uppercase tracking-wider text-[10px]">
            <span>Sacred Himalayan Pilgrimage Trail</span>
          </div>
          <div class="text-sm font-serif font-bold text-white mt-1">Shri Nanda Devi Raj Jat Trail (280 km)</div>
          <p class="text-white/85 text-[11px] mt-1.5 leading-relaxed">
            A 22-day barefoot pilgrimage from Nauti village to Homkund Lake at the base of Mount Trishul.
          </p>
          <div class="mt-3 pt-2 border-t border-white/15 flex items-center justify-between">
            <span class="text-[10px] text-amber-300 font-semibold">18 Sacred Stages</span>
            <a href="#nanda-raj-jat-section" class="px-2.5 py-1 rounded-lg bg-amber-500 text-charcoal font-bold text-[10px] hover:bg-amber-400 transition-colors">
              Explore Stages ↓
            </a>
          </div>
        </div>
      `);

      // Create Cultural Markers
      this.createCulturalMarkers();

      // Bridge popup actions to Alpine directory
      window.selectMapLocationFromPopup = (locId) => {
        const found = this.mapLocations.find(l => l.id === locId);
        if (found) {
          this.selectMapPin(found);
          const grid = document.getElementById('festivals-grid');
          if (grid) {
            grid.scrollIntoView({ behavior: 'smooth' });
          }
        }
      };

      setTimeout(() => {
        if (this.mapInstance) this.mapInstance.invalidateSize();
      }, 350);
    },

    switchMapLayer(layerKey) {
      if (!this.mapInstance || !this.tileLayers[layerKey]) return;
      if (this.activeTileLayerKey === layerKey) return;

      this.mapInstance.removeLayer(this.tileLayers[this.activeTileLayerKey]);
      this.tileLayers[layerKey].addTo(this.mapInstance);
      this.activeTileLayerKey = layerKey;
    },

    resetMapView() {
      if (!this.mapInstance) return;
      this.clearMapPin();
      this.mapInstance.flyTo([30.08, 79.40], 8, { duration: 1.2 });
    },

    focusRajJatTrail() {
      if (!this.mapInstance || !this.trailPolyline) return;
      this.mapInstance.fitBounds(this.trailPolyline.getBounds().pad(0.25), {
        duration: 1.4,
        maxZoom: 11
      });
      setTimeout(() => {
        if (this.trailPolyline) this.trailPolyline.openPopup();
      }, 600);
    },

    createCulturalMarkers() {
      if (!this.mapInstance) return;

      Object.values(this.mapMarkers).forEach(m => this.mapInstance.removeLayer(m));
      this.mapMarkers = {};

      this.mapLocations.forEach((loc) => {
        if (!loc.lat || !loc.lng) return;

        const isGarhwal = (loc.division || loc.region || '').toLowerCase().includes('garhwal');
        const isYatra = loc.id === 'nauti' || loc.id === 'wan-village' || loc.id === 'homkund';

        const bgClass = isYatra 
          ? 'bg-amber-600 text-white border-amber-300 ring-2 ring-amber-400/50' 
          : (isGarhwal 
              ? 'bg-[#16302b] text-[#f7f3ec] border-[#6b8f71]' 
              : 'bg-[#c1622d] text-white border-amber-200');

        const iconHtml = `
          <div class="relative cursor-pointer transition-transform duration-200 hover:scale-110">
            <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold shadow-lg border ${bgClass} whitespace-nowrap">
              <span class="w-2 h-2 rounded-full ${isYatra ? 'bg-amber-200 animate-ping' : 'bg-white/80'}"></span>
              <span>${loc.name}</span>
            </div>
          </div>
        `;

        const customIcon = L.divIcon({
          className: 'culture-map-pin',
          html: iconHtml,
          iconSize: [120, 28],
          iconAnchor: [60, 14]
        });

        const marker = L.marker([loc.lat, loc.lng], { icon: customIcon });

        const festivalsListHtml = (loc.festivals && loc.festivals.length) 
          ? `<div class="text-[11px] text-white/90 mt-1.5"><span class="text-amber-300 font-semibold">Festivals:</span> ${loc.festivals.join(', ')}</div>` 
          : '';
        const craftsListHtml = (loc.crafts && loc.crafts.length) 
          ? `<div class="text-[11px] text-white/90 mt-0.5"><span class="text-emerald-300 font-semibold">Crafts:</span> ${loc.crafts.join(', ')}</div>` 
          : '';

        marker.bindPopup(`
          <div class="p-3.5 text-xs max-w-xs">
            <div class="flex items-center justify-between gap-2">
              <span class="text-[10px] uppercase font-bold tracking-wider ${isGarhwal ? 'text-emerald-300' : 'text-amber-300'}">
                ${loc.division || loc.region} Division
              </span>
              <span class="px-1.5 py-0.5 rounded bg-white/10 text-[9px] text-white capitalize">${loc.type}</span>
            </div>
            <div class="text-sm font-serif font-bold text-white mt-1">${loc.name}</div>
            <p class="text-white/80 text-[11px] mt-1 leading-relaxed">${loc.description || ''}</p>
            ${festivalsListHtml}
            ${craftsListHtml}
            <div class="mt-3 pt-2.5 border-t border-white/15 flex items-center justify-between gap-2">
              <button type="button"
                      onclick="window.selectMapLocationFromPopup('${loc.id}')"
                      class="px-3 py-1 rounded-lg bg-terracotta text-white font-bold text-[11px] hover:bg-terracotta-hover transition-colors shadow-xs">
                Filter Festivals Below ↓
              </button>
              ${isYatra ? `<a href="#nanda-raj-jat-section" class="text-[10px] text-amber-300 underline font-medium">Raj Jat Details</a>` : ''}
            </div>
          </div>
        `);

        marker.on('click', () => {
          this.selectMapPin(loc);
        });

        this.mapMarkers[loc.id] = marker;
        marker.addTo(this.mapInstance);
      });
    },

    updateMarkerVisibility() {
      if (!this.mapInstance) return;
      const filtered = this.filteredMapLocations;
      const filteredIds = new Set(filtered.map(l => l.id));

      Object.entries(this.mapMarkers).forEach(([id, marker]) => {
        if (filteredIds.has(id)) {
          if (!this.mapInstance.hasLayer(marker)) {
            marker.addTo(this.mapInstance);
          }
        } else {
          if (this.mapInstance.hasLayer(marker)) {
            this.mapInstance.removeLayer(marker);
          }
        }
      });
    },

    selectMapPin(pin) {
      if (this.selectedMapPin === pin.id) {
        this.selectedMapPin = null;
      } else {
        this.selectedMapPin = pin.id;
        if (pin.region && this.activeTab !== 'all' && this.activeTab !== pin.region.toLowerCase()) {
          this.activeTab = 'all';
        }
        if (this.mapInstance && pin.lat && pin.lng) {
          this.mapInstance.flyTo([pin.lat, pin.lng], 11, { duration: 1.2 });
          const m = this.mapMarkers[pin.id];
          if (m) {
            setTimeout(() => m.openPopup(), 450);
          }
        }
      }
    },

    clearMapPin() {
      this.selectedMapPin = null;
      if (this.mapInstance) {
        this.mapInstance.closePopup();
        this.mapInstance.flyTo([30.08, 79.40], 8, { duration: 1.2 });
      }
    },

    clearAllFilters() {
      this.activeTab = 'all';
      this.region = 'all';
      sessionStorage.setItem('beyond_tour_region', 'all');
      this.selectedSeason = 'all';
      this.selectedMonth = 'all';
      this.selectedCategory = 'all';
      this.happeningSoon = false;
      this.selectedMapPin = null;
      this.searchQuery = '';
      this.mapFilterMode = 'all';
      const url = new URL(window.location);
      url.searchParams.delete('region');
      url.searchParams.delete('month');
      url.searchParams.delete('category');
      url.searchParams.delete('soon');
      url.searchParams.delete('q');
      window.history.pushState({}, '', url);
      if (this.mapInstance) {
        this.mapInstance.closePopup();
        this.mapInstance.flyTo([30.08, 79.40], 8, { duration: 1.2 });
      }
    },

    openModal(fest) {
      this.activeModal = fest;
      this.modalOpen = true;
      document.body.style.overflow = 'hidden';
      this.$nextTick(() => {
        if (window.lucide) lucide.createIcons();
      });
    },

    closeModal() {
      this.modalOpen = false;
      this.activeModal = null;
      document.body.style.overflow = '';
    },

    openArtModal(art) {
      this.activeArtModal = art;
      this.activeArtImageIndex = 0;
      this.artModalOpen = true;
      document.body.style.overflow = 'hidden';
      this.$nextTick(() => {
        if (window.lucide) lucide.createIcons();
      });
    },

    closeArtModal() {
      this.artModalOpen = false;
      this.activeArtModal = null;
      document.body.style.overflow = '';
    },

    openCalendarModal() {
      this.calendarModalOpen = true;
      document.body.style.overflow = 'hidden';
      this.$nextTick(() => {
        if (window.lucide) lucide.createIcons();
      });
    },

    closeCalendarModal() {
      this.calendarModalOpen = false;
      document.body.style.overflow = '';
    },

    get filteredFestivals() {
      const q = this.searchQuery.toLowerCase().trim();
      const tab = this.activeTab.toLowerCase();
      const season = this.selectedSeason.toLowerCase();
      const pinId = this.selectedMapPin;
      const reg = (this.region || 'all').toLowerCase();
      const monthFilter = (this.selectedMonth || 'all').toLowerCase();
      const catFilter = (this.selectedCategory || 'all').toLowerCase();

      return this.festivals.filter((f) => {
        // Region filter (shared state)
        if (reg !== 'all') {
          const fReg = (f.region || '').toLowerCase();
          if (!fReg.includes(reg)) return false;
        }

        // Tab filter
        if (tab === 'kumaon' && f.region !== 'kumaon') return false;
        if (tab === 'garhwal' && f.region !== 'garhwal') return false;
        if (tab === 'festivals' && f.type_key !== 'festivals' && !f.category.toLowerCase().includes('festival')) return false;
        if (tab === 'fairs' && f.type_key !== 'fairs' && !f.category.toLowerCase().includes('fair')) return false;
        if (tab === 'folk_culture' && f.type_key !== 'folk_culture' && !f.category.toLowerCase().includes('folk') && !f.category.toLowerCase().includes('tradition')) return false;
        if (tab === 'seasonal' && f.type_key !== 'seasonal' && !f.category.toLowerCase().includes('seasonal') && !f.category.toLowerCase().includes('harvest')) return false;

        // Month filter (AND logic)
        if (monthFilter !== 'all') {
          const mText = ((f.month || '') + ' ' + (f.when_celebrated || '') + ' ' + (f.date_display || '')).toLowerCase();
          if (!mText.includes(monthFilter)) return false;
        }

        // Category filter (AND logic)
        if (catFilter !== 'all') {
          const cText = (f.category || '').toLowerCase();
          if (!cText.includes(catFilter)) return false;
        }

        // Happening soon toggle (date-range logic)
        if (this.happeningSoon) {
          const nowMonth = new Date().toLocaleString('en-US', { month: 'long' }).toLowerCase();
          const dText = ((f.date_display || '') + ' ' + (f.when_celebrated || '') + ' ' + (f.month || '')).toLowerCase();
          const isSoon = Boolean(f.is_happening_soon || dText.includes(nowMonth));
          if (!isSoon) return false;
        }

        // Season filter
        if (season !== 'all') {
          const fSeason = (f.season || '').toLowerCase();
          if (!fSeason.includes(season)) return false;
        }

        // Map pin filter
        if (pinId) {
          const mKey = (f.map_location_key || '').toLowerCase();
          const dist = (f.district || '').toLowerCase();
          const loc = (f.location || '').toLowerCase();
          if (mKey !== pinId && !dist.includes(pinId) && !loc.includes(pinId)) {
            return false;
          }
        }

        // Search query
        if (q) {
          const searchFields = [
            f.title,
            f.subtitle,
            f.district,
            f.location,
            f.category,
            f.short_story,
            f.cultural_significance,
            ...(f.visitor_experience || [])
          ].filter(Boolean).join(' ').toLowerCase();

          if (!searchFields.includes(q)) return false;
        }

        return true;
      });
    },

    get activeYatraStage() {
      if (!this.nandaYatra || !this.nandaYatra.stages) return null;
      return this.nandaYatra.stages.find(s => s.number === this.activeYatraStageNumber) || this.nandaYatra.stages[0];
    },

    setYatraStage(num) {
      this.activeYatraStageNumber = num;
      this.$nextTick(() => {
        if (window.lucide) lucide.createIcons();
      });
    },

    get filteredMapLocations() {
      if (this.mapFilterMode === 'festivals') {
        return this.mapLocations.filter(l => l.type === 'festival' || l.type === 'both');
      }
      if (this.mapFilterMode === 'pilgrimage') {
        return this.mapLocations.filter(l => l.id === 'nauti' || l.id === 'wan-village' || l.id === 'homkund' || (l.festivals && l.festivals.some(f => f.toLowerCase().includes('yatra') || f.toLowerCase().includes('raj jat'))));
      }
      return this.mapLocations;
    },

    get activePinObject() {
      if (!this.selectedMapPin) return null;
      return this.mapLocations.find(l => l.id === this.selectedMapPin) || null;
    }
  }));
}

if (window.Alpine) {
  initLivingCultureDirectory();
} else {
  document.addEventListener('alpine:init', initLivingCultureDirectory);
}
