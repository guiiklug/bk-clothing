"""Monta o vídeo 1080x1920 a 30 fps: quadros gravados + cabeçalho, destaques, zoom de câmera, dedo e legenda.

Lê _trabalho/gravacao/ (quadros.json, eventos.json) e a linha do tempo. Compõe com Pillow (Pool de 6),
grava JPEG em _trabalho/quadros_finais/ e codifica com ffmpeg (H.264 + voz AAC). Também faz folha-de-quadros.jpg.
Quando a gravação não tem quadro novo (o screencast só emite quando a tela muda), o quadro anterior se repete.
"""
import bisect
import json
import math
import multiprocessing as mp
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import linha_do_tempo as L  # noqa: E402
from falas import paginas  # noqa: E402

GRAV = AQUI / "_trabalho" / "gravacao"
FINAIS = AQUI / "_trabalho" / "quadros_finais"
ICONES = AQUI / "_trabalho" / "icones"
FONTES = AQUI / "fontes"
VOZ = AQUI.parent / "voz"
MP4 = AQUI / "bk-gestao-apresentacao.mp4"
FOLHA = AQUI / "folha-de-quadros.jpg"
LOGO = AQUI.parent.parent.parent / "_coleta" / "logo.jpg"

W, H, FPS = 1080, 1920, 30
PRETO, OFF, AREIA, CINZA = (11, 11, 11), (243, 240, 234), (200, 184, 154), (185, 178, 162)
JX, JY = 180, 300                  # janela do app (borda esquerda = borda do título)
JW, JH = 720, 1180
VW, VH = 390, 640                  # viewport gravado, em px CSS
ESC = JW / VW                       # px CSS -> px do vídeo
T_JANELA = 2.35                     # entrada da janela
HX, HY = 180, 120                   # cabeçalho: borda esquerda e topo
ICONE = 96
FOLGA_DEST = 8
ZOOM_MIN, ZOOM_MAX = 1.35, 1.5
ZOOM_FATOR = {"02": 1.0, "13": 1.0}   # 02 e 13: sem zoom (a lista de atenção e o resumo ocupam a largura toda; o zoom cortava os números e os rótulos)

# ---------- estado de cada processo
_est = {}


def ease(p):
    p = min(max(p, 0.0), 1.0)
    return 1 - (1 - p) ** 3


def clamp(p):
    return min(max(p, 0.0), 1.0)


def jost(tam, peso=500):
    f = ImageFont.truetype(str(FONTES / "Jost.ttf"), tam)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def bebas(tam):
    return ImageFont.truetype(str(FONTES / "BebasNeue-Regular.ttf"), tam)


def largura(txt, font, trk):
    return sum(font.getlength(c) + trk for c in txt) - (trk if txt else 0)


def texto_img(txt, font, cor, trk=0):
    """RGBA tight com o texto; (img, linha de base em y)."""
    asc, desc = font.getmetrics()
    w = int(math.ceil(largura(txt, font, trk))) + 4
    im = Image.new("RGBA", (w, asc + desc + 4), cor + (0,))
    d = ImageDraw.Draw(im)
    x = 2.0
    for c in txt:
        d.text((x, asc + 2), c, font=font, fill=cor + (255,), anchor="ls")
        x += font.getlength(c) + trk
    return im, asc + 2


def colar(tela, im, xy, alpha=1.0):
    if alpha <= 0:
        return
    if im.mode == "RGBA":
        m = im.getchannel("A")
        if alpha < 1:
            m = m.point(lambda v: int(v * alpha))
        tela.paste(im.convert("RGB"), xy, m)
    else:
        if alpha >= 1:
            tela.paste(im, xy)
        else:
            m = Image.new("L", im.size, int(255 * alpha))
            tela.paste(im, xy, m)


def anel(d, esp=4, borda=2, escala=4):
    """Anel de diâmetro externo d: traço areia de `esp` px com borda externa preta de `borda` px; miolo vazio."""
    n = int(d) + 2 * borda + 6
    big = Image.new("RGBA", (n * escala, n * escala), (0, 0, 0, 0))
    dr = ImageDraw.Draw(big)
    c, r = n * escala / 2, d / 2 * escala
    rb = r + borda * escala
    dr.ellipse([c - rb, c - rb, c + rb, c + rb], fill=PRETO + (255,))
    dr.ellipse([c - r, c - r, c + r, c + r], fill=(0, 0, 0, 0))
    dr.ellipse([c - r, c - r, c + r, c + r], outline=AREIA + (255,), width=int(esp * escala))
    dr.ellipse([c - r + esp * escala, c - r + esp * escala, c + r - esp * escala, c + r - esp * escala], fill=(0, 0, 0, 0))
    return big.resize((n, n), Image.LANCZOS)


# ---------- preparo (uma vez por processo)
def preparar():
    q = json.loads((GRAV / "quadros.json").read_text())
    ev = json.loads((GRAV / "eventos.json").read_text(encoding="utf-8"))
    e = _est
    e["ts"] = [x[0] for x in q]
    e["arq"] = [x[1] for x in q]
    e["ev"] = ev
    e["ult"] = (None, None)

    # logo real invertida (off-white sobre preto), margem recortada
    lg = Image.open(LOGO).convert("L")
    alfa = lg.point(lambda v: max(0, min(255, int((255 - v) * 1.15))))
    box = alfa.point(lambda v: 255 if v > 40 else 0).getbbox()
    alfa = alfa.crop(box)
    e["logo"] = Image.merge("RGBA", [Image.new("L", alfa.size, c) for c in OFF] + [alfa])

    # ícones
    e["icone"] = {}
    for b, (num, titulo, ic, sub) in L.BLOCOS.items():
        e["icone"][ic] = Image.open(ICONES / f"{ic}.png").convert("RGBA").resize((ICONE, ICONE), Image.LANCZOS)

    # cabeçalhos
    e["cab"] = {b: cabecalho(num, titulo) for b, (num, titulo, ic, sub) in L.BLOCOS.items()}

    # legendas por fala
    e["leg"] = {n: legenda_layout(n) for n in L.NUMS}
    e["leg_cache"] = {}

    # instante em que o cabeçalho de cada bloco entra
    ini = {0: T_JANELA}
    for n in L.NUMS:
        b = L.bloco_da_fala(n)
        if b not in ini and 1 <= b <= 10:
            ini[b] = L.S(n)
    e["blocos"] = sorted(ini.items(), key=lambda x: x[1])
    e["toques"] = montar_toques(ev["toques"])

    e["hl"] = [d for d in ev["destaques"] if d["visivel"]]
    e["zooms"] = montar_zooms([d for d in ev["destaques"] if d["zoom"]])
    e["selo"] = selo_simulado()


TX = HX + ICONE + 30       # início do texto do cabeçalho


def cabecalho(num, titulo):
    maxw = W - TX - 90
    tam = 104
    while tam > 40:
        f = bebas(tam)
        if largura(titulo, f, 1) <= maxw:
            break
        tam -= 2
    f = bebas(tam)
    im = Image.new("RGBA", (W - TX, 150), OFF + (0,))
    if num is not None:
        lin, bl = texto_img(f"{num:02d} / 10", jost(30, 500), AREIA, 4)
        im.alpha_composite(lin, (0, 30 - bl))
    t_img, tb = texto_img(titulo, f, OFF, 1)
    im.alpha_composite(t_img, (0, 132 - tb))
    return im


def selo_simulado():
    """Etiqueta SIMULADO: Bebas 36 areia, contorno de 2 px, sem fundo."""
    t_img, bl = texto_img("SIMULADO", bebas(36), AREIA, 3)
    px, py = 14, 8
    im = Image.new("RGBA", (t_img.width + 2 * px, t_img.height + 2 * py - 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).rectangle([0, 0, im.width - 1, im.height - 1], outline=AREIA + (255,), width=2)
    im.alpha_composite(t_img, (px, py - 4))
    return im


def legenda_layout(n):
    """Páginas da legenda: [{'ini': idx da 1ª palavra, 'tam', 'linhas': [[(palavra, idx)]]}]."""
    out, k = [], 0
    for pag in paginas(n):
        linhas = [[(w, k + j) for j, w in enumerate(l.split())] for l in pag]
        k0 = k
        for l in pag:
            k += len(l.split())
        tam = 60
        while tam > 30:
            f = jost(tam, 500)
            if all(largura(" ".join(w for w, _ in l), f, 0) <= 900 for l in linhas):
                break
            tam -= 2
        out.append({"ini": k0, "tam": tam, "linhas": linhas})
    return out


def img_pagina(n, pg, falados, todos=False):
    chave = (n, pg, 10 ** 6 if todos else falados)
    c = _est["leg_cache"]
    if chave in c:
        return c[chave]
    P = _est["leg"][n][pg]
    f = jost(P["tam"], 500)
    lh = int(P["tam"] * 1.22)
    im = Image.new("RGBA", (900, lh * len(P["linhas"]) + 20), OFF + (0,))
    d = ImageDraw.Draw(im)
    esp = f.getlength(" ")
    for i, l in enumerate(P["linhas"]):
        tw = largura(" ".join(w for w, _ in l), f, 0)
        x = (900 - tw) / 2
        for w, idx in l:
            cor = OFF if (todos or idx < falados) else CINZA
            d.text((x, i * lh + P["tam"] + 6), w, font=f, fill=cor + (255,), anchor="ls")
            x += f.getlength(w) + esp
    # y da última linha de base dentro da imagem (para ancorar a legenda embaixo)
    im.base_ultima = (len(P["linhas"]) - 1) * lh + P["tam"] + 6
    im.lh = lh
    if len(c) > 400:
        c.clear()
    c[chave] = im
    return im


def montar_toques(toques):
    """Segmentos do dedo: onde toca, quando começa a mover e quando some (None = o próximo toque vem logo)."""
    seg = []
    for tq in sorted(toques, key=lambda x: x["t_tap"]):
        ant = seg[-1] if seg else None
        encadeia = ant is not None and tq["t_tap"] - ant["t_tap"] < 0.8
        if ant is not None:
            ant["some"] = None if encadeia else ant["t_tap"] + 0.25
        seg.append({"x": tq["x"], "y": tq["y"], "t_tap": tq["t_tap"], "some": None,
                    "t_move": max(tq["t_tap"] - 0.45, (ant["t_tap"] + 0.05) if ant else 0.0),
                    "ini_pos": (ant["x"], ant["y"]) if encadeia else None})
    if seg:
        seg[-1]["some"] = seg[-1]["t_tap"] + 0.25
    return seg


# ---------- retângulos amostrados
def rect_em(d, T):
    """Retângulo (px CSS) do destaque no instante T, interpolado entre amostras; None se o elemento saiu de cena."""
    r = d["rects"]
    if not r:
        return None
    ts = [x["t"] for x in r]
    k = bisect.bisect_right(ts, T)
    cx = ("x", "y", "w", "h")
    if k == 0:
        a = r[0]
        return None if a.get("off") else tuple(a[c] for c in cx)
    a = r[k - 1]
    if a.get("off"):
        return None
    if k >= len(r):
        return tuple(a[c] for c in cx)
    b = r[k]
    if b.get("off") or b["t"] - a["t"] > 0.4:
        return tuple(a[c] for c in cx)
    p = (T - a["t"]) / max(b["t"] - a["t"], 1e-6)
    return tuple(a[c] + (b[c] - a[c]) * p for c in cx)


def rect_zoom(d, T):
    """Como rect_em, mas se o elemento saiu de cena usa o último retângulo conhecido."""
    r = rect_em(d, T)
    if r is not None:
        return r
    ts = [x["t"] for x in d["rects"]]
    k = bisect.bisect_right(ts, T)
    for x in list(reversed(d["rects"][:k])) + d["rects"][k:]:
        if not x.get("off"):
            return x["x"], x["y"], x["w"], x["h"]
    return None


# ---------- zoom de câmera
def montar_zooms(regs):
    zs = []
    for d in sorted(regs, key=lambda x: x["ini"]):
        rs = [x for x in d["rects"] if not x.get("off")]
        if not rs:
            continue
        w = sorted(x["w"] for x in rs)[len(rs) // 2]
        h = sorted(x["h"] for x in rs)[len(rs) // 2]
        ajuste = min(VW * 0.94 / (w + 16), VH * 0.9 / (h + 16))
        # o zoom nunca corta o trecho citado: o fator é o que cabe (teto ZOOM_MAX); se quase não aproxima, não faz zoom
        f = ZOOM_FATOR.get(d["fala"], min(ZOOM_MAX, ajuste))
        if f < 1.1:
            continue
        zs.append({"d": d, "ini": d["ini"] - 0.2, "fim": d["fim"], "f": f, "sai": d["fim"],
                   "fala": d["fala"]})
    for a, b in zip(zs, zs[1:]):
        if a["fala"] == b["fala"] and b["ini"] < a["fim"] + 0.5:
            a["sai"] = None        # zoom encadeado: a câmera passa direto de um alvo ao outro
    return zs


def camera(T):
    """(escala, x0, y0): recorte do viewport (px CSS) que preenche a janela."""
    s, cx, cy = 1.0, VW / 2, VH / 2
    for z in _est["zooms"]:
        if T < z["ini"]:
            break
        r = rect_zoom(z["d"], T)
        if r is None:
            continue
        e = ease((T - z["ini"]) / 0.35)
        s += (z["f"] - s) * e
        alvo_x = VW / 2 if r[2] > VW * 0.5 else r[0] + r[2] / 2     # elemento largo: não corta as laterais
        cx += (alvo_x - cx) * e
        cy += (r[1] + r[3] / 2 - cy) * e
        if z["sai"] is not None and T > z["sai"]:
            x = ease((T - z["sai"]) / 0.3)
            s += (1 - s) * x
            cx += (VW / 2 - cx) * x
            cy += (VH / 2 - cy) * x
    vw, vh = VW / s, VH / s
    return s, min(max(cx - vw / 2, 0), VW - vw), min(max(cy - vh / 2, 0), VH - vh)


def proj(cam, x, y):
    """Ponto em px CSS -> px dentro da janela."""
    s, x0, y0 = cam
    return (x - x0) * s * ESC, (y - y0) * s * ESC


# ---------- peças do quadro
def quadro_gravado(T):
    e = _est
    i = max(0, bisect.bisect_right(e["ts"], T) - 1)
    if e["ult"][0] != i:
        e["ult"] = (i, Image.open(GRAV / e["arq"][i]).convert("RGB"))
    return e["ult"][1]


def janela_img(T, cam):
    im = quadro_gravado(T)
    k = im.width / VW
    s, x0, y0 = cam
    box = (x0 * k, y0 * k, (x0 + VW / s) * k, (y0 + VH / s) * k)
    return im.resize((JW, JH), Image.LANCZOS, box=box)


def destaques(T, win, cam):
    """Escurece o resto da janela e contorna o trecho citado: areia 4 px + linha interna preta 2 px, folga de 8 px."""
    ativos = []
    for d in _est["hl"]:
        if not (d["ini"] - 0.01 <= T <= d["fim"] + 0.2):
            continue
        al = min(clamp((T - d["ini"]) / 0.15), 1 - clamp((T - d["fim"]) / 0.15))
        r = rect_em(d, T)
        if al <= 0 or r is None:
            continue
        x0, y0 = proj(cam, r[0], r[1])
        x1, y1 = proj(cam, r[0] + r[2], r[1] + r[3])
        infl = FOLGA_DEST + 10 * (1 - ease((T - d["ini"]) / 0.25))
        ativos.append((al, [round(x0 - infl), round(y0 - infl), round(x1 + infl), round(y1 + infl)]))
    if not ativos:
        return win
    amax = max(a for a, _ in ativos)
    maxk = 0.45 * 255
    mascara = Image.new("L", (JW, JH), round(maxk * amax))
    md = ImageDraw.Draw(mascara)
    for al, c in ativos:
        md.rectangle(c, fill=round(maxk * (amax - al)))
    win.paste(PRETO, (0, 0), mascara)
    ov = Image.new("RGBA", (JW, JH), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for al, c in ativos:
        a = int(255 * al)
        od.rectangle(c, outline=AREIA + (a,), width=4)
        od.rectangle([c[0] + 4, c[1] + 4, c[2] - 4, c[3] - 4], outline=PRETO + (a,), width=2)
    return Image.alpha_composite(win.convert("RGBA"), ov).convert("RGB")


def colar_anel(tela, im, x, y, alfa=1.0):
    m = im.getchannel("A")
    if alfa < 1:
        m = m.point(lambda v: int(v * alfa))
    tela.paste(im.convert("RGB"), (round(x - im.width / 2), round(y - im.height / 2)), m)


def dedo(tela, T, cam):
    segs = _est["toques"]

    def tela_xy(x, y):
        px, py = proj(cam, x, y)
        if not (-10 <= px <= JW + 10 and -10 <= py <= JH + 10):
            return -9999, -9999          # toque fora do enquadro do zoom: não desenha fora da janela
        return JX + px, JY + py

    for s in segs:                       # onda do toque
        u = T - s["t_tap"]
        if 0 <= u < 0.35:
            x, y = tela_xy(s["x"], s["y"])
            colar_anel(tela, anel(round(76 + 76 * ease(u / 0.35))), x, y, 1 - u / 0.35)
    ativo = None
    for s in segs:
        if s["t_move"] <= T:
            ativo = s
        else:
            break
    if ativo is None:
        return
    s = ativo
    if T < s["t_tap"]:
        p = ease((T - s["t_move"]) / max(min(0.4, s["t_tap"] - s["t_move"]), 1e-6))
        if s["ini_pos"]:
            x = s["ini_pos"][0] + (s["x"] - s["ini_pos"][0]) * p
            y = s["ini_pos"][1] + (s["y"] - s["ini_pos"][1]) * p
            al = 1.0
        else:
            x, y, al = s["x"], s["y"], clamp((T - s["t_move"]) / 0.15)
    else:
        x, y = s["x"], s["y"]
        al = 1.0 if s["some"] is None else 1 - clamp((T - (s["some"] - 0.13)) / 0.13)
    if al <= 0:
        return
    u = T - s["t_tap"]
    esc = 1 - 0.2 * math.sin(math.pi * u / 0.2) if 0 <= u < 0.2 else 1.0
    px, py = tela_xy(x, y)
    colar_anel(tela, anel(max(20, round(76 * esc))), px, py, al)


def cena_em(T):
    for n in L.NUMS:
        if T < L.fim(n):
            return n
    return "15"


def ini_legenda(n):
    return 0.0 if n == "01" else L.A(n) - 0.1


def pos_legenda(im):
    """Âncora embaixo: a última linha de base fica em y 1620 (2 linhas) e sobe meia entrelinha por linha a menos."""
    nl = round((im.height - 20) / im.lh)
    base = 1620 - (2 - nl) * im.lh / 2
    return (W // 2 - 450, round(base - im.base_ultima))


def desenhar_legenda(tela, T):
    """Nunca fica sem legenda: a anterior só sai enquanto a nova entra (fade cruzado de 0,15 s)."""
    ativos = [n for n in L.NUMS if T >= ini_legenda(n)]
    if not ativos:
        return
    n = ativos[-1]
    ini_vis = ini_legenda(n)
    a0 = L.A(n)
    pal = L.palavras(n)
    falados = sum(1 for p in pal if a0 + p["ini"] <= T)
    paginas_ = _est["leg"][n]
    ini_pg = [ini_vis] + [a0 + pal[P["ini"]]["ini"] - 0.05 for P in paginas_[1:]]
    k = max(i for i, s in enumerate(ini_pg) if T >= s)
    entra = clamp((T - ini_vis) / 0.15)
    if n != "01" and entra < 1:
        ant = L.NUMS[L.NUMS.index(n) - 1]
        im_ant = img_pagina(ant, len(_est["leg"][ant]) - 1, 0, todos=True)
        colar(tela, im_ant, pos_legenda(im_ant), 1 - entra)
    im = img_pagina(n, k, falados)
    if k == 0:
        colar(tela, im, pos_legenda(im), entra)
    else:
        p = clamp((T - ini_pg[k]) / 0.12)
        if p < 1:
            ant = img_pagina(n, k - 1, 0, todos=True)
            colar(tela, ant, pos_legenda(ant), 1 - p)
        colar(tela, im, pos_legenda(im), p)


def desenhar_cabecalho(tela, T):
    """Título e ícone do bloco novo entram no mesmo instante em que os do anterior saem (fade cruzado de 0,25 s)."""
    blocos = _est["blocos"]
    for i, (b, tb) in enumerate(blocos):
        prox = blocos[i + 1][1] if i + 1 < len(blocos) else L.S("15")
        # em sequência, sem sobrepor: o anterior sai em 0,12 s e o novo entra depois disso (0,25 s)
        te = tb + (0.12 if i > 0 else 0.0)
        if T < te or T > prox + 0.12:
            continue
        al = clamp((T - te) / 0.25) * (1 - clamp((T - prox) / 0.12))
        dy = round(28 * (1 - ease((T - te) / 0.35)))
        colar(tela, _est["cab"][b], (TX, HY + dy), al)
        colar(tela, _est["icone"][L.BLOCOS[b][2]], (HX, HY + 22 + dy), al)


def desenhar_selo(tela, T):
    """Etiqueta SIMULADO na linha do número, alinhada à direita da janela, durante a fala 09 (bloco 05)."""
    ini, fim = L.S("09"), L.S("10")
    if not (ini <= T <= fim + 0.25):
        return
    al = min(clamp((T - ini) / 0.25), 1 - clamp((T - fim) / 0.25))
    im = _est["selo"]
    colar(tela, im, (JX + JW - im.width, HY + 20 - im.height // 2 + 4), al)


def desenhar_abertura(tela, T):
    lg = _est["logo"]
    if T <= 2.5:
        sai = 1 - clamp((T - 2.2) / 0.25)
        al = clamp(T / 0.4) * sai
        esc = 1.03 - 0.03 * ease(T / 0.5)
        w = round(560 * esc)
        h = round(w * lg.height / lg.width)
        im = lg.resize((w, h), Image.LANCZOS)
        colar(tela, im, (W // 2 - w // 2, 860 - h // 2), al)
        t_img, _ = texto_img("BK GESTÃO", bebas(76), AREIA, 10)
        a2 = clamp((T - 0.3) / 0.4) * sai
        colar(tela, t_img, (W // 2 - t_img.width // 2, 860 + 560 * lg.height // lg.width // 2 + 60), a2)


def desenhar_cartela(tela, T):
    s15 = L.S("15")
    if T < s15 + 0.4:
        return
    al = clamp((T - s15 - 0.4) / 0.4)
    lg = _est["logo"]
    w = 440
    h = round(w * lg.height / lg.width)
    colar(tela, lg.resize((w, h), Image.LANCZOS), (W // 2 - w // 2, 700 - h // 2), al)
    y = 700 + h // 2 + 40
    t1, _ = texto_img("BK GESTÃO", bebas(120), OFF, 8)
    colar(tela, t1, (W // 2 - t1.width // 2, y), al)
    t2, _ = texto_img("Feito para a BK Clothing", jost(40, 400), AREIA, 1)
    colar(tela, t2, (W // 2 - t2.width // 2, y + 150), al)
    t3, _ = texto_img("Demonstração · números de exemplo", jost(28, 400), AREIA, 1)
    colar(tela, t3, (W // 2 - t3.width // 2, 1380), al)


def desenhar_janela(tela, T, cam):
    s15 = L.S("15")
    if T < T_JANELA or T > s15 + 0.4:
        return
    al = min(clamp((T - T_JANELA) / 0.6), 1 - clamp((T - s15) / 0.4))
    dy = round(40 * (1 - ease((T - T_JANELA) / 0.6)))
    win = destaques(T, janela_img(T, cam), cam)
    box = (JX, JY + dy, JX + JW, JY + dy + JH)
    cor_c = tuple(round(PRETO[k] + (OFF[k] - PRETO[k]) * 0.28 * al) for k in range(3))
    d = ImageDraw.Draw(tela)
    d.rectangle([box[0] - 2, box[1] - 2, box[2] + 1, box[3] + 1], outline=cor_c, width=2)
    if al >= 1:
        tela.paste(win, (box[0], box[1]))
    else:
        reg = tela.crop(box)
        tela.paste(Image.blend(reg, win, al), (box[0], box[1]))


def compor(i):
    T = i / FPS
    tela = Image.new("RGB", (W, H), PRETO)
    cam = camera(T)
    desenhar_abertura(tela, T)
    desenhar_cartela(tela, T)
    desenhar_cabecalho(tela, T)
    desenhar_selo(tela, T)
    desenhar_janela(tela, T, cam)
    if T_JANELA <= T <= L.S("15") + 0.4:
        dedo(tela, T, cam)
    desenhar_legenda(tela, T)
    tela.save(FINAIS / f"{i:05d}.jpg", quality=95)
    return i


def ffprobe_dur(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(arq)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def arg(nome):
    return sys.argv[sys.argv.index(nome) + 1] if nome in sys.argv and sys.argv.index(nome) + 1 < len(sys.argv) else None


TRILHA = arg("--trilha")            # --trilha ARQUIVO: música por baixo, sem narração (versão alternativa)
if TRILHA:
    MP4 = MP4.with_name(MP4.stem + "-trilha.mp4")
    FOLHA = FOLHA.with_name(FOLHA.stem + "-trilha.jpg")


def codificar_trilha(crf):
    """Vídeo com a trilha (sem voz): repete a música se for curta, fade de 1 s na entrada e 2,5 s na saída."""
    tot = L.TOTAL
    filtro = (f"[1:a]aresample=48000,atrim=0:{tot:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=1,"
              f"afade=t=out:st={max(0.0, tot - 2.5):.3f}:d=2.5,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FINAIS / "%05d.jpg"),
           "-stream_loop", "-1", "-i", str(TRILHA), "-filter_complex", filtro, "-map", "0:v", "-map", "[a]",
           "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-t", f"{tot:.3f}", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-crf", str(crf), "-preset", "slow", "-r", str(FPS), "-movflags", "+faststart", str(MP4)]
    subprocess.run(cmd, check=True)
    return []


def codificar(crf):
    if TRILHA:
        return codificar_trilha(crf)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FINAIS / "%05d.jpg")]
    com = [n for n in L.NUMS if L.tem_audio(n) and (VOZ / f"{n}.mp3").exists()]
    for n in com:
        cmd += ["-i", str(VOZ / f"{n}.mp3")]
    if com:
        partes = []
        for k, n in enumerate(com):
            corte = L.TP[n].get("corte", 0.0)
            partes.append(f"[{k + 1}:a]atrim=start={corte},asetpts=PTS-STARTPTS,aresample=48000,adelay={round(L.A(n) * 1000)}:all=1[a{k}]")
        mix = "".join(f"[a{k}]" for k in range(len(com))) + f"amix=inputs={len(com)}:normalize=0:dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]"
        cmd += ["-filter_complex", ";".join(partes + [mix]), "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "160k", "-ar", "48000"]
    cmd += ["-t", f"{L.TOTAL:.3f}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", str(crf), "-preset", "slow", "-r", str(FPS),
            "-movflags", "+faststart", str(MP4)]
    subprocess.run(cmd, check=True)
    return com


def folha_de_quadros():
    tmp = AQUI / "_trabalho" / "folha_tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir()
    dur = ffprobe_dur(MP4)
    cw, ch, pad, rot = 300, 533, 8, 30
    folha = Image.new("RGB", (6 * cw + 7 * pad, 3 * (ch + rot) + 4 * pad), PRETO)
    d = ImageDraw.Draw(folha)
    f = jost(22, 500)
    for k in range(18):
        t = (k + 0.5) * dur / 18
        arq = tmp / f"{k:02d}.jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(MP4), "-frames:v", "1", "-q:v", "2", str(arq)], check=True)
        im = Image.open(arq).convert("RGB").resize((cw, ch), Image.LANCZOS)
        x = pad + (k % 6) * (cw + pad)
        y = pad + (k // 6) * (ch + rot + pad)
        folha.paste(im, (x, y))
        d.text((x + cw // 2, y + ch + 4), f"{int(t // 60):02d}:{int(t % 60):02d}", font=f, fill=OFF, anchor="mt")
    folha.save(FOLHA, quality=90)
    shutil.rmtree(tmp, ignore_errors=True)


def principal():
    ev = json.loads((GRAV / "eventos.json").read_text(encoding="utf-8"))
    if ev["assinatura"] != L.assinatura():
        sys.exit("a gravação foi feita com outra linha do tempo (áudios mudaram): rode fazer.py sem --so-montar")
    shutil.rmtree(FINAIS, ignore_errors=True)
    FINAIS.mkdir(parents=True)
    n = int(math.ceil(L.TOTAL * FPS))
    print(f"compondo {n} quadros ({L.TOTAL:.1f} s)…", flush=True)
    with mp.Pool(6, initializer=preparar) as pool:
        for k, _ in enumerate(pool.imap_unordered(compor, range(n), chunksize=8)):
            if k % 300 == 0:
                print(f"  {k}/{n}", flush=True)
    for crf in (22, 24, 26, 28):
        com = codificar(crf)
        mb = MP4.stat().st_size / 1e6
        print(f"crf {crf}: {mb:.1f} MB, voz em {len(com)} falas")
        if mb <= 20:
            break
    folha_de_quadros()
    print("ok", MP4.name, FOLHA.name)


if __name__ == "__main__":
    mp.freeze_support()
    if "--quadro" in sys.argv:        # teste: compõe só alguns quadros (instantes em segundos)
        preparar()
        FINAIS.mkdir(exist_ok=True)
        for t in sys.argv[sys.argv.index("--quadro") + 1:]:
            compor(int(float(t) * FPS))
    else:
        principal()
