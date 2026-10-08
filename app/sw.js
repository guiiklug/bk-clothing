/* BK Gestão: deixa o aplicativo abrir sem internet depois da primeira visita.
   Código (html, css, js) busca a versão nova primeiro e só usa a guardada se estiver sem rede;
   fotos e fontes usam a cópia guardada, que não muda. */
const NOME = 'bk-gestao-1';
const CASCA = ['./', 'index.html', 'css/app.css', 'js/catalogo.js', 'js/base.js', 'js/app.js', 'manifest.webmanifest', 'img/icone-192.png'];

self.addEventListener('install', e => { e.waitUntil(caches.open(NOME).then(c => c.addAll(CASCA)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== NOME).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const guardada = /\.(webp|png|jpg|woff2)$/.test(new URL(req.url).pathname) || /fonts\.(googleapis|gstatic)\.com/.test(req.url);
  const guardar = res => { if (res && (res.ok || res.type === 'opaque')) { const copia = res.clone(); caches.open(NOME).then(c => c.put(req, copia)); } return res; };
  if (guardada) e.respondWith(caches.match(req).then(r => r || fetch(req).then(guardar)));
  else e.respondWith(fetch(req).then(guardar).catch(() => caches.match(req).then(r => r || caches.match('index.html'))));
});
