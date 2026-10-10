"""Criativo de venda do drop de bermudas: vídeo vertical 1080x1920, 15 s, cortes no tempo do beat (140 BPM).

Uso:  python criativo.py   ->  criativo/drop-bermudas.mp4
Tudo por código, quadro a quadro: recortes das três cores, o vídeo da preta girando, as fotos reais
tiradas na loja e o beat de instagram/navegacao/beat.wav. Sem preço e sem crédito de geração.
"""
import os
import shutil
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
SAIDA = AQUI / 'criativo'
SAIDA.mkdir(exist_ok=True)
FPS, DUR = 30, 15.0
B = 60 / 140                     # um tempo do beat

intra = SAIDA / '_giro.mp4'      # todos os quadros como quadro-chave, para a página pular para qualquer instante
if not intra.exists():
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'video/bruto.mp4', '-an', '-c:v', 'libx264', '-g', '1', '-crf', '16',
                    '-pix_fmt', 'yuv420p', str(intra)], check=True)
for n in ('17', '20', '22'):
    dst = SAIDA / f'_loja{n}.jpg'
    if not dst.exists():
        Image.open(AQUI / 'orig' / f'{n}.webp').convert('RGB').save(dst, quality=92)

HTML = '''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Big+Shoulders+Display:wght@900&family=Bebas+Neue&family=Jost:wght@200&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0b0b0b;font-family:"Archivo",sans-serif}
.c{position:absolute;inset:0;overflow:hidden;visibility:hidden}
.w{position:absolute;font-family:"Big Shoulders Display","Archivo",sans-serif;font-weight:900;text-transform:uppercase;letter-spacing:0;line-height:.84;white-space:nowrap;will-change:transform}
.pc{position:absolute;height:auto;filter:drop-shadow(0 40px 44px rgba(0,0,0,.34));will-change:transform}
.ft,video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;will-change:transform}
.veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,11,.5) 0,rgba(11,11,11,0) 30%,rgba(11,11,11,0) 55%,rgba(11,11,11,.78) 100%)}
.rot{position:absolute;left:64px;font-weight:600;font-size:40px;letter-spacing:.14em;text-transform:uppercase}
.lg{position:relative;display:inline-grid;place-items:center;width:1.9em;height:2.2em;padding:.24em 0 .14em;line-height:1;font-size:52px}
.lg::before,.lg::after{content:"";position:absolute;top:0;bottom:0;width:32%;border:.045em solid currentColor}
.lg::before{left:0;border-right:0}.lg::after{right:0;border-left:0}
.lg b{font-family:"Jost";font-weight:200;font-size:.92em;letter-spacing:.06em;margin-top:.14em}
.lg i{font-family:"Bebas Neue";font-style:normal;font-size:.39em;letter-spacing:.08em;margin-top:-.1em}
.mk{position:absolute;left:64px;top:260px}
#cta{position:absolute;left:0;right:0;top:1330px;height:230px;background:#0b0b0b;color:#f3f0ea;display:grid;place-items:center;font-family:"Big Shoulders Display";font-weight:900;font-size:128px;text-transform:uppercase;letter-spacing:.01em}
</style></head><body>
<div class="c" id="s1" style="background:#0b0b0b;color:#f3f0ea"><div class="w" id="w1" style="font-size:340px;left:64px;top:700px">Drop</div></div>
<div class="c" id="s2" style="background:#dce8ef;color:#0b0b0b"><div class="w" id="w2" style="font-size:320px;left:64px;top:700px">Novo</div></div>
<div class="c" id="s3" style="background:#dce8ef;color:#0b0b0b"><div class="w" style="font-size:250px;left:60px;top:270px">Preta</div><img class="pc" id="p3" src="cut/preta.png" style="width:960px;left:540px;top:1080px"></div>
<div class="c" id="s4" style="background:#0b0b0b;color:#f3f0ea"><div class="w" style="font-size:312px;left:60px;top:260px">Gelo</div><img class="pc" id="p4" src="cut/cinza.png" style="width:940px;left:540px;top:1080px"></div>
<div class="c" id="s5" style="background:#e6dfd0;color:#0b0b0b"><div class="w" style="font-size:240px;left:60px;top:270px">Verde</div><img class="pc" id="p5" src="cut/verde.png" style="width:960px;left:540px;top:1080px"></div>
<div class="c" id="s6" style="background:#dce8ef;color:#0b0b0b"><video id="v" src="criativo/_giro.mp4" muted playsinline preload="auto"></video><div class="mk"><span class="lg"><b>BK</b><i>CLOTHING</i></span></div><div class="rot" style="top:1500px">Bermuda de basquete</div></div>
<div class="c" id="s7" style="color:#f3f0ea"><img class="ft" id="f7" src="cut/textura.jpg"><div class="veu"></div><div class="w" id="w7" style="font-size:230px;left:64px;top:1180px">De<br>perto</div></div>
<div class="c" id="s8" style="color:#f3f0ea"><img class="ft" id="f8a" src="criativo/_loja20.jpg"><img class="ft" id="f8b" src="criativo/_loja22.jpg"><div class="veu"></div><div class="w" id="w8" style="font-size:230px;left:64px;top:1180px">Já na<br>loja</div></div>
<div class="c" id="s9" style="background:#f3f0ea;color:#0b0b0b"><div class="w" style="font-size:212px;left:60px;top:270px">Qual leva?</div>
  <img class="pc" id="q1" src="cut/cinza.png" style="width:560px;left:290px;top:900px"><img class="pc" id="q2" src="cut/verde.png" style="width:560px;left:790px;top:880px"><img class="pc" id="q3" src="cut/preta.png" style="width:600px;left:540px;top:1090px">
  <div id="cta">Chama no direct</div></div>
<div class="c" id="s10" style="background:#0b0b0b;color:#f3f0ea;display:grid;place-items:center;text-align:center"><div><span class="lg" style="font-size:170px"><b>BK</b><i>CLOTHING</i></span>
  <p style="margin-top:70px;font-size:46px;font-weight:600;letter-spacing:.1em">@bkclothiing</p><p style="margin-top:22px;font-size:32px;letter-spacing:.08em;opacity:.75">Rua Santa Catarina, 2348 · Joinville</p></div></div>
<script>
const B=60/140,$=s=>document.querySelector(s);
const sai=x=>{x=Math.max(0,Math.min(1,x));return 1-Math.pow(1-x,3)};
const volta=x=>{x=Math.max(0,Math.min(1,x));const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
// cenas em tempos do beat: [início, fim]
const T={s1:[0,2],s2:[2,4],s3:[4,6],s4:[6,8],s5:[8,10],s6:[10,18],s7:[18,22],s8:[22,26],s9:[26,32],s10:[32,36]};
window.DUR=36*B;
const v=$('#v');
async function busca(t){if(Math.abs(v.currentTime-t)<.004)return;await new Promise(r=>{v.addEventListener('seeked',r,{once:true});v.currentTime=t})}
const soco=(el,k)=>{el.style.transform=`scale(${1+.55*(1-sai(k/.22))})`;el.style.transformOrigin='0 60%'};
const peca=(el,k,rot)=>{const e=volta(k/.34);el.style.transform=`translate(-50%,-50%) scale(${.72+.28*e}) rotate(${rot-(1-e)*12}deg)`};
window.render=async t=>{
  for(const [id,[a,b]] of Object.entries(T))$('#'+id).style.visibility=(t>=a*B&&t<b*B)?'visible':'hidden';
  const k=id=>t-T[id][0]*B;
  soco($('#w1'),k('s1'));soco($('#w2'),k('s2'));
  peca($('#p3'),k('s3'),-6);peca($('#p4'),k('s4'),5);peca($('#p5'),k('s5'),-5);
  if(t>=T.s6[0]*B&&t<T.s6[1]*B)await busca(Math.min(4.9,k('s6')*1.4));
  $('#f7').style.transform=`scale(${1.05+.12*k('s7')/(4*B)})`;soco($('#w7'),k('s7'));
  const meio=k('s8')>=2*B;$('#f8a').style.visibility=meio?'hidden':'inherit';$('#f8b').style.visibility=meio?'inherit':'hidden';
  const z=1.04+.08*((k('s8')%(2*B))/(2*B));$('#f8a').style.transform=$('#f8b').style.transform=`scale(${z})`;soco($('#w8'),k('s8'));
  [['#q1',0,-10],['#q2',1,10],['#q3',2,2]].forEach(([s,n,rot])=>{const kk=k('s9')-n*B,e=volta(kk/.36);$(s).style.opacity=kk>=0?1:0;
    $(s).style.transform=`translate(-50%,-50%) translateY(${(1-e)*-700}px) rotate(${rot+(1-e)*14}deg)`});
  const c=sai((k('s9')-3*B)/.3);$('#cta').style.transform=`translateY(${(1-c)*700}px)`;
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
};
</script></body></html>'''
(AQUI / 'criativo.html').write_text(HTML, encoding='utf-8')

qd = SAIDA / '_q'
shutil.rmtree(qd, ignore_errors=True)
qd.mkdir()
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True, args=['--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto((AQUI / 'criativo.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_function('[...document.images].every(i => i.complete && i.naturalWidth > 0) && document.querySelector("video").readyState >= 2', timeout=30000)
    pg.wait_for_timeout(800)
    # a letra do Bruno (Big Shoulders) é estreita: cada título cresce até a margem, com teto de 1,55x
    pg.evaluate('''() => document.querySelectorAll('.w').forEach(w => { const base = parseFloat(w.style.fontSize), max = 1080 - w.offsetLeft - 56;
        w.style.fontSize = Math.floor(Math.min(base * (w.querySelector('br') ? 1.25 : 1.55), base * max / w.offsetWidth)) + 'px' })''')
    dur = pg.evaluate('window.DUR')
    total = int(dur * FPS)
    for f in range(total):
        pg.evaluate('t => window.render(t)', f / FPS)
        pg.screenshot(path=str(qd / f'{f:04d}.jpg'), type='jpeg', quality=93)
    b.close()

final = SAIDA / 'drop-bermudas.mp4'
beat = AQUI.parent / 'instagram' / 'navegacao' / 'beat.wav'
cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(qd / '%04d.jpg')]
if beat.exists():       # o beat começa a bater no compasso 3 (3,43 s); os cortes do vídeo caem nos tempos
    cmd += ['-ss', '3.4286', '-t', f'{dur:.3f}', '-i', str(beat), '-af', f'afade=t=out:st={dur - 0.9:.2f}:d=0.9', '-c:a', 'aac', '-b:a', '192k']
cmd += ['-c:v', 'libx264', '-crf', '19', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-shortest', '-movflags', '+faststart', str(final)]
subprocess.run(cmd, check=True)
idx = [int(total * (k + .5) / 12) for k in range(12)]
S = Image.new('RGB', (12 * 180, 320))
for n, i in enumerate(idx):
    S.paste(Image.open(qd / f'{i:04d}.jpg').resize((180, 320)), (n * 180, 0))
S.save(SAIDA / '_conf.jpg', quality=86)
shutil.rmtree(qd, ignore_errors=True)
print('ok', round(dur, 2), 's', round(final.stat().st_size / 1e6, 1), 'MB')
