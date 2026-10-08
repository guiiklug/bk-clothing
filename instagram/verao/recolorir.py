"""Troca o fundo dos vídeos de verão por código (sem gerar de novo): recorta a peça quadro a quadro
e compõe sobre uma cor chapada, com uma sombra suave embaixo.

Uso:  python recolorir.py
Os originais (fundo vermelho e azul forte) ficam guardados em raw/ com o sufixo -cor-antiga.
"""
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from rembg import remove, new_session

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
ALVOS = {'tee': '#dce8ef', 'conjunto': '#e6dfd0'}     # azul esbranquiçado e areia clara
ses = new_session('isnet-general-use')

for nome, cor in ALVOS.items():
    antigo = AQUI / 'raw' / f'v-{nome}-cor-antiga.mp4'
    atual = AQUI / 'raw' / f'v-{nome}.mp4'
    if not antigo.exists():
        shutil.copy(atual, antigo)
    qd = AQUI / 'raw' / f'_q-{nome}'
    shutil.rmtree(qd, ignore_errors=True)
    qd.mkdir()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(antigo), str(qd / 'a%04d.png')], check=True)
    quadros = sorted(qd.glob('a*.png'))
    for n, f in enumerate(quadros):
        im = Image.open(f).convert('RGB')
        rec = remove(im, session=ses)
        alfa = rec.getchannel('A')
        caixa = alfa.point(lambda v: 255 if v > 40 else 0).getbbox()
        fundo = Image.new('RGB', im.size, cor)
        if caixa:
            x0, y0, x1, y1 = caixa
            som = Image.new('L', im.size, 0)
            larg = (x1 - x0) * 0.62
            cx, cy = (x0 + x1) / 2, min(im.height - 40, y1 + 70)
            ImageDraw.Draw(som).ellipse([cx - larg / 2, cy - 16, cx + larg / 2, cy + 16], fill=70)
            som = som.filter(ImageFilter.GaussianBlur(22))
            fundo.paste(Image.new('RGB', im.size, '#20262b'), (0, 0), som)
        fundo.paste(rec, (0, 0), alfa)
        fundo.save(qd / f'b{n + 1:04d}.png')
        f.unlink()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '24', '-i', str(qd / 'b%04d.png'), '-c:v', 'libx264',
                    '-crf', '17', '-preset', 'slow', '-pix_fmt', 'yuv420p', str(atual)], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(atual), '-an', '-c:v', 'libx264', '-crf', '21', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(AQUI / 'videos' / f'{nome}.mp4')], check=True)
    Image.open(qd / 'b0001.png').save(AQUI / 'raw' / f'q-{nome}.png')     # capa do post no feed
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(atual), '-vf', 'fps=4/5,scale=300:-1,tile=4x1', '-frames:v', '1',
                    str(AQUI / 'raw' / f'_tira-{nome}.jpg')], check=True)
    shutil.rmtree(qd, ignore_errors=True)
    print('ok', nome, len(quadros))
