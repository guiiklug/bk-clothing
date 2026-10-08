"""Exporta as imagens de apresentação (perfil hoje, perfil proposto, seções de 9) e uma folha de conferência do documento."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
AP = AQUI / 'apresentacao'
AP.mkdir(exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=2)
    pg.goto((AQUI / 'index.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(1500)
    pg.locator('#perfil-novo').screenshot(path=str(AP / 'perfil-proposta.jpg'), type='jpeg', quality=90)
    pg.locator('#perfil-hoje').screenshot(path=str(AP / 'perfil-hoje.jpg'), type='jpeg', quality=90)
    secs = pg.locator('header.capa, section').all()
    for i, s in enumerate(secs):
        s.screenshot(path=str(AP / f'_doc-{i:02d}.jpg'), type='jpeg', quality=70)
    largura = pg.evaluate('document.documentElement.scrollWidth')
    b.close()
    # celular: só para conferir rolagem lateral
    b = p.chromium.launch(channel='chrome', headless=True)
    pm = b.new_page(viewport={'width': 375, 'height': 800})
    pm.goto((AQUI / 'index.html').as_uri())
    pm.wait_for_timeout(800)
    print('desktop', largura, 'celular', pm.evaluate('document.documentElement.scrollWidth'))
    b.close()

# seções de 9, direto das publicações
feed = sorted((AQUI / 'feed').glob('*.jpg'))
for n in range(0, len(feed), 9):
    S = Image.new('RGB', (3 * 540 + 8, 3 * 675 + 8), '#0c1014')
    for k, f in enumerate(feed[n:n + 9]):
        S.paste(Image.open(f).resize((540, 675), Image.LANCZOS), ((k % 3) * 544, (k // 3) * 679))
    S.save(AP / f'secao-{n // 9 + 1}.jpg', quality=90)

# folha de conferência do documento
docs = sorted(AP.glob('_doc-*.jpg'))
ims = [Image.open(f) for f in docs]
w = 900
ims = [im.resize((w, round(im.height * w / im.width))) for im in ims]
cols = 3
alt = [0] * cols
pos = []
for im in ims:
    c = alt.index(min(alt))
    pos.append((c * (w + 10), alt[c]))
    alt[c] += im.height + 10
S = Image.new('RGB', (cols * (w + 10), max(alt)), '#444')
for im, xy in zip(ims, pos):
    S.paste(im, xy)
S.save(AP / '_conf-doc.jpg', quality=80)
for f in docs:
    f.unlink()
print('ok', S.size)
