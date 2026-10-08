"""Criativos de exemplo para Google Ads da BK Clothing: 4 conceitos x 3 formatos de display.

Uso:  python gerar.py
Monta artes.html com cada peça no tamanho real, exporta JPG em <conceito>/<formato>.jpg e gera a
página de apresentação index.html. Usa as peças recortadas do site2 e a foto real da loja. Custo zero.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
CUT = '../site2/img/cut/'
A1, A2, S, K, W = '#dce8ef', '#c5d6e1', '#e6dfd0', '#0b0b0b', '#f3f0ea'
FORMATOS = {'paisagem': (1200, 628), 'quadrado': (1200, 1200), 'retrato': (960, 1200)}
LG = '<span class="lg"><b>BK</b><i>CLOTHING</i></span>'


def pc(i, w, cx, cy, rot=0, z=2):
    return f'<img class="pc" src="{CUT}{i}.webp" style="width:{w}px;left:{cx}px;top:{cy}px;transform:translate(-50%,-50%) rotate({rot}deg);z-index:{z}">'


def palavra(txt, W_, H_, x, y, larg, cor=K, extra=''):
    fs = round(larg / (len(txt) * 0.86))
    return (f'<svg class="wd" viewBox="0 0 {W_} {H_}" style="{extra}"><text x="{x}" y="{y}" textLength="{larg}" '
            f'lengthAdjust="spacingAndGlyphs" font-size="{fs}" fill="{cor}">{txt}</text></svg>')


def base(txt, cta, cor=K, lado=30, fundo_cta=None):
    fc = fundo_cta or cor
    tc = W if fc == K else K
    return (f'<div class="rod" style="color:{cor};left:{lado}px;right:{lado}px"><span>{txt}</span>'
            f'<b style="background:{fc};color:{tc}">{cta} →</b></div>')


def topo(cor=K, dir_='Joinville · envio para todo o Brasil'):
    return f'<div class="top" style="color:{cor}">{LG}<span>{dir_}</span></div>'


def c1(f, w, h):          # bomber em três cores
    cfg = {'paisagem': (221, 330, 290, (330, 600, 870), 372), 'quadrado': (221, 400, 540, (320, 600, 880), 740), 'retrato': (175, 360, 480, (265, 480, 695), 730)}[f]
    _, y, pw, xs, cy = cfg
    jaq = pc('1914784', pw, xs[0], cy + 14, -8, 2) + pc('1914786', pw, xs[2], cy + 14, 8, 2) + pc('1914785', pw * 1.04, xs[1], cy - 6, 0, 3)
    return (f'<div class="ad" style="background:{A1}">' + topo() + palavra('BOMBER', w, h, 30, y, w - 60) + jaq
            + base('Jaqueta bomber em três cores', 'Ver na loja') + '</div>')


def c2(f, w, h):          # cargo: metade preta, metade areia, palavra invertendo
    if f == 'retrato':
        meio = f'<div class="mt" style="inset:0 0 50% 0;background:{K}"></div>'
        wd = palavra('CARGO', w, h, 40, 690, w - 80, '#fff', 'mix-blend-mode:difference')
        peca = pc('1679459', 400, 480, 590, -12)
    else:
        meio = f'<div class="mt" style="inset:0 50% 0 0;background:{K}"></div>'
        yy, pw, cy, rot = (410, 300, 330, -20) if f == 'paisagem' else (700, 470, 610, -14)
        wd = palavra('CARGO', w, h, 40, yy, w - 80, '#fff', 'mix-blend-mode:difference')
        peca = pc('1679459', pw, w / 2, cy, rot)
    rod = (f'<div class="rod" style="left:30px;right:30px"><span style="color:{W if f != "retrato" else K}">Calça cargo, do P ao GG</span>'
           f'<b style="background:{K};color:{W}">Ver na loja →</b></div>')
    cab = topo('#fff').replace('style="color:#fff"', 'style="color:#fff;mix-blend-mode:difference"')
    return f'<div class="ad" style="background:{S}">' + meio + cab + wd + peca + rod + '</div>'


def c3(f, w, h):          # etiqueta
    tw, tx, ty, jw, jx, jy = {'paisagem': (350, 310, 322, 500, 860, 345), 'quadrado': (520, 400, 560, 660, 850, 800), 'retrato': (470, 330, 500, 600, 640, 880)}[f]
    tag = f'''<div class="tag" style="width:{tw}px;left:{tx}px;top:{ty}px;font-size:{tw / 26}px">
      <i class="furo"></i>{LG}
      <dl><div><dt>Artigo</dt><dd>Moda masculina</dd></div><div><dt>Origem</dt><dd>Joinville / SC</dd></div>
      <div><dt>Loja</dt><dd>Rua Santa Catarina, 2348</dd></div><div><dt>Envio</dt><dd>Todo o Brasil</dd></div><div><dt>Pedido</dt><dd>Pelo WhatsApp</dd></div></dl>
      <div class="barras"></div><small>bkclothing.com.br</small></div>'''
    return (f'<div class="ad" style="background:{A2}">' + pc('1703184', jw, jx, jy, 9, 1) + f'<i class="fio" style="left:{tx}px;top:0;height:{ty - tw * .62}px"></i>' + tag
            + base('Vista estilo, vista BK Clothing', 'Ver a coleção') + '</div>')


def c4(f, w, h):          # a loja de verdade
    if f == 'paisagem':
        foto = '<img class="ft" src="../site2/img/loja.webp" style="left:44%;width:56%;object-position:70% 42%">'
        tx = '<div class="lj" style="left:30px;top:150px;width:460px"><h2 style="font-size:92px">A loja</h2><p>Rua Santa Catarina, 2348<br>Floresta · Joinville</p></div>'
    else:
        foto = '<img class="ft" src="../site2/img/loja.webp" style="height:60%;object-position:66% 40%">'
        tx = f'<div class="lj" style="left:40px;top:{h * .6 + 60}px;right:40px"><h2 style="font-size:{130 if f == "quadrado" else 112}px">A loja</h2><p>Rua Santa Catarina, 2348<br>Floresta · Joinville</p></div>'
    return (f'<div class="ad" style="background:{K};color:{W}">' + foto + topo(W, 'Provador e peça nova toda semana') + tx
            + base('Envio para todo o Brasil', 'Como chegar', W, 30, W) + '</div>')


CONCEITOS = [('1-bomber', c1, 'Três cores', 'A peça-chave nas três cores, por cima da palavra. Para campanha de coleção.'),
             ('2-cargo', c2, 'Corte ao meio', 'Fundo partido em preto e areia; a palavra inverte de cor ao cruzar a divisa. Para destacar uma peça só.'),
             ('3-etiqueta', c3, 'Etiqueta', 'As informações da loja escritas como etiqueta de roupa. Para apresentar a marca a quem não conhece.'),
             ('4-loja', c4, 'A loja', 'Foto real da parede da loja com endereço. Para anúncio local em Joinville.')]

CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#888;display:flex;flex-wrap:wrap;gap:16px;padding:16px;font-family:"Archivo",sans-serif}
.ad{position:relative;overflow:hidden;flex:none;color:#0b0b0b;isolation:isolate}
.ad .pc{position:absolute;height:auto;filter:drop-shadow(0 26px 30px rgba(0,0,0,.28))}
.ad .ft{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ad .mt{position:absolute}
.wd{position:absolute;inset:0;width:100%;height:100%;z-index:1}
.wd text{font-family:"Archivo";font-weight:900;font-stretch:125%}
.lg{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:30px}
.lg::before,.lg::after{content:"";position:absolute;top:0;bottom:0;width:32%;border:.05em solid currentColor}
.lg::before{left:0;border-right:0}.lg::after{right:0;border-left:0}
.lg b{font-family:"Jost";font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}
.lg i{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}
.top{position:absolute;left:30px;right:30px;top:26px;display:flex;justify-content:space-between;align-items:flex-start;z-index:5;font-size:15px;font-weight:500;letter-spacing:.14em;text-transform:uppercase}
.rod{position:absolute;bottom:28px;display:flex;justify-content:space-between;align-items:center;gap:20px;z-index:5;font-size:25px;font-weight:600}
.rod b{font-size:16px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;padding:17px 24px;white-space:nowrap}
.tag{position:absolute;transform:translate(-50%,-50%) rotate(-5deg);background:#f3f0ea;color:#0b0b0b;padding:4.2em 2.2em 2em;z-index:3;box-shadow:0 1.4em 2.6em rgba(0,0,0,.22);text-align:center}
.tag .furo{position:absolute;top:1.1em;left:50%;width:1.7em;height:1.7em;margin-left:-.85em;border-radius:50%;background:#c5d6e1;box-shadow:inset 0 .15em .3em rgba(0,0,0,.25)}
.tag .lg{font-size:3.4em}
.tag dl{margin-top:1.8em;text-align:left;border-top:.12em solid #0b0b0b}
.tag dl div{display:flex;justify-content:space-between;gap:1em;padding:.62em 0;border-bottom:.08em dashed rgba(11,11,11,.4);font-size:1.02em}
.tag dt{font-weight:500;letter-spacing:.16em;text-transform:uppercase;font-size:.78em;padding-top:.2em;color:#555}
.tag dd{font-weight:700;font-stretch:75%;text-transform:uppercase;letter-spacing:.04em}
.barras{height:3.4em;margin-top:1.6em;background:repeating-linear-gradient(90deg,#0b0b0b 0 .16em,transparent .16em .34em,#0b0b0b .34em .42em,transparent .42em .7em,#0b0b0b .7em 1em,transparent 1em 1.16em)}
.tag small{display:block;margin-top:.7em;font-size:.86em;letter-spacing:.22em;font-weight:500}
.fio{position:absolute;width:2px;background:#0b0b0b;z-index:2;transform-origin:top;transform:rotate(1.5deg)}
.lj{position:absolute;z-index:4}
.lj h2{font-family:"Archivo";font-weight:900;font-stretch:125%;text-transform:uppercase;line-height:.86;letter-spacing:-.025em}
.lj p{margin-top:22px;font-size:27px;font-weight:500;line-height:1.3}
'''
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Bebas+Neue'
          '&family=Jost:wght@200&display=swap" rel="stylesheet">')

artes = ''
for slug, fn, _, _ in CONCEITOS:
    (AQUI / slug).mkdir(exist_ok=True)
    for f, (w, h) in FORMATOS.items():
        artes += fn(f, w, h).replace('<div class="ad"', f'<div class="ad" id="{slug}__{f}"', 1).replace(f'id="{slug}__{f}" style="', f'id="{slug}__{f}" style="width:{w}px;height:{h}px;', 1)
(AQUI / 'artes.html').write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>{artes}</body></html>', encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 2600, 'height': 2000})
    pg.goto((AQUI / 'artes.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(2000)
    for el in pg.locator('.ad').all():
        slug, f = el.get_attribute('id').split('__')
        el.screenshot(path=str(AQUI / slug / f'{f}.jpg'), type='jpeg', quality=92)
    b.close()

# folha de conferência
S_ = Image.new('RGB', (4 * 620, 330 + 560 + 620), '#777')
for i, (slug, *_r) in enumerate(CONCEITOS):
    y = 0
    for f, alt in (('paisagem', 314), ('quadrado', 600), ('retrato', 600)):
        im = Image.open(AQUI / slug / f'{f}.jpg')
        larg = 600 if f != 'retrato' else 480
        im = im.resize((larg, round(im.height * larg / im.width)))
        if f == 'quadrado':
            im = im.resize((540, 540))
        S_.paste(im, (i * 620 + 10, y + 10))
        y += im.height + 10
S_.save(AQUI / '_conf.jpg', quality=84)

# página de apresentação
blocos = ''
for slug, _fn, nome, desc in CONCEITOS:
    blocos += f'''<section><div class="w"><header><h2>{nome}</h2><p>{desc}</p></header>
  <div class="tr"><figure class="l"><img src="{slug}/paisagem.jpg" alt=""><figcaption>Paisagem · 1200 x 628</figcaption></figure>
  <figure><img src="{slug}/quadrado.jpg" alt=""><figcaption>Quadrado · 1200 x 1200</figcaption></figure>
  <figure><img src="{slug}/retrato.jpg" alt=""><figcaption>Retrato · 960 x 1200</figcaption></figure></div></div></section>'''
PAG = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BK Clothing | Criativos para Google Ads</title><meta name="robots" content="noindex,nofollow">{FONTES}
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html{{font-size:clamp(16px,min(1.1111vw,1.78vh),52px)}}
body{{background:#f3f0ea;color:#0b0b0b;font-family:"Archivo",sans-serif;font-size:1.0625rem;line-height:1.5}}
img,video{{display:block;max-width:100%}}
.w{{max-width:96rem;margin:0 auto;padding:0 clamp(1.25rem,4vw,4.5rem)}}
h1,h2{{font-weight:900;font-stretch:125%;text-transform:uppercase;line-height:.86;letter-spacing:-.025em}}
h1{{font-size:min(8rem,12.5vw)}}h2{{font-size:min(3.6rem,8vw)}}
.capa{{background:#dce8ef;padding:clamp(3.5rem,7vw,7rem) 0}}.capa p{{margin-top:1.8rem;font-size:1.3rem;max-width:48ch}}
section{{padding:clamp(3rem,6vw,6rem) 0;border-top:2px solid #0b0b0b}}
header{{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem 3rem;flex-wrap:wrap;margin-bottom:2rem}}
header p{{max-width:38ch;color:#4d4840}}
.tr{{display:grid;grid-template-columns:1.6fr 1fr .8fr;gap:.8rem;align-items:start}}
.tr.um{{grid-template-columns:minmax(0,26rem) 1fr;gap:3rem;align-items:center}}
figcaption{{margin-top:.6rem;font-size:.75rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#676157}}
ul{{list-style:none;border-top:2px solid #0b0b0b;max-width:60rem}}
li{{padding:1rem 0;border-bottom:1px solid rgba(11,11,11,.16);display:grid;grid-template-columns:14rem 1fr;gap:1.5rem}}
li b{{font-weight:600}}
@media (max-width:860px){{.tr,.tr.um{{grid-template-columns:1fr}}li{{grid-template-columns:1fr;gap:.2rem}}}}
</style></head><body>
<div class="capa"><div class="w"><h1>Criativos<br>para anúncio</h1><p>Quatro conceitos de anúncio para a BK Clothing no Google, cada um nos três formatos de imagem que a rede de display pede, e um deles também em movimento.</p></div></div>
{blocos}
<section><div class="w"><header><h2>Em movimento</h2><p>O primeiro conceito em vídeo de seis segundos, quadrado, para YouTube e Demand Gen.</p></header>
  <div class="tr um"><video src="1-bomber/animado.mp4" autoplay muted loop playsinline controls></video>
  <p style="max-width:40ch">A palavra entra, as três jaquetas caem uma a uma e o nome da loja fecha. O mesmo roteiro serve para qualquer peça-chave: troca a palavra, as peças e a cor de fundo.</p></div></div></section>
<section><div class="w"><header><h2>Antes de subir</h2></header><ul>
  <li><b>Marcas de terceiros</b><span>O Google reprova, e pode suspender a conta, quando o anúncio mostra marca registrada de outra empresa sem autorização. Estes exemplos usam peças com a marca pouco visível, mas cada peça anunciada precisa ser conferida com o Bruno antes.</span></li>
  <li><b>Para onde o anúncio leva</b><span>O Google exige uma página de destino funcionando. O site novo resolve isso; o catálogo atual, com links quebrados, tende a ser reprovado.</span></li>
  <li><b>Textos do anúncio</b><span>Títulos e descrições são escritos à parte no Google Ads. As imagens foram feitas com pouco texto de propósito, para o Google combinar com os títulos sem repetir.</span></li>
  <li><b>O que é exemplo</b><span>"Do P ao GG" e os dizeres de loja são ilustrativos e precisam bater com o que o Bruno pratica.</span></li>
</ul></div></section>
</body></html>'''
(AQUI / 'index.html').write_text(PAG, encoding='utf-8')
print('ok')
