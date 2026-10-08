"""Recorta as peças da rodada de verão (fundo transparente) para compor sobre blocos de cor."""
import os
from pathlib import Path
from PIL import Image
from rembg import remove, new_session

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
(AQUI / 'cut').mkdir(exist_ok=True)
PIL_ = AQUI / '../../_coleta/piloto'
IMG = AQUI / '../../_coleta/img'
FONTES = {
    'tee-diesel': PIL_ / '1688777.png', 'jeans': PIL_ / '1703184.png', 'pochete': PIL_ / '1703193.png',
    'cargo-marrom': PIL_ / '1701345.png', 'cargo-off': PIL_ / '1703197.png', 'regata': PIL_ / '1690115.png',
    'conjunto-preto': PIL_ / '1849694.png', 'conjunto-branco': PIL_ / '1703189.png', 'bag': PIL_ / '1703192.png',
    'bermuda-high': PIL_ / '1688196.png', 'bermuda-lacoste': PIL_ / '1678831.png', 'tee-armani': PIL_ / '1849978.png',
    'polo-roads': IMG / '1914792_0.jpg', 'tee-comp': IMG / '1910183_0.jpg',
}
ses = new_session('isnet-general-use')
for nome, src in FONTES.items():
    dst = AQUI / 'cut' / f'{nome}.png'
    if dst.exists():
        continue
    im = Image.open(src).convert('RGB')
    out = remove(im, session=ses)
    box = out.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox()
    out = out.crop(box)
    out.save(dst)
    print(nome, out.size)
# folha de conferência sobre vermelho, para ver sobras de fundo
arqs = sorted((AQUI / 'cut').glob('*.png'))
t = 300
S = Image.new('RGB', (7 * t, 2 * t), '#e2372b')
for i, f in enumerate(arqs):
    im = Image.open(f)
    im.thumbnail((t - 20, t - 20))
    S.paste(im, ((i % 7) * t + (t - im.width) // 2, (i // 7) * t + (t - im.height) // 2), im)
S.save(AQUI / 'cut' / '_folha.jpg', quality=85)
print('ok', len(arqs))
