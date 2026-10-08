"""Criativos de exemplo para Google Ads da BK Clothing, versão 2 (sóbria): 4 conceitos x 3 formatos.

A versão 1 (palavra gigante, botão, etiqueta) foi rejeitada pelo Guilherme como brega e está em _v1-rejeitada/.
Aqui a regra é o contrário: uma peça ou uma foto, muito espaço vazio, letra pequena, sem botão.
Uso:  python gerar.py   ->  <conceito>/<formato>.jpg, 1-peca/animado.mp4, index.html
"""
import os
import shutil
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
CUT = '../site2/img/cut/'
OFF, AZ, K, W = '#f1eee8', '#e7edf1', '#0b0b0b', '#f3f0ea'
FORMATOS = {'paisagem': (1200, 628), 'quadrado': (1200, 1200), 'retrato': (960, 1200)}
LG = '<span class="lg"><b>BK</b><i>CLOTHING</i></span>'


def pc(i, w, cx, cy):
    return f'<img class="pc" src="{CUT}{i}.webp" style="width:{w}px;left:{cx}px;top:{cy}px">'


def moldura(cor, esq, dir_='bkclothing.com.br', logo=True):
    """logo pequeno em cima, uma linha em baixo à esquerda e o endereço do site à direita"""
    return ((f'<div class="lo" style="color:{cor}">{LG}</div>' if logo else '')
            + f'<div class="le" style="color:{cor}"><span>{esq}</span><span>{dir_}</span></div>')


def c1(f, w, h):          # uma peça, muito ar
    pw, cy = {'paisagem': (318, 318), 'quadrado': (600, 610), 'retrato': (560, 610)}[f]
    return f'<div class="ad" style="background:{OFF}">' + pc('1914786', pw, w / 2, cy) + moldura(K, 'Jaqueta bomber. Preta, marinho e bege.') + '</div>'


def c2(f, w, h):          # as três cores em fila
    pw, cy, passo = {'paisagem': (250, 312, 330), 'quadrado': (336, 600, 372), 'retrato': (276, 600, 296)}[f]
    nomes = ['Preta', 'Marinho', 'Bege']
    pecas = ''
    for k, i in enumerate(['1914784', '1914785', '1914786']):
        x = w / 2 + (k - 1) * passo
        pecas += pc(i, pw, x, cy) + f'<span class="nm" style="left:{x}px;top:{cy + pw * .52}px">{nomes[k]}</span>'
    return f'<div class="ad" style="background:{AZ}">' + pecas + moldura(K, 'Jaqueta bomber') + '</div>'


def c3(f, w, h):          # no corpo: foto real
    if f == 'paisagem':
        return (f'<div class="ad" style="background:{OFF}"><img class="ft" src="../site2/img/m1.webp" style="width:44%;object-position:50% 22%">'
                f'<div class="lo" style="color:{K};left:calc(44% + 44px)">{LG}</div>'
                f'<div class="le" style="color:{K};left:calc(44% + 44px)"><span>Polo oversized</span><span>bkclothing.com.br</span></div></div>')
    return (f'<div class="ad" style="background:{K}"><img class="ft" src="../site2/img/m1.webp" style="object-position:50% {18 if f == "quadrado" else 12}%">'
            '<i class="veu"></i>' + moldura(W, 'Polo oversized') + '</div>')


def c4(f, w, h):          # a loja
    pos = {'paisagem': '60% 46%', 'quadrado': '50% 50%', 'retrato': '66% 50%'}[f]
    return (f'<div class="ad" style="background:{K}"><img class="ft" src="../site2/img/loja.webp" style="object-position:{pos}"><i class="veu"></i>'
            + moldura(W, 'Rua Santa Catarina, 2348 · Floresta · Joinville', 'Provador na loja', logo=False) + '</div>')


CONCEITOS = [('1-peca', c1, 'Uma peça', 'A peça sozinha no centro, com espaço de sobra em volta. É o anúncio de produto.'),
             ('2-cores', c2, 'As cores', 'A mesma jaqueta nas três cores, lado a lado, com o nome de cada uma.'),
             ('3-corpo', c3, 'No corpo', 'Foto real de alguém vestindo. Sem texto em cima do modelo.'),
             ('4-loja', c4, 'A loja', 'A parede da loja com o letreiro, só com o endereço. Para anúncio local em Joinville.')]

CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#999;display:flex;flex-wrap:wrap;gap:16px;padding:16px;font-family:"Jost",sans-serif}
.ad{position:relative;overflow:hidden;flex:none;color:#0b0b0b}
.pc{position:absolute;height:auto;transform:translate(-50%,-50%);filter:drop-shadow(0 22px 22px rgba(30,25,15,.16))}
.ft{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,11,.34) 0,rgba(11,11,11,0) 22%,rgba(11,11,11,0) 70%,rgba(11,11,11,.55) 100%)}
.lg{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:33px}
.lg::before,.lg::after{content:"";position:absolute;top:0;bottom:0;width:32%;border:.045em solid currentColor}
.lg::before{left:0;border-right:0}.lg::after{right:0;border-left:0}
.lg b{font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}
.lg i{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}
.lo{position:absolute;left:44px;top:38px;z-index:3}
.le{position:absolute;left:44px;right:44px;bottom:38px;display:flex;justify-content:space-between;align-items:baseline;gap:24px;z-index:3;font-size:25px;font-weight:400;letter-spacing:.01em}
.le span:last-child{font-size:19px;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}
.nm{position:absolute;transform:translateX(-50%);font-size:19px;letter-spacing:.14em;text-transform:uppercase}
'''
FONTES = '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Jost:wght@200;300;400;500&display=swap" rel="stylesheet">'
CAB = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>'

artes = ''
for slug, fn, _, _ in CONCEITOS:
    (AQUI / slug).mkdir(exist_ok=True)
    for f, (w, h) in FORMATOS.items():
        artes += fn(f, w, h).replace('<div class="ad" style="', f'<div class="ad" id="{slug}__{f}" style="width:{w}px;height:{h}px;', 1)
(AQUI / 'artes.html').write_text(CAB + artes + '</body></html>', encoding='utf-8')

# versão em movimento do conceito 1: aproximação lenta, a linha de texto entra, fecha na logo
ANIM = CAB.replace('body{background:#999;display:flex;flex-wrap:wrap;gap:16px;padding:16px;', 'body{background:#f1eee8;overflow:hidden;') + f'''
<div class="ad" id="p" style="width:1080px;height:1080px;background:{OFF}">
  <img class="pc" id="j" src="{CUT}1914786.webp" style="width:560px;left:540px;top:548px">
  <div class="lo" id="lo">{LG}</div><div class="le" id="le"><span>Jaqueta bomber. Preta, marinho e bege.</span><span>bkclothing.com.br</span></div>
  <div id="fim" style="position:absolute;inset:0;background:{OFF};display:grid;place-items:center;opacity:0;z-index:5"><span class="lg" style="font-size:118px">{LG[17:-7]}</span></div>
</div><script>
const $=s=>document.querySelector(s),su=x=>{{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)}};
window.render=async t=>{{
  $('#j').style.opacity=su(t/.8);$('#j').style.transform=`translate(-50%,-50%) scale(${{1+.07*t/6}})`;
  $('#lo').style.opacity=su((t-.5)/.7);$('#le').style.opacity=su((t-1.1)/.8);
  $('#fim').style.opacity=su((t-4.7)/.6);
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));}};
</script></body></html>'''
(AQUI / 'anim.html').write_text(ANIM, encoding='utf-8')

qd = AQUI / '_quadros'
shutil.rmtree(qd, ignore_errors=True)
qd.mkdir()
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 2600, 'height': 2000})
    pg.goto((AQUI / 'artes.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(1800)
    for el in pg.locator('.ad').all():
        slug, f = el.get_attribute('id').split('__')
        el.screenshot(path=str(AQUI / slug / f'{f}.jpg'), type='jpeg', quality=92)
    pa = b.new_page(viewport={'width': 1080, 'height': 1080})
    pa.goto((AQUI / 'anim.html').as_uri())
    pa.evaluate('document.fonts.ready')
    pa.wait_for_timeout(1200)
    for f in range(180):
        pa.evaluate('t => window.render(t)', f / 30)
        pa.screenshot(path=str(qd / f'{f:04d}.jpg'), type='jpeg', quality=93)
    b.close()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', str(qd / '%04d.jpg'), '-c:v', 'libx264', '-crf', '18',
                '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(AQUI / '1-peca' / 'animado.mp4')], check=True)
tira = Image.new('RGB', (4 * 300, 300))
for n, i in enumerate([8, 45, 120, 175]):
    tira.paste(Image.open(qd / f'{i:04d}.jpg').resize((300, 300)), (n * 300, 0))
tira.save(AQUI / '_conf-anim.jpg', quality=85)
shutil.rmtree(qd, ignore_errors=True)

# folha de conferência
S_ = Image.new('RGB', (4 * 620, 334 + 560 + 620), '#888')
for i, (slug, *_r) in enumerate(CONCEITOS):
    y = 0
    for f in ('paisagem', 'quadrado', 'retrato'):
        im = Image.open(AQUI / slug / f'{f}.jpg')
        larg = {'paisagem': 600, 'quadrado': 540, 'retrato': 480}[f]
        im = im.resize((larg, round(im.height * larg / im.width)))
        S_.paste(im, (i * 620 + 10, y + 10))
        y += im.height + 10
S_.save(AQUI / '_conf.jpg', quality=86)

# página de apresentação
blocos = ''
for slug, _fn, nome, desc in CONCEITOS:
    blocos += f'''<section><div class="w"><header><h2>{nome}</h2><p>{desc}</p></header>
  <div class="tr"><figure><img src="{slug}/paisagem.jpg" alt=""><figcaption>Paisagem · 1200 x 628</figcaption></figure>
  <figure><img src="{slug}/quadrado.jpg" alt=""><figcaption>Quadrado · 1200 x 1200</figcaption></figure>
  <figure><img src="{slug}/retrato.jpg" alt=""><figcaption>Retrato · 960 x 1200</figcaption></figure></div></div></section>'''
PAG = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BK Clothing | Criativos para Google Ads</title><meta name="robots" content="noindex,nofollow">{FONTES}
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html{{font-size:clamp(16px,min(1.1111vw,1.78vh),52px)}}
body{{background:#fbfaf7;color:#0b0b0b;font-family:"Jost",sans-serif;font-weight:400;font-size:1.1rem;line-height:1.5}}
img,video{{display:block;max-width:100%}}
.w{{max-width:92rem;margin:0 auto;padding:0 clamp(1.25rem,4vw,4.5rem)}}
h1,h2{{font-weight:300;line-height:1;letter-spacing:-.01em}}
h1{{font-size:min(5.5rem,11vw)}}h2{{font-size:min(2.6rem,7vw)}}
.capa{{padding:clamp(3.5rem,7vw,7rem) 0 clamp(2rem,4vw,4rem)}}.capa p{{margin-top:1.6rem;font-size:1.3rem;max-width:46ch;color:#4d4840}}
section{{padding:clamp(2.5rem,5vw,5rem) 0;border-top:1px solid rgba(11,11,11,.2)}}
header{{display:flex;justify-content:space-between;align-items:baseline;gap:1rem 3rem;flex-wrap:wrap;margin-bottom:1.8rem}}
header p{{max-width:40ch;color:#4d4840}}
.tr{{display:grid;grid-template-columns:1.6fr 1fr .8fr;gap:.8rem;align-items:start}}
.tr img,.tr video{{border:1px solid rgba(11,11,11,.1)}}
.tr.um{{grid-template-columns:minmax(0,24rem) 1fr;gap:3rem;align-items:center}}
figcaption{{margin-top:.6rem;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:#676157}}
ul{{list-style:none;border-top:1px solid #0b0b0b;max-width:60rem}}
li{{padding:1rem 0;border-bottom:1px solid rgba(11,11,11,.16);display:grid;grid-template-columns:14rem 1fr;gap:1.5rem}}
li b{{font-weight:500}}
@media (max-width:860px){{.tr,.tr.um{{grid-template-columns:1fr}}li{{grid-template-columns:1fr;gap:.2rem}}}}
</style></head><body>
<div class="capa"><div class="w"><h1>Criativos para anúncio</h1><p>Quatro conceitos de anúncio para a BK Clothing no Google, nos três formatos de imagem que a rede de display pede. A regra é uma só: a peça ou a foto fala, o texto fica pequeno.</p></div></div>
{blocos}
<section><div class="w"><header><h2>Em movimento</h2><p>O primeiro conceito em vídeo de seis segundos, quadrado, sem som.</p></header>
  <div class="tr um"><video src="1-peca/animado.mp4" autoplay muted loop playsinline controls></video>
  <p style="max-width:40ch;color:#4d4840">A peça aparece, a câmera se aproxima devagar, a linha de texto entra e o vídeo fecha na logo. Serve para qualquer peça: troca a foto e a linha.</p></div></div></section>
<section><div class="w"><header><h2>Antes de subir</h2></header><ul>
  <li><b>Marcas de terceiros</b><span>O Google reprova, e pode suspender a conta, quando o anúncio mostra marca registrada de outra empresa sem autorização. Cada peça anunciada precisa ser conferida com o Bruno antes.</span></li>
  <li><b>Para onde o anúncio leva</b><span>O Google exige uma página de destino funcionando. O site novo resolve isso.</span></li>
  <li><b>Textos e botão</b><span>Título, descrição e botão são montados pelo próprio Google Ads em volta da imagem. Por isso a imagem não leva botão nem frase de venda.</span></li>
</ul></div></section>
</body></html>'''
(AQUI / 'index.html').write_text(PAG, encoding='utf-8')
print('ok')
