"""Copia/otimiza as imagens usadas na apresentação (antes e depois, loja)."""
import pathlib
from PIL import Image
H = pathlib.Path(__file__).resolve().parent.parent; R = H.parent
O = H / "apresentacao" / "img"; O.mkdir(parents=True, exist_ok=True)
PARES = ["1914785", "1701345", "1690115", "1703184", "1703192", "1849694"]
def save(src, dst, w):
    im = Image.open(src).convert("RGB"); h = int(im.height * w / im.width)
    im.resize((w, h), Image.LANCZOS).save(dst, quality=88)
for i in PARES:
    save(R/"_coleta"/"img"/f"{i}_0.jpg", O/f"antes-{i}.jpg", 640)
    save(R/"_coleta"/"piloto"/f"{i}.png", O/f"depois-{i}.jpg", 640)
save(R/"site"/"img"/"loja.webp", O/"loja.jpg", 1000)
# prints: PNG 2x vira JPG para o HTML ficar leve
for p in O.glob("*-desktop-*.png"): save(p, p.with_suffix(".jpg"), 1600)
for p in O.glob("*-mobile-*.png"): save(p, p.with_suffix(".jpg"), 780)
save(O/"site-atual-desktop.png", O/"site-atual-desktop.jpg", 1440)
print("ok")

# recortes com a mesma proporção da moldura (nada é cortado de forma torta pelo object-fit)
def crop(src, dst, ratio, ax="left", ay="top", w_out=None):
    im = Image.open(src).convert("RGB"); W, H = im.size
    if W / H > ratio: cw, ch = int(H * ratio), H
    else: cw, ch = W, int(W / ratio)
    x = {"left": 0, "center": (W - cw)//2, "right": W - cw}[ax] if isinstance(ax, str) else ax
    y = {"top": 0, "center": (H - ch)//2, "bottom": H - ch}[ay] if isinstance(ay, str) else ay
    c = im.crop((x, y, x + cw, y + ch))
    if w_out: c = c.resize((w_out, int(c.height * w_out / c.width)), Image.LANCZOS)
    c.save(dst, quality=88)
R2 = 380/260
crop(O/"links-mobile-dark.png", O/"c-links.jpg", R2, w_out=760)
crop(O/"lookbook-desktop-dark.png", O/"c-lookbook.jpg", R2, w_out=1140)
crop(O/"produto-desktop-dark.png", O/"c-troca.jpg", R2, ax="right", ay=120, w_out=1140)
a, b = Image.open(O/"home-desktop-dark.png").convert("RGB"), Image.open(O/"home-desktop-light.png").convert("RGB")
s = a.copy(); s.paste(b.crop((a.width//2, 0, a.width, a.height)), (a.width//2, 0)); s.save(O/"_split.png")
crop(O/"_split.png", O/"c-tema.jpg", R2, ax="center", w_out=1140)
R3 = 522/408
crop(O/"produto-desktop-dark.png", O/"c-produto.jpg", R3, ax="right", w_out=1044)
crop(O/"sacola-desktop-dark.png", O/"c-sacola.jpg", R3, ax="right", w_out=1044)
crop(O/"home-desktop-dark.png", O/"c-home-d.jpg", 720/450, w_out=1440)
crop(O/"home-mobile-dark.png", O/"c-home-m.jpg", 296/640, w_out=592)
crop(O/"home-desktop-light.png", O/"c-home-d-l.jpg", 720/450, w_out=1440)
crop(O/"home-mobile-light.png", O/"c-home-m-l.jpg", 296/640, w_out=592)
for n in ("links-mobile", "lookbook-desktop", "produto-desktop", "sacola-desktop"):
    pass
# versões claras dos recortes
crop(O/"links-mobile-light.png", O/"c-links-l.jpg", R2, w_out=760)
crop(O/"lookbook-desktop-light.png", O/"c-lookbook-l.jpg", R2, w_out=1140)
crop(O/"produto-desktop-light.png", O/"c-troca-l.jpg", R2, ax="right", ay=120, w_out=1140)
crop(O/"produto-desktop-light.png", O/"c-produto-l.jpg", R3, ax="right", w_out=1044)
crop(O/"sacola-desktop-light.png", O/"c-sacola-l.jpg", R3, ax="right", w_out=1044)
print("recortes ok")
