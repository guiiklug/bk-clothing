"""Explorações de logo para a BK Clothing, desenhadas em SVG por código (nada gerado por IA).
Uso:  python gerar.py   ->  logos.html, logos.jpg e uma imagem por opção em opcoes/"""
from pathlib import Path
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
(AQUI / 'opcoes').mkdir(exist_ok=True)

ESPELHO = ('<g fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linejoin="miter">'
           '<path d="M300 130V430M300 280L420 130M300 280L420 430"/>'
           '<path d="M300 130H225A75 75 0 0 0 225 280H300M300 280H215A75 75 0 0 0 215 430H300"/></g>')

OPC = [
    ('0', 'Atual', 'A logo de hoje, para comparar.',
     '<path class="s" stroke-width="5" d="M250 150H190V450H250M350 150H410V450H350"/>'
     '<text class="jo" x="300" y="335" font-size="112" text-anchor="middle" style="font-weight:200;letter-spacing:6px">BK</text>'
     '<text class="be" x="300" y="392" font-size="42" text-anchor="middle" style="letter-spacing:3px">CLOTHING</text>'),
    ('A', 'Espelho', 'O B virado de costas para o K, dividindo a mesma haste. Vira um símbolo só, como monograma de grife.',
     ESPELHO.format(sw=16) + '<text class="jo" x="307" y="510" font-size="26" text-anchor="middle" style="font-weight:400;letter-spacing:15px">CLOTHING</text>'),
    ('B', 'Vertical', 'Os colchetes esticam e as letras empilham. Formato de etiqueta de roupa, bom para costurar na peça.',
     '<path class="s" stroke-width="4" d="M268 60H212V540H268M332 60H388V540H332"/>'
     '<text class="jo" x="300" y="268" font-size="158" text-anchor="middle" style="font-weight:200">B</text>'
     '<text class="jo" x="300" y="432" font-size="158" text-anchor="middle" style="font-weight:200">K</text>'
     '<text class="be" x="300" y="505" font-size="30" text-anchor="middle" style="letter-spacing:4px">CLOTHING</text>'),
    ('C', 'Bloco', 'Letra larga e pesada, com os colchetes reduzidos a dois cantos. A mais streetwear.',
     '<text class="ar" x="296" y="372" font-size="262" text-anchor="middle" style="letter-spacing:-10px">BK</text>'
     '<path class="s" stroke-width="6" d="M70 190V110H150M530 360V440H450"/>'
     '<text class="ar2" x="311" y="505" font-size="24" text-anchor="middle" style="letter-spacing:22px">CLOTHING</text>'),
    ('D', 'Selo', 'O monograma dentro de um carimbo redondo com cidade e slogan. Para sacola, adesivo e etiqueta.',
     '<defs><path id="circ" d="M300 300m-222 0a222 222 0 1 1 444 0a222 222 0 1 1 -444 0"/></defs>'
     '<circle cx="300" cy="300" r="268" fill="none" stroke="currentColor" stroke-width="5"/><circle cx="300" cy="300" r="176" fill="none" stroke="currentColor" stroke-width="2"/>'
     '<text class="ar2" font-size="31" style="font-weight:600;letter-spacing:5px"><textPath href="#circ" textLength="1380">BK CLOTHING · JOINVILLE SC · VISTA ESTILO · </textPath></text>'
     '<g transform="translate(136,146) scale(.55)">' + ESPELHO.format(sw=22) + '</g>'),
    ('E', 'Corte', 'A sigla pesada e inclinada, fatiada na diagonal com as duas metades desalinhadas. A mais louca.',
     '<defs><clipPath id="cima"><polygon points="0,0 600,0 600,250 0,390"/></clipPath><clipPath id="baixo"><polygon points="0,390 600,250 600,600 0,600"/></clipPath></defs>'
     '<g clip-path="url(#cima)"><text class="ari" x="318" y="392" font-size="250" text-anchor="middle" style="letter-spacing:-8px">BK</text></g>'
     '<g clip-path="url(#baixo)"><text class="ari" x="282" y="406" font-size="250" text-anchor="middle" style="letter-spacing:-8px">BK</text></g>'
     '<text class="ar2" x="300" y="500" font-size="24" text-anchor="middle" style="letter-spacing:22px">CLOTHING</text>'),
    ('F', 'Alta', 'Letras estreitas esticadas para cima, bem altas. Cara de marca de passarela.',
     '<g transform="translate(300,468) scale(1,2.25)"><text class="an" x="0" y="0" font-size="190" text-anchor="middle" style="letter-spacing:4px">BK</text></g>'
     '<path class="s" stroke-width="4" d="M150 120V90H190M450 498V528H410"/>'
     '<text class="jo" x="306" y="560" font-size="22" text-anchor="middle" style="font-weight:400;letter-spacing:19px">CLOTHING</text>'),
    ('G', 'Sobreposta', 'O B cheio e o K só em contorno, um por cima do outro. Lembra capa de revista.',
     '<text class="ar" x="232" y="400" font-size="330" text-anchor="middle">B</text>'
     '<text class="ar" x="372" y="400" font-size="330" text-anchor="middle" style="fill:none;stroke:currentColor;stroke-width:5px;paint-order:stroke">K</text>'
     '<text class="ar2" x="311" y="505" font-size="24" text-anchor="middle" style="letter-spacing:22px">CLOTHING</text>'),
    ('H', 'Clássica', 'Letra de alto contraste entre colchetes bem finos. A mais elegante e a menos streetwear.',
     '<text class="bo" x="300" y="388" font-size="262" text-anchor="middle" style="letter-spacing:-6px">BK</text>'
     '<path class="s" stroke-width="2.5" d="M150 150H96V450H150M450 150H504V450H450"/>'
     '<text class="jo" x="308" y="520" font-size="22" text-anchor="middle" style="font-weight:300;letter-spacing:18px">CLOTHING</text>'),
]
FONTES = ('https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Anton&family=Bebas+Neue'
          '&family=Bodoni+Moda:opsz,wght@6..96,500&family=Jost:wght@200;300;400&display=swap')
CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#cfcbc2;font-family:'Archivo',sans-serif;color:#0b0b0b;padding:16px;display:grid;grid-template-columns:repeat(3,780px);gap:16px;width:max-content}
.op{background:#f3f0ea;width:780px;padding:26px 30px 28px}
.op header{display:grid;grid-template-columns:auto 1fr;gap:2px 14px;align-items:baseline;padding-bottom:14px;border-bottom:1.5px solid #0b0b0b}
.le{grid-row:1/3;font-weight:900;font-stretch:125%;font-size:44px;line-height:1}
.no{font-weight:600;font-size:20px}.ob{font-size:15px;color:#5d574e;line-height:1.35}
.pal{display:grid;grid-template-columns:1fr 190px;gap:18px;margin-top:18px;align-items:center}
.gr svg{width:100%;display:block}
.pq{display:grid;gap:14px;justify-items:center}
.av{width:170px;height:170px;border-radius:50%;background:#0b0b0b;color:#f3f0ea;display:grid;place-items:center}.av svg{width:128%}
.mi{display:flex;gap:12px;align-items:center}
.mi span{width:64px;height:64px;display:grid;place-items:center;background:#dce8ef}.mi span+span{width:40px;height:40px;background:#fff;border:1px solid #ddd}
.mi svg{width:120%}
svg{overflow:visible}
.s{fill:none;stroke:currentColor}
text{fill:currentColor}
.jo{font-family:'Jost',sans-serif}.be{font-family:'Bebas Neue',sans-serif}.an{font-family:'Anton',sans-serif}.bo{font-family:'Bodoni Moda',serif;font-weight:500}
.ar{font-family:'Archivo',sans-serif;font-weight:900;font-stretch:125%}.ar2{font-family:'Archivo',sans-serif;font-weight:500;font-stretch:110%}
.ari{font-family:'Archivo',sans-serif;font-weight:900;font-stretch:125%;font-style:italic}
'''


def painel(l, nome, obs, svg):
    s = f'<svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'
    return (f'<section class="op" id="op-{l}"><header><span class="le">{l}</span><span class="no">{nome}</span><span class="ob">{obs}</span></header>'
            f'<div class="pal"><div class="gr">{s}</div><div class="pq"><div class="av">{s}</div><div class="mi"><span>{s}</span><span>{s}</span></div></div></div></section>')


html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>BK Clothing | explorações de logo</title><link href="{FONTES}" rel="stylesheet">'
        f'<style>{CSS}</style></head><body>' + ''.join(painel(*o) for o in OPC) + '</body></html>')
(AQUI / 'logos.html').write_text(html, encoding='utf-8')
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 2420, 'height': 1400})
    pg.goto((AQUI / 'logos.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(2500)
    pg.screenshot(path=str(AQUI / 'logos.jpg'), type='jpeg', quality=88, full_page=True)
    for o in OPC:
        pg.locator(f'#op-{o[0]}').screenshot(path=str(AQUI / 'opcoes' / f'{o[0]}-{o[1].lower()}.jpg'), type='jpeg', quality=90)
    b.close()
print('ok')
