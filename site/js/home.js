/* Página inicial: categorias, lookbook, destaques */
(function () {
  const BK = window.BK, P = BK.P, $ = s => document.querySelector(s);
  const byId = Object.fromEntries(P.map(p => [p.id, p]));
  const qtd = c => P.filter(p => p.c === c).length;

  $('#mq').innerHTML = Array(2).fill(['Jaquetas', 'Oversized', 'Bermudas', 'Polos', 'Conjuntos', 'Moletons', 'Regatas', 'Acessórios']).flat().map(t => `<span>${t}</span>`).join('');

  const cats = [
    ['Jaquetas & Moletons', 'img/std/1914784.webp'],
    ['Oversized', 'img/p/1914792_1.webp'],
    ['Bermudas & Shorts', 'img/std/1703197.webp'],
    ['Camisetas', 'img/std/1688777.webp'],
    ['Acessórios', 'img/std/1849734.webp'],
  ];
  $('#cats').innerHTML = cats.map(([c, src]) => `
    <a class="cat rv" href="catalogo.html?c=${encodeURIComponent(c)}">
      <img src="${src}" alt="" loading="lazy">
      <div><h3>${c.replace(' & ', '<br>& ')}</h3><small>${qtd(c)} peças</small></div>
    </a>`).join('');

  /* lookbook: sessões da coleção, na ordem do feed */
  const look = [
    { id: 'puffer', t: 'Puffer', d: 'Jaquetas acolchoadas com capuz, em marinho, grafite e preto.', f: [['look1', 'w', 'Puffer marinho'], ['look/ig1', '', 'Puffer marinho'], ['look/ig3', '', 'Puffer preta'], ['look/ig2', 'w', 'Puffer, três cores']] },
    { id: 'tricot', t: 'Tricot & bomber', d: 'Tricot com gola polo e meio zíper, e a bomber em tom areia.', f: [['look/ig6', '', 'Tricot polo preto'], ['look/ig5', '', 'Tricot polo, cores'], ['look/ig4', '', 'Bomber areia']] },
    { id: 'conjuntos', t: 'Conjuntos', d: 'Corta-vento com calça ou bermuda, para usar junto ou separado.', f: [['look/ig8', '', 'Conjunto cinza'], ['look/ig9', '', 'Conjunto branco e azul'], ['look/ig10', '', 'Conjunto preto']] },
    { id: 'street', t: 'Street', d: 'Oversized, polo e bermuda de moletom para o dia a dia.', f: [['look/ig11', '', 'Polo oversized'], ['look2', '', 'Oversized preta e cargo'], ['look/ig12', '', 'Bermuda moletom']] },
  ];
  $('#lookChips').innerHTML = `<button class="chip on" data-l="">Tudo</button>` + look.map(s => `<button class="chip" data-l="${s.id}">${s.t}</button>`).join('');
  $('#look').innerHTML = look.map((s, i) => `
    <div class="look-s rv" data-s="${s.id}">
      <div class="look-t"><span class="num">${String(i + 1).padStart(2, '0')}</span><h3>${s.t}</h3><p>${s.d}</p></div>
      <div class="look-g">${s.f.map(([src, cls, cap]) => `<figure class="shot ${cls}"><img src="img/${src}.webp" alt="${cap}" loading="lazy" data-zoom data-cap="${cap}"><figcaption>${cap}</figcaption></figure>`).join('')}</div>
    </div>`).join('');
  $('#lookChips').addEventListener('click', e => {
    const b = e.target.closest('.chip'); if (!b) return;
    document.querySelectorAll('#lookChips .chip').forEach(c => c.classList.toggle('on', c === b));
    document.querySelectorAll('.look-s').forEach(s => { s.classList.toggle('hide', !!b.dataset.l && s.dataset.s !== b.dataset.l); s.classList.add('in'); });
  });
  /* o lightbox do lookbook percorre a coleção inteira, não só a sessão */
  $('#look').addEventListener('click', e => {
    const z = e.target.closest('[data-zoom]'); if (!z) return;
    e.stopPropagation();
    const all = [...document.querySelectorAll('.look-s:not(.hide) [data-zoom]')];
    BK.lightbox(all.map(i => ({ src: i.src, cap: i.dataset.cap })), all.indexOf(z));
  });

  const dest = ['1914786', '1910184', '1914792', '1910185', '1679459', '1849734', '1703197', '1910183',
    '1849694', '1914784', '1910182', '1688777', '1701345', '1703193', '1703189', '1849982'];
  $('#rail').innerHTML = dest.filter(id => byId[id]).map((id, i) => BK.card(byId[id], i < 4 ? 'Novo' : '')).join('');

  $('#btnMapa').href = BK.mapa; $('#btnVip').href = BK.vip;
  $('#btnWa').href = BK.wa('Olá! Vim pelo site da BK Clothing.');

  /* arte do hero: quatro leituras da logo, desenhadas em SVG. ?arte na URL mostra o seletor */
  const tg = '<text class="tg" x="300" y="668" text-anchor="middle" font-size="12">VISTA ESTILO, VISTA BK CLOTHING</text>';
  const artes = {
    a: `<svg viewBox="0 0 600 720"><path class="s draw" pathLength="1" d="M250 110H150V590H250"/><path class="s draw" pathLength="1" d="M350 110H450V590H350"/>
        <g class="fade"><text class="bk" x="300" y="388" text-anchor="middle" font-size="190" letter-spacing="6">BK</text><text class="cl" x="300" y="472" text-anchor="middle" font-size="74" letter-spacing="3">CLOTHING</text>${tg}</g></svg>`,
    b: `<svg viewBox="0 0 600 720" preserveAspectRatio="xMidYMid slice"><defs><pattern id="pbk" width="100" height="120" patternUnits="userSpaceOnUse"><path class="s" style="stroke-width:1" d="M42 24H27V96H42M58 24H73V96H58"/><text class="bk" x="50" y="64" text-anchor="middle" font-size="25">BK</text><text class="cl" x="50" y="78" text-anchor="middle" font-size="9.5">CLOTHING</text></pattern></defs>
        <rect width="600" height="720" fill="url(#pbk)" opacity=".26"/><rect x="150" y="180" width="300" height="360" fill="var(--panel)"/>
        <path class="s ac draw" pathLength="1" d="M265 235H205V485H265"/><path class="s ac draw" pathLength="1" d="M335 235H395V485H335"/>
        <g class="fade"><text class="bk" x="300" y="380" text-anchor="middle" font-size="100" letter-spacing="3">BK</text><text class="cl" x="300" y="426" text-anchor="middle" font-size="39" letter-spacing="1.5">CLOTHING</text></g></svg>`,
    c: `<svg viewBox="0 0 600 720"><image class="fade" href="img/loja.webp" x="170" y="135" width="260" height="430" preserveAspectRatio="xMaxYMid slice"/>
        <path class="s draw" pathLength="1" d="M250 105H140V595H250"/><path class="s draw" pathLength="1" d="M350 105H460V595H350"/><g class="fade">${tg}</g></svg>`,
    d: `<svg viewBox="0 0 600 720" preserveAspectRatio="xMidYMid slice"><text x="300" y="490" text-anchor="middle" font-size="480" style="font-family:var(--body);font-weight:200;fill:none;stroke:currentColor;stroke-width:1.2">BK</text>
        <g class="fade"><text class="cl" x="300" y="612" text-anchor="middle" font-size="128" letter-spacing="6">CLOTHING</text><path class="s ac" d="M110 648H490"/></g></svg>`,
  };
  const art = $('#art');
  const setArte = k => { art.innerHTML = artes[k] || artes.a; document.querySelectorAll('.art-pick button').forEach(b => b.classList.toggle('on', b.dataset.k === k)); };
  const qs = new URLSearchParams(location.search);
  let k = 'a'; try { k = localStorage.getItem('bk_arte') || 'a'; } catch (e) {}
  if (artes[qs.get('arte')]) k = qs.get('arte');
  if (qs.has('arte')) {
    document.body.insertAdjacentHTML('beforeend', `<div class="art-pick">Arte ${Object.keys(artes).map(x => `<button data-k="${x}">${x.toUpperCase()}</button>`).join('')}</div>`);
    document.querySelector('.art-pick').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; try { localStorage.setItem('bk_arte', b.dataset.k); } catch (er) {} setArte(b.dataset.k); });
  }
  setArte(k);

  BK.reveal();
})();
