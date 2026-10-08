# Aplica tema claro/escuro, textos novos e artes da logo nas páginas do site
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site'))
V = '?v=7"'
TH = "<script>try{var t=localStorage.getItem('bk_tema');if(t)document.documentElement.dataset.theme=t}catch(e){}</script>\n"
CSS_OLD = '<link rel="stylesheet" href="css/style.css?v=6">'
CSS_NEW = TH + '<link rel="stylesheet" href="css/style.css?v=7">'
ICONS = ('<svg class="lua" viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/></svg>'
         '<svg class="sol" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/>'
         '<path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/></svg>')


def rd(p):
    return open(p, encoding='utf-8').read()


def wr(p, s):
    open(p, 'w', encoding='utf-8').write(s)


def sub(s, old, new):
    assert old in s, old[:70]
    return s.replace(old, new)


# index.html
s = rd('index.html')
s = s.replace('class="sec paper"', 'class="sec alt"')
s = sub(s, '<h2 class="d">Escolha<br>seu corre</h2>', '<h2 class="d">Compre por<br>categoria</h2>')
s = sub(s, '<h2 class="d">Passa<br>aqui</h2>', '<h2 class="d">Visite<br>a loja</h2>')
s = sub(s, '<h2 class="d">Chegou<br>na BK</h2>', '<h2 class="d">Novidades<br>da semana</h2>')
a = s.index('    <div class="hero-bg">')
b = s.index('    <div class="hero-in">')
s = s[:a] + '    <div class="hero-bg"><div class="art" id="art" role="img" aria-label="Logo BK Clothing"></div></div>\n' + s[b:]
s = s.replace('<link rel="preload" as="image" href="img/loja.webp">\n', '')
s = sub(s, CSS_OLD, CSS_NEW).replace('?v=6"', V)
wr('index.html', s)

# catalogo.html
s = rd('catalogo.html')
s = sub(s, '<body data-page="catalogo" class="paper">', '<body data-page="catalogo">')
s = sub(s, CSS_OLD, CSS_NEW).replace('?v=6"', V)
wr('catalogo.html', s)

# links.html
s = rd('links.html')
s = sub(s, CSS_OLD, CSS_NEW)
s = sub(s, '<main class="lk">', '<main class="lk">\n  <button class="ico tema" id="tema" aria-label="Alternar tema claro e escuro">' + ICONS + '</button>')
s = sub(s, '</main>\n</body>', "</main>\n<script>document.getElementById('tema').onclick=function(){var r=document.documentElement,t=r.dataset.theme==='light'?'dark':'light';r.dataset.theme=t;try{localStorage.setItem('bk_tema',t)}catch(e){}}</script>\n</body>")
wr('links.html', s)

# js/app.js
s = rd('js/app.js')
s = sub(s, '      <button class="ico" data-bag aria-label="Abrir sacola">',
        '      <button class="ico tema" data-tema aria-label="Alternar tema claro e escuro">' + ICONS + '</button>\n      <button class="ico" data-bag aria-label="Abrir sacola">')
old = "    if (t.closest('[data-bag]')) { drawBag(); openBag(); return; }"
new = """    if (t.closest('[data-tema]')) {
      const r = document.documentElement, tema = r.dataset.theme === 'light' ? 'dark' : 'light';
      r.dataset.theme = tema; try { localStorage.setItem('bk_tema', tema); } catch (e) {}
      const m = $('meta[name="theme-color"]'); if (m) m.content = tema === 'light' ? '#f6f4ef' : '#0b0b0b';
      return;
    }
"""
s = sub(s, old, new + old)
s = sub(s, '<p style="font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#8f887b;margin-top:22px">Ref. ${p.id}</p>', '<p class="ref">Ref. ${p.id}</p>')
wr('js/app.js', s)

# js/home.js
ART = r'''  /* arte do hero: quatro leituras da logo, desenhadas em SVG. ?arte na URL mostra o seletor */
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
    d: `<svg viewBox="0 0 600 720" preserveAspectRatio="xMidYMid slice"><text x="300" y="455" text-anchor="middle" font-size="500" style="font-family:var(--body);font-weight:200;fill:none;stroke:currentColor;stroke-width:1.2">BK</text>
        <g class="fade"><text class="cl" x="300" y="585" text-anchor="middle" font-size="128" letter-spacing="6">CLOTHING</text><path class="s ac" d="M110 620H490"/></g></svg>`,
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

'''
s = rd('js/home.js')
s = sub(s, "  BK.reveal();\n})();", ART + "  BK.reveal();\n})();")
wr('js/home.js', s)
print('ok')
