"""Vídeos verticais do drop de verão (1080x1920), feitos por código, quadro a quadro, com corte no tempo do beat (140 BPM).

Uso:  python video.py                  (todos)
      python video.py verao grupo-vip  (só os citados)
      python video.py --roteiro verao  (um quadro por cena, para conferir antes de gravar)
Saída em videos/: verao.mp4 (a campanha inteira, marca por marca, com mais tempo para a Jordan), grupo-vip.mp4,
jordan.mp4, nike.mp4, brooksfield.mp4, tommy.mp4 e uma folha de quadros _conf-<nome>.jpg. Sem preço e sem crédito de geração.
Mesma linguagem dos posts (base.py): frase normal, símbolo da marca, peça grande com o nome pequeno.
Só entram as peças tratadas: as fotos de celular tiradas na loja saíram do vídeo a pedido do Guilherme.
O giro da bermuda preta vem de drop-jordan/video/bruto.mp4; o beat é beat.wav (python beat.py 34).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import marcas
from base import A1, A2, S, K, W, LGI, MARCAS, PECAS, RAZAO, tinta
from marcas import simb, fila

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
SAIDA = AQUI / 'videos'
SAIDA.mkdir(exist_ok=True)
FPS, BPM = 30, 140
M = 56          # margem lateral
FUNDO_M = {'jordan': A2, 'nike': W, 'brooksfield': S, 'tommy': A2}                      # fundo da abertura de cada marca
FUNDO_P = {'basquete-preta': S, 'basquete-menta': A1, 'basquete-creme': A2, 'basquete-gelo': K, 'basquete-verde': S,
           'cargo-preta': S, 'vivo-preta': A2, 'praia-azul': W, 'praia-agua': K,
           'listra-offwhite': K, 'listra-preta': A1, 'listra-marinho': S}               # fundo da cena de cada peça
# como as peças se arrumam na abertura de cada marca: (peça, largura, x, y, giro, camada)
ARRANJO = {
    'jordan': [('basquete-menta', 430, 220, 880, -4, 2), ('basquete-preta', 430, 540, 880, 2, 3), ('basquete-creme', 430, 860, 880, 4, 2),
               ('basquete-gelo', 430, 380, 1250, 3, 4), ('basquete-verde', 430, 700, 1250, -3, 5)],
    'nike': [('cargo-preta', 720, 400, 900, -6, 2), ('vivo-preta', 760, 660, 1210, 5, 3)],
    'brooksfield': [('praia-azul', 800, 430, 900, -8, 2), ('praia-agua', 740, 670, 1200, 6, 3)],
    'tommy': [('listra-marinho', 560, 790, 840, 8, 2), ('listra-offwhite', 580, 310, 1000, -7, 3), ('listra-preta', 640, 640, 1230, -2, 4)],
}


def cena(dur, fundo, *els):
    return dur, fundo, ''.join(els)


def COL(x, y, linhas, cor=K, tam=112, w=968, t0=0, passo=.5):
    """Frase em linhas empilhadas; cada linha entra num tempo."""
    out = ''.join(f'<div class="w" data-a="soco" data-t="{t0 + k * passo}" data-s="{tam}" data-w="{w}" style="color:{cor}">{li}</div>'
                  for k, li in enumerate(linhas))
    return f'<div class="col" style="left:{x}px;top:{y}px">{out}</div>'


def P(n, w, x, y, rot=0, a='pop', t0=0, z=2):
    return f'<img class="pc" data-a="{a}" data-t="{t0}" data-r="{rot}" src="cut/{n}.png" style="width:{w}px;left:{x}px;top:{y}px;z-index:{z}">'


def X(t, x, y, tam=44, cor=K, t0=0):
    return f'<p class="t" data-a="sobe" data-t="{t0}" style="left:{x}px;top:{y}px;font-size:{tam}px;color:{cor}">{"<br>".join(t.split("|"))}</p>'


def FX(t, fundo=K, cor=W, t0=0, y=1340, alt=200, tam=108):
    return f'<div class="fx" data-a="faixa" data-t="{t0}" style="top:{y}px;height:{alt}px;background:{fundo};color:{cor};font-size:{tam}px">{t}</div>'


def rot(t):
    return f'<span class="rt">{t}</span>'


def cab(direita='', cor=K):
    """Cabeçalho fixo: logo da BK à esquerda e o símbolo da marca à direita."""
    return f'<div class="cab" style="color:{cor}"><span class="lg">{LGI}</span>{direita}</div>'


def leg(n, cor=K, t0=.25):
    _, nome, c = PECAS[n]
    return f'<div class="leg" data-a="sobe" data-t="{t0}" style="color:{cor}"><b>{nome}</b><span>{c}</span></div>'


def frase(linhas, fundo, dur=2, tam=176):
    """Cena só de frase, uma linha por tempo."""
    return cena(dur, fundo, COL(M, 920 - len(linhas) * tam // 2, linhas, tinta(fundo), tam, passo=1))


def abertura(marca, dur=2):
    fundo = FUNDO_M[marca]
    cor = tinta(fundo)
    els = [cab(simb(marca, cor, 1.15), cor), COL(M, 372, MARCAS[marca][0].split('|'), cor)]
    els += [P(n, w, x, y, r, t0=.5 + .25 * j, z=z) for j, (n, w, x, y, r, z) in enumerate(ARRANJO[marca])]
    return cena(dur, fundo, *els)


def peca(n, dur=2, giro=-5):
    fundo = FUNDO_P[n]
    cor = tinta(fundo)
    return cena(dur, fundo, cab(simb(PECAS[n][0], cor, 1.15), cor), P(n, min(1000, int(900 * RAZAO[n])), 540, 890, giro), leg(n, cor))


def pecas(marca, durs=None):
    return [peca(n, durs[j] if durs else 2, (-5, 5)[j % 2]) for j, n in enumerate(MARCAS[marca][2])]


def giro(dur=4):
    return cena(dur, A1, '<video data-a="video" src="videos/_giro.mp4" muted playsinline preload="auto"></video>',
                cab(simb('jordan', K, 1.15)), leg('basquete-preta', K, 0))


def chamada(lista, dur=6):
    n = len(lista)
    pos = {2: [(640, 330, 880, -8), (640, 750, 1060, 8)],
           3: [(560, 290, 900, -10), (560, 790, 880, 10), (600, 540, 1090, 2)],
           4: [(500, 300, 820, -7), (500, 780, 810, 7), (500, 310, 1120, 5), (500, 770, 1130, -5)],
           5: [(400, 220, 800, -4), (400, 540, 790, 2), (400, 860, 800, 4), (400, 380, 1110, 3), (400, 700, 1110, -3)]}[n]
    passo = 1 if n <= 3 else .5
    els = [cab(), COL(M, 372, ['Qual você leva?'], K, 150)]
    els += [P(p, w, x, y, r, a='cai', t0=j * passo, z=2 + j) for j, (p, (w, x, y, r)) in enumerate(zip(lista, pos))]
    els += [FX('Chama no direct', t0=n * passo)]
    return cena(dur, W, *els)


def vip(dur=4):
    return cena(dur, A1, cab(rot('Grupo VIP')), COL(M, 372, ['Quem está no grupo VIP', 'vê primeiro.']),
                P('basquete-preta', 760, 540, 980, -5, t0=.75), FX('Link na bio', t0=1))


def vantagem(num, linhas, n, fundo, giro_, dur=3):
    cor = tinta(fundo)
    return cena(dur, fundo, cab(rot(f'Vantagem {num}'), cor), COL(M, 372, linhas, cor), P(n, min(900, int(760 * RAZAO[n])), 540, 1060, giro_, t0=.75))


def fim(dur=4):
    return cena(dur, K, f'<div class="fim" style="color:{W}"><span class="lg" style="font-size:170px">{LGI}</span>'
                '<p style="margin-top:64px;font-size:46px;font-weight:500">Vista estilo, vista BK Clothing.</p>'
                '<p style="margin-top:40px;font-size:40px;font-weight:600;letter-spacing:.1em">@bkclothiing</p>'
                '<p style="margin-top:18px;font-size:30px;letter-spacing:.08em;opacity:.75">Rua Santa Catarina, 2348 · Joinville</p></div>')


VIDEOS = {
    'verao': [frase(['Vista estilo,'], K), frase(['Vista', 'BK Clothing.'], A1), frase(['Seu verão', 'começa na BK.'], S)]
             + [abertura('jordan', 3)] + pecas('jordan') + [giro(4)]
             + [abertura('nike')] + pecas('nike') + [abertura('brooksfield')] + pecas('brooksfield') + [abertura('tommy')] + pecas('tommy')
             + [chamada(['basquete-menta', 'cargo-preta', 'praia-azul', 'listra-offwhite']), vip(), fim()],
    'jordan': [frase(['Bermudas', 'da Jordan.'], A2), frase(['Cinco cores', 'na loja.'], K)] + pecas('jordan')
              + [giro(5), chamada(MARCAS['jordan'][2]), fim()],
    'nike': [frase(['Cargo e short', 'da Nike.'], W)] + pecas('nike', [3, 3]) + [abertura('nike', 3), chamada(MARCAS['nike'][2], 5), fim()],
    'brooksfield': [frase(['Shorts', 'Brooksfield.'], S)] + pecas('brooksfield', [3, 3])
                   + [abertura('brooksfield', 3), chamada(MARCAS['brooksfield'][2], 5), fim()],
    'tommy': [frase(['Shorts', 'Tommy Hilfiger.'], A2)] + pecas('tommy', [3, 3, 3]) + [abertura('tommy', 3), chamada(MARCAS['tommy'][2]), fim()],
    'grupo-vip': [frase(['Quem está', 'no grupo VIP'], K), frase(['vê primeiro.'], A1),
                  vantagem('01', ['Recebe o drop', 'antes do Instagram.'], 'basquete-menta', S, -5),
                  vantagem('02', ['Reserva o tamanho', 'antes de acabar.'], 'praia-azul', W, 5),
                  cena(6, K, cab(rot('Grupo VIP'), W), COL(M, 372, ['Entre no', 'grupo VIP.'], W, 150),
                       P('basquete-gelo', 760, 540, 1040, 6, a='cai', t0=1), FX('Link na bio', A1, K, t0=2)),
                  fim()],
}

CSS = marcas.CSS + '''
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0b0b0b;font-family:"Archivo",sans-serif}
.c{position:absolute;inset:0;overflow:hidden;visibility:hidden}
.w{font-family:"Big Shoulders Display","Archivo",sans-serif;font-weight:900;text-transform:uppercase;letter-spacing:0;line-height:1;white-space:nowrap;transform-origin:0 60%;will-change:transform}
.col{position:absolute;display:flex;flex-direction:column;align-items:flex-start;z-index:7}
.pc{position:absolute;height:auto;filter:drop-shadow(0 40px 44px rgba(0,0,0,.34));will-change:transform}
video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cab{position:absolute;left:56px;right:56px;top:206px;height:120px;display:flex;justify-content:space-between;align-items:center;z-index:9}
.rt{font-weight:600;font-size:30px;letter-spacing:.14em;text-transform:uppercase}
.leg{position:absolute;left:60px;top:1420px;display:flex;flex-direction:column;gap:8px;z-index:8}
.leg b{font-weight:600;font-size:48px}
.leg span{font-size:38px;opacity:.72}
.t{position:absolute;font-weight:500;line-height:1.2;z-index:8}
.fx{position:absolute;left:0;right:0;display:grid;place-items:center;font-family:"Big Shoulders Display";font-weight:900;text-transform:uppercase;letter-spacing:.01em;z-index:9}
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
async function busca(v,t){if(Math.abs(v.currentTime-t)<.004)return;await new Promise(r=>{v.addEventListener('seeked',r,{once:true});v.currentTime=t})}
const anim={
  soco(e,k){e.style.opacity=k<0?0:1;e.style.transform=`scale(${1+.45*(1-sai(k/.22))})`},
  pop(e,k){const r=+e.dataset.r,v=volta(k/.34);e.style.opacity=k<0?0:1;
    e.style.transform=`translate(-50%,-50%) scale(${(.72+.28*v)*(1+.014*Math.max(0,k))}) rotate(${r-(1-v)*12}deg)`},
  cai(e,k){const r=+e.dataset.r,v=volta(k/.36);e.style.opacity=k<0?0:1;
    e.style.transform=`translate(-50%,-50%) translateY(${(1-v)*-760}px) rotate(${r+(1-v)*14}deg)`},
  sobe(e,k){const v=sai(k/.26);e.style.opacity=v;e.style.transform=`translateY(${(1-v)*36}px)`},
  faixa(e,k){e.style.transform=`translateY(${(1-sai(k/.3))*760}px)`},
  async video(e,k){await busca(e,Math.min(4.9,Math.max(0,k)*1.4))},
};
window.render=async t=>{
  for(const c of cenas){
    const on=t>=c.a&&t<c.b;c.el.style.visibility=on?'visible':'hidden';
    if(!on)continue;
    for(const e of c.ani)await anim[e.dataset.a](e,t-c.a-(+e.dataset.t||0)*B,c.b-c.a);
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
    corpo, ini = '', 0
    for dur, fundo, els in VIDEOS[nome]:
        corpo += f'<div class="c" data-i="{ini}" data-f="{ini + dur}" style="background:{fundo}">{els}</div>'
        ini += dur
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
        b = p.chromium.launch(channel='chrome', headless=True, args=['--autoplay-policy=no-user-gesture-required'])
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(arq.as_uri())
        pg.evaluate('document.fonts.ready')
        pg.wait_for_function('[...document.images].every(i => i.complete && i.naturalWidth > 0)'
                             ' && [...document.querySelectorAll("video")].every(v => v.readyState >= 2)', timeout=60000)
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
    beat = AQUI / 'beat.wav'
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
    giro_mp4 = SAIDA / '_giro.mp4'      # todos os quadros como quadro-chave, para a página pular para qualquer instante
    if not giro_mp4.exists():
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(AQUI.parent / 'drop-jordan' / 'video' / 'bruto.mp4'), '-an',
                        '-c:v', 'libx264', '-g', '1', '-crf', '16', '-pix_fmt', 'yuv420p', str(giro_mp4)], check=True)
    args = [a for a in sys.argv[1:] if a != '--roteiro']
    for nome in args or list(VIDEOS):
        gravar(nome, '--roteiro' in sys.argv)
