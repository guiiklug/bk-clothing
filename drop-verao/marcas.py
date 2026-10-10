"""Símbolos das marcas das peças, prontos para entrar nas artes e nos vídeos (HTML).

De onde vieram (pasta marcas/):
  jordan.svg   Wikipédia em inglês, File:Jumpman_logo.svg        (baixado com o ok do Guilherme em 10/10/2026)
  nike.svg     Wikimedia Commons, File:Logo_NIKE.svg
  tommy.svg    Wikimedia Commons, File:Tommy_Hilfiger_logo.svg
  brooksfield-orig.png   enviado pelo Guilherme (pato branco em fundo verde, 180 px); daqui saem as versões -k e -w
São marcas de terceiros: entram só ao lado das peças dessas marcas que a loja vende.
"""
import re
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

M = Path(__file__).resolve().parent / 'marcas'
K, W = '#0b0b0b', '#f3f0ea'
ALT = {'jordan': 104, 'nike': 60, 'brooksfield': 92, 'tommy': 64}       # altura em px para os quatro pesarem igual
ORDEM = ['jordan', 'nike', 'brooksfield', 'tommy']                      # a hierarquia que o Guilherme definiu
CSS = '.sb{display:block;width:auto;flex:none}'


def _caminho(arq):
    s = (M / arq).read_text(encoding='utf-8')
    return re.search(r'viewBox="([^"]+)"', s).group(1), ' '.join(re.search(r'<path[^>]*?\sd="([^"]+)"', s, re.S).group(1).split())


def _pato():
    """A imagem pequena vira recorte limpo: amplia, suaviza e fica só o que é branco."""
    if (M / 'brooksfield-k.png').exists():
        return
    im = Image.open(M / 'brooksfield-orig.png').convert('L')
    im = im.resize((im.width * 6, im.height * 6), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2.4))
    alfa = Image.fromarray((np.clip((np.asarray(im, float) - 118) / 60, 0, 1) * 255).astype('uint8'))
    caixa = alfa.getbbox()
    for nome, cor in (('k', K), ('w', W)):
        out = Image.new('RGBA', alfa.size, cor)
        out.putalpha(alfa)
        out.crop(caixa).save(M / f'brooksfield-{nome}.png')


def simb(marca, cor=K, escala=1.0):
    """O símbolo da marca na cor do texto (o da Tommy mantém as cores da bandeira)."""
    h = round(ALT[marca] * escala)
    if marca in ('jordan', 'nike'):
        vb, d = _caminho(f'{marca}.svg')
        return f'<svg class="sb" style="height:{h}px;color:{cor}" viewBox="{vb}"><path fill="currentColor" d="{d}"/></svg>'
    if marca == 'tommy':
        borda = ';outline:2px solid rgba(243,240,234,.55)' if cor == W else ''
        return (f'<svg class="sb" style="height:{h}px{borda}" viewBox=".5 0 3 2"><rect x="0" width="4" height="2" fill="#001c4b"/>'
                '<path d="M0,1H4" stroke="#fff"/><path d="M2,1H4" stroke="#d2002f"/></svg>')
    _pato()
    return f'<img class="sb" style="height:{h}px" src="marcas/brooksfield-{"w" if cor == W else "k"}.png">'


def fila(cor=K, escala=.5, vao=34):
    """Os quatro símbolos em linha, na ordem da hierarquia."""
    return f'<span style="display:flex;align-items:center;gap:{vao}px">{"".join(simb(m, cor, escala) for m in ORDEM)}</span>'
