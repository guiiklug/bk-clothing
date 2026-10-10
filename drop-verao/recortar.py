"""Recorta as peças das fotos (fundo transparente), endireita e monta a folha de conferência cut/_conf.jpg.

Uso:  python recortar.py            (só o que falta)
      python recortar.py praia-azul (refaz uma)
      python recortar.py tudo       (refaz todas)
As fotos limpas (peça estendida no tapete) são recortadas direto, sem crédito: é a foto real da peça.
As fotos tiradas em cima da mesa da loja passam antes pelo Higgsfield (pasta pack/) e só então são recortadas.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from rembg import remove, new_session

AQUI = Path(__file__).resolve().parent
CUT = AQUI / 'cut'
CUT.mkdir(exist_ok=True)

# nome -> (foto de origem, giro em graus que deixa o cós na horizontal, retângulos a apagar na foto: etiqueta de tamanho)
PECAS = {
    'praia-azul': ('orig/23.jpg', 25, [(80, 1120, 500, 1250)]),
    'praia-agua': ('orig/24.jpg', 13, [(170, 905, 328, 1000)]),
    'listra-offwhite': ('orig/02.jpg', -15, [(1000, 850, 1090, 940)]),
    'listra-preta': ('orig/03.jpg', -16, []),
    'listra-marinho': ('orig/04.jpg', -15, []),
    'vivo-preta': ('orig/01.jpg', -8, []),
    'basquete-menta': ('pack/basquete-menta.png', 0, []),
    'basquete-creme': ('pack/basquete-creme.png', 0, []),
    'cargo-preta': ('pack/cargo-preta.png', 0, []),
}
pedidos = sys.argv[1:]
ses = None
for nome, (src, giro, apaga) in PECAS.items():
    dst = CUT / f'{nome}.png'
    if not (AQUI / src).exists() or (dst.exists() and nome not in pedidos and 'tudo' not in pedidos):
        continue
    ses = ses or new_session('isnet-general-use')
    out = remove(Image.open(AQUI / src).convert('RGB'), session=ses)
    a = out.getchannel('A')
    d = ImageDraw.Draw(a)
    for r in apaga:
        d.rectangle(r, fill=0)
    # fica só a peça: ilhas soltas (etiqueta, pedaço de tapete) saem
    m = np.array(a)
    rot, n = ndimage.label(m > 40)
    if n > 1:
        maior = 1 + int(np.argmax(ndimage.sum(m > 40, rot, range(1, n + 1))))
        m[rot != maior] = 0
    out.putalpha(Image.fromarray(m))
    if giro:      # gira com a cor já multiplicada pela transparência, para a borda não puxar a cor do tapete
        out = out.convert('RGBa').rotate(giro, resample=Image.BICUBIC, expand=True).convert('RGBA')
    out = out.crop(out.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox())
    out.save(dst)
    print(nome, out.size)

feitos = [n for n in PECAS if (CUT / f'{n}.png').exists()]
LADO = 520
S = Image.new('RGB', (len(feitos) * LADO, LADO), '#dce8ef')
for k, n in enumerate(feitos):
    im = Image.open(CUT / f'{n}.png')
    im.thumbnail((LADO - 30, LADO - 30), Image.LANCZOS)
    S.paste(im, (k * LADO + (LADO - im.width) // 2, (LADO - im.height) // 2), im)
S.save(CUT / '_conf.jpg', quality=88)
print('folha', S.size)
