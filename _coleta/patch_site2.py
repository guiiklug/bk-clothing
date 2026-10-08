# Adapta os arquivos compartilhados do site2 (script, catálogo, links) à identidade nova. Roda uma vez.
import re
from pathlib import Path
S2 = Path(__file__).resolve().parent.parent / 'site2'
FONTE_NOVA = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Bebas+Neue'
              '&family=Jost:wght@200&display=swap" rel="stylesheet">')
TEMA = "<script>try{document.documentElement.dataset.theme=localStorage.getItem('bk_tema2')||'light'}catch(e){document.documentElement.dataset.theme='light'}</script>"


def rd(p):
    return (S2 / p).read_text(encoding='utf-8')


def wr(p, s):
    (S2 / p).write_text(s, encoding='utf-8')


def sub(s, a, b):
    assert a in s, a[:70]
    return s.replace(a, b)


s = rd('js/app.js')
s = sub(s, "const nav = [['index.html#lookbook', 'Lookbook'], ['catalogo.html', 'Catálogo'], ['index.html#como-comprar', 'Como comprar'], ['index.html#loja', 'A loja']];",
        "const nav = [['index.html#selecao', 'Seleção'], ['catalogo.html', 'Catálogo'], ['index.html#corpo', 'No corpo'], ['index.html#loja', 'A loja']];")
s = sub(s, '<a href="index.html#lookbook">Lookbook</a>', '<a href="index.html#corpo">No corpo</a>')
s = sub(s, "  const STD = new Set(window.BK_STD || []);",
        "  const STD = new Set(window.BK_STD || []);\n"
        "  /* peça com recorte: no card ela aparece solta sobre um bloco de cor da paleta */\n"
        "  const CUT = new Set(window.BK_CUT || []);\n"
        "  const bloco = p => CUT.has(p.id) ? ` ct\" style=\"--tc:var(--t${1 + (+p.id % 4)});--r:${(+p.id % 9) - 4}deg` : '';")
s = sub(s, '      <div class="ph">${tag ?', '      <div class="ph${bloco(p)}">${tag ?')
s = sub(s, '<img src="${img(p)}" alt="${titulo(p)}" loading="lazy" width="560" height="672">',
        '<img src="${CUT.has(p.id) ? `img/cut/${p.id}.webp` : img(p)}" alt="${titulo(p)}" loading="lazy">')
s = s.replace("localStorage.setItem('bk_tema', tema)", "localStorage.setItem('bk_tema2', tema)")
s = s.replace("tema === 'light' ? '#f6f4ef' : '#0b0b0b'", "tema === 'light' ? '#f3f0ea' : '#0b0b0b'")
s = re.sub(r'<h2 class="d" style="font-size:clamp\([^"]*\)">', '<h2 class="h2" style="font-size:min(3rem,7vw)">', s)
s = sub(s, "BK.P = P; BK.brl = brl; BK.wa = wa;", "BK.P = P; BK.brl = brl; BK.wa = wa; BK.CUT = CUT;")
wr('js/app.js', s)

for f in ['catalogo.html', 'links.html']:
    s = rd(f)
    s = re.sub(r'<link href="https://fonts.googleapis.com/css2[^>]*>', FONTE_NOVA, s)
    s = re.sub(r"<script>try\{var t=localStorage.getItem\('bk_tema'\)[^<]*</script>", TEMA, s)
    s = re.sub(r'\?v=\d+"', '?v=20"', s)
    s = s.replace('content="#0b0b0b"', 'content="#f3f0ea"')
    if f == 'catalogo.html':
        s = sub(s, '<script src="js/std.js?v=20"></script>', '<script src="js/std.js?v=20"></script>\n<script src="js/cut.js?v=20"></script>')
    else:
        s = s.replace("localStorage.setItem('bk_tema',t)", "localStorage.setItem('bk_tema2',t)")
    wr(f, s)
print('ok')
