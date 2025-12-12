self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("fetch", () => {
  // Minimal PWA → no caching yet
});
