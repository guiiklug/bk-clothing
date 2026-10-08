"""Confere o site2 por prints: primeira tela em várias larguras, seções da home, catálogo, produto e celular."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
S2 = RAIZ / 'site2'
OUT = RAIZ / '_coleta' / 'conf2'
OUT.mkdir(exist_ok=True)
modo = sys.argv[1] if len(sys.argv) > 1 else 'tudo'
erros = []


def abre(b, w, h, pagina='index.html', tema=None, dsf=1):
    pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=dsf)
    pg.on('console', lambda m: erros.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: erros.append(str(e)))
    if tema:
        pg.add_init_script(f"try{{localStorage.setItem('bk_tema2','{tema}')}}catch(e){{}}")
    pg.goto((S2 / pagina.split('#')[0].split('?')[0]).as_uri() + pagina[len(pagina.split('#')[0].split('?')[0]):])
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(1400)
    pg.evaluate("document.querySelectorAll('.rv').forEach(e=>{e.style.transition='none';e.classList.add('in')});document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
    pg.wait_for_timeout(600)
    return pg


with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True, args=['--autoplay-policy=no-user-gesture-required'])
    # primeira tela em várias larguras
    telas = [(1000, 640), (1440, 900), (1920, 1080), (2560, 1080), (3832, 1796)]
    ims = []
    for w, h in telas:
        pg = abre(b, w, h)
        f = OUT / f'hero-{w}.jpg'
        pg.screenshot(path=str(f), type='jpeg', quality=80)
        print(w, 'larg. rolagem', pg.evaluate('document.documentElement.scrollWidth'))
        ims.append(Image.open(f))
        pg.close()
    alt = 420
    ims = [im.resize((round(im.width * alt / im.height), alt)) for im in ims]
    S = Image.new('RGB', (sum(i.width for i in ims[:3]) + 16, alt * 2 + 8), '#888')
    x = 0
    for im in ims[:3]:
        S.paste(im, (x, 0)); x += im.width + 8
    x = 0
    for im in ims[3:]:
        S.paste(im, (x, alt + 8)); x += im.width + 8
    S.save(OUT / '_heros.jpg', quality=82)
    if modo == 'tudo':
        pg = abre(b, 1440, 900)
        secs = pg.locator('main section, footer.ft').all()
        partes = []
        for i, s in enumerate(secs[1:]):
            f = OUT / f's{i:02d}.jpg'
            s.screenshot(path=str(f), type='jpeg', quality=72)
            partes.append(Image.open(f))
        larg = 720
        partes = [im.resize((larg, round(im.height * larg / im.width))) for im in partes]
        col = [0, 0, 0]
        pos = []
        for im in partes:
            c = col.index(min(col)); pos.append((c * (larg + 8), col[c])); col[c] += im.height + 8
        S = Image.new('RGB', (3 * (larg + 8), max(col)), '#888')
        for im, xy in zip(partes, pos):
            S.paste(im, xy)
        S.save(OUT / '_home.jpg', quality=80)
        pg.close()
        # catálogo, produto, escuro e celular
        extras = []
        for nome, (w, h, pagina, tema) in {'catalogo': (1440, 900, 'catalogo.html', None), 'produto': (1440, 900, 'catalogo.html#p=1914786', None),
                                           'escuro': (1440, 900, 'index.html', 'dark'), 'links': (1440, 900, 'links.html', None)}.items():
            pg = abre(b, w, h, pagina, tema)
            f = OUT / f'x-{nome}.jpg'
            pg.screenshot(path=str(f), type='jpeg', quality=78)
            extras.append(Image.open(f).resize((720, 450)))
            pg.close()
        pg = abre(b, 375, 760, dsf=2)
        print('celular larg. rolagem', pg.evaluate('document.documentElement.scrollWidth'))
        cel = []
        for y in (0, 760, 1900, 3200):
            pg.evaluate(f'scrollTo(0,{y})'); pg.wait_for_timeout(350)
            f = OUT / f'm-{y}.jpg'
            pg.screenshot(path=str(f), type='jpeg', quality=78)
            cel.append(Image.open(f).resize((222, 450)))
        pg.close()
        S = Image.new('RGB', (4 * 728 , 2 * 458), '#888')
        for i, im in enumerate(extras):
            S.paste(im, (i * 728, 0))
        for i, im in enumerate(cel):
            S.paste(im, (i * 230, 458))
        S.save(OUT / '_extras.jpg', quality=80)
    b.close()
print('erros', erros[:5])
