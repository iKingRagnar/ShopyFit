// Toro Kaizen · Service Worker · v1
const CACHE='tk-v1';
const ASSETS=['/','/index.html','/about.html','/manifesto.html','/marks.html','/faq.html','/returns.html','/terms.html','/privacy.html','/atletas.html','/sostenibilidad.html','/blog.html','/404.html','/favicon.svg','/manifest.webmanifest'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET')return;
  if(u.origin!==location.origin)return; // skip third-party (pollinations, fonts, jsdelivr)
  e.respondWith(
    caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{
      if(res.ok)caches.open(CACHE).then(c=>c.put(e.request,res.clone()));
      return res;
    }).catch(()=>caches.match('/index.html')))
  );
});
