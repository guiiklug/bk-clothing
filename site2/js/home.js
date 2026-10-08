/* Página inicial (versão 2): categorias com peça recortada, drops, vitrines com banner e carrossel */
(function () {
  const BK = window.BK, P = BK.P, $ = s => document.querySelector(s);
  const byId = Object.fromEntries(P.map(p => [p.id, p]));
  const LOGO = '<span class="logo"><b>BK</b><i>CLOTHING</i></span>';

  /* categorias: uma peça recortada por categoria, nome embaixo */
  const cats = [['Jaquetas & Moletons', '1914785'], ['Oversized', '1914792'], ['Camisetas', '1688777'], ['Polos', '1849982'],
    ['Bermudas & Shorts', '1701345'], ['Calças', '1679459'], ['Conjuntos', '1910185'], ['Regatas', '1690115'], ['Acessórios', '1703193']];
  $('#cats').innerHTML = cats.map(([c, id]) => {
    const n = P.filter(p => p.c === c).length;
    return `<a href="catalogo.html?c=${encodeURIComponent(c)}"><span class="im"><img src="img/cut/${id}.webp" alt="" loading="lazy"></span>
      <span class="rot">${c}<small>${n} ${n === 1 ? 'peça' : 'peças'}</small></span></a>`;
  }).join('');

  /* drops: as oito mais recentes com recorte */
  const sel = ['1914786', '1688777', '1849734', '1703184', '1914792', '1910185', '1703193', '1679459'];
  $('#sel').innerHTML = sel.filter(id => byId[id]).map(id => BK.card(byId[id], 'Novo')).join('');

  /* vitrines: banner com a palavra em pé de um lado, carrossel da categoria do outro */
  const pc = (id, est, hover) => `<img class="pc" src="img/cut/${id}.webp" alt="" loading="lazy" style="${est};--h:${hover}">`;
  const video = n => `<video src="img/video/${n}.mp4" autoplay muted loop playsinline></video>`;
  const vitrines = {
    '#vitrines-1': [
      { t: 'Jaquetas & Moletons', pal: 'Jaquetas', cs: ['Jaquetas & Moletons'], md: video('bomber'), fundo: '' },
      { t: 'Camisetas', pal: 'Camisetas', cs: ['Camisetas', 'Oversized', 'Polos'], md: video('tee'), fundo: '', inv: true },
    ],
    '#vitrines-2': [
      { t: 'Bermudas & Shorts', pal: 'Bermudas', cs: ['Bermudas & Shorts'], fundo: 'var(--t3)',
        md: pc('1703184', 'width:74%;left:2%;top:6%;transform:rotate(-10deg)', 'rotate(-5deg) translateY(-.5rem)') + pc('1701345', 'width:80%;left:20%;top:44%;transform:rotate(8deg)', 'rotate(3deg) translateY(.4rem)') },
      { t: 'Acessórios', pal: 'Acessórios', cs: ['Acessórios'], fundo: 'var(--t2)', inv: true,
        md: pc('1849734', 'height:66%;left:8%;top:4%;transform:rotate(-7deg)', 'rotate(-2deg) translateY(-.5rem)') + pc('1703193', 'width:76%;left:20%;top:56%;transform:rotate(9deg)', 'rotate(4deg) translateY(.4rem)') },
    ],
  };
  const tam = s => s.length <= 6 ? 5 : s.length <= 8 ? 3.9 : 3.1;
  for (const [alvo, lista] of Object.entries(vitrines)) {
    $(alvo).innerHTML = lista.map(v => {
      const itens = P.filter(p => v.cs.includes(p.c)).sort((a, b) => BK.CUT.has(b.id) - BK.CUT.has(a.id)).slice(0, 9);
      return `<section class="sec" style="padding-top:0"><div class="w"><div class="vit rv${v.inv ? ' inv' : ''}">
        <a class="bn" href="catalogo.html?c=${encodeURIComponent(v.cs[0])}" style="--tp:${tam(v.pal)}rem" aria-label="${v.t}">
          <div class="pal"><b>${v.pal}</b></div>
          <div class="md"${v.fundo ? ` style="background:${v.fundo}"` : ''}>${v.md}<span class="mk">${LOGO}</span></div>
        </a>
        <div class="lado">
          <div class="topo"><h2>${v.t}</h2><div class="setas"><button data-s="-1" aria-label="Anteriores">←</button><button data-s="1" aria-label="Próximas">→</button></div></div>
          <div class="trilho">${itens.map(p => BK.card(p)).join('')}</div>
        </div></div></div></section>`;
    }).join('');
  }
  document.addEventListener('click', e => {
    const b = e.target.closest('.setas button'); if (!b) return;
    const tr = b.closest('.lado').querySelector('.trilho');
    tr.scrollBy({ left: +b.dataset.s * tr.clientWidth * .68, behavior: 'smooth' });
  });

  $('#btnMapa').href = BK.mapa; $('#btnVip').href = BK.vip;
  $('#btnWa').href = BK.wa('Olá! Vim pelo site da BK Clothing.');

  /* abertura: as peças acompanham de leve o mouse e a rolagem */
  const pcs = [...document.querySelectorAll('.hero .pc')];
  const base = pcs.map(el => getComputedStyle(el).transform);
  const calmo = matchMedia('(prefers-reduced-motion:reduce)').matches || matchMedia('(hover:none)').matches;
  if (!calmo) {
    let mx = 0, my = 0, sy = 0, pend = false;
    const pinta = () => {
      pend = false;
      pcs.forEach((el, i) => {
        const d = +el.dataset.d || 10;
        el.style.transform = `translate(${mx * d}px,${my * d * .7 - sy * d * .012}px) ${base[i] === 'none' ? '' : base[i]}`;
      });
    };
    const pede = () => { if (!pend) { pend = true; requestAnimationFrame(pinta); } };
    addEventListener('mousemove', e => { mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5; pede(); }, { passive: true });
    addEventListener('scroll', () => { if (scrollY < innerHeight) { sy = scrollY; pede(); } }, { passive: true });
  }
  BK.reveal();
})();
