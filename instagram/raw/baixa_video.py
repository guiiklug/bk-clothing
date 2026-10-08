"""Baixa os quadros iniciais e os vídeos do Higgsfield e monta uma folha para conferir."""
import os, sys, subprocess, urllib.request
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
B = 'https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/'
ARQ = {
    'q-bomber.png': 'hf_20261008_004634_d7729c9c-3633-4355-998a-446ce4ada54c.png',
    'q-mochila.png': 'hf_20261008_004634_eadb8140-8bf6-4037-ada7-85b2d87d4573.png',
    'q-arara.png': 'hf_20261008_004635_7ecd0358-bbaf-42ac-ad82-6019e0b6f74e.png',
}
for a in sys.argv[1:]:          # pares nome=arquivo-remoto para os vídeos
    k, v = a.split('=', 1)
    ARQ[k] = v
for nome, rem in ARQ.items():
    if not os.path.exists(nome):
        urllib.request.urlretrieve(B + rem, nome)
qs = sorted(f for f in os.listdir('.') if f.startswith('q-') and f.endswith('.png'))
t = 400
S = Image.new('RGB', (len(qs) * t, int(t * 16 / 9)), 'white')
for i, f in enumerate(qs):
    im = Image.open(f).convert('RGB')
    print(f, im.size)
    S.paste(im.resize((t, int(t * 16 / 9))), (i * t, 0))
S.save('_quadros.jpg', quality=85)
vs = sorted(f for f in os.listdir('.') if f.startswith('v-') and f.endswith('.mp4'))
for v in vs:                    # 4 quadros de cada vídeo numa tira
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', v, '-vf', 'fps=4/5,scale=300:-1,tile=4x1', '-frames:v', '1', f'_tira-{v[2:-4]}.jpg'])
print('videos', vs)
