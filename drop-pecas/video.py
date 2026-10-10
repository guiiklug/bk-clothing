"""Três vídeos verticais (1080x1920) por código, quadro a quadro, com corte no tempo do beat (140 BPM).

Uso:  python video.py                     (os três)
      python video.py grupo               (só um: grupo, basicas, conjuntos-bermudas)
      python video.py --roteiro grupo     (um quadro por cena, para conferir antes de gravar)
Saída em videos/:
  grupo.mp4               convite para o grupo VIP com as melhores peças (drop de verão, site e peças novas)
  basicas.mp4             as peças básicas, tratadas (sem modelo): camiseta básica, camiseta texturizada, polo e camisa
  conjuntos-bermudas.mp4  os conjuntos e as bermudas
Mesma linguagem do drop de verão (drop-verao/base.py): frase normal, logo da BK, marca da peça, peça grande e nome pequeno.
Conjuntos e bermudas foram recortados direto da foto, sem crédito; as básicas passaram pelo Higgsfield (9,75 créditos),
porque o Guilherme não quis foto com modelo. As peças do site e as do drop de verão já existiam.
O começo de cada vídeo é mais lento de propósito: ele pediu tempo para a pessoa ler antes de os cortes acelerarem.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(RAIZ / 'drop-verao'))
import marcas  # noqa: E402  (símbolos das marcas, pasta drop-verao/marcas)

os.chdir(AQUI)
SAIDA = AQUI / 'videos'
SAIDA.mkdir(exist_ok=True)
FPS, BPM = 30, 140
M = 56
A1, A2, S, K, W = '#dce8ef', '#c5d6e1', '#e6dfd0', '#0b0b0b', '#f3f0ea'
LGI = '<b>BK</b><i>CLOTHING</i>'
V, ST, C = '../drop-verao/cut/', '../site2/img/cut/', 'cut/'

# chave -> (arquivo, marca, nome, cor, fundo da cena). Marca com símbolo: jordan, nike, tommy, brooksfield; as outras vão escritas.
PECAS = {
    # drop de verão
    'j-preta': (V + 'basquete-preta.png', 'jordan', 'Bermuda Jordan', 'Preta com azul-claro', S),
    'j-menta': (V + 'basquete-menta.png', 'jordan', 'Bermuda Jordan', 'Preta com verde-menta', A1),
    'j-creme': (V + 'basquete-creme.png', 'jordan', 'Bermuda Jordan', 'Creme com preto', A2),
    'j-gelo': (V + 'basquete-gelo.png', 'jordan', 'Bermuda Jordan', 'Gelo com branco', K),
    'j-verde': (V + 'basquete-verde.png', 'jordan', 'Bermuda Jordan', 'Verde com off-white', S),
    'n-cargo': (V + 'cargo-preta.png', 'nike', 'Bermuda cargo Nike', 'Preta, com bolso de fivela', S),
    'n-short': (V + 'vivo-preta.png', 'nike', 'Short Nike', 'Preto com vivo branco', A2),
    'b-azul': (V + 'praia-azul.png', 'brooksfield', 'Short de praia Brooksfield', 'Azul', W),
    'b-agua': (V + 'praia-agua.png', 'brooksfield', 'Short de praia Brooksfield', 'Verde-água', K),
    't-offwhite': (V + 'listra-offwhite.png', 'tommy', 'Short Tommy Hilfiger', 'Off-white com marinho', K),
    't-marinho': (V + 'listra-marinho.png', 'tommy', 'Short Tommy Hilfiger', 'Marinho com branco', S),
    # site
    's-conj-preto': (ST + '1849694.webp', 'nike', 'Conjunto Nike', 'Preto', A1),
    's-conj-branco': (ST + '1703189.webp', 'nike', 'Conjunto Nike', 'Branco', K),
    's-lacoste': (ST + '1678831.webp', 'Lacoste', 'Bermuda Lacoste', 'Preta', A2),
    's-diesel': (ST + '1688777.webp', 'Diesel', 'Camiseta Diesel', 'Preta', W),
    's-nike-marrom': (ST + '1701345.webp', 'nike', 'Bermuda Nike', 'Marrom com bolso cargo', A1),
    's-pochete': (ST + '1703193.webp', 'jordan', 'Pochete Jordan', 'Bege', A2),
    # peças novas (recortar.py)
    'c04': (C + 'c04.png', '', 'Conjunto jaqueta e short', 'Branco com azul', K),
    'c01': (C + 'c01.png', '', 'Conjunto jaqueta e short', 'Marinho com gelo', S),
    'c02': (C + 'c02.png', 'nike', 'Conjunto Nike', 'Bege com branco', A1),
    'c20': (C + 'c20.png', 'nike', 'Short Nike', 'Preto com branco', S),
    'c18': (C + 'c18.png', 'nike', 'Short Nike', 'Preto com lateral branca', A1),
    'c13': (C + 'c13.png', 'High', 'Bermuda cargo High', 'Preta com vivo branco', A2),
    'c15': (C + 'c15.png', 'High', 'Short High', 'Preto com cinza', S),
    'c12': (C + 'c12.png', 'High', 'Shorts High', 'Preto e verde-militar', W),
    'c06': (C + 'c06.png', 'Thug Nine', 'Short Thug Nine', 'Preto com cinza', A1),
    'c10': (C + 'c10.png', 'Hurley', 'Short Hurley', 'Preto com listras brancas', S),
    'c09': (C + 'c09.png', '', 'Shorts', 'Azul com marinho', A2),
    # básicas tratadas (recortar.py, a partir das imagens de pack/)
    'tb-branca': (C + 'tb-branca.png', 'Básicas', 'Camiseta básica', 'Branca', K),
    'tb-marrom': (C + 'tb-marrom.png', 'Básicas', 'Camiseta básica', 'Marrom', A1),
    'tb-marinho': (C + 'tb-marinho.png', 'Básicas', 'Camiseta básica', 'Marinho', S),
    'tb-bege': (C + 'tb-bege.png', 'Básicas', 'Camiseta básica', 'Bege', K),
    'tb-chumbo': (C + 'tb-chumbo.png', 'Básicas', 'Camiseta básica', 'Chumbo', S),
    'tb-preta': (C + 'tb-preta.png', 'Básicas', 'Camiseta básica', 'Preta', A1),
    'tt-marinho': (C + 'tt-marinho.png', 'Básicas', 'Camiseta texturizada', 'Marinho', A1),
    'tt-branca': (C + 'tt-branca.png', 'Básicas', 'Camiseta texturizada', 'Branca', K),
    'tt-marrom': (C + 'tt-marrom.png', 'Básicas', 'Camiseta texturizada', 'Marrom', W),
    'tt-preta': (C + 'tt-preta.png', 'Básicas', 'Camiseta texturizada', 'Preta', S),
    'po-preta': (C + 'po-preta.png', 'Básicas', 'Polo de malha', 'Preta', S),
    'po-offwhite': (C + 'po-offwhite.png', 'Básicas', 'Polo de malha', 'Off-white', K),
    'po-bege': (C + 'po-bege.png', 'Básicas', 'Polo de malha', 'Bege', A1),
    'camisa-bege': (C + 'camisa-bege.png', 'Básicas', 'Camisa', 'Bege, tecido com textura', A2),
}
RAZAO = {k: (lambda i: i.width / i.height)(Image.open(AQUI / v[0])) for k, v in PECAS.items()}
QUINTETO = [('j-menta', 430, 220, 880, -4, 2), ('j-preta', 430, 540, 880, 2, 3), ('j-creme', 430, 860, 880, 4, 2),
            ('j-gelo', 430, 380, 1250, 3, 4), ('j-verde', 430, 700, 1250, -3, 5)]


def tinta(fundo):
    return W if fundo == K else K


def cena(dur, fundo, *els):
    return dur, fundo, ''.join(els)


def COL(x, y, linhas, cor=K, tam=112, w=968, t0=0, passo=.5):
    """Frase em linhas empilhadas; cada linha entra num tempo."""
    out = ''.join(f'<div class="w" data-a="soco" data-t="{t0 + k * passo}" data-s="{tam}" data-w="{w}" style="color:{cor}">{li}</div>'
                  for k, li in enumerate(linhas))
    return f'<div class="col" style="left:{x}px;top:{y}px">{out}</div>'


def P(ch, w, x, y, giro=0, a='pop', t0=0, z=2, v=.34):
    return (f'<img class="pc" data-a="{a}" data-t="{t0}" data-r="{giro}" data-v="{v}" src="{PECAS[ch][0]}" '
            f'style="width:{w}px;left:{x}px;top:{y}px;z-index:{z}">')


def rot(t):
    return f'<span class="rt">{t}</span>'


def marca(m, cor):
    if m in marcas.ALT:
        return marcas.simb(m, cor, 1.15).replace('src="marcas/', 'src="../drop-verao/marcas/')
    return rot(m) if m else ''


def cab(direita='', cor=K):
    """Cabeçalho fixo: logo da BK à esquerda e a marca da peça à direita."""
    return f'<div class="cab" style="color:{cor}"><span class="lg">{LGI}</span>{direita}</div>'


def leg(nome, c, cor=K, t0=.25):
    anima = f' data-a="sobe" data-t="{t0}"' if t0 is not None else ''
    return f'<div class="leg"{anima} style="color:{cor}"><b>{nome}</b><span>{c}</span></div>'


def chama(t, cor=K, t0=0, y=1400):
    """Chamada final em letra grande entre dois fios (sem faixa preta)."""
    return f'<div class="ch" data-a="sobe" data-t="{t0}" style="top:{y}px;color:{cor}">{t}</div>'


def frase(linhas, fundo, dur=None, tam=176):
    """Cena só de frase, uma linha por tempo, e mais dois tempos parada para dar tempo de ler."""
    return cena(dur or len(linhas) + 2, fundo, COL(M, 920 - len(linhas) * tam // 2, linhas, tinta(fundo), tam, passo=1))


def peca(ch, dur=2, giro=-5, fundo=None, rapido=False):
    _, m, nome, c, f0 = PECAS[ch]
    fundo = fundo or f0
    cor = tinta(fundo)
    return cena(dur, fundo, cab(marca(m, cor), cor), P(ch, min(1000, int(960 * RAZAO[ch])), 540, 880, giro, v=.18 if rapido else .34),
                leg(nome, c, cor, None if rapido else .25))


def montagem(chaves, lentas=0):
    """Peças em sequência: as primeiras (lentas) ficam dois tempos, as outras um tempo cada."""
    return [peca(ch, 2 if j < lentas else 1, (-5, 5)[j % 2], rapido=j >= lentas) for j, ch in enumerate(chaves)]


def cartao(linhas, chaves, fundo, direita='', dur=4):
    """Frase e todas as cores de uma peça juntas."""
    cor = tinta(fundo)
    pos = {6: [(380, x, y) for y in (850, 1230) for x in (200, 540, 880)],
           4: [(470, x, y) for y in (860, 1260) for x in (300, 780)],
           3: [(500, 290, 860), (500, 790, 860), (500, 540, 1250)]}[len(chaves)]
    giros = (-4, 3, 4, 3, -3, 2)
    return cena(dur, fundo, cab(direita, cor), COL(M, 372, linhas, cor),
                *[P(ch, w, x, y, giros[j], t0=.5 + .25 * j, z=2 + j) for j, (ch, (w, x, y)) in enumerate(zip(chaves, pos))])


def vantagem(num, linhas, ch, fundo, giro, dur=4):
    cor = tinta(fundo)
    return cena(dur, fundo, cab(rot(f'Vantagem {num}'), cor), COL(M, 372, linhas, cor), P(ch, min(900, int(760 * RAZAO[ch])), 540, 1060, giro, t0=.75))


def grade(chaves, y1=820, y2=1120, w=500, a='cai', passo=.5):
    """Quatro peças em duas fileiras."""
    pos = [(300, y1, -7), (780, y1 - 10, 7), (310, y2, 5), (770, y2 + 10, -5)]
    return ''.join(P(ch, w, x, y, r, a=a, t0=j * passo, z=2 + j) for j, (ch, (x, y, r)) in enumerate(zip(chaves, pos)))


def chamada(chaves, texto='Qual você leva?', dur=6):
    return cena(dur, W, cab(), COL(M, 372, [texto], K, 150), grade(chaves), chama('Chama no direct', K, 2))


def fim(dur=4):
    return cena(dur, K, f'<div class="fim" style="color:{W}"><span class="lg" style="font-size:170px">{LGI}</span>'
                '<p style="margin-top:64px;font-size:46px;font-weight:500">Vista estilo, vista BK Clothing.</p>'
                '<p style="margin-top:40px;font-size:40px;font-weight:600;letter-spacing:.1em">@bkclothiing</p>'
                '<p style="margin-top:18px;font-size:30px;letter-spacing:.08em;opacity:.75">Rua Santa Catarina, 2348 · Joinville</p></div>')


VIDEOS = {
    'grupo': [frase(['Quem está', 'no grupo VIP'], K), frase(['vê primeiro.'], A1)]
             + montagem(['j-preta', 's-conj-preto', 'b-azul', 'c20', 't-offwhite', 'j-menta', 'c04', 's-lacoste'], lentas=4)
             + [vantagem('01', ['Recebe o drop', 'antes do Instagram.'], 't-marinho', S, -5)]
             + montagem(['c13', 's-diesel', 'c02', 'j-gelo', 's-nike-marrom', 'c15'])
             + [vantagem('02', ['Reserva o tamanho', 'antes de acabar.'], 'b-agua', K, 5)]
             + montagem(['c12', 's-conj-branco', 's-pochete', 'c01', 'n-short', 'j-verde'])
             + [cena(8, A1, cab(rot('Grupo VIP')), COL(M, 372, ['Entre no', 'grupo VIP.'], K, 150),
                     grade(['j-preta', 't-marinho', 'b-azul', 'c20'], 900, 1190, 440), chama('Link na bio', K, 2)),
                fim()],
    'basicas': [frase(['Peças básicas.'], W), frase(['Para o', 'dia a dia.'], K),
                cartao(['Camiseta básica.', 'Seis cores.'], ['tb-marinho', 'tb-bege', 'tb-marrom', 'tb-chumbo', 'tb-preta', 'tb-branca'], A2, rot('Básicas')),
                peca('tb-branca', 3, -4), peca('tb-marrom', 2, 4), peca('tb-marinho', 2, -4)]
               + montagem(['tb-bege', 'tb-chumbo', 'tb-preta'])
               + [cartao(['Camiseta texturizada.', 'Quatro cores.'], ['tt-preta', 'tt-marrom', 'tt-marinho', 'tt-branca'], S, rot('Básicas')),
                  peca('tt-marinho', 2, -4), peca('tt-branca', 2, 4)]
               + montagem(['tt-marrom', 'tt-preta'])
               + [cartao(['Polo de malha.', 'Três cores.'], ['po-preta', 'po-offwhite', 'po-bege'], A2, rot('Básicas')),
                  peca('po-preta', 2, -4), peca('po-offwhite', 2, 4), peca('po-bege', 2, -4), peca('camisa-bege', 3, 4),
                  chamada(['tb-marinho', 'tt-marrom', 'po-preta', 'camisa-bege'], 'Qual é a sua?'), fim()],
    'conjuntos-bermudas': [frase(['Conjuntos', 'e bermudas.'], A2), frase(['Novidade', 'na loja.'], K),
                           peca('c04', 4, -4, A1), peca('c01', 3, 4), peca('c02', 3, -3),
                           peca('s-conj-preto', 2, 0, S), peca('s-conj-branco', 2, 0),
                           frase(['Agora', 'as bermudas.'], W),
                           peca('c20', 2, -5), peca('c18', 2, 5), peca('c13', 2, -5), peca('c15', 2, 5)]
                          + montagem(['c12', 'c06', 'c10', 'c09'])
                          + [cena(4, A1, cab(marca('jordan', K)), COL(M, 372, ['Bermudas da Jordan.', 'Cinco cores na loja.']),
                                  *[P(ch, w, x, y, r, t0=.5 + .25 * j, z=z) for j, (ch, w, x, y, r, z) in enumerate(QUINTETO)]),
                             chamada(['c20', 'j-menta', 'b-azul', 'c13']), fim()],
}

CSS = marcas.CSS + '''
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0b0b0b;font-family:"Archivo",sans-serif}
.c{position:absolute;inset:0;overflow:hidden;visibility:hidden}
.w{font-family:"Big Shoulders Display","Archivo",sans-serif;font-weight:900;text-transform:uppercase;letter-spacing:0;line-height:1;white-space:nowrap;transform-origin:0 60%;will-change:transform}
.col{position:absolute;display:flex;flex-direction:column;align-items:flex-start;z-index:7}
.pc{position:absolute;height:auto;filter:drop-shadow(0 40px 44px rgba(0,0,0,.34));will-change:transform}
.cab{position:absolute;left:56px;right:56px;top:206px;height:120px;display:flex;justify-content:space-between;align-items:center;z-index:9}
.rt{font-weight:600;font-size:30px;letter-spacing:.14em;text-transform:uppercase}
.leg{position:absolute;left:60px;top:1420px;display:flex;flex-direction:column;gap:8px;z-index:8}
.leg b{font-weight:600;font-size:48px}
.leg span{font-size:38px;opacity:.72}
.ch{position:absolute;left:56px;right:56px;height:150px;padding-top:4px;display:grid;place-items:center;border-top:2px solid currentColor;border-bottom:2px solid currentColor;font-family:"Big Shoulders Display";font-weight:900;font-size:92px;line-height:1;text-transform:uppercase;z-index:9}
.fim{position:absolute;inset:0;display:grid;place-content:center;justify-items:center;text-align:center}
.lg{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:52px;flex:none}
.lg::before,.lg::after{content:"";position:absolute;top:0;bottom:0;width:32%;border:.045em solid currentColor}
.lg::before{left:0;border-right:0}.lg::after{right:0;border-left:0}
.lg b{font-family:"Jost";font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}
.lg i{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}
'''
JS = '''
const B=60/BPM,$$=(s,r=document)=>[...r.querySelectorAll(s)];
const sai=x=>{x=Math.max(0,Math.min(1,x));return 1-Math.pow(1-x,3)};
const volta=x=>{x=Math.max(0,Math.min(1,x));const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const cenas=$$('.c').map(el=>({el,a:+el.dataset.i*B,b:+el.dataset.f*B,ani:$$('[data-a]',el)}));
window.DUR=Math.max(...cenas.map(c=>c.b));
const anim={
  soco(e,k){e.style.opacity=k<0?0:1;e.style.transform=`scale(${1+.45*(1-sai(k/.22))})`},
  pop(e,k){const r=+e.dataset.r,v=volta(k/(+e.dataset.v||.34));e.style.opacity=k<0?0:1;
    e.style.transform=`translate(-50%,-50%) scale(${(.72+.28*v)*(1+.014*Math.max(0,k))}) rotate(${r-(1-v)*12}deg)`},
  cai(e,k){const r=+e.dataset.r,v=volta(k/.36);e.style.opacity=k<0?0:1;
    e.style.transform=`translate(-50%,-50%) translateY(${(1-v)*-760}px) rotate(${r+(1-v)*14}deg)`},
  sobe(e,k){const v=sai(k/.26);e.style.opacity=v;e.style.transform=`translateY(${(1-v)*36}px)`},
};
window.render=async t=>{
  for(const c of cenas){
    const on=t>=c.a&&t<c.b;c.el.style.visibility=on?'visible':'hidden';
    if(!on)continue;
    for(const e of c.ani)anim[e.dataset.a](e,t-c.a-(+e.dataset.t||0)*B,c.b-c.a);
  }
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
};
'''
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=Big+Shoulders+Display:wght@900'
          '&family=Bebas+Neue&family=Jost:wght@200&display=swap" rel="stylesheet">')
# cada frase fica no tamanho pedido (data-s); se uma linha passa da largura (data-w), a frase inteira encolhe junta
AJUSTE = '''() => document.querySelectorAll('.col').forEach(c => { const ls = [...c.children];
    const f = Math.min(1, ...ls.map(e => { e.style.fontSize = e.dataset.s + 'px'; return e.dataset.w / e.offsetWidth }));
    ls.forEach(e => { e.style.fontSize = Math.floor(e.dataset.s * f) + 'px' }) })'''


def montar(nome):
    corpo, ini, antes = '', 0, None
    for dur, fundo, els in VIDEOS[nome]:
        if fundo == antes:
            print(f'  aviso ({nome}): duas cenas seguidas com o mesmo fundo no tempo {ini}')
        corpo += f'<div class="c" data-i="{ini}" data-f="{ini + dur}" style="background:{fundo}">{els}</div>'
        ini, antes = ini + dur, fundo
    arq = AQUI / f'_video-{nome}.html'
    arq.write_text(f'<!doctype html><html><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>{corpo}'
                   f'<script>const BPM={BPM};{JS}</script></body></html>', encoding='utf-8')
    return arq


def gravar(nome, so_roteiro=False):
    arq = montar(nome)
    qd = SAIDA / f'_q-{nome}'
    shutil.rmtree(qd, ignore_errors=True)
    qd.mkdir()
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome', headless=True)
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(arq.as_uri())
        pg.evaluate('document.fonts.ready')
        pg.wait_for_function('[...document.images].every(i => i.complete && i.naturalWidth > 0)', timeout=60000)
        pg.wait_for_timeout(1200)
        pg.evaluate(AJUSTE)
        dur = pg.evaluate('window.DUR')
        total = int(dur * FPS)
        if so_roteiro:      # um quadro por cena, para conferir o desenho antes de gravar tudo
            ini, quadros = 0, []
            for d, *_ in VIDEOS[nome]:
                pg.evaluate('t => window.render(t)', (ini + .82 * d) * 60 / BPM)
                pg.screenshot(path=str(qd / 'r.jpg'), type='jpeg', quality=88)
                quadros.append(Image.open(qd / 'r.jpg').resize((225, 400)))
                ini += d
            b.close()
            col = 13
            R = Image.new('RGB', (col * 225, -(-len(quadros) // col) * 400))
            for k, q in enumerate(quadros):
                R.paste(q, ((k % col) * 225, (k // col) * 400))
            R.save(SAIDA / f'_roteiro-{nome}.jpg', quality=86)
            shutil.rmtree(qd, ignore_errors=True)
            arq.unlink()
            print('roteiro', nome, len(quadros), 'cenas', round(dur, 2), 's', flush=True)
            return
        for f in range(total):
            pg.evaluate('t => window.render(t)', f / FPS)
            pg.screenshot(path=str(qd / f'{f:04d}.jpg'), type='jpeg', quality=92)
        b.close()
    final = SAIDA / f'{nome}.mp4'
    beat = RAIZ / 'drop-verao' / 'beat.wav'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(qd / '%04d.jpg')]
    if beat.exists():       # o beat começa a bater no compasso 3 (3,43 s); os cortes do vídeo caem nos tempos
        cmd += ['-ss', '3.4286', '-t', f'{dur:.3f}', '-i', str(beat), '-af', f'afade=t=out:st={dur - 0.9:.2f}:d=0.9', '-c:a', 'aac', '-b:a', '192k']
    cmd += ['-c:v', 'libx264', '-crf', '19', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-shortest', '-movflags', '+faststart', str(final)]
    subprocess.run(cmd, check=True)
    n = 14
    Sx = Image.new('RGB', (n * 180, 320))
    for k in range(n):
        Sx.paste(Image.open(qd / f'{int(total * (k + .5) / n):04d}.jpg').resize((180, 320)), (k * 180, 0))
    Sx.save(SAIDA / f'_conf-{nome}.jpg', quality=86)
    shutil.rmtree(qd, ignore_errors=True)
    arq.unlink()
    print('ok', nome, round(dur, 2), 's', round(final.stat().st_size / 1e6, 1), 'MB', flush=True)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--roteiro']
    for nome in args or list(VIDEOS):
        gravar(nome, '--roteiro' in sys.argv)
