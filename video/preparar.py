"""Prepara o que os vídeos de demonstração precisam: logo em PNG, capas de destaque em 1080x1920 e a fonte das cartelas."""
import urllib.request
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
PROJ = AQUI.parent
(AQUI / 'capas').mkdir(exist_ok=True)

# logo preta sobre branco, quadrada (foto de perfil e cartelas)
HTML = '''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Jost:wght@200&display=swap" rel="stylesheet">
<style>body{margin:0;width:800px;height:800px;background:#fff;display:grid;place-items:center;color:#0b0b0b}
.lg{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:190px}
.lg::before,.lg::after{content:"";position:absolute;top:0;bottom:0;width:32%;border:.04em solid currentColor}
.lg::before{left:0;border-right:0}.lg::after{right:0;border-left:0}
.lg b{font-family:"Jost";font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}
.lg i{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}</style></head>
<body><span class="lg"><b>BK</b><i>CLOTHING</i></span></body></html>'''
(AQUI / '_logo.html').write_text(HTML, encoding='utf-8')
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 800, 'height': 800})
    pg.goto((AQUI / '_logo.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(1200)
    pg.screenshot(path=str(AQUI / 'logo.png'))
    b.close()
(AQUI / '_logo.html').unlink()

# capas de destaque: a arte quadrada no centro de uma tela 1080x1920 da mesma cor da borda
for f in (PROJ / 'instagram' / 'verao' / 'destaques').glob('*.jpg'):
    im = Image.open(f).convert('RGB')
    tela = Image.new('RGB', (1080, 1920), im.getpixel((6, 6)))
    tela.paste(im, (0, 420))
    tela.save(AQUI / 'capas' / f.name, quality=90)

fonte = AQUI / 'ArchivoBlack-Regular.ttf'
if not fonte.exists():
    try:
        urllib.request.urlretrieve('https://github.com/google/fonts/raw/main/ofl/archivoblack/ArchivoBlack-Regular.ttf', fonte)
    except Exception as e:
        print('fonte não baixou:', e)
print('ok', fonte.exists(), len(list((AQUI / 'capas').glob('*.jpg'))))
