# Leva para o site2 as ideias vistas na Maze: barra de avisos, item do menu em destaque, categorias com
# peça recortada ao lado de um banner, e vitrines por categoria com banner lateral e carrossel. Roda uma vez.
import re
from pathlib import Path
S2 = Path(__file__).resolve().parent.parent / 'site2'


def rd(p):
    return (S2 / p).read_text(encoding='utf-8')


def wr(p, s):
    (S2 / p).write_text(s, encoding='utf-8')


def sub(s, a, b, n=1):
    assert a in s, a[:70]
    return s.replace(a, b, n)


# script compartilhado: barra de avisos e nome do primeiro item do menu
s = rd('js/app.js')
s = sub(s, "['index.html#selecao', 'Seleção']", "['index.html#selecao', 'Drops']")
if 'class="tb' not in s:
    s = sub(s, '<header class="hd', '<div class="tb rot"><div><span>Enviamos para todo o Brasil</span><span>Pix, cartão ou a combinar</span>'
            '<span>Retire na loja do Floresta</span><span>Novidades primeiro no grupo VIP</span></div></div>\n  <header class="hd')
wr('js/app.js', s)

# estilos novos
css = rd('css/style.css')
if '/* ideias da Maze */' not in css:
    css = sub(css, ".hd{position:fixed;inset:0 0 auto 0;", ".hd{position:fixed;inset:var(--tb) 0 auto 0;")
    css = sub(css, ".hero{padding-top:4.75rem;", ".hero{padding-top:calc(4.75rem + var(--tb));")
    css = sub(css, ".bar{position:sticky;top:4.6rem;", ".bar{position:sticky;top:calc(4.6rem + var(--tb));")
    css = sub(css, "  .bar{top:4.6rem}", "  .bar{top:calc(4.6rem + var(--tb))}")
    css = sub(css, ".cat-top{padding:8rem var(--pad) 2rem;", ".cat-top{padding:calc(8rem + var(--tb)) var(--pad) 2rem;")
    css = sub(css, "  .cat-top{padding-top:7rem}", "  .cat-top{padding-top:calc(7rem + var(--tb))}")
    css = sub(css, "@media (max-width:1100px){", r'''/* ideias da Maze */
:root{--tb:2.15rem}
.tb{position:fixed;inset:0 0 auto 0;height:var(--tb);z-index:51;background:#0b0b0b;color:#f3f0ea;overflow:hidden;display:flex;align-items:center;font-size:.7rem}
.tb div{display:flex;justify-content:center;gap:clamp(1.5rem,4vw,4.5rem);width:100%;white-space:nowrap}
.tb span+span::before{content:"";display:inline-block;width:.3rem;height:.3rem;border-radius:50%;background:#c5d6e1;margin-right:clamp(1.5rem,4vw,4.5rem);vertical-align:middle}
.hd nav a:first-child{background:var(--fg);color:var(--bg);padding:.5rem .95rem}
.hd nav a:first-child::after{display:none}
.hd nav a:first-child:hover{background:var(--accent)}
/* categorias: peça recortada com nome embaixo, ao lado de um banner */
.catg{display:grid;grid-template-columns:1.25fr 1fr;gap:clamp(1.5rem,3vw,3.5rem);align-items:stretch}
.catg .gr{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem .6rem;align-content:space-between}
.catg .gr a{display:grid;justify-items:center;gap:.7rem;text-align:center}
.catg .gr .im{width:100%;aspect-ratio:1/1;display:grid;place-items:center;transition:background .35s}
.catg .gr img{width:74%;height:74%;object-fit:contain;filter:drop-shadow(0 .8rem .9rem rgba(0,0,0,.2));transition:transform .5s var(--ease)}
.catg .gr a:hover .im{background:var(--t1)}
.catg .gr a:nth-child(3n+2):hover .im{background:var(--t2)}.catg .gr a:nth-child(3n):hover .im{background:var(--t3)}
.catg .gr a:hover img{transform:scale(1.1) rotate(-5deg)}
.catg .gr small{color:var(--mute);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;display:block;margin-top:.15rem}
/* banner: faixa preta com a palavra em pé e uma imagem ao lado */
.bn{position:relative;display:grid;grid-template-columns:minmax(4.2rem,21%) 1fr;overflow:hidden;background:#0b0b0b;color:#f3f0ea;min-height:24rem}
.bn .pal{position:relative}
.bn .pal b{position:absolute;left:50%;bottom:1.2rem;transform-origin:0 100%;transform:rotate(-90deg) translate(0,50%);font-family:var(--display);font-weight:900;font-stretch:125%;text-transform:uppercase;letter-spacing:-.02em;line-height:1;white-space:nowrap;font-size:var(--tp,4.2rem)}
.bn .md{position:relative;overflow:hidden;background:var(--t1)}
.bn .md>img.ft,.bn .md>video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}
.bn:hover .md>img.ft,.bn:hover .md>video{transform:scale(1.04)}
.bn .md .pc{position:absolute;filter:drop-shadow(0 1.4rem 1.6rem rgba(0,0,0,.26));transition:transform .8s var(--ease)}
.bn:hover .md .pc{transform:var(--h)}
.bn .mk{position:absolute;right:.9rem;bottom:.9rem;color:#0b0b0b;z-index:2}.bn .mk.w{color:#f3f0ea}
.bn .mk .logo{width:2.4rem;height:2.8rem}.bn .mk .logo b{font-size:1.1rem}.bn .mk .logo i{font-size:.5rem}
/* vitrine: banner de um lado, carrossel do outro */
.vit{display:grid;grid-template-columns:minmax(15rem,.9fr) 2.4fr;gap:.6rem;align-items:stretch}
.vit.inv{grid-template-columns:2.4fr minmax(15rem,.9fr)}.vit.inv .bn{order:2}
.vit .lado{min-width:0;display:flex;flex-direction:column}
.vit .topo{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;padding:0 0 1.1rem .4rem}
.vit .topo h2{font-size:min(3.2rem,7vw)}
.setas{display:flex;gap:.4rem}
.setas button{width:3rem;height:3rem;border:1.5px solid var(--fg);display:grid;place-items:center;font-size:1.1rem;transition:.25s}
.setas button:hover{background:var(--fg);color:var(--bg)}
.trilho{display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 1.2rem)/3);gap:.6rem;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;flex:1}
.trilho::-webkit-scrollbar{display:none}
.trilho>*{scroll-snap-align:start}
.vit .card .ph{aspect-ratio:4/4.6}
@media (max-width:1100px){''')
    css = sub(css, "  .hd nav{display:none}.burger{display:grid}", "  .hd nav{display:none}.burger{display:grid}\n  .tb div{justify-content:flex-start;width:max-content;animation:mq 26s linear infinite;padding-left:100%}\n"
              "  .catg{grid-template-columns:1fr}.catg .gr{gap:1.2rem .4rem}\n  .vit,.vit.inv{grid-template-columns:1fr}.vit.inv .bn{order:0}.bn{min-height:15rem}.vit .bn{aspect-ratio:16/10;min-height:0}\n"
              "  .trilho{grid-auto-columns:62%}.vit .topo{padding:1.2rem 0 .9rem}")
    wr('css/style.css', css)

for f in ['catalogo.html', 'links.html']:
    wr(f, re.sub(r'\?v=\d+"', '?v=30"', rd(f)))
print('ok')
