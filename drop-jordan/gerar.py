"""Criativos do drop de bermudas de basquete (três cores), na identidade de verão da BK.

Uso:  python gerar.py
Recorta as fotos padronizadas (pack/), monta as artes em artes.html e exporta:
  feed/ (6 posts 1080x1350), stories/ (2, 1080x1920), anuncio/ (3 formatos, sóbrio) e _conf.jpg.
Sem preço nas artes. A foto de textura é a foto real tirada na loja.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from rembg import remove, new_session

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
A1, A2, S, K, W = '#dce8ef', '#c5d6e1', '#e6dfd0', '#0b0b0b', '#f3f0ea'
LG = '<span class="lg"><b>BK</b><i>CLOTHING</i></span>'

(AQUI / 'cut').mkdir(exist_ok=True)
ses = None
for n in ['preta', 'cinza', 'verde']:
    dst = AQUI / 'cut' / f'{n}.png'
    if not dst.exists():
        ses = ses or new_session('isnet-general-use')
        out = remove(Image.open(AQUI / 'pack' / f'{n}.png').convert('RGB'), session=ses)
        out.crop(out.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox()).save(dst)
tex = AQUI / 'cut' / 'textura.jpg'
if not tex.exists():
    Image.open(AQUI / 'orig' / '18.webp').convert('RGB').save(tex, quality=92)


def pc(n, w, x, y, rot=0, z=2):
    return f'<img class="ct" src="cut/{n}.png" style="width:{w}px;left:{x}px;top:{y}px;transform:translate(-50%,-50%) rotate({rot}deg);z-index:{z}">'


def wd(t, tam, x, y, cor=K):
    return f'<div class="wd" style="font-size:{tam}px;left:{x}px;top:{y}px;color:{cor}">{"<br>".join(t.split("|"))}</div>'


FEED = [
    ('01-preta', A1, wd('Preta', 250, 48, 48) + pc('preta', 900, 540, 790, -6)),
    ('02-gelo', K, wd('Gelo', 312, 48, 44, W) + pc('cinza', 880, 540, 790, 5)),
    ('03-verde', S, wd('Verde', 240, 48, 48) + pc('verde', 900, 540, 790, -5)),
    ('04-trio', W, wd('Drop|novo', 250, 50, 50) + pc('verde', 560, 800, 820, 10, 2) + pc('cinza', 560, 300, 860, -10, 3) + pc('preta', 600, 548, 1000, 2, 4)),
    ('05-textura', K, '<img class="ft" src="cut/textura.jpg">'),
    ('06-drop', A2, wd('Três|cores', 222, 50, 60) + f'<div class="mk">{LG}</div>'),
]
STORIES = [
    ('1-chegou', A1, wd('Chegou', 330, 56, 250) + pc('preta', 780, 540, 1030, -6) + f'<p class="pe">Bermuda de basquete. Responda QUERO e a gente separa a sua</p>'),
    ('2-enquete', W, wd('Qual|leva?', 212, 60, 250) + pc('preta', 440, 240, 1040, -8) + pc('cinza', 440, 540, 1010, 3) + pc('verde', 440, 840, 1040, 8)
     + '<div class="adesivo"><span>Preta</span><span>Gelo</span><span>Verde</span></div>'),
]


def anuncio(w, h):
    pw, cy, passo = {(1200, 628): (300, 300, 350), (1200, 1200): (360, 590, 380), (960, 1200): (290, 590, 305)}[(w, h)]
    out = ''
    for k, (n, nome) in enumerate([('preta', 'Preta'), ('cinza', 'Gelo'), ('verde', 'Verde')]):
        x = w / 2 + (k - 1) * passo
        out += f'<img class="cs" src="cut/{n}.png" style="width:{pw}px;left:{x}px;top:{cy}px"><span class="nm" style="left:{x}px;top:{cy + pw * .5}px">{nome}</span>'
    return (f'<div class="lo">{LG}</div>' + out + '<div class="le"><span>Bermuda de basquete</span><span>bkclothing.com.br</span></div>')


CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#777;display:flex;flex-wrap:wrap;gap:16px;padding:16px;font-family:"Jost",sans-serif}
.arte{position:relative;overflow:hidden;flex:none;color:#0b0b0b}
.post{width:1080px;height:1350px}.story{width:1080px;height:1920px}
.ft{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ct{position:absolute;height:auto;filter:drop-shadow(0 34px 38px rgba(0,0,0,.3))}
.wd{position:absolute;font-family:"Big Shoulders Display","Archivo",sans-serif;font-weight:900;text-transform:uppercase;letter-spacing:0;line-height:.84;white-space:nowrap;z-index:1}
.lg{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:60px}
.lg::before,.lg::after{content:"";position:absolute;top:0;bottom:0;width:32%;border:.045em solid currentColor}
.lg::before{left:0;border-right:0}.lg::after{right:0;border-left:0}
.lg b{font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}
.lg i{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}
.mk{position:absolute;left:54px;bottom:60px}
.pe{position:absolute;left:60px;right:60px;bottom:370px;font-family:"Archivo";font-size:44px;font-weight:500;line-height:1.25;max-width:21ch;z-index:3}
.adesivo{position:absolute;top:1380px;left:120px;right:120px;background:#0b0b0b;color:#f3f0ea;border-radius:28px;display:grid;grid-template-columns:repeat(3,1fr);overflow:hidden;font-family:"Archivo";font-size:42px;font-weight:500;text-align:center;z-index:3}
.adesivo span{padding:46px 0}.adesivo span+span{border-left:2px solid #444}
/* anúncio sóbrio */
.ad{background:#e7edf1}
.ad .lg{font-size:33px}.lo{position:absolute;left:44px;top:38px}
.cs{position:absolute;height:auto;transform:translate(-50%,-50%);filter:drop-shadow(0 22px 22px rgba(30,25,15,.16))}
.nm{position:absolute;transform:translateX(-50%);font-size:19px;letter-spacing:.14em;text-transform:uppercase}
.le{position:absolute;left:44px;right:44px;bottom:38px;display:flex;justify-content:space-between;align-items:baseline;font-size:25px}
.le span:last-child{font-size:19px;letter-spacing:.14em;text-transform:uppercase}
'''
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Big+Shoulders+Display:wght@900&family=Bebas+Neue'
          '&family=Jost:wght@200;300;400;500&display=swap" rel="stylesheet">')
html = ''.join(f'<div class="arte post" id="feed__{n}" style="background:{f}">{c}</div>' for n, f, c in FEED)
html += ''.join(f'<div class="arte story" id="stories__{n}" style="background:{f}">{c}</div>' for n, f, c in STORIES)
for nome, (w, h) in {'paisagem': (1200, 628), 'quadrado': (1200, 1200), 'retrato': (960, 1200)}.items():
    html += f'<div class="arte ad" id="anuncio__{nome}" style="width:{w}px;height:{h}px">{anuncio(w, h)}</div>'
(AQUI / 'artes.html').write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>{html}</body></html>', encoding='utf-8')

for d in ['feed', 'stories', 'anuncio']:
    (AQUI / d).mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 2600, 'height': 2000})
    pg.goto((AQUI / 'artes.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(2000)
    # a letra do Bruno (Big Shoulders) é estreita: cada título cresce até a margem, com teto de 1,55x
    pg.evaluate('''() => document.querySelectorAll('.wd').forEach(w => { const base = parseFloat(w.style.fontSize), max = w.parentElement.offsetWidth - w.offsetLeft - 56;
        w.style.fontSize = Math.floor(Math.min(base * (w.querySelector('br') ? 1.25 : 1.55), base * max / w.offsetWidth)) + 'px' })''')
    pg.wait_for_timeout(300)
    for el in pg.locator('.arte').all():
        pasta, nome = el.get_attribute('id').split('__')
        el.screenshot(path=str(AQUI / pasta / f'{nome}.jpg'), type='jpeg', quality=92)
    b.close()

# folha de conferência
arqs = [(AQUI / 'feed' / f'{n}.jpg', (360, 450)) for n, *_ in FEED] + [(AQUI / 'stories' / f'{n}.jpg', (253, 450)) for n, *_ in STORIES] \
    + [(AQUI / 'anuncio' / 'quadrado.jpg', (450, 450)), (AQUI / 'anuncio' / 'paisagem.jpg', (860, 450))]
linhas = [arqs[:6], arqs[6:]]
Sx = Image.new('RGB', (6 * 366 + 6, 2 * 456 + 6), '#666')
for li, linha in enumerate(linhas):
    x = 6
    for f, tam in linha:
        Sx.paste(Image.open(f).convert('RGB').resize(tam, Image.LANCZOS), (x, 6 + li * 456))
        x += tam[0] + 6
Sx.save(AQUI / '_conf.jpg', quality=86)
print('ok')
