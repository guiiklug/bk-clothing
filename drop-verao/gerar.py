"""Drop de verão da BK: posts, stories e artes do grupo VIP, organizados por marca.

Uso:  python gerar.py
Monta artes.html e exporta:
  feed/      18 posts 1080x1350: capa com o bordão, o verão, o grupo VIP e as fileiras de cada marca
             (Jordan com duas fileiras, depois Nike, Brooksfield e Tommy Hilfiger)
  stories/   7 stories 1080x1920
  whatsapp/  convite do grupo VIP (1080x1080) e aviso do drop para postar dentro do grupo (1080x1350)
  grade.jpg  como o feed fica no perfil; _conf-*.jpg para conferir
Sem preço. A abertura de cada marca leva uma frase; os outros posts mostram só a peça, com o nome pequeno.
Frases, peças e decisões ficam em base.py; os símbolos das marcas em marcas.py; as peças vêm de cut/ (recortar.py).
"""
import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import marcas
from base import A1, A2, S, K, W, LGI, BORDAO, VERAO, VIP, VANTAGENS, ORDEM, MARCAS, PECAS, RAZAO, tinta
from marcas import simb, fila

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
FR, CAPA = 104, 140       # tamanho das frases e do bordão da capa


def pc(n, w, x, y, rot=0, z=2):
    return f'<img class="ct" src="cut/{n}.png" style="width:{w}px;left:{x}px;top:{y}px;transform:translate(-50%,-50%) rotate({rot}deg);z-index:{z}">'


def uma(n, rot, cy=700, alt=800, larg=1000):
    """Uma peça só, no centro, o maior que cabe."""
    return pc(n, min(larg, int(alt * RAZAO[n])), 540, cy, rot)


def rot(t):
    return f'<span class="rt">{t}</span>'


def cab(direita='', cor=K, y=50, m=50):
    """Cabeçalho: logo da BK à esquerda e, à direita, o símbolo da marca da peça."""
    return f'<div class="cab" style="top:{y}px;left:{m}px;right:{m}px;color:{cor}"><span class="lg">{LGI}</span>{direita}</div>'


def fr(t, x, y, tam=FR, cor=K, larg=980):
    return f'<div class="fr" data-s="{tam}" data-w="{larg}" style="left:{x}px;top:{y}px;color:{cor}">{"<br>".join(t.split("|"))}</div>'


def leg(n, cor=K, m=50, b=46):
    _, nome, c = PECAS[n]
    return f'<div class="leg" style="left:{m}px;bottom:{b}px;color:{cor}"><b>{nome}</b><span>{c}</span></div>'


def et(t, cor=K, lado='right', m=50, b=50):
    return f'<span class="et" style="{lado}:{m}px;bottom:{b}px;color:{cor}">{t}</span>'


def tx(t, x, y, tam=46, cor=K):
    return f'<p class="tx" style="left:{x}px;top:{y}px;font-size:{tam}px;color:{cor}">{"<br>".join(t.split("|"))}</p>'


def lista(itens, y, cor=W, tam=40, x=50, larg=980):
    linhas = ''.join(f'<div><b>{k:02d}</b><span>{t}</span></div>' for k, t in enumerate(itens, 1))
    return f'<div class="ls" style="left:{x}px;top:{y}px;width:{larg}px;color:{cor};font-size:{tam}px">{linhas}</div>'


def faixa(t, y, alt=150, fundo=A1, cor=K, tam=88):
    return f'<div class="fx" style="top:{y}px;height:{alt}px;background:{fundo};color:{cor};font-size:{tam}px">{t}</div>'


def enquete(opcoes, y=1500, cor=K, m=56):
    """As opções em letra grande entre dois fios, sem caixa: o Guilherme não gostou da faixa preta que imitava a figurinha."""
    return (f'<div class="op" style="top:{y}px;left:{m}px;right:{m}px;color:{cor}"><small>Qual você leva?</small>'
            f'<div style="font-size:{72 if len(opcoes) < 3 else 60}px">{"".join(f"<span>{o}</span>" for o in opcoes)}</div></div>')


def quinteto(y1, y2, w, passo, cx=540):
    p = MARCAS['jordan'][2]
    return (pc(p[1], w, cx - passo, y1, -4, 2) + pc(p[0], w, cx, y1, 2, 3) + pc(p[2], w, cx + passo, y1, 4, 2)
            + pc(p[3], w, cx - passo / 2, y2, 3, 4) + pc(p[4], w, cx + passo / 2, y2, -3, 5))


def monte(dy=0):
    """A pilha da capa: as bermudas da Jordan na frente e uma peça de cada outra marca em volta."""
    return (pc('basquete-menta', 500, 250, 740 + dy, -11, 2) + pc('basquete-creme', 500, 840, 730 + dy, 10, 2)
            + pc('praia-azul', 500, 250, 1110 + dy, 7, 3) + pc('cargo-preta', 440, 850, 1120 + dy, -6, 3)
            + pc('listra-offwhite', 380, 560, 1150 + dy, 4, 4) + pc('basquete-preta', 620, 540, 850 + dy, -3, 5))


def indice(y0):
    """A hierarquia numa imagem: uma fileira por marca, a Jordan maior."""
    out, y = '', y0
    for m in ORDEM:
        grande = m == 'jordan'
        alt = 290 if grande else 200
        titulo, sub = MARCAS[m][1].split(' · ')
        out += f'<i class="div" style="top:{y}px"></i>'
        out += f'<span class="ab" style="left:50px;top:{y + (36 if grande else 24)}px">{simb(m, K, .86 if grande else .6)}</span>'
        out += f'<span class="in" style="left:50px;top:{y + (158 if grande else 100)}px"><b>{titulo}</b><span>{sub}</span></span>'
        larg, passo = (224, 116) if grande else (180, 190)
        for j, p in enumerate(MARCAS[m][2]):
            out += pc(p, larg, 350 + larg / 2 + j * passo, y + alt / 2, (-4, 3)[j % 2], 2 + j)
        y += alt
    return out + f'<i class="div" style="top:{y}px"></i>'


def abertura(marca, fundo, pecas, rodape=True):
    cor = tinta(fundo)
    return (cab(simb(marca, cor), cor) + fr(MARCAS[marca][0], 50, 196, cor=cor) + pecas
            + (et(MARCAS[marca][1], cor, 'left') + et('Drop de verão', cor) if rodape else ''))


def peca(n, fundo, giro):
    cor = tinta(fundo)
    return cab(simb(PECAS[n][0], cor), cor) + uma(n, giro) + leg(n, cor) + et('Drop de verão', cor)


ARR = {     # como as peças se arrumam na abertura de cada marca
    'jordan': quinteto(650, 1010, 420, 320),
    'nike': pc('cargo-preta', 700, 380, 740, -6, 2) + pc('vivo-preta', 700, 690, 990, 6, 3),
    'brooksfield': pc('praia-azul', 780, 410, 730, -8, 2) + pc('praia-agua', 700, 690, 960, 7, 3),
    'tommy': pc('listra-marinho', 540, 800, 650, 8, 2) + pc('listra-offwhite', 540, 290, 770, -7, 3) + pc('listra-preta', 620, 640, 1000, -2, 4),
}

FEED = [
    ('00-capa', S, cab(fila(K)) + fr(BORDAO, 50, 196, CAPA) + monte()),
    ('01-verao', W, cab(rot('Drop de verão')) + fr(VERAO, 50, 196) + indice(440)),
    ('02-vip', K, cab(rot('Grupo VIP'), W) + fr(VIP, 50, 196, cor=W) + lista(VANTAGENS, 450)
     + pc('basquete-gelo', 620, 740, 950, 7, 2) + faixa('Link na bio', 1200)),
    # Jordan: duas fileiras
    ('10-jordan', A2, abertura('jordan', A2, ARR['jordan'])),
    ('11-jordan-preta', S, peca('basquete-preta', S, -5)),
    ('12-jordan-menta', A1, peca('basquete-menta', A1, 5)),
    ('13-jordan-creme', A1, peca('basquete-creme', A1, -5)),
    ('14-jordan-gelo', K, peca('basquete-gelo', K, 5)),
    ('15-jordan-verde', S, peca('basquete-verde', S, -5)),
    # Nike
    ('20-nike', W, abertura('nike', W, ARR['nike'])),
    ('21-nike-cargo', S, peca('cargo-preta', S, 5)),
    ('22-nike-short', A2, peca('vivo-preta', A2, -5)),
    # Brooksfield
    ('30-brooksfield', S, abertura('brooksfield', S, ARR['brooksfield'])),
    ('31-brooksfield-azul', W, peca('praia-azul', W, -5)),
    ('32-brooksfield-agua', K, peca('praia-agua', K, 6)),
    # Tommy Hilfiger
    ('40-tommy', A2, abertura('tommy', A2, ARR['tommy'])),
    ('41-tommy-offwhite', K, peca('listra-offwhite', K, 5)),
    ('42-tommy-marinho', S, peca('listra-marinho', S, -5)),
]

ST = 56         # margem lateral dos stories; o cabeçalho começa em 230 para fugir da barra do Instagram


def abre_story(marca, fundo, pecas, frase=None):
    cor = tinta(fundo)
    return cab(simb(marca, cor), cor, 230, ST) + fr(frase or MARCAS[marca][0], ST, 384, cor=cor, larg=968) + pecas


STORIES = [
    ('1-capa', S, cab(fila(K), y=230, m=ST) + fr(BORDAO, ST, 384, 150, larg=968) + tx('Seu verão começa na BK.', 60, 676, 50) + monte(380)),
    ('2-jordan', A2, abre_story('jordan', A2, quinteto(870, 1240, 430, 320)) + tx('Qual você leva? Responda com a cor.', 60, 1500, 44)),
    ('3-jordan-novas', A1, abre_story('jordan', A1, pc('basquete-menta', 700, 400, 930, -6, 2) + pc('basquete-creme', 700, 680, 1290, 5, 3),
                                      'Duas cores novas.|Menta e creme.')),
    ('4-nike', W, abre_story('nike', W, pc('cargo-preta', 720, 400, 870, -6, 2) + pc('vivo-preta', 740, 660, 1170, 5, 3)) + enquete(['Cargo', 'Short'])),
    ('5-brooksfield', S, abre_story('brooksfield', S, pc('praia-azul', 800, 430, 880, -8, 2) + pc('praia-agua', 720, 670, 1150, 6, 3))
     + enquete(['Azul', 'Verde-água'])),
    ('6-tommy', A2, abre_story('tommy', A2, pc('listra-marinho', 560, 790, 820, 8, 2) + pc('listra-offwhite', 580, 310, 980, -7, 3)
                               + pc('listra-preta', 620, 640, 1200, -2, 4)) + enquete(['Off-white', 'Preto', 'Marinho'])),
    ('7-vip', K, cab(rot('Grupo VIP'), W, 230, ST) + fr(VIP, ST, 384, cor=W, larg=968) + lista(VANTAGENS, 650, tam=42, x=ST, larg=968)
     + pc('basquete-gelo', 620, 700, 1170, 7, 2) + tx('Toque no link e entre ↓', ST, 1500, 44, A1)),
]

ZAP = [
    ('convite-vip', K, 1080, 1080, cab(rot('Grupo VIP'), W) + fr(VIP, 50, 190, 96, W) + lista(VANTAGENS, 430, tam=38)
     + pc('basquete-gelo', 500, 800, 850, 7, 2) + et('Entre pelo link', A1, 'left')),
    ('drop-no-grupo', A1, 1080, 1350, cab(fila(K)) + fr('Chegou primeiro|no grupo VIP.', 50, 196) + monte()),
]

CSS = marcas.CSS + '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#777;display:flex;flex-wrap:wrap;gap:16px;padding:16px;font-family:"Archivo",sans-serif}
.arte{position:relative;overflow:hidden;flex:none;color:#0b0b0b}
.ct{position:absolute;height:auto;filter:drop-shadow(0 34px 38px rgba(0,0,0,.3))}
.cab{position:absolute;display:flex;justify-content:space-between;align-items:center;height:104px;z-index:9}
.rt,.et{font-weight:600;font-size:27px;letter-spacing:.14em;text-transform:uppercase}
.et{position:absolute;z-index:8}
.fr{position:absolute;font-family:"Big Shoulders Display","Archivo",sans-serif;font-weight:900;text-transform:uppercase;letter-spacing:0;line-height:1;white-space:nowrap;z-index:7}
.leg{position:absolute;display:flex;flex-direction:column;gap:6px;z-index:8}
.leg b{font-weight:600;font-size:40px}
.leg span{font-size:32px;opacity:.72}
.tx{position:absolute;font-weight:500;line-height:1.2;z-index:8}
.ls{position:absolute;z-index:8}
.ls div{display:flex;align-items:baseline;gap:30px;padding:24px 0;border-top:2px solid rgba(243,240,234,.3);font-weight:500}
.ls div:last-child{border-bottom:2px solid rgba(243,240,234,.3)}
.ls b{font-family:"Big Shoulders Display";font-weight:900;font-size:1.1em;width:1.5em;color:#dce8ef}
.fx{position:absolute;left:0;right:0;display:grid;place-items:center;font-family:"Big Shoulders Display";font-weight:900;text-transform:uppercase;letter-spacing:.01em;z-index:8}
.op{position:absolute;z-index:8}
.op small{display:block;font-weight:600;font-size:27px;letter-spacing:.14em;text-transform:uppercase;margin-bottom:18px}
.op div{display:flex;border-top:2px solid currentColor;border-bottom:2px solid currentColor}
.op span{flex:1;display:grid;place-items:center;height:124px;padding-top:4px;font-family:"Big Shoulders Display";font-weight:900;line-height:1;text-transform:uppercase}
.op span+span{border-left:2px solid currentColor}
.div{position:absolute;left:50px;right:50px;height:2px;background:#0b0b0b}
.ab{position:absolute}
.in{position:absolute;display:flex;flex-direction:column;gap:4px}
.in b{font-weight:600;font-size:31px}
.in span{font-size:26px;opacity:.7}
.lg{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:46px;flex:none}
.lg::before,.lg::after{content:"";position:absolute;top:0;bottom:0;width:32%;border:.045em solid currentColor}
.lg::before{left:0;border-right:0}.lg::after{right:0;border-left:0}
.lg b{font-family:"Jost";font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}
.lg i{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}
'''
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=Big+Shoulders+Display:wght@900'
          '&family=Bebas+Neue&family=Jost:wght@200&display=swap" rel="stylesheet">')
html = ''.join(f'<div class="arte" id="feed__{n}" style="width:1080px;height:1350px;background:{f}">{c}</div>' for n, f, c in FEED)
html += ''.join(f'<div class="arte" id="stories__{n}" style="width:1080px;height:1920px;background:{f}">{c}</div>' for n, f, c in STORIES)
html += ''.join(f'<div class="arte" id="whatsapp__{n}" style="width:{w}px;height:{h}px;background:{f}">{c}</div>' for n, f, w, h, c in ZAP)
(AQUI / 'artes.html').write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>{html}</body></html>', encoding='utf-8')

for d in ['feed', 'stories', 'whatsapp']:
    shutil.rmtree(AQUI / d, ignore_errors=True)     # nomes de arte mudam de uma versão para outra; não deixa sobra
    (AQUI / d).mkdir()
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 2600, 'height': 2000})
    pg.goto((AQUI / 'artes.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_function('[...document.images].every(i => i.complete && i.naturalWidth > 0)', timeout=60000)
    pg.wait_for_timeout(1500)
    # frase no tamanho pedido (data-s); só encolhe se passar da largura (data-w)
    pg.evaluate('''() => document.querySelectorAll('.fr').forEach(e => { const s = +e.dataset.s; e.style.fontSize = s + 'px';
        if (e.offsetWidth > +e.dataset.w) e.style.fontSize = Math.floor(s * e.dataset.w / e.offsetWidth) + 'px' })''')
    pg.wait_for_timeout(300)
    for el in pg.locator('.arte').all():
        pasta, nome = el.get_attribute('id').split('__')
        el.screenshot(path=str(AQUI / pasta / f'{nome}.jpg'), type='jpeg', quality=92)
    b.close()


def folha(arqs, alt, col, saida):
    ims = [Image.open(f).convert('RGB') for f in arqs]
    ims = [i.resize((round(i.width * alt / i.height), alt), Image.LANCZOS) for i in ims]
    linhas = [ims[k:k + col] for k in range(0, len(ims), col)]
    larg = max(sum(i.width + 6 for i in li) for li in linhas) + 6
    Sx = Image.new('RGB', (larg, len(linhas) * (alt + 6) + 6), '#666')
    for li, linha in enumerate(linhas):
        x = 6
        for i in linha:
            Sx.paste(i, (x, 6 + li * (alt + 6)))
            x += i.width + 6
    Sx.save(saida, quality=86)


folha([AQUI / 'feed' / f'{n}.jpg' for n, *_ in FEED], 600, 6, AQUI / '_conf-feed.jpg')
folha([AQUI / 'stories' / f'{n}.jpg' for n, *_ in STORIES] + [AQUI / 'whatsapp' / f'{n}.jpg' for n, *_ in ZAP], 640, 9, AQUI / '_conf-stories.jpg')

# como o feed aparece no perfil: três colunas, miniatura 3:4 cortada do post 4:5
G = Image.new('RGB', (3 * 360 + 8, (len(FEED) // 3) * 484 - 4), '#ffffff')
for k, (n, *_) in enumerate(FEED):
    im = Image.open(AQUI / 'feed' / f'{n}.jpg').convert('RGB')
    corte = (im.width - im.height * 3 // 4) // 2
    im = im.crop((corte, 0, im.width - corte, im.height)).resize((360, 480), Image.LANCZOS)
    G.paste(im, ((k % 3) * 364, (k // 3) * 484))
G.save(AQUI / 'grade.jpg', quality=90)
print('ok', len(FEED), 'posts,', len(STORIES), 'stories,', len(ZAP), 'artes do grupo')
