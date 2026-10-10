"""Cinco opções de letra para os criativos, cada uma em três usos: título, marca d'água de fundo e marca d'água sobre foto.

Uso:  python letras.py   ->  letras/A..E.jpg e letras/_todas.jpg
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
SAIDA = AQUI / 'letras'
SAIDA.mkdir(exist_ok=True)
A1, A2, S, K, W = '#dce8ef', '#c5d6e1', '#e6dfd0', '#0b0b0b', '#f3f0ea'

# letra, nome, família, estilo extra, altura de linha
OPCOES = [
    ('A', 'Archivo larga (a atual)', 'Archivo', 'font-weight:900;font-stretch:125%;letter-spacing:-.025em', .82),
    ('B', 'Anton', 'Anton', 'font-weight:400;letter-spacing:-.005em', .9),
    ('C', 'Big Shoulders', 'Big Shoulders Display', 'font-weight:900;letter-spacing:0', .84),
    ('D', 'Unbounded', 'Unbounded', 'font-weight:800;letter-spacing:-.03em', .9),
    ('E', 'Syne', 'Syne', 'font-weight:800;letter-spacing:-.035em', .84),
]
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Anton'
          '&family=Big+Shoulders+Display:wght@900&family=Unbounded:wght@800&family=Syne:wght@800&family=Jost:wght@400&display=swap" rel="stylesheet">')
CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#555;padding:20px;display:grid;gap:20px;font-family:"Jost",sans-serif}
.op{width:3240px;background:#0b0b0b}
.cab{height:110px;display:flex;align-items:center;gap:26px;padding:0 44px;color:#f3f0ea;font-size:44px;letter-spacing:.06em}
.cab b{background:#dce8ef;color:#0b0b0b;width:70px;height:70px;display:grid;place-items:center;font-weight:400}
.lin{display:flex}
.t{position:relative;width:1080px;height:1350px;overflow:hidden;flex:none}
.f{position:absolute;text-transform:uppercase;white-space:nowrap}
.pc{position:absolute;height:auto;transform:translate(-50%,-50%) rotate(var(--r,0deg));filter:drop-shadow(0 34px 38px rgba(0,0,0,.3))}
.ft{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.fundo{position:absolute;left:-40px;top:-30px;display:flex;flex-direction:column;align-items:flex-start}
.cen{left:50%;top:50%;transform:translate(-50%,-50%) rotate(-12deg);color:#fff;opacity:.5;text-align:center}
.ass{right:44px;bottom:40px;color:#fff;opacity:.8;font-size:44px}
'''


def opcao(l, nome, fam, est, lh):
    f = f'font-family:\'{fam}\';{est};line-height:{lh}'
    titulo = (f'<div class="t" style="background:{A1}"><div class="f aj" data-w="980" data-max="300" data-h="450" style="{f};left:50px;top:52px;color:{K}">Drop<br>novo</div>'
              f'<img class="pc" src="cut/preta.png" style="width:820px;left:540px;top:870px;--r:-6deg"></div>')
    linhas = ''.join(f'<div class="f aj" data-w="1160" data-max="400" style="{f};position:static;color:{"#303030" if k % 2 else "#202020"}">BK Clothing</div>' for k in range(14))
    fundo = (f'<div class="t" style="background:{K}"><div class="fundo">{linhas}</div>'
             f'<img class="pc" src="cut/cinza.png" style="width:860px;left:540px;top:690px;--r:5deg"></div>')
    foto = (f'<div class="t"><img class="ft" src="criativo/_loja20.jpg">'
            f'<div class="f cen aj" data-w="820" data-max="300" style="{f}">BK<br>Clothing</div><div class="f ass" style="{f}">BK Clothing</div></div>')
    return f'<div class="op" id="op{l}"><div class="cab"><b>{l}</b>{nome}</div><div class="lin">{titulo}{fundo}{foto}</div></div>'


html = f'<!doctype html><html><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>{"".join(opcao(*o) for o in OPCOES)}</body></html>'
(AQUI / 'letras.html').write_text(html, encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 3300, 'height': 2000})
    pg.goto((AQUI / 'letras.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(2500)
    # cada palavra é ajustada à largura pedida, para as cinco letras ocuparem o mesmo espaço
    pg.evaluate('''() => document.querySelectorAll('.aj').forEach(e => { e.style.fontSize = '100px';
        let t = Math.min(+e.dataset.max, Math.floor(100 * e.dataset.w / e.offsetWidth));
        if (e.dataset.h) t = Math.min(t, Math.floor(100 * e.dataset.h / e.offsetHeight)); e.style.fontSize = t + 'px' })''')
    pg.wait_for_timeout(300)
    for l, *_ in OPCOES:
        pg.locator(f'#op{l}').screenshot(path=str(SAIDA / f'{l}.jpg'), type='jpeg', quality=90)
    b.close()

ims = [Image.open(SAIDA / f'{l}.jpg') for l, *_ in OPCOES]
T = Image.new('RGB', (1620, sum(i.height // 2 for i in ims)))
y = 0
for i in ims:
    T.paste(i.resize((1620, i.height // 2), Image.LANCZOS), (0, y))
    y += i.height // 2
T.save(SAIDA / '_todas.jpg', quality=88)
print('ok')
