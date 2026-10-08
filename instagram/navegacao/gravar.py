"""Grava o vídeo de navegação no Instagram da BK, quadro a quadro, e junta com o beat.

Uso:  python beat.py
      python gravar.py verao      (ou: inverno)
Saída: navegacao-verao.mp4 (1080x1920, 30 fps, com áudio). Nada é filmado em tempo real: o script
pede à página o estado de cada instante e tira uma foto, então a imagem sai nítida e sempre igual.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
QUAL = sys.argv[1] if len(sys.argv) > 1 else 'verao'
FPS = 30
VID = {'verao': {'tee': '../verao/raw/v-tee.mp4', 'conjunto': '../verao/raw/v-conjunto.mp4'},
       'inverno': {'bomber': '../raw/v-bomber.mp4', 'mochila': '../raw/v-mochila.mp4', 'arara': '../raw/v-arara.mp4'}}[QUAL]

# vídeos com todos os quadros-chave, para a página conseguir pular para qualquer instante
(AQUI / 'tmp').mkdir(exist_ok=True)
for nome, src in VID.items():
    dst = AQUI / 'tmp' / f'{nome}.mp4'
    if not dst.exists():
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-an', '-vf', 'scale=720:-2', '-c:v', 'libx264',
                        '-g', '1', '-crf', '17', '-pix_fmt', 'yuv420p', str(dst)], check=True)

qd = AQUI / 'tmp' / f'q-{QUAL}'
shutil.rmtree(qd, ignore_errors=True)
qd.mkdir(parents=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True, args=['--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': 360, 'height': 640}, device_scale_factor=3)
    pg.goto((AQUI / 'app.html').as_uri() + f'?id={QUAL}')
    pg.evaluate('document.fonts.ready')
    pg.wait_for_function('[...document.images].every(i => i.complete && i.naturalWidth > 0)', timeout=30000)
    pg.wait_for_timeout(800)
    dur = pg.evaluate('window.DUR')
    total = int(dur * FPS)
    for f in range(total):
        pg.evaluate('t => window.render(t)', f / FPS)
        pg.screenshot(path=str(qd / f'{f:04d}.jpg'), type='jpeg', quality=93)
    b.close()
print('quadros', total)

saida = AQUI / f'navegacao-{QUAL}.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(qd / '%04d.jpg'), '-i', 'beat.wav',
                '-c:v', 'libx264', '-crf', '19', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                '-shortest', '-movflags', '+faststart', str(saida)], check=True)

# folha de conferência: 12 quadros espalhados
idx = [int(total * k / 12) for k in range(12)]
S = Image.new('RGB', (6 * 270, 2 * 480))
for n, i in enumerate(idx):
    S.paste(Image.open(qd / f'{i:04d}.jpg').resize((270, 480)), ((n % 6) * 270, (n // 6) * 480))
S.save(AQUI / f'_conf-{QUAL}.jpg', quality=85)
shutil.rmtree(qd, ignore_errors=True)
print('ok', saida.name, round(saida.stat().st_size / 1e6, 1), 'MB')
