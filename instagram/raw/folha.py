from PIL import Image, ImageOps, ImageDraw
import glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
fs = sorted(glob.glob('m_*.jpg'))
t = 360
S = Image.new('RGB', (len(fs) * t, int(t * 1.25)), 'white')
d = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB')
    print(f, im.size)
    S.paste(ImageOps.fit(im, (t, int(t * 1.25)), centering=(0.5, 0.2)), (i * t, 0))
    d.text((i * t + 6, 6), f[2:-4], fill='yellow')
S.save('_folha.jpg', quality=84)
