"""Organiza as fotos novas (pastas orig/basicas-N e orig/conjunto-N, extraídas dos zips de ../peças) em
orig/b01.jpg... e orig/c01.jpg..., e monta as folhas orig/_folha-b.jpg e orig/_folha-c.jpg.

Uso:  python preparar.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ORIG = Path(__file__).resolve().parent / 'orig'
try:
    fonte = ImageFont.truetype('arialbd.ttf', 46)
except OSError:
    fonte = ImageFont.load_default()
COL, LADO = 6, 440
for letra, prefixo in (('b', 'basicas'), ('c', 'conjunto')):
    fotos = [f for d in sorted(ORIG.glob(f'{prefixo}-*')) for f in sorted(d.glob('*.jpeg'))]
    nomes = []
    for k, f in enumerate(fotos, 1):
        im = ImageOps.exif_transpose(Image.open(f)).convert('RGB')
        dst = ORIG / f'{letra}{k:02d}.jpg'
        im.save(dst, quality=95)
        nomes.append(dst)
        print(dst.name, im.size, '<-', f.parent.name)
    S = Image.new('RGB', (COL * LADO, -(-len(nomes) // COL) * LADO), '#222')
    d = ImageDraw.Draw(S)
    for k, dst in enumerate(nomes):
        im = Image.open(dst)
        im.thumbnail((LADO - 8, LADO - 8), Image.LANCZOS)
        x, y = (k % COL) * LADO, (k // COL) * LADO
        S.paste(im, (x + (LADO - im.width) // 2, y + (LADO - im.height) // 2))
        d.rectangle([x + 6, y + 6, x + 104, y + 62], fill='#000')
        d.text((x + 12, y + 6), dst.stem, fill='#fff', font=fonte)
    S.save(ORIG / f'_folha-{letra}.jpg', quality=88)
    print('folha', letra, S.size)
