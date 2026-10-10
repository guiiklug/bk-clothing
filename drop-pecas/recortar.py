"""Recorta as peças das fotos novas (fundo transparente), sem crédito, e monta cut/_conf.jpg.

Uso:  python recortar.py           (só o que falta)
      python recortar.py c06 c13   (refaz as citadas)
      python recortar.py tudo
São fotos da peça estendida no chão ou no tapete: o recorte é a foto real. Ficam as partes grandes (um conjunto tem
duas peças); ilhas pequenas, como etiqueta solta, saem. Quando a foto tem duas peças e só uma interessa, UMA diz qual.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from rembg import remove, new_session

AQUI = Path(__file__).resolve().parent
CUT = AQUI / 'cut'
CUT.mkdir(exist_ok=True)
FOTOS = ['c01', 'c02', 'c04', 'c05', 'c06', 'c07', 'c08', 'c09', 'c10', 'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21']
UMA = {}        # foto -> índice da parte que fica (0 = a maior), quando só uma das peças interessa
pedidos = sys.argv[1:]
ses = None
for nome in FOTOS:
    dst = CUT / f'{nome}.png'
    if dst.exists() and nome not in pedidos and 'tudo' not in pedidos:
        continue
    ses = ses or new_session('isnet-general-use')
    out = remove(Image.open(AQUI / 'orig' / f'{nome}.jpg').convert('RGB'), session=ses)
    m = np.array(out.getchannel('A'))
    rot, n = ndimage.label(m > 40)
    if n > 1:
        areas = ndimage.sum(m > 40, rot, range(1, n + 1))
        ordem = np.argsort(areas)[::-1]
        fica = [1 + int(ordem[UMA[nome]])] if nome in UMA else [1 + int(k) for k in ordem if areas[k] >= .12 * areas[ordem[0]]]
        m[~np.isin(rot, fica)] = 0
    out.putalpha(Image.fromarray(m))
    out = out.crop(out.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox())
    out.save(dst)
    print(nome, out.size, 'partes:', n, flush=True)

# As básicas vieram com modelo. O Guilherme pediu a peça tratada, sem modelo: o Higgsfield gerou três imagens com
# várias cores cada (pack/), em grade de células iguais, e aqui cada célula vira um recorte. 9,75 créditos no total.
GRADES = {      # imagem -> (colunas, linhas, nomes na ordem de leitura)
    'camisetas': (3, 2, ['tb-marinho', 'tb-bege', 'tb-marrom', 'tb-chumbo', 'tb-preta', 'tb-branca']),
    'texturizadas': (2, 2, ['tt-preta', 'tt-marrom', 'tt-marinho', 'tt-branca']),
    'polos': (2, 2, ['po-preta', 'po-offwhite', 'po-bege', 'camisa-bege']),
}
for img, (col, lin, nomes) in GRADES.items():
    if not (AQUI / 'pack' / f'{img}.png').exists():
        continue
    folha_ = None
    for k, nome in enumerate(nomes):
        dst = CUT / f'{nome}.png'
        if dst.exists() and nome not in pedidos and 'tudo' not in pedidos:
            continue
        folha_ = folha_ or Image.open(AQUI / 'pack' / f'{img}.png').convert('RGB')
        cw, ch = folha_.width // col, folha_.height // lin
        cel = folha_.crop(((k % col) * cw, (k // col) * ch, (k % col + 1) * cw, (k // col + 1) * ch))
        ses = ses or new_session('isnet-general-use')
        out = remove(cel, session=ses)
        m = np.array(out.getchannel('A'))
        rot, n = ndimage.label(m > 40)
        if n > 1:
            m[rot != 1 + int(np.argmax(ndimage.sum(m > 40, rot, range(1, n + 1))))] = 0
        out.putalpha(Image.fromarray(m))
        out = out.crop(out.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox())
        out.save(dst)
        print(nome, out.size, flush=True)
FOTOS += [n for _, _, nomes in GRADES.values() for n in nomes]

feitos = [n for n in FOTOS if (CUT / f'{n}.png').exists()]
COL, LADO = 7, 420
S = Image.new('RGB', (COL * LADO, -(-len(feitos) // COL) * LADO), '#9fb2c0')
for k, n in enumerate(feitos):
    im = Image.open(CUT / f'{n}.png')
    im.thumbnail((LADO - 24, LADO - 24), Image.LANCZOS)
    S.paste(im, ((k % COL) * LADO + (LADO - im.width) // 2, (k // COL) * LADO + (LADO - im.height) // 2), im)
S.save(CUT / '_conf.jpg', quality=88)
print('folha', S.size)
