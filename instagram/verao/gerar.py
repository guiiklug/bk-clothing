"""Segunda identidade do Instagram da BK: Verão 27, blocos de cor, peça recortada por cima da letra.

Uso:  python recortar.py   (uma vez, recorta as peças)
      python gerar.py      (monta artes.html, exporta JPGs, gera index.html e o mock do perfil)
Para trocar peça, cor ou palavra, edite as listas abaixo e rode de novo. Custo zero.
"""
import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
# paleta pedida pelo Bruno em 07/10/2026: azul esbranquiçado em dois tons, sem vermelho nem azul forte
# (R e B ficaram como nomes das duas casas de cor; R é o azul um tom acima, B o mais claro)
R, B, S, K, W = '#c5d6e1', '#dce8ef', '#e6dfd0', '#0b0b0b', '#f3f0ea'
LG = '<span class="lg"><b>BK</b><i>CLOTHING</i></span>'


def pc(nome, w, x, y, rot=0):
    """peça recortada: largura e centro em px, rotação em graus"""
    return (f'<img class="ct" src="cut/{nome}.png" style="width:{w}px;left:{x}px;top:{y}px;'
            f'transform:translate(-50%,-50%) rotate({rot}deg)">')


def wd(txt, tam, x, y, cor=K, rot=0):
    linhas = '<br>'.join(txt.split('|'))
    return f'<div class="wd" style="font-size:{tam}px;left:{x}px;top:{y}px;color:{cor};transform:rotate({rot}deg)">{linhas}</div>'


def pano(i):
    """fatia i (0 a 2) da palavra VERÃO que atravessa a linha inteira"""
    return (f'<svg class="pano" viewBox="{1080 * i} 0 1080 1350"><text x="40" y="985" textLength="3160" '
            f'lengthAdjust="spacingAndGlyphs" font-size="800">VERÃO</text></svg>')


def foto(src, pos='50% 20%'):
    return f'<img class="ft" src="{src}" style="object-position:{pos}">'


IMG = '../../_coleta/img/'
# (nome, fundo, conteúdo). Ordem: da publicação mais recente para a mais antiga, linha a linha.
POSTS = [
    ('01-verao-1', R, pano(0) + pc('jeans', 800, 600, 700, -10)),
    ('02-verao-2', W, pano(1) + pc('tee-diesel', 930, 540, 690, 5)),
    ('03-verao-3', B, pano(2) + pc('pochete', 900, 500, 720, -9)),
    ('04-video-tee', K, foto('raw/q-tee.png', '50% 44%')),
    ('05-detalhe-tee', K, pc('tee-diesel', 3300, 540, 700, 0)),
    ('06-nova', S, wd('Nova|cole|ção', 266, 54, 70)),
    ('07-cargo', S, wd('Cargo', 212, 50, 54) + pc('cargo-marrom', 1020, 560, 780, -12)),
    ('08-cargo-off', K, pc('cargo-off', 960, 540, 690, 9)),
    ('09-jeans', B, wd('Jeans', 218, 50, 54) + pc('jeans', 900, 560, 800, 7)),
    ('10-no-corpo-1', K, foto(IMG + '1914792_1.jpg', '50% 25%')),
    ('11-polo', R, pc('polo-roads', 1060, 540, 690, -6)),
    ('12-no-corpo-2', K, foto(IMG + '1914792_2.jpg', '50% 40%')),
    ('13-regata', K, wd('Rega|ta', 268, 50, 54, W) + pc('regata', 640, 600, 760, 8)),
    ('14-video-conjunto', K, foto('raw/q-conjunto.png', '50% 46%')),
    ('15-bag', S, pc('bag', 620, 540, 690, -9)),
    ('16-pochete', R, pc('pochete', 980, 540, 690, 12)),
    ('17-logo', W, f'<div class="centro" style="color:{K}">{LG}</div>'),
    ('18-conjunto', B, pc('conjunto-branco', 690, 540, 690, -6)),
]
CAPAS = [
    ('novo', R, pc('tee-diesel', 900, 540, 560, 5)),
    ('quem-usa', K, foto(IMG + '1914792_1.jpg', '50% 22%')),
    ('tamanhos', B, wd('P M G', 250, 110, 430)),
    ('envio', S, pc('bag', 470, 540, 540, -9)),
    ('loja', K, foto('../../site/img/loja.webp', '70% 45%')),
    ('vip', K, wd('VIP', 330, 190, 400, W)),
]
STORIES = [
    ('1-chegou', R, wd('Che|gou', 330, 56, 250) + pc('tee-diesel', 860, 560, 1060, 7)
     + f'<p class="pe" style="color:{K}">Responda QUERO e a gente separa a sua</p>'),
    ('2-enquete', W, wd('Qual|leva?', 212, 60, 250) + pc('cargo-marrom', 520, 250, 1030, -10) + pc('jeans', 470, 560, 1000, 4)
     + pc('bermuda-high', 520, 840, 1040, 9) + '<div class="adesivo"><span>Cargo</span><span>Jeans</span><span>Preta</span></div>'),
    ('3-ainda-tem', B, wd('Ainda|tem', 214, 60, 250) + pc('conjunto-preto', 620, 600, 1010, -5)
     + '<div class="grade"><span>P</span><span class="x">M</span><span>G</span><span>GG</span></div>'),
    ('4-quem-usa', K, foto(IMG + '1914792_1.jpg', '50% 30%') + '<div class="veu"></div>' + wd('Quem|usa|BK', 236, 60, 250, W)
     + f'<p class="pe" style="color:{W}">Marque @bkclothiing na sua foto e apareça aqui</p>'),
]

CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#777;font-family:"Jost",sans-serif;display:flex;flex-wrap:wrap;gap:20px;padding:20px}
.arte{position:relative;overflow:hidden;flex:none}
.post{width:1080px;height:1350px}.capa{width:1080px;height:1080px}.story{width:1080px;height:1920px}
.ft{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ct{position:absolute;height:auto;filter:drop-shadow(0 34px 38px rgba(0,0,0,.3));z-index:2}
.wd,.pano text{font-family:"Archivo",sans-serif;font-weight:900;font-stretch:125%;text-transform:uppercase;letter-spacing:-.025em}
.wd{position:absolute;line-height:.82;white-space:nowrap;transform-origin:0 0;z-index:1}
.pano{position:absolute;inset:0;width:100%;height:100%;z-index:1}.pano text{fill:#0b0b0b;letter-spacing:0}
.lg{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:250px}
.lg::before,.lg::after{content:"";position:absolute;top:0;bottom:0;width:32%;border:.045em solid currentColor}
.lg::before{left:0;border-right:0}.lg::after{right:0;border-left:0}
.lg b{font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}
.lg i{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}
.centro{position:absolute;inset:0;display:grid;place-items:center}
.pe{position:absolute;left:60px;right:60px;bottom:370px;font-size:46px;font-weight:500;line-height:1.25;max-width:20ch;z-index:3}
.veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,11,.6) 0,rgba(11,11,11,0) 38%,rgba(11,11,11,0) 60%,rgba(11,11,11,.8) 100%);z-index:1}
.adesivo{position:absolute;top:1370px;left:120px;right:120px;background:#0b0b0b;color:#f3f0ea;border-radius:28px;display:grid;grid-template-columns:repeat(3,1fr);overflow:hidden;font-size:42px;font-weight:500;text-align:center;z-index:3}
.adesivo span{padding:46px 0}.adesivo span+span{border-left:2px solid #444}
.grade{position:absolute;left:60px;bottom:380px;display:flex;gap:14px;z-index:3}
.grade span{width:160px;height:160px;background:#0b0b0b;color:#f3f0ea;display:grid;place-items:center;font-family:"Archivo";font-weight:800;font-stretch:125%;font-size:60px}
.grade .x{background:transparent;color:#0b0b0b;border:4px solid #0b0b0b;opacity:.45;text-decoration:line-through}
'''
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Bebas+Neue'
          '&family=Jost:wght@200;300;400;500&display=swap" rel="stylesheet">')

for d in ['feed', 'destaques', 'stories']:
    shutil.rmtree(AQUI / d, ignore_errors=True)
for d in ['feed', 'destaques', 'stories', 'apresentacao', 'videos']:
    (AQUI / d).mkdir(exist_ok=True)

artes = ''.join(f'<div class="arte post" id="p-{n}" style="background:{f}">{c}</div>' for n, f, c in POSTS)
artes += ''.join(f'<div class="arte capa" id="c-{n}" style="background:{f}">{c}</div>' for n, f, c in CAPAS)
artes += ''.join(f'<div class="arte story" id="s-{n}" style="background:{f}">{c}</div>' for n, f, c in STORIES)
(AQUI / 'artes.html').write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>{artes}</body></html>', encoding='utf-8')

# página de apresentação desta identidade
nomes = [p[0] for p in POSTS]
celulas = ''.join(
    (f'<video src="videos/{n.split("video-")[1]}.mp4" poster="feed/{n}.jpg" autoplay muted loop playsinline></video>' if 'video-' in n
     else f'<img src="feed/{n}.jpg" alt="">') for n in nomes)
rot = ['Novidades', 'Quem usa', 'Tamanhos', 'Envio', 'Loja', 'Grupo VIP']
dst = ''.join(f'<div><img src="destaques/{c[0]}.jpg" alt="">{r}</div>' for c, r in zip(CAPAS, rot))
PAG = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BK Clothing | Verão 27, segunda identidade</title><meta name="robots" content="noindex,nofollow">{FONTES}
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html{{font-size:clamp(16px,min(1.1111vw,1.78vh),52px)}}
body{{background:#f3f0ea;color:#0b0b0b;font-family:"Jost",sans-serif;font-weight:400;font-size:1.0625rem;line-height:1.55}}
img,video{{display:block;max-width:100%}}
.w{{max-width:84rem;margin:0 auto;padding:0 clamp(1.25rem,4vw,4rem)}}
h1,h2,h3{{font-family:"Archivo";font-weight:900;font-stretch:125%;text-transform:uppercase;line-height:.84;letter-spacing:-.025em}}
h1{{font-size:min(12rem,17vw)}}h2{{font-size:min(5.2rem,10vw);margin-bottom:1.5rem}}h3{{font-size:1.15rem;letter-spacing:0;line-height:1.1;margin-bottom:.35rem}}
p{{max-width:58ch}}.lead{{font-size:1.3rem;max-width:50ch}}
header{{background:{R};padding:clamp(3rem,7vw,7rem) 0}}header .lead{{margin-top:2rem}}
section{{padding:clamp(3.5rem,7vw,7rem) 0;border-top:3px solid #0b0b0b}}
.duas{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(2rem,5vw,6rem);align-items:start}}
.cores{{display:grid;grid-template-columns:repeat(5,1fr);margin-top:2rem;border:3px solid #0b0b0b}}
.cores div{{padding:3.2rem 1rem 1rem;font-size:.85rem;font-weight:500}}
.fone{{width:100%;max-width:27rem;background:#0c1014;color:#f5f5f5;font-family:system-ui,"Segoe UI",sans-serif;line-height:1.35}}
.fone .top{{padding:1rem 1rem .25rem;font-weight:700;font-size:1.15rem}}
.fone .cab{{display:grid;grid-template-columns:5.2rem 1fr;gap:1rem;align-items:center;padding:.75rem 1rem}}
.fone .av{{width:5.2rem;height:5.2rem;border-radius:50%;background:#fff;color:#0b0b0b;display:grid;place-items:center}}
.lg{{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:1.25rem}}
.lg::before,.lg::after{{content:"";position:absolute;top:0;bottom:0;width:32%;border:.05em solid currentColor}}
.lg::before{{left:0;border-right:0}}.lg::after{{right:0;border-left:0}}
.lg b{{font-family:"Jost";font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}}
.lg i{{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}}
.fone .nums{{display:grid;grid-template-columns:repeat(3,1fr);font-size:.82rem}}.fone .nums b{{display:block;font-size:1.05rem}}
.fone .bio{{padding:0 1rem .75rem;font-size:.86rem}}.fone .bio b{{display:block}}.fone .bio a{{color:#85a1ff;font-weight:600}}
.fone .bts{{display:grid;grid-template-columns:1fr 1fr;gap:.4rem;padding:0 1rem .9rem}}
.fone .bts span{{border-radius:.5rem;padding:.45rem;text-align:center;font-weight:600;font-size:.84rem;background:#25292e}}.fone .bts span:first-child{{background:#4a5df9}}
.fone .dst{{display:flex;gap:.85rem;padding:.25rem 1rem 1rem;overflow:hidden}}
.fone .dst div{{flex:none;width:4.1rem;text-align:center;font-size:.66rem;white-space:nowrap}}
.fone .dst img{{width:3.7rem;height:3.7rem;border-radius:50%;margin:0 auto .3rem;border:2px solid #333;padding:2px;object-fit:cover}}
.fone .abas{{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid #262626;text-align:center;font-size:.8rem;color:#888}}
.fone .abas span{{padding:.6rem 0}}.fone .abas span:first-child{{color:#fff;box-shadow:inset 0 -1px 0 #fff}}
.fone .gr{{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}}
.fone .gr img,.fone .gr video{{width:100%;aspect-ratio:4/5;object-fit:cover}}
.par{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,5rem);justify-items:center;align-items:start;margin-top:2.5rem}}
.par figure{{width:100%;max-width:27rem;min-width:0}}.par figcaption{{margin-top:.8rem;font-size:.85rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase}}
.fila{{display:grid;gap:.75rem;margin-top:2rem}}.c2{{grid-template-columns:repeat(2,1fr);max-width:40rem}}.c4{{grid-template-columns:repeat(4,1fr)}}.c6{{grid-template-columns:repeat(6,1fr)}}
.fila video{{width:100%;aspect-ratio:9/16;object-fit:cover;background:#111}}.fila figcaption{{margin-top:.7rem;font-size:.95rem}}
.capas img{{border-radius:50%}}
.nota{{font-size:.95rem;max-width:70ch;color:#4d4840}}
@media (max-width:860px){{.duas,.par{{grid-template-columns:1fr}}.c4{{grid-template-columns:repeat(2,1fr)}}.c6{{grid-template-columns:repeat(3,1fr)}}.cores{{grid-template-columns:repeat(2,1fr)}}}}
</style></head><body>
<header><div class="w"><h1>Verão<br>27</h1><p class="lead">A mesma loja, outra identidade. Bloco de cor clara, peça recortada por cima da letra e uma tipografia larga e pesada. Feita para a coleção de calor: camisetas, bermudas, regata e acessórios.</p></div></header>
<section><div class="w"><div class="duas">
  <div><h2>O que muda</h2><p class="lead">A identidade de inverno é calma: tons neutros, letra alta e estreita, peça em close. Esta é mais solta: cor chapada clara, peça jogada em diagonal com sombra, palavra enorme atrás.</p></div>
  <div><h3>As cores</h3><p>Um azul esbranquiçado em dois tons, como o Bruno pediu, mais areia clara. Preto e off-white seguram o resto. A primeira versão usava vermelho e azul forte e saiu por não ser a cara da marca.</p>
  <div class="cores"><div style="background:{R}">Azul</div><div style="background:{B}">Azul claro</div><div style="background:{S}">Areia</div><div style="background:{K};color:{W}">Preto</div><div style="background:{W}">Off-white</div></div></div>
</div></div></section>
<section><div class="w"><h2>O perfil</h2><p class="lead">A linha do topo é uma palavra só, VERÃO, atravessando os três posts, com uma peça por cima de cada pedaço. Os dois vídeos entram no meio da grade.</p>
  <div class="par">
    <figure><div class="fone" id="perfil">
      <div class="top">bkclothiing</div>
      <div class="cab"><div class="av">{LG}</div><div class="nums"><span><b>444</b>posts</span><span><b>1.428</b>seguidores</span><span><b>1.226</b>seguindo</span></div></div>
      <div class="bio"><b>BK CLOTHING</b>Moda masculina · Joinville<br>Jaquetas, oversized, bermudas e acessórios<br>Loja: Rua Santa Catarina, 2348 · Floresta<br>Enviamos para todo o Brasil<br><a>bkclothing.com.br/links</a></div>
      <div class="bts"><span>Seguir</span><span>Enviar mensagem</span></div>
      <div class="dst">{dst}</div>
      <div class="abas"><span>Posts</span><span>Reels</span><span>Marcados</span></div>
      <div class="gr">{celulas}</div>
    </div><figcaption>Verão 27</figcaption></figure>
    <figure><img src="../apresentacao/perfil-proposta.jpg" alt=""><figcaption>Inverno 26, a identidade anterior</figcaption></figure>
  </div></div></section>
<section><div class="w"><h2>Os vídeos</h2><p class="lead">Dois vídeos de cinco segundos, verticais, cada peça girando sobre um fundo da paleta.</p>
  <div class="fila c2">
    <figure><video src="videos/tee.mp4" poster="feed/04-video-tee.jpg" autoplay muted loop playsinline controls></video><figcaption>Camiseta preta sobre o azul claro.</figcaption></figure>
    <figure><video src="videos/conjunto.mp4" poster="feed/14-video-conjunto.jpg" autoplay muted loop playsinline controls></video><figcaption>Conjunto sobre o azul claro.</figcaption></figure>
  </div></div></section>
<section><div class="w"><h2>Stories e destaques</h2>
  <div class="fila c4">{''.join(f'<figure><img src="stories/{s[0]}.jpg" alt=""></figure>' for s in STORIES)}</div>
  <div class="fila c6 capas" style="margin-top:3rem">{''.join(f'<figure><img src="destaques/{c[0]}.jpg" alt=""><figcaption>{r}</figcaption></figure>' for c, r in zip(CAPAS, rot))}</div>
</div></section>
<section><div class="w"><p class="nota">As peças foram recortadas das fotos padronizadas já feitas para o site, por código, sem gerar imagem nova. As duas fotos com modelo são da própria loja. Os dois vídeos foram gerados a partir das fotos das peças e mostram a ideia: o definitivo é filmar a peça real sobre um fundo de papel na cor da paleta. O fundo dos vídeos foi trocado por código, quadro a quadro. Tamanhos e o "M" riscado são ilustrativos.</p></div></section>
</body></html>'''
(AQUI / 'index.html').write_text(PAG, encoding='utf-8')

DEST = {'p': 'feed', 'c': 'destaques', 's': 'stories'}
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 2400, 'height': 2000})
    pg.goto((AQUI / 'artes.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(2000)
    for el in pg.locator('.arte').all():
        pre, nome = el.get_attribute('id').split('-', 1)
        el.screenshot(path=str(AQUI / DEST[pre] / f'{nome}.jpg'), type='jpeg', quality=90)
    pg2 = b.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=2)
    pg2.goto((AQUI / 'index.html').as_uri())
    pg2.evaluate('document.fonts.ready')
    pg2.wait_for_timeout(2000)
    pg2.locator('#perfil').screenshot(path=str(AQUI / 'apresentacao' / 'perfil-verao.jpg'), type='jpeg', quality=90)
    pm = b.new_page(viewport={'width': 375, 'height': 800})
    pm.goto((AQUI / 'index.html').as_uri())
    pm.wait_for_timeout(600)
    print('celular', pm.evaluate('document.documentElement.scrollWidth'))
    b.close()


def folha(arqs, saida, cols, w, h):
    lin = (len(arqs) + cols - 1) // cols
    Sx = Image.new('RGB', (cols * w + (cols + 1) * 6, lin * h + (lin + 1) * 6), '#555')
    for n, f in enumerate(arqs):
        Sx.paste(Image.open(f).convert('RGB').resize((w, h), Image.LANCZOS), (6 + (n % cols) * (w + 6), 6 + (n // cols) * (h + 6)))
    Sx.save(saida, quality=85)


folha([AQUI / 'feed' / f'{n}.jpg' for n in nomes], AQUI / 'apresentacao' / '_conf-feed.jpg', 3, 360, 450)
folha([AQUI / 'stories' / f'{s[0]}.jpg' for s in STORIES] , AQUI / 'apresentacao' / '_conf-stories.jpg', 4, 270, 480)
folha([AQUI / 'destaques' / f'{c[0]}.jpg' for c in CAPAS], AQUI / 'apresentacao' / '_conf-capas.jpg', 6, 220, 220)
print('ok')
