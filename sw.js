// Toro Kaizen · Service Worker · KILL SWITCH (was causing blank mobile renders)
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.registration.unregister())
      .then(() => self.clients.matchAll())
      .then(clients => clients.forEach(c => c.navigate(c.url)))
  );
});
self.addEventListener('fetch', e => {
  // Always go to network, never serve cache
  e.respondWith(fetch(e.request));
});
