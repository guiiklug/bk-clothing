"""Junta imagens numa folha de conferência. Uso: folha.py saida.jpg col largura img1 img2 ..."""
import sys
from PIL import Image
out, cols, w, *fs = sys.argv[1:]
cols, w = int(cols), int(w)
ims = []
for f in fs:
    im = Image.open(f).convert("RGB"); h = int(im.height * w / im.width); ims.append(im.resize((w, h)))
rows = [ims[i:i+cols] for i in range(0, len(ims), cols)]
H = sum(max(i.height for i in r) + 8 for r in rows)
sheet = Image.new("RGB", (cols*(w+8), H), (128, 128, 128)); y = 0
for r in rows:
    for k, im in enumerate(r): sheet.paste(im, (k*(w+8), y))
    y += max(i.height for i in r) + 8
sheet.save(out, quality=85)
