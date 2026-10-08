"""Gera as artes do Instagram da BK, versão 2 (sem preço, uma ideia por linha, com vídeo).

Uso:  python gerar.py
Monta artes.html com cada arte no tamanho real e exporta tudo em JPG com o Playwright.
Entram as fotos padronizadas (_coleta/piloto), as fotos reais do feed (raw/m_*), a foto da loja
e os quadros dos vídeos (raw/q-*). Para trocar peça ou texto, edite as listas e rode de novo.
"""
import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
P = '../_coleta/piloto/'
LG = '<span class="lg"><b>BK</b><i>CLOTHING</i></span>'

# cada linha da grade é uma ideia. Ordem: da publicação mais recente para a mais antiga.
# (tipo, nome, imagem, transformação/posição, fundo, texto)
POSTS = [
    # linha 1: a peça-chave em três cores, palavra grande
    ('cor', '01-preta', P + '1914784.png', 'scale(1.62) translate(0,17%)', '#e3e3e3', 'Preta'),
    ('cor', '02-marinho', P + '1914785.png', 'scale(1.62) translate(0,17%)', '#dfe2e6', 'Marinho'),
    ('cor', '03-bege', P + '1914786.png', 'scale(1.62) translate(0,17%)', '#e6dfd2', 'Bege'),
    # linha 2: vídeo, detalhe e coleção
    ('video', '04-video-bomber', 'raw/q-bomber.png', '50% 42%', '', 'bomber'),
    ('peca', '05-detalhe-gola', P + '1914786.png', 'scale(3.1) translate(1%,19%)', '#e6dfd2', ''),
    ('tipo', '06-inverno', '', '', '#0b0b0b', 'Inverno|26'),
    # linha 3: mochila
    ('peca', '07-mochila', P + '1849734.png', 'scale(1.38) translate(0,1%)', '#d9d0bd', ''),
    ('video', '08-video-mochila', 'raw/q-mochila.png', '50% 46%', '', 'mochila'),
    ('peca', '09-detalhe-mochila', P + '1849734.png', 'scale(3) translate(0,-17%)', '#e3e3e3', ''),
    # linha 4: no corpo
    ('foto', '10-no-corpo-1', 'raw/m_DYZwCrnkSnr.jpg', '50% 20%', '', ''),
    ('tipo-claro', '11-slogan', '', '', '#f3f0ea', 'Vista|estilo.|Vista|BK.'),
    ('foto', '12-no-corpo-2', 'raw/m_DYr4JXkEbkN.jpg', '50% 18%', '', ''),
    # linha 5: movimento
    ('peca', '13-cargo', P + '1679459.png', 'scale(1.75) rotate(-14deg) translate(2%,6%)', '#ddd6c4', ''),
    ('video', '14-video-arara', 'raw/q-arara.png', '50% 44%', '', 'arara'),
    ('peca', '15-conjunto', P + '1910185.png', 'scale(1.5) rotate(9deg) translate(0,10%)', '#e3e3e3', ''),
    # linha 6: a loja
    ('foto', '16-loja', '../site/img/loja.webp', '62% 40%', '', ''),
    ('logo', '17-logo', '', '', '#0b0b0b', ''),
    ('foto', '18-no-corpo-3', 'raw/m_DYZvpUtEWYv.jpg', '50% 20%', '', ''),
]
# capas dos destaques: recortes do próprio material, no mesmo idioma do feed
CAPAS = [
    ('novo', 'img', P + '1914786.png', 'scale(3.1) translate(1%,19%)', '#e6dfd2', ''),
    ('quem-usa', 'foto', 'raw/m_DYZv6EcEdTi.jpg', '50% 30%', '', ''),
    ('tamanhos', 'txt', '', '', '#f3f0ea', 'P M G'),
    ('envio', 'img', P + '1849734.png', 'scale(3) translate(0,-17%)', '#e3e3e3', ''),
    ('loja', 'foto', '../site/img/loja.webp', '70% 45%', '', ''),
    ('vip', 'txt', '', '', '#0b0b0b', 'VIP'),
]


def post(tipo, nome, src, tr, fundo, txt):
    linhas = ''.join(f'<span>{x}</span>' for x in txt.split('|'))
    if tipo == 'cor':
        tam = 410 if len(txt) <= 5 else 296
        corpo = f'<img class="pk" src="{src}" style="transform:{tr}"><h2 class="palavra" style="font-size:{tam}px;top:{34 if tam > 300 else 70}px">{txt}</h2>'
    elif tipo == 'peca':
        corpo = f'<img class="pk" src="{src}" style="transform:{tr}">'
    elif tipo in ('foto', 'video'):
        corpo = f'<img src="{src}" style="object-position:{tr}">'
    elif tipo == 'logo':
        corpo = f'<div class="centro">{LG}</div>'
    else:
        corpo = f'<h2 class="frase">{linhas}</h2><div class="mk">{LG}</div>'
    est = f' style="background:{fundo}"' if fundo else ''
    return f'<div class="arte post {tipo}" id="p-{nome}"{est}>{corpo}</div>'


def capa(slug, tipo, src, tr, fundo, txt):
    if tipo == 'img':
        corpo = f'<img class="pk" src="{src}" style="transform:{tr}">'
    elif tipo == 'foto':
        corpo = f'<img src="{src}" style="object-position:{tr}">'
    else:
        cor = '#0b0b0b' if fundo != '#0b0b0b' else '#f3f0ea'
        corpo = f'<h3 style="color:{cor}">{txt}</h3>'
    est = f' style="background:{fundo}"' if fundo else ''
    return f'<div class="arte capa" id="c-{slug}"{est}>{corpo}</div>'


CARROSSEL = f'''
<div class="arte post cor" id="k-1" style="background:#e6dfd2"><img class="pk" src="{P}1914786.png" style="transform:scale(1.62) translate(0,17%)"><h2 class="palavra">Bege</h2><div class="pg">1 / 4</div></div>
<div class="arte post foto" id="k-2"><img src="../_coleta/img/1914786_0.jpg"><div class="pg w">2 / 4</div></div>
<div class="arte post peca" id="k-3" style="background:#e6dfd2"><img class="pk" src="{P}1914786.png" style="transform:scale(3.1) translate(1%,19%)"><div class="pg">3 / 4</div></div>
<div class="arte post tipo ficha" id="k-4" style="background:#0b0b0b"><h2 class="frase"><span>Jaqueta</span><span>bomber</span></h2>
  <dl><div><dt>Cores</dt><dd>Preta · Marinho · Bege</dd></div><div><dt>Tamanhos</dt><dd>P · M · G · GG</dd></div><div><dt>Como pedir</dt><dd>Comente QUERO ou chame no direct</dd></div></dl><div class="pg w">4 / 4</div></div>'''

STORIES = f'''
<div class="arte story" id="s-1-chegou" style="background:#0b0b0b"><img class="solta" src="{P}1849734.png"><div class="topo"><h2>Chegou</h2></div>
  <div class="base"><p>Mochila High. Responda QUERO e a gente separa a sua</p></div></div>
<div class="arte story" id="s-2-enquete" style="background:#0b0b0b"><div class="topo"><h2 style="font-size:250px">Qual você<br>leva?</h2></div>
  <div class="trio"><img src="feed/01-preta.jpg"><img src="feed/02-marinho.jpg"><img src="feed/03-bege.jpg"></div>
  <div class="adesivo"><span>Preta</span><span>Marinho</span><span>Bege</span></div></div>
<div class="arte story" id="s-3-tamanhos" style="background:#ddd6c4;color:#0b0b0b"><img class="pk" src="{P}1679459.png" style="transform:scale(2.2) rotate(-14deg) translate(4%,6%)"><div class="topo"><h2>Ainda<br>tem</h2></div>
  <div class="base"><div class="grade"><span>P</span><span class="x">M</span><span>G</span><span>GG</span></div><p>Calça cargo. M esgotou. Chame no direct para garantir a sua</p></div></div>
<div class="arte story foto" id="s-4-quem-usa"><img class="bg" src="raw/m_DYZv6EcEdTi.jpg" style="object-position:50% 20%"><div class="topo w"><h2>Quem<br>usa BK</h2></div>
  <div class="base w"><p>Marque @bkclothiing na sua foto e apareça aqui</p></div></div>
<div class="arte story foto" id="s-5-loja"><img class="bg" src="../site/img/loja.webp" style="object-position:66% 40%"><div class="topo w"><h2>Passe<br>na loja</h2></div>
  <div class="base w"><b>Rua Santa Catarina, 2348</b><p>Floresta · Joinville</p><div class="link">Como chegar</div></div></div>
<div class="arte story" id="s-6-caixinha" style="background:#f3f0ea;color:#0b0b0b"><div class="topo"><h2 style="font-size:236px">Que peça<br>você quer<br>ver aqui?</h2></div>
  <div class="caixa"><b>Conta pra gente</b><span>Digite alguma coisa...</span></div><div class="mk" style="top:auto;bottom:380px">{LG}</div></div>'''

CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#777;font-family:"Jost",sans-serif;display:flex;flex-wrap:wrap;gap:20px;padding:20px}
.arte{position:relative;overflow:hidden;flex:none;background:#0b0b0b;color:#f3f0ea}
.arte img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.arte img.pk{mix-blend-mode:multiply}
.arte img.solta{inset:auto 0 auto 0;top:560px;height:830px;object-fit:cover;object-position:50% 46%}
.post{width:1080px;height:1350px}.capa{width:1080px;height:1080px}.story{width:1080px;height:1920px}
.lg{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:44px}
.lg::before,.lg::after{content:"";position:absolute;top:0;bottom:0;width:32%;border:.045em solid currentColor}
.lg::before{left:0;border-right:0}.lg::after{right:0;border-left:0}
.lg b{font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}
.lg i{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}
.mk{position:absolute;left:64px;bottom:64px;z-index:2}
.cor,.peca{color:#0b0b0b}
.palavra{position:absolute;left:0;right:0;top:34px;text-align:center;font-family:"Bebas Neue";font-weight:400;font-size:410px;line-height:.86;letter-spacing:-.005em;text-transform:uppercase;white-space:nowrap;color:#0b0b0b;z-index:0}
.cor img.pk{z-index:1}
.frase{position:absolute;left:64px;right:64px;top:70px;font-family:"Bebas Neue";font-weight:400;font-size:300px;line-height:.84;text-transform:uppercase}
.frase span{display:block}
.tipo-claro{color:#0b0b0b}
.tipo .frase{font-size:340px}
.centro{position:absolute;inset:0;display:grid;place-items:center}.centro .lg{font-size:250px}
.pg{position:absolute;top:60px;right:60px;font-size:30px;font-weight:500;letter-spacing:.12em;color:#0b0b0b;z-index:3}.pg.w{color:#f3f0ea}
.ficha .frase{font-size:230px}
.ficha dl{position:absolute;left:64px;right:64px;bottom:70px}
.ficha dl div{display:grid;grid-template-columns:300px 1fr;padding:32px 0;border-top:2px solid rgba(243,240,234,.3);font-size:42px}
.ficha dt{font-size:28px;letter-spacing:.2em;text-transform:uppercase;color:#c8b89a;padding-top:8px}
.ficha dd{font-weight:400}
.capa h3{position:absolute;inset:0;display:grid;place-items:center;font-family:"Bebas Neue";font-weight:400;font-size:330px;letter-spacing:.02em}
.story.foto::before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(11,11,11,.62) 0,rgba(11,11,11,0) 36%,rgba(11,11,11,0) 60%,rgba(11,11,11,.8) 100%)}
.topo{position:absolute;top:260px;left:70px;right:70px;z-index:2}
.story h2{font-family:"Bebas Neue";font-weight:400;font-size:300px;line-height:.84;text-transform:uppercase}
.story .base{position:absolute;left:70px;right:70px;bottom:360px;z-index:2}
.story .base b{display:block;font-family:"Bebas Neue";font-weight:400;font-size:96px;text-transform:uppercase;line-height:1}
.story .base p{font-size:42px;font-weight:400;line-height:1.3;margin-top:10px;max-width:22ch}
.story .w{color:#f3f0ea}
.trio{position:absolute;top:840px;left:0;right:0;display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.trio img{position:static;aspect-ratio:4/5;height:auto}
.adesivo{position:absolute;top:1370px;left:150px;right:150px;background:#fff;color:#0b0b0b;border-radius:28px;display:grid;grid-template-columns:repeat(3,1fr);overflow:hidden;font-size:40px;font-weight:500;text-align:center}
.adesivo span{padding:44px 0}.adesivo span+span{border-left:2px solid #ddd}
.grade{display:flex;gap:14px;margin-bottom:26px}
.grade span{width:150px;height:150px;border:3px solid #0b0b0b;display:grid;place-items:center;font-size:60px;font-weight:400;background:rgba(255,255,255,.35)}
.grade .x{opacity:.35;text-decoration:line-through}
.link{display:inline-block;margin-top:30px;background:#fff;color:#0b0b0b;border-radius:18px;padding:22px 34px;font-size:38px;font-weight:500}
.caixa{position:absolute;left:70px;right:70px;top:1130px;background:#fff;color:#0b0b0b;border-radius:30px;padding:50px;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.12)}
.caixa b{display:block;font-size:46px;font-weight:500;margin-bottom:34px}
.caixa span{display:block;background:#efefef;border-radius:18px;padding:34px;font-size:38px;color:#888}
'''

for d in ['feed', 'carrossel', 'destaques', 'stories']:
    shutil.rmtree(AQUI / d, ignore_errors=True)
for d in ['feed', 'carrossel', 'destaques', 'stories', 'apresentacao']:
    (AQUI / d).mkdir(exist_ok=True)
DEST = {'p': 'feed', 'k': 'carrossel', 'c': 'destaques', 's': 'stories'}
CAB = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
       '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Jost:wght@200;300;400;500&display=swap" rel="stylesheet">'
       f'<style>{CSS}</style></head><body>')


def exporta(pg, html):
    (AQUI / 'artes.html').write_text(CAB + html + '</body></html>', encoding='utf-8')
    pg.goto((AQUI / 'artes.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(1500)
    for el in pg.locator('.arte').all():
        pre, nome = el.get_attribute('id').split('-', 1)
        el.screenshot(path=str(AQUI / DEST[pre] / f'{nome}.jpg'), type='jpeg', quality=90)


with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 2400, 'height': 2000})
    exporta(pg, ''.join(post(*x) for x in POSTS) + CARROSSEL + ''.join(capa(*c) for c in CAPAS))
    exporta(pg, STORIES)        # o story da enquete usa posts já exportados
    b.close()


def folha(arqs, saida, cols, w, h):
    lin = (len(arqs) + cols - 1) // cols
    S = Image.new('RGB', (cols * w + (cols + 1) * 6, lin * h + (lin + 1) * 6), '#555')
    for n, f in enumerate(arqs):
        S.paste(Image.open(f).convert('RGB').resize((w, h), Image.LANCZOS), (6 + (n % cols) * (w + 6), 6 + (n // cols) * (h + 6)))
    S.save(saida, quality=85)


feed = [AQUI / 'feed' / f'{x[1]}.jpg' for x in POSTS]
folha(feed, AQUI / 'apresentacao' / '_conf-feed.jpg', 3, 360, 450)
folha(sorted((AQUI / 'carrossel').glob('*.jpg')), AQUI / 'apresentacao' / '_conf-carrossel.jpg', 4, 300, 375)
folha(sorted((AQUI / 'stories').glob('*.jpg')), AQUI / 'apresentacao' / '_conf-stories.jpg', 6, 270, 480)
folha([AQUI / 'destaques' / f'{c[0]}.jpg' for c in CAPAS], AQUI / 'apresentacao' / '_conf-capas.jpg', 6, 220, 220)
print('ok', len(feed))
