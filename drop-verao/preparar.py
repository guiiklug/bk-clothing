"""Organiza as fotos tiradas na loja (pastas orig/a e orig/b) em orig/01.jpg, 02.jpg... e monta a folha orig/_folha.jpg.

Uso:  python preparar.py
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

AQUI = Path(__file__).resolve().parent
ORIG = AQUI / 'orig'
fotos = sorted((ORIG / 'a').glob('*.jpeg')) + sorted((ORIG / 'b').glob('*.jpeg'))
if not fotos:
    sys.exit('sem fotos em orig/a e orig/b')
nomes = []
for k, f in enumerate(fotos, 1):
    im = ImageOps.exif_transpose(Image.open(f)).convert('RGB')
    dst = ORIG / f'{k:02d}.jpg'
    im.save(dst, quality=95)
    nomes.append((dst, im.size, f.name))
    print(dst.name, im.size, '<-', f.name)

COL, LADO = 4, 560
lin = -(-len(nomes) // COL)
S = Image.new('RGB', (COL * LADO, lin * LADO), '#222')
d = ImageDraw.Draw(S)
try:
    fonte = ImageFont.truetype('arialbd.ttf', 54)
except OSError:
    fonte = ImageFont.load_default()
for k, (dst, _, _) in enumerate(nomes):
    im = Image.open(dst)
    im.thumbnail((LADO - 8, LADO - 8), Image.LANCZOS)
    x, y = (k % COL) * LADO, (k // COL) * LADO
    S.paste(im, (x + (LADO - im.width) // 2, y + (LADO - im.height) // 2))
    d.rectangle([x + 8, y + 8, x + 100, y + 76], fill='#000')
    d.text((x + 18, y + 10), f'{k + 1:02d}', fill='#fff', font=fonte)
S.save(ORIG / '_folha.jpg', quality=88)
print('folha', S.size)
