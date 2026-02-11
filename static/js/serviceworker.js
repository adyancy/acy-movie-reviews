// static/js/serviceworker.js

const assets = [
  "static/css/style.css",
  "static/js/app.js",
  "static/images/logo.png",
  "static/images/favicon.png",
  "static/icons/icon-128x128.png",
  "static/icons/icon-192x192.png",
  "static/icons/icon-384x384.png",
  "static/icons/icon-512x512.png",
];

// Bump this whenever you change cached assets
const CATALOGUE_ASSETS = "movie-review-assets-v2";

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CATALOGUE_ASSETS).then((cache) => {
      return cache.addAll(assets);
    })
  );

  // Activate updated SW ASAP
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  // Remove old caches
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CATALOGUE_ASSETS)
          .map((key) => caches.delete(key))
      )
    )
  );

  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  // Always go to network for page navigations (so filters/sorting work every time)
  if (event.request.mode === "navigate") {
    event.respondWith(fetch(event.request));
    return;
  }

  // For static assets: network first, fallback to cache if offline
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
