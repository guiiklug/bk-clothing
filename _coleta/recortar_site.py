"""Prepara a pasta site2 (cópia do site atual) e recorta as peças com foto limpa para compor sobre cor.
Saída: site2/img/cut/ID.webp (fundo transparente) e site2/js/cut.js (lista dos ids recortados)."""
import shutil
from pathlib import Path
from PIL import Image
from rembg import remove, new_session

RAIZ = Path(__file__).resolve().parent.parent
S1, S2 = RAIZ / 'site', RAIZ / 'site2'
if not S2.exists():
    shutil.copytree(S1, S2)
CUT = S2 / 'img' / 'cut'
CUT.mkdir(parents=True, exist_ok=True)
fontes = {f.stem: f for f in (RAIZ / '_coleta' / 'piloto').glob('*.png')}
for i in ['1910184', '1914792', '1910183', '1910186']:          # peças cuja foto original já é limpa
    fontes[i] = RAIZ / '_coleta' / 'img' / f'{i}_0.jpg'
ses = new_session('isnet-general-use')
for i, src in sorted(fontes.items()):
    dst = CUT / f'{i}.webp'
    if dst.exists():
        continue
    out = remove(Image.open(src).convert('RGB'), session=ses)
    out = out.crop(out.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox())
    out.thumbnail((1100, 1100), Image.LANCZOS)
    out.save(dst, 'WEBP', quality=88)
    print(i, out.size)
ids = sorted(f.stem for f in CUT.glob('*.webp'))
(S2 / 'js' / 'cut.js').write_text('/* peças com recorte (img/cut), para compor sobre cor */\nwindow.BK_CUT=%s;\n' % ids, encoding='utf-8')
# vídeos de peça-chave
V = S2 / 'img' / 'video'
V.mkdir(exist_ok=True)
for nome, src in {'tee': 'instagram/verao/videos/tee.mp4', 'conjunto': 'instagram/verao/videos/conjunto.mp4', 'bomber': 'instagram/videos/bomber.mp4'}.items():
    shutil.copy(RAIZ / src, V / f'{nome}.mp4')
for nome, src in {'m1': '_coleta/img/1914792_1.jpg', 'm2': '_coleta/img/1914792_2.jpg', 'm3': 'instagram/raw/m_DYZwCrnkSnr.jpg',
                  'm4': 'instagram/raw/m_DYr4JXkEbkN.jpg', 'm5': 'instagram/raw/m_DYZvpUtEWYv.jpg'}.items():
    im = Image.open(RAIZ / src).convert('RGB')
    im.thumbnail((1400, 1800), Image.LANCZOS)
    im.save(S2 / 'img' / f'{nome}.webp', 'WEBP', quality=86)
print('ok', len(ids))
