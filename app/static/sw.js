// BeyondTour Himalayan Offline & 2G Resilient Service Worker v3
const CACHE_NAME = 'beyondtour-v3';
const OFFLINE_URL = '/offline';

const PRECACHE_ASSETS = [
  '/',
  '/destinations/',
  '/hotels/',
  '/guides/',
  '/community/',
  '/culture/',
  '/culture/art',
  '/culture/food',
  '/culture/festivals',
  '/plan/',
  '/safety/emergency-info',
  '/offline',
  '/destinations/?district=almora',
  '/destinations/?district=nainital',
  '/destinations/?district=pithoragarh',
  '/destinations/?district=uttarkashi',
  '/static/manifest.json',
  '/static/css/main.css',
  '/static/css/culture.css',
  '/static/js/tailwind-config.js',
  '/static/js/main.js',
  '/static/js/culture-directory.js',
  '/static/js/culture-food.js',
  '/static/js/culture-art.js',
  '/static/js/home.js',
  '/static/js/trip-planner.js',
  '/static/js/smart-route.js',
  '/static/js/vendor-guide-editor.js',
  '/static/js/vendor-hotel-editor.js',
  '/static/js/festival-uploader.js',
  '/static/js/tourism-dashboard.js',
  '/static/js/community-upload.js',
  '/static/js/guide-booking.js',
  '/static/images/coverpic/gharwal.png',
  '/static/images/coverpic/kumaon.png',
  '/static/images/Nanital/lakenanital.png',
  '/static/images/Almora/almora.png',
  '/static/images/destinations/uttarkashi.jpg',
  '/static/images/destinations/pithoragarh_fort.jpg',
  '/static/images/destinations/munsiyari.jpg',
  '/static/images/destinations/kausani.jpg',
  '/static/images/destinations/binsar.jpg',
  '/static/images/destinations/auli.jpg',
  '/static/images/destinations/chopta_tungnath.jpg',
  '/static/images/destinations/haridwar.jpg',
  '/static/images/destinations/rishikesh.jpg',
  '/static/images/destinations/valley_of_flowers.jpg',
  '/static/images/destinations/tehri_lake.jpg',
  '/static/images/destinations/abbott_mount.jpg',
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/lucide@latest',
  'https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js',
  'https://unpkg.com/htmx.org@1.9.10',
  'https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,600&family=Manrope:wght@300;400;500;600;700;800&display=swap'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      // Fetch each asset individually so one failure does not abort caching the rest
      await Promise.allSettled(
        PRECACHE_ASSETS.map(async (asset) => {
          try {
            await cache.add(asset);
          } catch (err) {
            console.debug('ServiceWorker cache add notice for:', asset, err);
          }
        })
      );
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Ignore non-GET requests
  if (req.method !== 'GET') {
    return;
  }

  // HTML navigation requests -> Network first, fallback to cache, then offline fallback page
  if (req.mode === 'navigate' || req.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(req, responseClone);
            });
          }
          return networkResponse;
        })
        .catch(async () => {
          // 1. Check exact match
          const cachedResponse = await caches.match(req);
          if (cachedResponse) {
            return cachedResponse;
          }

          // 2. Check path without search or trailing slash variant
          const pathname = url.pathname;
          const matchPath = await caches.match(pathname);
          if (matchPath) return matchPath;

          const altPath = pathname.endsWith('/') ? pathname.slice(0, -1) : (pathname + '/');
          const matchAlt = await caches.match(altPath);
          if (matchAlt) return matchAlt;

          // 3. Fallback to offline guidance page
          const offlinePage = await caches.match(OFFLINE_URL);
          if (offlinePage) {
            return offlinePage;
          }

          return new Response('You are currently offline in the Himalayas. BeyondTour cached content will reload once connected.', {
            headers: { 'Content-Type': 'text/plain' }
          });
        })
    );
    return;
  }

  // Static assets (images, styles, scripts, fonts) -> Cache first, fallback to network
  event.respondWith(
    caches.match(req).then((cachedResponse) => {
      if (cachedResponse) {
        // Revalidate in background when connected
        fetch(req).then((networkResponse) => {
          if (networkResponse && (networkResponse.status === 200 || networkResponse.type === 'opaque')) {
            caches.open(CACHE_NAME).then((cache) => cache.put(req, networkResponse));
          }
        }).catch(() => {});
        return cachedResponse;
      }

      return fetch(req).then((networkResponse) => {
        if (networkResponse && (networkResponse.status === 200 || networkResponse.type === 'opaque')) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(req, responseClone);
          });
        }
        return networkResponse;
      }).catch(async () => {
        // If image request fails offline, serve fallback hero image if available
        if (req.destination === 'image') {
          const fallbackImg = await caches.match('/static/images/coverpic/kumaon.png');
          if (fallbackImg) return fallbackImg;
        }
      });
    })
  );
});
