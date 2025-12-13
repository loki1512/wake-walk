self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

// IMPORTANT: fetch handler must respond
self.addEventListener("fetch", (event) => {
  event.respondWith(fetch(event.request));
});
