"""Monta uma folha de comparação de letras para os títulos do site2, sem mexer no site.
Uso:  python gerar.py   ->  letras.html e letras.jpg (e uma imagem por opção em opcoes/)"""
from pathlib import Path
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
(AQUI / 'opcoes').mkdir(exist_ok=True)
# (letra, nome, família CSS, regras extras, tamanho base em px, observação curta)
OPC = [
    ('A', 'Archivo Expanded (atual)', "'Archivo'", 'font-weight:900;font-stretch:125%;letter-spacing:-.025em', 64, 'Larga e pesada. É a que está no site e no feed de verão.'),
    ('B', 'Bebas Neue', "'Bebas Neue'", 'font-weight:400;letter-spacing:.01em', 104, 'Alta e estreita. É a letra do "CLOTHING" da logo.'),
    ('C', 'Anton', "'Anton'", 'font-weight:400;letter-spacing:.005em', 92, 'Estreita e bem mais pesada que a Bebas. Cara de pôster.'),
    ('D', 'Big Shoulders Display', "'Big Shoulders Display'", 'font-weight:900;letter-spacing:.005em', 100, 'Estreita, industrial, com cantos retos. Lembra placa e uniforme.'),
    ('E', 'Barlow Condensed itálica', "'Barlow Condensed'", 'font-weight:800;font-style:italic;letter-spacing:-.005em', 96, 'Inclinada, esportiva. Puxa para camisa de time.'),
    ('F', 'Syne', "'Syne'", 'font-weight:800;letter-spacing:-.03em', 70, 'Larga com desenho próprio (olha o G e o S). A mais autoral.'),
    ('G', 'Unbounded', "'Unbounded'", 'font-weight:800;letter-spacing:-.03em', 58, 'Larga e arredondada. Mais macia, menos agressiva.'),
    ('H', 'Bricolage Grotesque', "'Bricolage Grotesque'", 'font-weight:800;font-stretch:75%;letter-spacing:-.03em', 88, 'Meio-termo: compacta, com detalhes irregulares de letra impressa.'),
    ('I', 'Syncopate', "'Syncopate'", 'font-weight:700;letter-spacing:-.02em', 56, 'Muito larga e fina no traço. Cara de marca de moda.'),
]
FONTES = ('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Bebas+Neue&family=Anton'
          '&family=Big+Shoulders+Display:wght@900&family=Barlow+Condensed:ital,wght@1,800&family=Syne:wght@800&family=Unbounded:wght@800'
          '&family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,800&family=Syncopate:wght@700&family=Jost:wght@200&display=swap')
LINHAS = ['Bermudas & Shorts', 'Calças', 'Conjuntos', 'Acessórios']


def painel(l, nome, fam, extra, tam, obs):
    linhas = ''.join(f'<div class="ln{" on" if t == "Conjuntos" else ""}"><span class="n">{i + 5:02d}</span><b>{t}</b></div>' for i, t in enumerate(LINHAS))
    return f'''<section class="op" id="op-{l}" style="--f:{fam};--t:{tam}px">
  <header><span class="le">{l}</span><span class="no">{nome}</span><span class="ob">{obs}</span></header>
  <div class="hero"><b style="{extra}">Vista<br>estilo.</b></div>
  <div class="lista" style="--e:1"><style>#op-{l} b{{{extra}}}</style>{linhas}</div>
</section>'''


CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#cfcbc2;font-family:'Archivo',sans-serif;color:#0b0b0b;padding:16px;display:grid;grid-template-columns:repeat(3,820px);gap:16px;width:max-content}
.op{background:#f3f0ea;width:820px;padding:26px 30px 30px}
.op header{display:grid;grid-template-columns:auto 1fr;gap:2px 14px;align-items:baseline;padding-bottom:16px;border-bottom:1.5px solid #0b0b0b}
.le{grid-row:1/3;font-weight:900;font-stretch:125%;font-size:44px;line-height:1}
.no{font-weight:600;font-size:19px}.ob{font-size:14.5px;color:#5d574e}
.op b{font-family:var(--f);text-transform:uppercase;line-height:.9;font-size:var(--t);display:block;white-space:nowrap}
.hero{background:#dce8ef;margin:16px 0 4px;padding:22px 22px 26px}
.hero b{font-size:calc(var(--t)*1.25);line-height:.86}
.ln{display:grid;grid-template-columns:44px 1fr;align-items:center;padding:13px 0;border-bottom:1px solid rgba(11,11,11,.16)}
.ln.on{background:#dce8ef;padding-left:16px}
.n{font-size:12px;color:#676157;font-weight:500;letter-spacing:.1em}
'''
html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>BK Clothing | opções de letra</title><link href="{FONTES}" rel="stylesheet">'
        f'<style>{CSS}</style></head><body>' + ''.join(painel(*o) for o in OPC) + '</body></html>')
(AQUI / 'letras.html').write_text(html, encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 2540, 'height': 1400})
    pg.goto((AQUI / 'letras.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(2500)
    # encolhe a letra de cada painel se a linha mais longa passar da largura
    pg.evaluate('''() => document.querySelectorAll('.op').forEach(op => {
        const b = op.querySelector('.lista b'); const max = 820 - 60 - 44;
        if (b.scrollWidth > max) op.style.setProperty('--t', (parseFloat(getComputedStyle(op).getPropertyValue('--t')) * max / b.scrollWidth) + 'px'); })''')
    pg.wait_for_timeout(300)
    print(pg.evaluate("[...document.querySelectorAll('.op')].map(o => o.id + ':' + document.fonts.check('40px ' + getComputedStyle(o).getPropertyValue('--f'))).join(' ')"))
    pg.screenshot(path=str(AQUI / 'letras.jpg'), type='jpeg', quality=88, full_page=True)
    for o in OPC:
        pg.locator(f'#op-{o[0]}').screenshot(path=str(AQUI / 'opcoes' / f'{o[0]}.jpg'), type='jpeg', quality=90)
    b.close()
print('ok')
