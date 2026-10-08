/* BK Clothing — comportamento compartilhado: cabeçalho, sacola, produto, WhatsApp */
(function () {
  const BK = {
    fone: '5547988204407',
    vip: 'https://chat.whatsapp.com/FCX9FvsBWBeACbsrjiNW62',
    insta: 'https://instagram.com/bkclothiing',
    mapa: 'https://www.google.com/maps/search/?api=1&query=Rua+Santa+Catarina+2348+Floresta+Joinville+SC',
  };
  const P = window.BK_PRODUTOS || [];
  const byId = Object.fromEntries(P.map(p => [p.id, p]));
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const brl = v => v == null ? 'Sob consulta' : v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  const STD = new Set(window.BK_STD || []);
  /* peça padronizada: a foto limpa vem primeiro e as originais seguem depois */
  const nf = p => p.i + (STD.has(p.id) ? 1 : 0);
  const img = (p, k = 0, t = true) => STD.has(p.id)
    ? (k === 0 ? `img/std/${p.id}${t ? '_t' : ''}.webp` : `img/p/${p.id}_${k - 1}${t ? '_t' : ''}.webp`)
    : `img/p/${p.id}_${k}${t ? '_t' : ''}.webp`;
  const wa = msg => `https://wa.me/${BK.fone}?text=${encodeURIComponent(msg)}`;
  const titulo = p => p.n + (p.cor && p.cor !== 'Várias cores' ? ' · ' + p.cor : '');
  const page = document.body.dataset.page || '';

  const WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.200 8.200 0 0 1-4.200-1.150l-.300-.180-3 .800.800-2.900-.200-.300A8.200 8.200 0 1 1 12 20.200Zm4.500-6.100c-.250-.120-1.450-.720-1.680-.800-.220-.080-.390-.120-.550.120-.160.250-.630.800-.780.960-.140.170-.290.190-.530.060a6.700 6.700 0 0 1-3.330-2.910c-.250-.430.250-.400.720-1.330.080-.170.040-.300-.020-.430-.060-.120-.550-1.330-.760-1.820-.200-.480-.400-.410-.550-.420h-.470a.900.900 0 0 0-.650.300 2.750 2.750 0 0 0-.860 2.040c0 1.200.880 2.370 1 2.530.120.170 1.720 2.630 4.170 3.690 1.550.670 2.160.720 2.930.610.470-.070 1.450-.590 1.650-1.170.200-.570.200-1.060.140-1.160-.060-.110-.220-.170-.470-.290Z"/></svg>';

  /* ---------- estrutura compartilhada ---------- */
  const nav = [['index.html#lookbook', 'Lookbook'], ['catalogo.html', 'Catálogo'], ['index.html#como-comprar', 'Como comprar'], ['index.html#loja', 'A loja']];
  const header = `
  <header class="hd${page === 'home' ? '' : ' solid'}">
    <a href="index.html" class="logo" aria-label="BK Clothing, página inicial"><b>BK</b><i>CLOTHING</i></a>
    <nav aria-label="Principal">${nav.map(([h, t]) => `<a href="${h}"${page === 'catalogo' && h === 'catalogo.html' ? ' class="on"' : ''}>${t}</a>`).join('')}</nav>
    <div class="hd-r">
      <button class="ico tema" data-tema aria-label="Alternar tema claro e escuro"><svg class="lua" viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/></svg><svg class="sol" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/></svg></button>
      <button class="ico" data-bag aria-label="Abrir sacola"><svg viewBox="0 0 24 24"><path d="M5 8h14l-1 13H6L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg><span class="q"></span></button>
      <button class="ico burger" data-menu aria-label="Abrir menu"><svg viewBox="0 0 24 24"><path d="M3 8h18M3 16h18"/></svg></button>
    </div>
  </header>
  <div class="mnav" id="mnav">
    <button class="ico x" data-menu aria-label="Fechar menu"><svg viewBox="0 0 24 24"><path d="M5 5l14 14M19 5 5 19"/></svg></button>
    <a href="index.html">Início</a>${nav.map(([h, t]) => `<a href="${h}">${t}</a>`).join('')}
    <small>Rua Santa Catarina, 2348 · Floresta · Joinville/SC</small>
  </div>`;

  const footer = `
  <footer class="ft">
    <p class="ft-big" aria-hidden="true">Vista <em>BK.</em></p>
    <div class="ft-g">
      <div><a href="index.html" class="logo"><b>BK</b><i>CLOTHING</i></a><p style="margin-top:1.125rem;color:var(--mute);max-width:30ch">Moda masculina em Joinville. Vista estilo, vista BK Clothing.</p></div>
      <div><h5>Loja</h5><ul><li>Rua Santa Catarina, 2348</li><li>Floresta · Joinville/SC</li><li><a href="${BK.mapa}" target="_blank" rel="noopener">Como chegar</a></li></ul></div>
      <div><h5>Comprar</h5><ul><li><a href="catalogo.html">Catálogo</a></li><li><a href="index.html#lookbook">Lookbook</a></li><li><a href="index.html#duvidas">Trocas e envios</a></li><li><a href="links.html">Todos os links</a></li></ul></div>
      <div><h5>Contato</h5><ul><li><a href="${wa('Olá! Vim pelo site da BK Clothing.')}" target="_blank" rel="noopener">WhatsApp (47) 98820-4407</a></li><li><a href="${BK.insta}" target="_blank" rel="noopener">Instagram @bkclothiing</a></li><li><a href="${BK.vip}" target="_blank" rel="noopener">Grupo VIP</a></li></ul></div>
    </div>
    <div class="ft-b"><span>© ${new Date().getFullYear()} BK Clothing. Enviamos para todo o Brasil.</span><span>Pix · Cartão · A combinar pelo WhatsApp</span></div>
  </footer>
  <a class="wa" href="${wa('Olá! Vim pelo site da BK Clothing.')}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">${WA_SVG}</a>
  <div class="veil" id="veil"></div>
  <aside class="bag" id="bag" aria-label="Sacola">
    <div class="bag-h"><h3>Sacola</h3><button class="ico" data-close aria-label="Fechar sacola"><svg viewBox="0 0 24 24"><path d="M5 5l14 14M19 5 5 19"/></svg></button></div>
    <div class="bag-l" id="bagList"></div>
    <div class="bag-f" id="bagFoot"></div>
  </aside>
  <section class="pm" id="pm" aria-label="Produto"><button class="pm-x" data-close aria-label="Fechar produto">✕</button><div id="pmBody"></div></section>
  <div class="lb" id="lb"><button class="x" aria-label="Fechar">✕</button><button class="pv" aria-label="Anterior">‹</button><img alt=""><button class="nx" aria-label="Próxima">›</button><p></p></div>
  <div class="toast" id="toast" role="status"></div>`;

  if (page !== 'links') {
    document.body.insertAdjacentHTML('afterbegin', header);
    document.body.insertAdjacentHTML('beforeend', footer);
  }

  /* ---------- card de produto ---------- */
  BK.card = (p, tag) => `
    <a class="card" href="#p=${p.id}" data-p="${p.id}">
      <div class="ph">${tag ? `<span class="tag">${tag}</span>` : ''}
        <img src="${img(p)}" alt="${titulo(p)}" loading="lazy" width="560" height="672">
        ${nf(p) > 1 ? `<img src="${img(p, 1)}" alt="" loading="lazy">` : ''}
        <span class="add" aria-hidden="true">+</span>
      </div>
      <div class="mt"><div>${p.b ? `<div class="br">${p.b}</div>` : ''}<h4>${p.n}</h4><div class="co">${p.cor}</div></div><div class="pr">${brl(p.p)}</div></div>
    </a>`;
  BK.P = P; BK.brl = brl; BK.wa = wa;
  window.BK = BK;
  if (page === 'links') return;

  /* ---------- sacola ---------- */
  let bag = [];
  try { bag = JSON.parse(localStorage.getItem('bk_sacola') || '[]').filter(i => byId[i.id]); } catch (e) {}
  const save = () => { try { localStorage.setItem('bk_sacola', JSON.stringify(bag)); } catch (e) {} };
  const toast = t => { const el = $('#toast'); el.textContent = t; el.classList.add('on'); clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove('on'), 2400); };

  function pedido(itens) {
    let total = 0, consulta = false;
    const linhas = itens.map(i => {
      const p = byId[i.id];
      if (p.p == null) consulta = true; else total += p.p * i.q;
      return `• ${i.q}x ${p.n} (${p.cor})${i.s && i.s !== 'Único' ? ' tam. ' + i.s : ''} — ${p.p == null ? 'valor sob consulta' : brl(p.p * i.q)} [ref ${p.id}]`;
    });
    return `Olá! Quero fechar este pedido pelo site da BK Clothing:\n\n${linhas.join('\n')}\n\nTotal: ${brl(total)}${consulta ? ' + itens sob consulta' : ''}\n\nPode confirmar os tamanhos e o frete?`;
  }

  function drawBag() {
    const n = bag.reduce((a, i) => a + i.q, 0);
    $$('.q').forEach(e => e.textContent = n || '');
    const list = $('#bagList'), foot = $('#bagFoot');
    if (!bag.length) {
      list.innerHTML = `<div class="bag-e"><p>Sua sacola está vazia.</p></div>`;
      foot.innerHTML = `<a class="btn solid full" href="catalogo.html">Ver o catálogo</a>`;
      return;
    }
    list.innerHTML = bag.map((i, k) => {
      const p = byId[i.id];
      return `<div class="bag-i"><img src="${img(p)}" alt="">
        <div><h4>${p.n}</h4><small>${p.cor}${i.s ? ' · ' + i.s : ''}</small>
          <div class="qty"><button data-q="${k}:-1" aria-label="Diminuir">−</button><span>${i.q}</span><button data-q="${k}:1" aria-label="Aumentar">+</button></div></div>
        <div style="display:grid"><span class="pr">${p.p == null ? 'Sob consulta' : brl(p.p * i.q)}</span><button class="rm" data-q="${k}:0">Remover</button></div></div>`;
    }).join('');
    const total = bag.reduce((a, i) => a + (byId[i.id].p || 0) * i.q, 0);
    foot.innerHTML = `<div class="tot"><span>Total</span><b>${brl(total)}</b></div>
      <small>Frete e tamanhos são confirmados na conversa. Pagamento por Pix, cartão ou a combinar.</small>
      <a class="btn solid full" href="${wa(pedido(bag))}" target="_blank" rel="noopener">${WA_SVG} Fechar pedido no WhatsApp</a>`;
  }
  function addBag(id, s) {
    const it = bag.find(i => i.id === id && i.s === s);
    if (it) it.q++; else bag.push({ id, s, q: 1 });
    save(); drawBag();
  }

  /* ---------- painéis ---------- */
  const veil = $('#veil'), bagEl = $('#bag'), pm = $('#pm');
  const openBag = () => { bagEl.classList.add('open'); veil.classList.add('open'); document.body.classList.add('lock'); };
  const closeAll = () => {
    bagEl.classList.remove('open'); veil.classList.remove('open'); $('#mnav').classList.remove('open');
    if (pm.classList.contains('open')) { pm.classList.remove('open'); if (location.hash.startsWith('#p=')) history.replaceState(null, '', location.pathname + location.search); }
    document.body.classList.remove('lock');
  };

  /* ---------- produto ---------- */
  let curSize = '';
  function openProduct(id) {
    const p = byId[id]; if (!p) return;
    const sel = p.s.length === 1 ? p.s[0] : null;
    const fotos = Array.from({ length: nf(p) }, (_, k) => `<img src="${img(p, k, false)}" alt="${titulo(p)}, foto ${k + 1}" data-zoom>`).join('');
    const roupa = p.s.includes('M');
    const rel = P.filter(o => o.c === p.c && o.id !== p.id).sort((a, b) => (b.b === p.b) - (a.b === p.b)).slice(0, 4);
    $('#pmBody').innerHTML = `
      <div class="pm-g">
        <div class="pm-ph${nf(p) <= 2 ? ' one' : ''}">${fotos}</div>
        <div class="pm-in">
          <div class="br">${p.b || 'BK Clothing'} · ${p.c}</div>
          <h2>${p.n}</h2>
          <div class="co">Cor: ${p.cor}</div>
          <div class="pr">${brl(p.p)}</div>
          <div class="pix">${p.p == null ? 'Consulte valor e disponibilidade no WhatsApp.' : 'Pix, cartão ou a combinar. Envio para todo o Brasil.'}</div>
          <div class="pm-lb"><span>Tamanho</span>${roupa ? '<button data-guia>Guia de medidas</button>' : ''}</div>
          <div class="sizes">${p.s.map(s => `<button${s === sel ? ' class="on"' : ''} data-size="${s}">${s}</button>`).join('')}</div>
          <div class="pm-act">
            <button class="btn solid full" data-add="${p.id}">Adicionar à sacola</button>
            <button class="btn ghost full" data-buy="${p.id}">${WA_SVG} Comprar agora no WhatsApp</button>
          </div>
          ${p.d ? `<p style="margin-bottom:1.375rem">${p.d}</p>` : ''}
          <details id="guia"${roupa ? '' : ' hidden'}><summary>Guia de medidas</summary>
            <table class="guide"><tr><th>Tam.</th><th>Largura</th><th>Comprimento</th></tr><tr><td>P</td><td>52 cm</td><td>70 cm</td></tr><tr><td>M</td><td>54 cm</td><td>72 cm</td></tr><tr><td>G</td><td>56 cm</td><td>74 cm</td></tr><tr><td>GG</td><td>58 cm</td><td>76 cm</td></tr></table>
            <p>Medidas de referência para camisetas. Na dúvida, mande sua altura e peso no WhatsApp que a gente indica o tamanho certo.</p></details>
          <details><summary>Envio e retirada</summary><p>Enviamos para todo o Brasil. O frete é calculado na conversa, pelo seu CEP. Também dá para retirar na loja, no Floresta, em Joinville.</p></details>
          <details><summary>Trocas</summary><p>Não serviu? Fale com a gente no WhatsApp em até 7 dias após receber, com a peça sem uso e com etiqueta, e combinamos a troca.</p></details>
          <p class="ref">Ref. ${p.id}</p>
        </div>
      </div>
      ${rel.length ? `<div class="sec" style="padding-top:4.375rem;padding-bottom:5.625rem"><div class="sec-h"><div><span class="eyebrow">Na mesma linha</span><h2 class="d" style="font-size:clamp(2.75rem,6vw,5.625rem)">Você também vai curtir</h2></div></div><div class="grid">${rel.map(o => BK.card(o)).join('')}</div></div>` : ''}`;
    curSize = sel || '';
    pm.scrollTop = 0;
    bagEl.classList.remove('open'); veil.classList.remove('open');
    pm.classList.add('open'); document.body.classList.add('lock');
    if (location.hash !== '#p=' + id) history.pushState(null, '', '#p=' + id);
  }
  const fromHash = () => { const m = location.hash.match(/^#p=(\d+)/); if (m) openProduct(m[1]); else if (pm.classList.contains('open')) closeAll(); };
  window.addEventListener('popstate', fromHash);

  /* ---------- lightbox ---------- */
  const lb = $('#lb'); let lbSet = [], lbK = 0;
  const lbShow = k => { lbK = (k + lbSet.length) % lbSet.length; $('img', lb).src = lbSet[lbK].src; $('p', lb).textContent = (lbSet[lbK].cap ? lbSet[lbK].cap + ' · ' : '') + (lbK + 1) + ' / ' + lbSet.length; };
  const lbOpen = (set, k) => { lbSet = set; lb.classList.add('open'); lbShow(k); };

  /* ---------- eventos ---------- */
  document.addEventListener('click', e => {
    const t = e.target;
    const c = t.closest('[data-p]');
    if (c) { e.preventDefault(); openProduct(c.dataset.p); return; }
    if (t.closest('[data-tema]')) {
      const r = document.documentElement, tema = r.dataset.theme === 'light' ? 'dark' : 'light';
      r.dataset.theme = tema; try { localStorage.setItem('bk_tema', tema); } catch (e) {}
      const m = $('meta[name="theme-color"]'); if (m) m.content = tema === 'light' ? '#f6f4ef' : '#0b0b0b';
      return;
    }
    if (t.closest('[data-bag]')) { drawBag(); openBag(); return; }
    if (t.closest('[data-menu]')) { $('#mnav').classList.toggle('open'); return; }
    if (t.closest('#mnav a')) { $('#mnav').classList.remove('open'); return; }
    if (t.closest('[data-close]') || t === veil) { closeAll(); return; }
    const sz = t.closest('[data-size]');
    if (sz) { $$('.sizes button').forEach(b => b.classList.toggle('on', b === sz)); curSize = sz.dataset.size; return; }
    if (t.closest('[data-guia]')) { const g = $('#guia'); g.open = true; g.scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
    const add = t.closest('[data-add]'), buy = t.closest('[data-buy]');
    if (add || buy) {
      const s = curSize;
      if (!s) { toast('Escolha um tamanho'); $('.sizes').animate([{ transform: 'translateX(0)' }, { transform: 'translateX(-6px)' }, { transform: 'translateX(6px)' }, { transform: 'translateX(0)' }], { duration: 260 }); return; }
      if (add) { addBag(add.dataset.add, s); pm.classList.remove('open'); if (location.hash.startsWith('#p=')) history.replaceState(null, '', location.pathname + location.search); openBag(); }
      else window.open(wa(pedido([{ id: buy.dataset.buy, s, q: 1 }])), '_blank', 'noopener');
      return;
    }
    const q = t.closest('[data-q]');
    if (q) { const [k, d] = q.dataset.q.split(':').map(Number); if (d === 0) bag.splice(k, 1); else { bag[k].q += d; if (bag[k].q < 1) bag.splice(k, 1); } save(); drawBag(); return; }
    const z = t.closest('[data-zoom]');
    if (z) { const set = $$('[data-zoom]', z.parentElement).map(i => ({ src: i.dataset.full || i.src, cap: i.dataset.cap || '' })); lbOpen(set, $$('[data-zoom]', z.parentElement).indexOf(z)); return; }
    if (t.closest('.lb .nx')) return lbShow(lbK + 1);
    if (t.closest('.lb .pv')) return lbShow(lbK - 1);
    if (t.closest('.lb')) lb.classList.remove('open');
  });
  document.addEventListener('keydown', e => {
    if (lb.classList.contains('open')) { if (e.key === 'Escape') lb.classList.remove('open'); if (e.key === 'ArrowRight') lbShow(lbK + 1); if (e.key === 'ArrowLeft') lbShow(lbK - 1); return; }
    if (e.key === 'Escape') closeAll();
  });
  BK.lightbox = lbOpen;

  /* ---------- cabeçalho e entrada ---------- */
  const hd = $('.hd');
  const onScroll = () => hd.classList.toggle('stuck', scrollY > 30);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  BK.reveal = () => {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
    $$('.rv:not(.in)').forEach(el => io.observe(el));
  };
  drawBag();
  document.addEventListener('DOMContentLoaded', () => { BK.reveal(); fromHash(); });
})();
