/**
 * Beyond Tour — AI Smart Route & Google Maps Controller
 * Implements Google Maps JavaScript API with DirectionsService, DirectionsRenderer,
 * Places Autocomplete, and zero-breakage Leaflet Mountain Tile Fallback.
 */

class MountainRouteManager {
  constructor() {
    const serverData = JSON.parse(document.getElementById('server-route-config')?.textContent || '{}');
    window.SERVER_DATA = serverData;

    this.apiKey = localStorage.getItem('beyond_tour_gmaps_key') || serverData.apiKey || '';
    this.stops = [...(serverData.initialStops || [])];
    this.knownPlaces = serverData.knownPlaces || {};
    this.travelMode = 'DRIVING';
    this.optimizeWaypoints = true;
    this.activeLayer = 'terrain'; // terrain | satellite | roadmap

    // Engine instances
    this.engine = 'pending'; // 'google' | 'leaflet'
    this.gmap = null;
    this.directionsService = null;
    this.directionsRenderer = null;
    this.googleMarkers = [];
    this.autocompleteInstances = [];

    // Leaflet fallback instances
    this.leafletMap = null;
    this.leafletLayers = {};
    this.leafletMarkers = [];
    this.leafletPolyline = null;

    this.initElements();
    this.bindEvents();
    this.loadMapEngine();
  }

  initElements() {
    this.mapContainer = document.getElementById('google-mountain-map');
    this.loadingOverlay = document.getElementById('map-loading-overlay');
    this.stopsListEl = document.getElementById('stops-list');
    this.btnAddStop = document.getElementById('btn-add-stop');
    this.btnCalcRoute = document.getElementById('btn-calculate-route');
    this.btnReverse = document.getElementById('btn-reverse-route');
    this.btnRecenter = document.getElementById('btn-recenter-map');
    this.chkOptimize = document.getElementById('chk-optimize-waypoints');
  }

  bindEvents() {
    // Calculate route click
    this.btnCalcRoute?.addEventListener('click', () => this.calculateAndDrawRoute());

    // Add Stop
    this.btnAddStop?.addEventListener('click', () => this.addStop());

    // Reverse Route
    this.btnReverse?.addEventListener('click', () => this.reverseRoute());

    // Recenter
    this.btnRecenter?.addEventListener('click', () => this.recenterMap());

    // Waypoint Optimization checkbox
    this.chkOptimize?.addEventListener('change', (e) => {
      this.optimizeWaypoints = e.target.checked;
      this.calculateAndDrawRoute();
    });

    // Travel mode switcher
    document.querySelectorAll('.travel-mode-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.travel-mode-btn').forEach((b) => {
          b.classList.remove('bg-white', 'text-charcoal', 'shadow-2xs');
          b.classList.add('text-charcoal/60');
        });
        const target = e.currentTarget;
        target.classList.add('bg-white', 'text-charcoal', 'shadow-2xs');
        target.classList.remove('text-charcoal/60');
        this.travelMode = target.dataset.mode;
        const typeBadge = document.getElementById('route-type-badge');
        if (typeBadge) {
          typeBadge.textContent = this.travelMode === 'DRIVING' ? 'Driving Route' : 'Walking / Trekking Trail';
        }
        this.calculateAndDrawRoute();
      });
    });

    // Map layer buttons
    document.querySelectorAll('.map-layer-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const layer = e.currentTarget.dataset.layer;
        this.setMapLayer(layer);
      });
    });

    // Preset buttons
    document.querySelectorAll('.preset-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const preset = e.currentTarget.dataset.preset;
        this.loadPreset(preset);
      });
    });

    // Day filter pills
    document.querySelectorAll('.day-filter-pill').forEach((pill) => {
      pill.addEventListener('click', (e) => {
        document.querySelectorAll('.day-filter-pill').forEach((p) => {
          p.classList.remove('bg-pine', 'text-white', 'border-pine', 'shadow-sm');
          p.classList.add('bg-stone/20', 'text-charcoal', 'border-stone/30');
        });
        const target = e.currentTarget;
        target.classList.add('bg-pine', 'text-white', 'border-pine', 'shadow-sm');
        target.classList.remove('bg-stone/20', 'text-charcoal', 'border-stone/30');

        const stopsRaw = target.dataset.stops;
        if (stopsRaw) {
          const stopsArr = stopsRaw.split('||').filter((s) => s.trim().length > 0);
          if (stopsArr.length >= 2) {
            this.setStops(stopsArr);
          } else if (stopsArr.length === 1) {
            // Add gateway hub if only one stop
            this.setStops(['Haldwani', stopsArr[0]]);
          }
        } else {
          // All highlights
          this.loadPreset('kumaon');
        }
      });
    });

    // Fullscreen toggle
    document.getElementById('btn-toggle-fullscreen')?.addEventListener('click', () => {
      const card = this.mapContainer?.closest('.bg-white');
      if (!document.fullscreenElement) {
        card?.requestFullscreen?.().catch(() => {});
      } else {
        document.exitFullscreen?.().catch(() => {});
      }
    });

    // Event delegation for dynamically added stops
    this.stopsListEl?.addEventListener('click', (e) => {
      const btnRemove = e.target.closest('.btn-remove-stop');
      if (btnRemove) {
        const item = btnRemove.closest('.stop-item');
        const idx = parseInt(item.dataset.index, 10);
        this.removeStop(idx);
        return;
      }

      const btnUp = e.target.closest('.btn-move-up');
      if (btnUp) {
        const item = btnUp.closest('.stop-item');
        const idx = parseInt(item.dataset.index, 10);
        this.moveStop(idx, -1);
        return;
      }

      const btnDown = e.target.closest('.btn-move-down');
      if (btnDown) {
        const item = btnDown.closest('.stop-item');
        const idx = parseInt(item.dataset.index, 10);
        this.moveStop(idx, 1);
        return;
      }
    });

    this.stopsListEl?.addEventListener('change', (e) => {
      if (e.target.classList.contains('stop-input')) {
        this.syncStopsFromInputs();
      }
    });
  }

  loadMapEngine() {
    this.loadingOverlay?.classList.remove('opacity-0', 'pointer-events-none');

    // Check for Google Maps auth failures
    window.gm_authFailure = () => {
      console.warn('Google Maps API authentication failed or key restricted. Switching to Leaflet mountain terrain fallback.');
      this.initLeafletFallback();
    };

    // Attempt Google Maps JS API script injection
    const script = document.createElement('script');
    const keyParam = this.apiKey ? `key=${encodeURIComponent(this.apiKey)}&` : '';
    script.src = `https://maps.googleapis.com/maps/api/js?${keyParam}libraries=places,geometry&callback=__initBeyondTourMap`;
    script.async = true;
    script.defer = true;

    window.__initBeyondTourMap = () => {
      this.initGoogleMaps();
    };

    script.onerror = () => {
      console.warn('Google Maps script failed to load. Initializing Leaflet terrain fallback.');
      this.initLeafletFallback();
    };

    // Safety timeout: if Google Maps doesn't initialize within 4 seconds, fallback immediately
    setTimeout(() => {
      if (this.engine === 'pending') {
        console.info('Google Maps timeout reached, mounting high-res Leaflet mountain engine.');
        this.initLeafletFallback();
      }
    }, 4000);

    document.head.appendChild(script);
  }

  /**
   * Official Google Maps JS API Engine
   */
  initGoogleMaps() {
    if (this.engine === 'google') return;
    try {
      this.engine = 'google';
      const statusEl = document.getElementById('engine-status-text');
      if (statusEl) statusEl.textContent = 'Google Maps Active';

      // Custom muted mountain styling matching Beyond Tour design palette
      const mountainStyle = [
        { featureType: 'administrative', elementType: 'labels.text.fill', stylers: [{ color: '#2B2A28' }] },
        { featureType: 'landscape', elementType: 'all', stylers: [{ color: '#F7F3EC' }] },
        { featureType: 'landscape.natural.terrain', elementType: 'all', stylers: [{ visibility: 'on' }] },
        { featureType: 'poi', elementType: 'all', stylers: [{ visibility: 'off' }] },
        { featureType: 'poi.park', elementType: 'geometry', stylers: [{ color: '#E3EBE4' }, { visibility: 'on' }] },
        { featureType: 'road', elementType: 'all', stylers: [{ saturation: -20 }, { lightness: 20 }] },
        { featureType: 'road.highway', elementType: 'geometry.fill', stylers: [{ color: '#E8C5A8' }] },
        { featureType: 'road.highway', elementType: 'geometry.stroke', stylers: [{ color: '#D99B73' }] },
        { featureType: 'water', elementType: 'all', stylers: [{ color: '#C8D9D2' }, { visibility: 'on' }] }
      ];

      // Centered over Uttarakhand (Kumaon-Garhwal center)
      this.gmap = new google.maps.Map(this.mapContainer, {
        center: { lat: 29.85, lng: 79.75 },
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        styles: mountainStyle,
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: false,
        zoomControl: true,
        zoomControlOptions: { position: google.maps.ControlPosition.RIGHT_BOTTOM }
      });

      this.directionsService = new google.maps.DirectionsService();
      this.directionsRenderer = new google.maps.DirectionsRenderer({
        map: this.gmap,
        suppressMarkers: true,
        polylineOptions: {
          strokeColor: '#C1622D',
          strokeOpacity: 0.95,
          strokeWeight: 6
        }
      });

      this.bindGoogleAutocomplete();
      this.loadingOverlay?.classList.add('opacity-0', 'pointer-events-none');
      this.calculateAndDrawRoute();
    } catch (err) {
      console.error('Error in initGoogleMaps:', err);
      this.initLeafletFallback();
    }
  }

  bindGoogleAutocomplete() {
    if (typeof google === 'undefined' || !google.maps || !google.maps.places) return;

    const uttarakhandBounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(28.7, 77.5),
      new google.maps.LatLng(31.5, 81.1)
    );

    document.querySelectorAll('.stop-input').forEach((input) => {
      if (input._ac_bound) return;
      try {
        const ac = new google.maps.places.Autocomplete(input, {
          bounds: uttarakhandBounds,
          componentRestrictions: { country: 'in' },
          fields: ['name', 'geometry', 'formatted_address']
        });
        ac.addListener('place_changed', () => {
          const place = ac.getPlace();
          if (place && place.name) {
            input.value = place.name;
            this.syncStopsFromInputs();
            this.calculateAndDrawRoute();
          }
        });
        input._ac_bound = true;
      } catch (e) {
        // Autocomplete error fallback
      }
    });
  }

  /**
   * High-Fidelity Leaflet Fallback with Google Maps Satellite/Terrain/Road Tiles
   */
  initLeafletFallback() {
    if (this.engine === 'leaflet') return;
    this.engine = 'leaflet';
    const statusEl = document.getElementById('engine-status-text');
    if (statusEl) statusEl.textContent = 'Google Tiles (Leaflet Engine)';

    if (this.mapContainer) {
      this.mapContainer.innerHTML = '';
    }

    this.leafletMap = L.map('google-mountain-map', {
      center: [29.85, 79.75],
      zoom: 8,
      minZoom: 6,
      maxZoom: 18,
      scrollWheelZoom: true,
      zoomControl: false
    });

    L.control.zoom({ position: 'bottomright' }).addTo(this.leafletMap);

    this.leafletLayers = {
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
      roadmap: L.tileLayer('https://mt{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        subdomains: ['0', '1', '2', '3'],
        attribution: 'Map data &copy; Google Maps',
        maxZoom: 18
      })
    };

    this.leafletLayers.terrain.addTo(this.leafletMap);
    this.loadingOverlay?.classList.add('opacity-0', 'pointer-events-none');
    this.calculateAndDrawRoute();
  }

  setMapLayer(layerKey) {
    this.activeLayer = layerKey;
    document.querySelectorAll('.map-layer-btn').forEach((btn) => {
      if (btn.dataset.layer === layerKey) {
        btn.classList.add('bg-pine', 'text-ivory', 'shadow-2xs');
        btn.classList.remove('text-charcoal/70');
      } else {
        btn.classList.remove('bg-pine', 'text-ivory', 'shadow-2xs');
        btn.classList.add('text-charcoal/70');
      }
    });

    if (this.engine === 'google' && this.gmap) {
      const typeMap = {
        terrain: google.maps.MapTypeId.TERRAIN,
        satellite: google.maps.MapTypeId.HYBRID,
        roadmap: google.maps.MapTypeId.ROADMAP
      };
      this.gmap.setMapTypeId(typeMap[layerKey] || google.maps.MapTypeId.TERRAIN);
    } else if (this.engine === 'leaflet' && this.leafletMap) {
      Object.values(this.leafletLayers).forEach((l) => this.leafletMap.removeLayer(l));
      if (this.leafletLayers[layerKey]) {
        this.leafletLayers[layerKey].addTo(this.leafletMap);
      }
    }
  }

  calculateAndDrawRoute() {
    this.syncStopsFromInputs();
    if (this.stops.length < 2) return;

    if (this.btnCalcRoute) this.btnCalcRoute.disabled = true;
    const calcText = document.getElementById('calc-btn-text');
    if (calcText) calcText.textContent = 'Optimizing Route...';

    if (this.engine === 'google' && this.directionsService) {
      this.calculateGoogleRoute();
    } else {
      this.calculateFallbackRoute();
    }
  }

  calculateGoogleRoute() {
    const origin = this.stops[0];
    const destination = this.stops[this.stops.length - 1];
    const waypoints = this.stops.slice(1, -1).map((stop) => ({
      location: stop + ', Uttarakhand, India',
      stopover: true
    }));

    const request = {
      origin: origin + ', Uttarakhand, India',
      destination: destination + ', Uttarakhand, India',
      waypoints: waypoints,
      optimizeWaypoints: this.optimizeWaypoints,
      travelMode: this.travelMode === 'WALKING' ? google.maps.TravelMode.WALKING : google.maps.TravelMode.DRIVING
    };

    this.directionsService.route(request, (result, status) => {
      if (this.btnCalcRoute) this.btnCalcRoute.disabled = false;
      const calcText = document.getElementById('calc-btn-text');
      if (calcText) calcText.textContent = 'Optimize & Draw Route';

      if (status === google.maps.DirectionsStatus.OK) {
        if (this.googlePolyline) {
          this.googlePolyline.setMap(null);
          this.googlePolyline = null;
        }
        this.directionsRenderer.setDirections(result);
        this.renderGoogleCustomMarkers(result);
        this.updateRouteSummary(result);
      } else {
        console.warn('Google DirectionsService status:', status, '- fallback active.');
        this.calculateFallbackRoute();
      }
    });
  }

  renderGoogleCustomMarkers(directionsResult) {
    this.googleMarkers.forEach((m) => m.setMap(null));
    this.googleMarkers = [];

    const route = directionsResult.routes[0];
    const legs = route.legs;
    const colors = ['#16302B', '#C1622D', '#6B8F71', '#2B2A28', '#A65123', '#4A4844'];

    legs.forEach((leg, i) => {
      const labelChar = String.fromCharCode(65 + i);
      const marker = this.createGoogleMarker(leg.start_location, labelChar, colors[i % colors.length], this.stops[i]);
      this.googleMarkers.push(marker);

      if (i === legs.length - 1) {
        const lastChar = String.fromCharCode(65 + i + 1);
        const endMarker = this.createGoogleMarker(leg.end_location, lastChar, '#2B2A28', this.stops[this.stops.length - 1]);
        this.googleMarkers.push(endMarker);
      }
    });
  }

  createGoogleMarker(position, label, bgColor, name) {
    const svgPin = `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
      <svg xmlns="http://www.w3.org/2000/svg" width="36" height="46" viewBox="0 0 36 46">
        <path d="M18 0C8.06 0 0 8.06 0 18c0 13.5 18 28 18 28s18-14.5 18-28C36 8.06 27.94 0 18 0z" fill="${bgColor}" stroke="#FFFFFF" stroke-width="2"/>
        <circle cx="18" cy="18" r="12" fill="#FFFFFF"/>
        <text x="18" y="22" font-size="12" font-family="monospace" font-weight="bold" fill="${bgColor}" text-anchor="middle">${label}</text>
      </svg>
    `)}`;

    const marker = new google.maps.Marker({
      position: position,
      map: this.gmap,
      icon: {
        url: svgPin,
        scaledSize: new google.maps.Size(36, 46),
        anchor: new google.maps.Point(18, 46)
      },
      title: name,
      animation: google.maps.Animation.DROP
    });

    const info = new google.maps.InfoWindow({
      content: `
        <div style="padding: 8px 10px; font-family: 'Manrope', sans-serif; max-width: 220px;">
          <div style="font-size: 10px; font-weight: 700; color: #C1622D; text-transform: uppercase; letter-spacing: 0.5px;">Stop ${label}</div>
          <div style="font-size: 14px; font-weight: 700; color: #2B2A28; margin: 2px 0 4px;">${name}</div>
          <div style="font-size: 11px; color: #666; line-height: 1.4;">Scenic Himalayan waypoint along the route.</div>
        </div>
      `
    });

    marker.addListener('click', () => {
      info.open(this.gmap, marker);
    });

    return marker;
  }

  calculateFallbackRoute() {
    if (this.btnCalcRoute) this.btnCalcRoute.disabled = false;
    const calcText = document.getElementById('calc-btn-text');
    if (calcText) calcText.textContent = 'Optimize & Draw Route';

    const points = [];
    const resolvedStops = [];

    this.stops.forEach((stop, i) => {
      const norm = stop.toLowerCase().trim();
      let match = this.knownPlaces[norm];

      if (!match) {
        for (const [key, val] of Object.entries(this.knownPlaces)) {
          if (norm.includes(key) || key.includes(norm)) {
            match = val;
            break;
          }
        }
      }

      if (match) {
        points.push([match.lat, match.lng]);
        resolvedStops.push({ name: match.name, lat: match.lat, lng: match.lng, alt: match.altitude_m });
      } else {
        const fallbackLat = 29.4 + (i * 0.15);
        const fallbackLng = 79.5 + (i * 0.15);
        points.push([fallbackLat, fallbackLng]);
        resolvedStops.push({ name: stop, lat: fallbackLat, lng: fallbackLng, alt: 1800 });
      }
    });

    if (this.gmap && typeof google !== 'undefined' && google.maps) {
      if (this.googleMarkers) {
        this.googleMarkers.forEach((m) => m.setMap(null));
      }
      this.googleMarkers = [];
      if (this.googlePolyline) {
        this.googlePolyline.setMap(null);
      }

      const googleLatLngs = [];
      const bounds = new google.maps.LatLngBounds();
      const colors = ['#16302B', '#C1622D', '#6B8F71', '#2B2A28', '#A65123', '#4A4844'];

      resolvedStops.forEach((st, i) => {
        const char = String.fromCharCode(65 + i);
        const color = colors[i % colors.length];
        const latLng = new google.maps.LatLng(st.lat, st.lng);
        googleLatLngs.push(latLng);
        bounds.extend(latLng);

        const marker = this.createGoogleMarker(latLng, char, color, st.name);
        this.googleMarkers.push(marker);
      });

      this.googlePolyline = new google.maps.Polyline({
        path: googleLatLngs,
        geodesic: true,
        strokeColor: '#C1622D',
        strokeOpacity: 0.9,
        strokeWeight: 6,
        map: this.gmap
      });

      this.gmap.fitBounds(bounds);
    }

    if (this.leafletMap && points.length >= 2) {
      this.leafletMarkers.forEach((m) => this.leafletMap.removeLayer(m));
      this.leafletMarkers = [];
      if (this.leafletPolyline) this.leafletMap.removeLayer(this.leafletPolyline);

      this.leafletPolyline = L.polyline(points, {
        color: '#C1622D',
        weight: 5,
        opacity: 0.9,
        lineCap: 'round',
        lineJoin: 'round'
      }).addTo(this.leafletMap);

      const colors = ['#16302B', '#C1622D', '#6B8F71', '#2B2A28', '#A65123', '#4A4844'];

      resolvedStops.forEach((st, i) => {
        const char = String.fromCharCode(65 + i);
        const color = colors[i % colors.length];

        const customIcon = L.divIcon({
          className: 'custom-route-pin',
          html: `
            <div style="width:32px;height:42px;position:relative;">
              <svg width="32" height="42" viewBox="0 0 36 46">
                <path d="M18 0C8.06 0 0 8.06 0 18c0 13.5 18 28 18 28s18-14.5 18-28C36 8.06 27.94 0 18 0z" fill="${color}" stroke="#FFFFFF" stroke-width="2"/>
                <circle cx="18" cy="18" r="11" fill="#FFFFFF"/>
                <text x="18" y="22" font-size="12" font-family="monospace" font-weight="bold" fill="${color}" text-anchor="middle">${char}</text>
              </svg>
            </div>
          `,
          iconSize: [32, 42],
          iconAnchor: [16, 42]
        });

        const m = L.marker([st.lat, st.lng], { icon: customIcon }).addTo(this.leafletMap);
        m.bindPopup(`
          <div style="font-family:'Manrope', sans-serif; font-size:12px; padding:4px;">
            <div style="font-weight:700; color:#C1622D; font-size:10px; text-transform:uppercase;">Waypoint ${char}</div>
            <div style="font-weight:700; font-size:14px; color:#2B2A28; margin:2px 0;">${st.name}</div>
            <div style="font-size:11px; color:#666;">Altitude: ~${st.alt || 1900} m</div>
          </div>
        `);
        this.leafletMarkers.push(m);
      });

      this.leafletMap.fitBounds(this.leafletPolyline.getBounds(), { padding: [60, 60] });
    }

    let totalKm = 0;
    const legDetails = [];

    for (let i = 0; i < resolvedStops.length - 1; i++) {
      const p1 = resolvedStops[i];
      const p2 = resolvedStops[i + 1];
      const directKm = this.getHaversineDistance(p1.lat, p1.lng, p2.lat, p2.lng);
      const roadKm = Math.round(directKm * 1.55);
      totalKm += roadKm;
      const durationMins = Math.round((roadKm / 30) * 60);
      legDetails.push({
        from: p1.name,
        to: p2.name,
        distanceKm: roadKm,
        durationMins: durationMins
      });
    }

    this.renderMetrics(totalKm, legDetails);
  }

  getHaversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  updateRouteSummary(directionsResult) {
    const route = directionsResult.routes[0];
    let totalMeters = 0;
    let totalSeconds = 0;
    const legDetails = [];

    route.legs.forEach((leg, i) => {
      totalMeters += leg.distance.value;
      totalSeconds += leg.duration.value;
      legDetails.push({
        from: this.stops[i],
        to: this.stops[i + 1],
        distanceKm: Math.round(leg.distance.value / 1000),
        durationMins: Math.round(leg.duration.value / 60)
      });
    });

    const totalKm = Math.round(totalMeters / 1000);
    this.renderMetrics(totalKm, legDetails);
  }

  renderMetrics(totalKm, legDetails) {
    const chainEl = document.getElementById('route-chain-text');
    if (chainEl) chainEl.textContent = this.stops.join(' → ');

    const distEl = document.getElementById('metric-distance');
    if (distEl) distEl.textContent = `${totalKm} km`;

    let totalMins = 0;
    legDetails.forEach((l) => totalMins += l.durationMins);
    const hrs = Math.floor(totalMins / 60);
    const mins = totalMins % 60;

    const durEl = document.getElementById('metric-duration');
    if (durEl) durEl.textContent = `${hrs}h ${mins}m`;

    let recommendedDays = '1–2 Days';
    if (totalKm > 250) recommendedDays = '3–4 Days';
    else if (totalKm > 120) recommendedDays = '2–3 Days';
    else if (totalKm < 50) recommendedDays = 'Day Trip';

    const daysEl = document.getElementById('metric-days');
    if (daysEl) daysEl.textContent = recommendedDays;

    const legsContainer = document.getElementById('legs-container');
    if (legsContainer) {
      legsContainer.innerHTML = '';
      legDetails.forEach((leg, idx) => {
        const legCard = document.createElement('div');
        legCard.className = 'p-3 rounded-xl bg-white border border-stone/30 flex items-center justify-between text-xs hover:border-terracotta/40 transition-colors';
        legCard.innerHTML = `
          <div class="flex items-center gap-2.5 min-w-0">
            <span class="w-5 h-5 rounded-md bg-stone/20 text-charcoal/70 font-mono font-bold text-[10px] flex items-center justify-center flex-shrink-0">${idx + 1}</span>
            <span class="font-semibold text-charcoal truncate">${leg.from} → ${leg.to}</span>
          </div>
          <div class="flex items-center gap-3 flex-shrink-0 text-charcoal/70">
            <span>${leg.distanceKm} km</span>
            <span class="font-medium text-terracotta">${Math.floor(leg.durationMins / 60)}h ${leg.durationMins % 60}m</span>
          </div>
        `;
        legsContainer.appendChild(legCard);
      });
    }

    const advisoryEl = document.getElementById('route-advisory-text');
    if (advisoryEl) {
      if (totalKm > 200) {
        advisoryEl.textContent = 'High elevation route with steep ghat passes. Ensure daylight travel and carry warm layers.';
      } else if (this.travelMode === 'WALKING') {
        advisoryEl.textContent = 'Trek route on Himalayan trails. Wear sturdy hiking shoes and carry hydration packs.';
      } else {
        advisoryEl.textContent = 'Curated mountain road segment. Moderate speed advised along winding river valleys.';
      }
    }

    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
  }

  recenterMap() {
    if (this.engine === 'google' && this.gmap && this.directionsRenderer) {
      const dir = this.directionsRenderer.getDirections();
      if (dir && dir.routes && dir.routes[0]) {
        this.gmap.fitBounds(dir.routes[0].bounds);
      }
    } else if (this.engine === 'leaflet' && this.leafletMap && this.leafletPolyline) {
      this.leafletMap.fitBounds(this.leafletPolyline.getBounds(), { padding: [60, 60] });
    }
  }

  reverseRoute() {
    this.stops.reverse();
    this.renderStopsUI();
    this.calculateAndDrawRoute();
  }

  loadPreset(presetKey) {
    const presets = {
      'kumaon': ['Haldwani', 'Nainital', 'Almora', 'Munsiyari'],
      'nainital-day2': ["Tiffin Top (Dorothy's Seat)", 'Snow View Point', 'Eco Cave Gardens'],
      'garhwal': ['Rishikesh', 'Devprayag', 'Rudraprayag', 'Joshimath'],
      'lakes': ['Kathgodam', 'Bhimtal', 'Sattal', 'Nainital']
    };

    if (presets[presetKey]) {
      this.setStops(presets[presetKey]);
    }
  }

  setStops(newStops) {
    this.stops = [...newStops];
    this.renderStopsUI();
    this.calculateAndDrawRoute();
  }

  addStop() {
    if (this.stops.length >= 8) {
      alert('Maximum of 8 stops supported for optimal mountain routing.');
      return;
    }
    this.stops.push('');
    this.renderStopsUI();
    const inputs = document.querySelectorAll('.stop-input');
    if (inputs.length) inputs[inputs.length - 1].focus();
  }

  removeStop(index) {
    if (this.stops.length <= 2) {
      alert('A minimum of 2 stops (Origin and Destination) is required.');
      return;
    }
    this.stops.splice(index, 1);
    this.renderStopsUI();
    this.calculateAndDrawRoute();
  }

  moveStop(index, direction) {
    const targetIdx = index + direction;
    if (targetIdx < 0 || targetIdx >= this.stops.length) return;
    const temp = this.stops[index];
    this.stops[index] = this.stops[targetIdx];
    this.stops[targetIdx] = temp;
    this.renderStopsUI();
    this.calculateAndDrawRoute();
  }

  syncStopsFromInputs() {
    const inputs = document.querySelectorAll('.stop-input');
    const newStops = [];
    inputs.forEach((inp) => {
      const val = inp.value.trim();
      if (val) newStops.push(val);
    });
    if (newStops.length >= 2) {
      this.stops = newStops;
    }
  }

  renderStopsUI() {
    if (!this.stopsListEl) return;
    this.stopsListEl.innerHTML = '';
    const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'];
    const colors = ['bg-pine text-ivory', 'bg-terracotta text-white', 'bg-sage text-white', 'bg-charcoal text-ivory'];

    this.stops.forEach((stop, i) => {
      const isFirst = (i === 0);
      const isLast = (i === this.stops.length - 1);
      const badgeColor = isFirst ? 'bg-pine text-ivory' : (isLast ? 'bg-charcoal text-ivory' : colors[i % colors.length]);
      const label = letters[i] || (i + 1);

      const div = document.createElement('div');
      div.className = 'stop-item flex items-center gap-2.5 p-2 bg-ivory/70 rounded-2xl border border-stone/40 transition-all hover:border-stone/80 group';
      div.dataset.index = i;

      div.innerHTML = `
        <div class="stop-badge w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold flex-shrink-0 shadow-2xs font-mono ${badgeColor}">
          ${label}
        </div>
        <div class="relative flex-1">
          <input type="text"
                 class="stop-input w-full bg-white border border-stone/40 rounded-xl px-3.5 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-terracotta/40 focus:border-terracotta text-charcoal font-medium shadow-2xs transition-all placeholder:text-charcoal/40"
                 placeholder="Enter destination, landmark or trek..."
                 value="${stop}"
                 autocomplete="off">
        </div>
        <div class="flex items-center gap-1">
          <button type="button" class="btn-move-up p-1.5 text-charcoal/40 hover:text-charcoal hover:bg-stone/30 rounded-lg transition-colors" title="Move Up" ${isFirst ? 'disabled style="opacity:0.3;"' : ''}>
            <i data-lucide="chevron-up" class="w-4 h-4"></i>
          </button>
          <button type="button" class="btn-move-down p-1.5 text-charcoal/40 hover:text-charcoal hover:bg-stone/30 rounded-lg transition-colors" title="Move Down" ${isLast ? 'disabled style="opacity:0.3;"' : ''}>
            <i data-lucide="chevron-down" class="w-4 h-4"></i>
          </button>
          <button type="button" class="btn-remove-stop p-1.5 text-red-500/60 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors" title="Remove Stop" ${this.stops.length <= 2 ? 'disabled style="opacity:0.3;"' : ''}>
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>
      `;

      this.stopsListEl.appendChild(div);
    });

    const counterEl = document.getElementById('stops-counter');
    if (counterEl) counterEl.textContent = `${this.stops.length} Stops`;
    this.bindGoogleAutocomplete();
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
  }
}

// Export class & instantiate on DOM load
window.MountainRouteManager = MountainRouteManager;

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }
  window.mountainRouteManager = new MountainRouteManager();
});
