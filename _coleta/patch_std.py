# Liga as fotos padronizadas (img/std) ao site: lista em js/std.js, cards, produto, home e ordem do catálogo
import os, re, glob
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site'))


def rd(p):
    return open(p, encoding='utf-8').read()


def wr(p, s):
    open(p, 'w', encoding='utf-8').write(s)


def sub(s, old, new):
    assert old in s, old[:70]
    return s.replace(old, new)


ids = sorted(os.path.basename(f)[:-5] for f in glob.glob('img/std/*.webp') if not f.endswith('_t.webp'))
# peças cuja foto original já é limpa: entram na vitrine sem foto nova
LIMPAS = ['1910184', '1914792', '1910183', '1910186']
wr('js/std.js', '/* fotos padronizadas (img/std) e peças que já têm foto limpa */\nwindow.BK_STD=%s;\nwindow.BK_LIMPAS=%s;\n' % (ids, LIMPAS))

s = rd('js/app.js')
if 'BK_STD' not in s:
    s = sub(s, "  const img = (p, k = 0, t = true) => `img/p/${p.id}_${k}${t ? '_t' : ''}.webp`;",
            "  const STD = new Set(window.BK_STD || []);\n"
            "  /* peça padronizada: a foto limpa vem primeiro e as originais seguem depois */\n"
            "  const nf = p => p.i + (STD.has(p.id) ? 1 : 0);\n"
            "  const img = (p, k = 0, t = true) => STD.has(p.id)\n"
            "    ? (k === 0 ? `img/std/${p.id}${t ? '_t' : ''}.webp` : `img/p/${p.id}_${k - 1}${t ? '_t' : ''}.webp`)\n"
            "    : `img/p/${p.id}_${k}${t ? '_t' : ''}.webp`;")
    s = sub(s, "${p.i > 1 ? `<img src=\"${img(p, 1)}\" alt=\"\" loading=\"lazy\">` : ''}", "${nf(p) > 1 ? `<img src=\"${img(p, 1)}\" alt=\"\" loading=\"lazy\">` : ''}")
    s = sub(s, "Array.from({ length: p.i }, (_, k)", "Array.from({ length: nf(p) }, (_, k)")
    s = sub(s, "${p.i <= 2 ? ' one' : ''}", "${nf(p) <= 2 ? ' one' : ''}")
    wr('js/app.js', s)

s = rd('js/home.js')
s = sub(s, "['Jaquetas & Moletons', 'img/look/ig2.webp']", "['Jaquetas & Moletons', 'img/std/1914784.webp']")
s = sub(s, "['Bermudas & Shorts', 'img/p/1703197_0.webp']", "['Bermudas & Shorts', 'img/std/1703197.webp']")
s = sub(s, "['Camisetas', 'img/p/1688777_0.webp']", "['Camisetas', 'img/std/1688777.webp']")
s = sub(s, "['Acessórios', 'img/p/1849734_1.webp']", "['Acessórios', 'img/std/1849734.webp']")
a = s.index("  const dest = [")
b = s.index("\n", s.index("$('#rail').innerHTML", a))
s = s[:a] + ("  const dest = ['1914786', '1910184', '1914792', '1910185', '1679459', '1849734', '1703197', '1910183',\n"
             "    '1849694', '1914784', '1910182', '1688777', '1701345', '1703193', '1703189', '1849982'];\n"
             "  $('#rail').innerHTML = dest.filter(id => byId[id]).map((id, i) => BK.card(byId[id], i < 4 ? 'Novo' : '')).join('');") + s[b:]
wr('js/home.js', s)

s = rd('index.html')
s = s.replace('<div class="rail" id="rail"></div>', '<div class="grid" id="rail"></div>')
s = s.replace('<h2 class="d">Novidades<br>da semana</h2>', '<h2 class="d">Seleção<br>BK</h2>')
if 'js/std.js' not in s:
    s = sub(s, '<script src="js/app.js', '<script src="js/std.js?v=9"></script>\n<script src="js/app.js')
wr('index.html', re.sub(r'\?v=\d+"', '?v=9"', s))

s = rd('catalogo.html')
if 'js/std.js' not in s:
    s = sub(s, '<script src="js/app.js', '<script src="js/std.js?v=9"></script>\n<script src="js/app.js')
    # ordem padrão: peças com foto limpa primeiro
    s = sub(s, "  const BK = window.BK, P = BK.P, $ = s => document.querySelector(s);\n  const cats",
            "  const top = new Set([...(window.BK_STD || []), ...(window.BK_LIMPAS || [])]);\n"
            "  const BK = window.BK, P = [...BK.P].sort((a, b) => top.has(b.id) - top.has(a.id)), $ = s => document.querySelector(s);\n  const cats")
wr('catalogo.html', re.sub(r'\?v=\d+"', '?v=9"', s))
print(len(ids), 'padronizadas')
