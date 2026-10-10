"""Artes para o grupo VIP do WhatsApp da BK (foto do grupo, post de boas-vindas e modelos de post).

Uso:  python gerar.py   (monta artes.html, exporta JPGs em foto-grupo/, posts/ e apresentacao/)
Mesma identidade do Instagram de verão (instagram/verao): azul esbranquiçado, areia, preto e off-white,
Archivo larga e pesada, peça recortada por cima da letra. Sem preço, sem gíria, sem enfeite. Custo zero.
Para trocar peça, cor ou texto, edite as listas abaixo e rode de novo.
"""
import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
R, B, S, K, W = '#c5d6e1', '#dce8ef', '#e6dfd0', '#0b0b0b', '#f3f0ea'
CUT = '../instagram/verao/cut/'
IMG = '../_coleta/img/'
LG = '<span class="lg"><b>BK</b><i>CLOTHING</i></span>'
CHROME = os.environ.get('CHROME_PATH') or ('/opt/pw-browsers/chromium' if Path('/opt/pw-browsers/chromium').exists() else None)


def pc(nome, w, x, y, rot=0):
    return (f'<img class="ct" src="{CUT}{nome}.png" style="width:{w}px;left:{x}px;top:{y}px;'
            f'transform:translate(-50%,-50%) rotate({rot}deg)">')


def wd(txt, tam, x, y, cor=K, rot=0):
    linhas = '<br>'.join(txt.split('|'))
    return f'<div class="wd" style="font-size:{tam}px;left:{x}px;top:{y}px;color:{cor};transform:rotate({rot}deg)">{linhas}</div>'


def pe(txt, cor=K, bottom=90):
    return f'<p class="pe" style="color:{cor};bottom:{bottom}px">{txt}</p>'


def foto(src, pos='50% 20%'):
    return f'<img class="ft" src="{src}" style="object-position:{pos}">'


def selo(txt, cor=K, fundo='transparent'):
    return f'<span class="selo" style="color:{cor};border-color:{cor};background:{fundo}">{txt}</span>'


# Foto do grupo: 1080x1080. O WhatsApp mostra em círculo, então tudo fica dentro dos 76% centrais.
FOTOS = [
    ('A-azul', B, f'<div class="centro" style="color:{K}">{LG}</div>'),
    ('B-preto', K, f'<div class="centro" style="color:{W}">{LG}</div>'),
    ('C-areia', S, f'<div class="centro" style="color:{K}">{LG}</div>'),
    ('D-vip', B, f'<div class="centro" style="color:{K}">{LG.replace("lg", "lg peq")}</div>' + '<div class="vip">VIP</div>'),
]

# Posts para mandar no grupo: 1080x1350 (mesma proporção do feed, pra reaproveitar entre os dois).
POSTS = [
    # fixado no topo do grupo
    ('01-bem-vindo', B, wd('Bem|vindo', 250, 54, 70) + pc('tee-diesel', 700, 660, 790, 6)
     + pe('Grupo VIP da BK Clothing. Ofertas e novidades chegam aqui primeiro.')),
    ('02-como-funciona', W, wd('Como|funciona', 148, 54, 70)
     + '<ol class="passos"><li><b>1</b><span>A peça aparece aqui</span></li>'
       '<li><b>2</b><span>Você responde <em>QUERO</em> com o tamanho</span></li>'
       '<li><b>3</b><span>A gente separa e envia, ou deixa na loja</span></li></ol>'),
    # rotina da semana
    ('03-chegou-hoje', S, wd('Che|gou|hoje', 250, 54, 70) + pc('cargo-marrom', 640, 740, 880, -10)
     + pe('Responda QUERO com o tamanho e a gente separa a sua.')),
    ('04-ultimas', K, wd('Últi|mas|peças', 236, 54, 70, W) + pc('conjunto-preto', 500, 760, 900, -5)
     + '<div class="grade"><span>P</span><span class="x">M</span><span>G</span><span>GG</span></div>'),
    ('05-qual-leva', R, wd('Qual|leva?', 212, 54, 70) + pc('bermuda-high', 500, 240, 820, -8)
     + pc('jeans', 450, 560, 800, 4) + pc('bermuda-lacoste', 500, 860, 840, 9)
     + '<div class="num"><span>1</span><span>2</span><span>3</span></div>'
     + pe('Responda com o número.')),
    ('06-nova-colecao', S, wd('Nova|cole|ção', 266, 54, 70) + pc('polo-roads', 640, 720, 880, -6)),
    ('07-so-no-grupo', K, wd('Só|no|grupo', 215, 54, 70, W) + pc('tee-comp', 580, 760, 900, 8)
     + pe('Condição exclusiva para quem está no grupo, até domingo.', W)),
    ('08-quem-usa', K, foto(IMG + '1914792_1.jpg', '50% 25%') + '<div class="veu"></div>' + wd('Quem|usa|BK', 236, 54, 70, W)
     + pe('Mande sua foto com a peça e ela aparece aqui e no Instagram.', W)),
    ('09-loja', K, foto('../site/img/loja.webp', '70% 45%') + '<div class="veu"></div>' + wd('Visite|a loja', 200, 54, 70, W)
     + pe('Rua Santa Catarina, 2348, Floresta, Joinville.', W)),
    ('10-todo-brasil', B, wd('Todo|Brasil', 200, 54, 70) + pc('bag', 500, 700, 800, -9)
     + pe('Enviamos para todo o país. Pedido e rastreio pelo WhatsApp.')),
]

CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#777;font-family:"Jost",sans-serif;display:flex;flex-wrap:wrap;gap:20px;padding:20px}
.arte{position:relative;overflow:hidden;flex:none}
.post{width:1080px;height:1350px}.quad{width:1080px;height:1080px}
.ft{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ct{position:absolute;height:auto;filter:drop-shadow(0 34px 38px rgba(0,0,0,.3));z-index:2}
.wd{font-family:"Archivo",sans-serif;font-weight:900;font-stretch:125%;text-transform:uppercase;letter-spacing:-.025em;
 position:absolute;line-height:.82;white-space:nowrap;transform-origin:0 0;z-index:1}
.lg{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:250px}
.lg::before,.lg::after{content:"";position:absolute;top:0;bottom:0;width:32%;border:.045em solid currentColor}
.lg::before{left:0;border-right:0}.lg::after{right:0;border-left:0}
.lg b{font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}
.lg i{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}
.centro{position:absolute;inset:0;display:grid;place-items:center}
.lg.peq{font-size:210px;margin-top:-70px}
.vip{position:absolute;left:50%;top:50%;transform:translate(-50%,230px);font-family:"Archivo";font-weight:900;font-stretch:125%;font-size:60px;letter-spacing:.1em;color:#0b0b0b}
.pe{position:absolute;left:60px;right:60px;font-size:40px;font-weight:500;line-height:1.25;max-width:26ch;z-index:3}
.veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,11,.6) 0,rgba(11,11,11,0) 38%,rgba(11,11,11,0) 60%,rgba(11,11,11,.8) 100%);z-index:1}
.grade{position:absolute;left:60px;bottom:90px;display:flex;gap:14px;z-index:3}
.grade span{width:160px;height:160px;background:#f3f0ea;color:#0b0b0b;display:grid;place-items:center;font-family:"Archivo";font-weight:800;font-stretch:125%;font-size:60px}
.grade .x{background:transparent;color:#f3f0ea;border:4px solid #f3f0ea;opacity:.45;text-decoration:line-through}
.num{position:absolute;left:0;right:0;top:1120px;display:grid;grid-template-columns:repeat(3,1fr);text-align:center;z-index:3;font-family:"Archivo";font-weight:900;font-stretch:125%;font-size:90px;color:#0b0b0b}
.passos{position:absolute;left:60px;right:60px;top:560px;list-style:none;font-size:54px;font-weight:400;line-height:1.2;color:#0b0b0b}
.passos li{display:grid;grid-template-columns:150px 1fr;align-items:center;gap:30px;padding:46px 0;border-top:3px solid #0b0b0b}
.passos span{display:block}
.passos li:last-child{border-bottom:3px solid #0b0b0b}
.passos b{font-family:"Archivo";font-weight:900;font-stretch:125%;font-size:120px;line-height:1}
.passos em{font-style:normal;font-weight:600}
'''
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Bebas+Neue'
          '&family=Jost:wght@200;300;400;500;600&display=swap" rel="stylesheet">')

for d in ['foto-grupo', 'posts', 'apresentacao']:
    shutil.rmtree(AQUI / d, ignore_errors=True)
    (AQUI / d).mkdir()

artes = ''.join(f'<div class="arte quad" id="f-{n}" style="background:{f}">{c}</div>' for n, f, c in FOTOS)
artes += ''.join(f'<div class="arte post" id="p-{n}" style="background:{f}">{c}</div>' for n, f, c in POSTS)
(AQUI / 'artes.html').write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>{artes}</body></html>', encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME) if CHROME else p.chromium.launch()
    pg = b.new_page(viewport={'width': 1140, 'height': 1400})
    pg.goto((AQUI / 'artes.html').as_uri())
    pg.wait_for_load_state('networkidle')
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(800)
    for n, _, _ in FOTOS:
        pg.locator(f'#f-{n}').screenshot(path=f'foto-grupo/{n}.jpg', type='jpeg', quality=92)
    for n, _, _ in POSTS:
        pg.locator(f'#p-{n}').screenshot(path=f'posts/{n}.jpg', type='jpeg', quality=92)
    b.close()

# apresentação: prévia da foto em círculo (como o WhatsApp mostra) e folha com todos os posts
circ = Image.new('RGB', (4 * 560, 560), '#1b1b1b')
for i, (n, _, _) in enumerate(FOTOS):
    im = Image.open(f'foto-grupo/{n}.jpg').resize((480, 480))
    m = Image.new('L', (480, 480), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(m).ellipse((0, 0, 479, 479), fill=255)
    circ.paste(im, (i * 560 + 40, 40), m)
circ.save('apresentacao/fotos-em-circulo.jpg', quality=88)

folha = Image.new('RGB', (5 * 432 + 6 * 16, 2 * 540 + 3 * 16), '#1b1b1b')
for i, (n, _, _) in enumerate(POSTS):
    im = Image.open(f'posts/{n}.jpg').resize((432, 540))
    folha.paste(im, (16 + (i % 5) * 448, 16 + (i // 5) * 556))
folha.save('apresentacao/posts.jpg', quality=88)
html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>BK Clothing: grupo VIP do WhatsApp</title>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#141414;color:#eee;font-family:Jost,sans-serif;padding:4vw}}h1{{font-weight:500;font-size:2.4rem;margin:0 0 .3em}}h2{{font-weight:500;font-size:1.5rem;margin:2.5em 0 .6em}}
p{{max-width:70ch;line-height:1.5;color:#bbb}}.g{{display:grid;gap:1.5vw}}.c4{{grid-template-columns:repeat(4,1fr)}}.c5{{grid-template-columns:repeat(5,1fr)}}img{{width:100%;display:block}}
figure{{margin:0}}figcaption{{font-size:.9rem;color:#999;margin-top:.4em}}.circ{{border-radius:50%}}pre{{background:#1f1f1f;padding:1.5em;white-space:pre-wrap;max-width:70ch;line-height:1.5}}a{{color:#c5d6e1}}</style></head><body>
<h1>Grupo VIP do WhatsApp</h1><p>Foto do grupo, descrição e dez modelos de post na identidade aprovada. Sem preço nas artes. Lista do que postar em <a href="ideias.md">ideias.md</a>.</p>
<h2>Foto do grupo (como o WhatsApp mostra)</h2><div class="g c4">""" + ''.join(f'<figure><img class="circ" src="foto-grupo/{n}.jpg"><figcaption>{n}</figcaption></figure>' for n, _, _ in FOTOS) + """</div>
<h2>Descrição</h2><pre>""" + (AQUI / 'descricao.txt').read_text(encoding='utf-8') + """</pre>
<h2>Posts</h2><div class="g c5">""" + ''.join(f'<figure><img src="posts/{n}.jpg"><figcaption>{n}</figcaption></figure>' for n, _, _ in POSTS) + """</div></body></html>"""
(AQUI / 'index.html').write_text(html, encoding='utf-8')
print('ok:', len(FOTOS), 'fotos,', len(POSTS), 'posts')
