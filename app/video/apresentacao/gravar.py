"""Grava o aplicativo de verdade (index.html, viewport 390x640, escala 2) com screencast CDP, seguindo a linha do tempo.

O relógio da gravação r = 0 no primeiro quadro, e r é o tempo do vídeo: cada ação espera até o instante absoluto
que a linha do tempo (linha_do_tempo.py) marca para a palavra da fala. Saída em _trabalho/gravacao/:
  q/NNNNN.jpg, quadros.json ([[t, arquivo], ...]) e eventos.json (toques, destaques com retângulos amostrados, movimentos).
Nunca clica em link que abre o WhatsApp nem nos botões de ajuste de estoque (data-a='aj').
"""
import asyncio
import base64
import json
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import linha_do_tempo as L  # noqa: E402
from linha_do_tempo import A, S, t, tf  # noqa: E402

APP = AQUI.parent.parent
SAIDA = AQUI / "_trabalho" / "gravacao"
RELOGIO = "?agora=2026-10-08T18:40"
JAQUETA = "1914784"
VIEW_W, VIEW_H = 390, 640
ESCALA = 2.5              # fator de escala do dispositivo (o zoom de câmera da montagem recorta o quadro gravado)
INTERVALO = 0.07          # amostragem dos retângulos de destaque


class Gravacao:
    def __init__(self, pg, cdp):
        self.pg, self.cdp = pg, cdp
        self.marcas = []          # (timestamp, arquivo)
        self.t0 = None
        self.erro = None
        self.toques = []
        self.destaques = []
        self.movimentos = []
        self.acoes = []
        self.fim = False

    # ---- relógio
    def agora(self):
        return time.time() - self.t0 if self.t0 else 0.0

    async def ate(self, T):
        while True:
            if self.erro:
                raise self.erro
            falta = T - self.agora()
            if falta <= 0:
                return
            await asyncio.sleep(min(falta, 0.05))

    # ---- quadros
    def chegou(self, ev):
        nome = SAIDA / "q" / f"{len(self.marcas):05d}.jpg"
        nome.write_bytes(base64.b64decode(ev["data"]))
        self.marcas.append((ev["metadata"]["timestamp"], nome))
        if self.t0 is None:
            self.t0 = self.marcas[0][0]
        asyncio.ensure_future(self.cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]}))

    # ---- agenda de ações (executadas em ordem de tempo)
    def agendar(self, T, fn):
        self.acoes.append((T, len(self.acoes), fn))

    # ---- destaques
    def destaque(self, fala, ini, fim, sel, nth=0, texto=None, fixo=False, alvos=None, visivel=True, zoom=False, par=None):
        """Registro de destaque. fixo=True: não é estendido até o próximo (o elemento é tocado em seguida).
        visivel=False: só serve de alvo de zoom (alvos pode ter vários elementos: usa-se a união)."""
        alvos = alvos or [{"sel": sel, "nth": nth, "texto": texto}]
        self.destaques.append({"fala": fala, "ini": round(ini, 3), "fim": None if fim is None else round(fim, 3),
                               "sel": alvos[0]["sel"], "nth": alvos[0]["nth"], "texto": alvos[0]["texto"], "alvos": alvos,
                               "fixo": fixo, "visivel": visivel, "zoom": zoom, "par": par, "rects": []})
        return len(self.destaques) - 1

    def estender(self):
        """Cada destaque fica até o próximo da mesma fala (ou o fim da fala); o zoom herda o fim do par."""
        for n in L.NUMS:
            limite = A(n) + L.dur(n) + 0.15
            vis = [d for d in self.destaques if d["fala"] == n and d["visivel"]]
            for d in vis:
                if d["fixo"]:
                    continue
                prox = [o["ini"] for o in vis if o["ini"] > d["ini"] + 0.06]
                d["fim"] = round(min(prox) if prox else limite, 3)
        for d in self.destaques:
            if not d["visivel"]:
                lim = A(d["fala"]) + L.dur(d["fala"]) + 0.1
                fim = self.destaques[d["par"]]["fim"] if d["par"] is not None else d["fim"]
                d["fim"] = round(min(lim if fim is None else fim, lim), 3)

    async def amostrar(self):
        js = """(lista) => lista.map(a => {
            let caixa = null;
            for (const al of a) {
                let l = [...document.querySelectorAll(al.sel)];
                if (al.texto) l = l.filter(e => e.textContent.includes(al.texto));
                const e = l[al.nth]; if (!e) continue;
                const r = e.getBoundingClientRect();
                if (r.width === 0 && r.height === 0) continue;
                if (!caixa) caixa = [r.left, r.top, r.right, r.bottom];
                else caixa = [Math.min(caixa[0], r.left), Math.min(caixa[1], r.top), Math.max(caixa[2], r.right), Math.max(caixa[3], r.bottom)];
            }
            return caixa ? [caixa[0], caixa[1], caixa[2] - caixa[0], caixa[3] - caixa[1]] : null; })"""
        while not self.fim:
            ini = self.agora()
            ativos = [d for d in self.destaques if d["ini"] - 0.2 <= ini <= d["fim"] + 0.05]
            if ativos:
                r = await self.pg.evaluate(js, [d["alvos"] for d in ativos])
                tm = (ini + self.agora()) / 2
                for d, v in zip(ativos, r):
                    if v:
                        d["rects"].append({"t": round(tm, 3), "x": v[0], "y": v[1], "w": v[2], "h": v[3]})
                    elif not d["rects"] and ini > d["ini"] + 0.5:
                        self.erro = RuntimeError(
                            f"destaque sem elemento: fala {d['fala']}, seletor {d['sel']!r} nth={d['nth']} texto={d['texto']!r} "
                            f"(instante {ini:.2f} s, previsto {d['ini']:.2f}-{d['fim']:.2f} s)")
                        return
                    elif d["rects"] and not d["rects"][-1].get("off"):
                        d["rects"].append({"t": round(tm, 3), "off": 1})     # o elemento saiu de cena
            await asyncio.sleep(max(0.0, INTERVALO - (self.agora() - ini)))

    # ---- toques e rolagem
    async def toque(self, sel, t_tap, nth=0, texto=None, fala=None, foco=False):
        if "btn cheio" in sel or "data-a='aj'" in sel or 'data-a="aj"' in sel:
            raise RuntimeError(f"toque proibido: {sel}")
        alvo = {"sel": sel, "nth": nth, "texto": texto}
        pos_js = """(a) => {
            let l = [...document.querySelectorAll(a.sel)];
            if (a.texto) l = l.filter(e => e.textContent.includes(a.texto));
            const e = l[a.nth]; if (!e) return null;
            const tela = document.getElementById('tela');
            if (tela.contains(e)) {
                const r0 = e.getBoundingClientRect(), tr = tela.getBoundingClientRect();
                if (r0.top < tr.top + 8 || r0.bottom > tr.bottom - 8) e.scrollIntoView({block: 'center', behavior: 'instant'});
            }
            const r = e.getBoundingClientRect();
            return [r.x + r.width / 2, r.y + r.height / 2]; }"""
        pos = await self.pg.evaluate(pos_js, alvo)
        if pos is None:
            raise RuntimeError(f"toque sem elemento: fala {fala}, {sel!r} nth={nth} texto={texto!r} (instante {self.agora():.2f} s)")
        await self.ate(t_tap)
        clique = """(a) => {
            let l = [...document.querySelectorAll(a.sel)];
            if (a.texto) l = l.filter(e => e.textContent.includes(a.texto));
            const e = l[a.nth]; if (!e) return false;
            if (a.foco) e.focus();
            e.click(); return true; }"""
        ok = await self.pg.evaluate(clique, {**alvo, "foco": foco})
        if not ok:
            raise RuntimeError(f"clique sem elemento: fala {fala}, {sel!r}")
        self.toques.append({"fala": fala, "sel": sel, "t_tap": round(t_tap, 3), "x": pos[0], "y": pos[1]})

    def toca(self, fala, t_tap, sel, **kw):
        """Agenda um toque: mede a posição 0,12 s antes (depois de qualquer rolagem) e clica em t_tap."""
        self.agendar(t_tap - 0.12, lambda: self.toque(sel, t_tap, fala=fala, **kw))

    def rolar_para(self, T, sel, nth=0, texto=None, bloco="center", dur=1.0):
        # rolagem por requestAnimationFrame (ease cúbico, tempo real), no ancestral rolável do elemento
        js = """(a) => { let l = [...document.querySelectorAll(a.sel)];
            if (a.texto) l = l.filter(e => e.textContent.includes(a.texto));
            const e = l[a.nth]; if (!e) return false;
            let tela = e.parentElement;
            while (tela && !(tela.scrollHeight > tela.clientHeight + 2 && /(auto|scroll)/.test(getComputedStyle(tela).overflowY))) tela = tela.parentElement;
            if (!tela) tela = document.getElementById('tela');
            const tr = tela.getBoundingClientRect(), r = e.getBoundingClientRect();
            let alvo = tela.scrollTop;
            if (a.bloco === 'center') alvo += (r.top + r.height / 2) - (tr.top + tr.height / 2);
            else if (a.bloco === 'end') alvo += r.bottom - tr.bottom;
            else alvo += r.top - tr.top;
            alvo = Math.max(0, Math.min(alvo, tela.scrollHeight - tela.clientHeight));
            const de = tela.scrollTop, t0 = performance.now();
            const passo = (agora) => {
                const p = Math.min(1, (agora - t0) / (a.dur * 1000));
                tela.scrollTop = de + (alvo - de) * (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
                if (p < 1) requestAnimationFrame(passo);
            };
            requestAnimationFrame(passo); return true; }"""

        async def f():
            ok = await self.pg.evaluate(js, {"sel": sel, "nth": nth, "texto": texto, "bloco": bloco, "dur": dur})
            if not ok:
                raise RuntimeError(f"rolagem sem elemento: {sel!r}")
            self.movimentos.append([round(self.agora(), 3), round(self.agora() + dur, 3)])
        self.agendar(T, f)

    def rolar_topo(self, T, dur=0.7):
        js = """(dur) => { const tela = document.getElementById('tela'); const de = tela.scrollTop, t0 = performance.now();
            const passo = (agora) => { const p = Math.min(1, (agora - t0) / (dur * 1000));
                tela.scrollTop = de * (1 - (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2));
                if (p < 1) requestAnimationFrame(passo); };
            requestAnimationFrame(passo); }"""

        async def f():
            await self.pg.evaluate(js, dur)
            self.movimentos.append([round(self.agora(), 3), round(self.agora() + dur, 3)])
        self.agendar(T, f)

    def digitar(self, T, sel, texto):
        async def f():
            await self.pg.locator(sel).first.press_sequentially(texto, delay=80)
        self.agendar(T, f)

    def silencioso(self, T, js):
        async def f():
            await self.pg.evaluate(js)
        self.agendar(T, f)

    async def executar(self):
        for T, _, fn in sorted(self.acoes, key=lambda a: (a[0], a[1])):
            await self.ate(T)
            await fn()


def porta_livre():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def roteiro(g):
    """Todas as ações, ancoradas nas palavras de cada fala (ver plano-de-cenas.md, seção 4)."""
    D = g.destaque

    def dest(n, de, ate, sel, ini_d=-0.1, fim_d=0.12, zoom=False, **kw):
        """Destaque de `de` (início da palavra) até `ate` (fim da palavra); estender() prolonga até o próximo.
        zoom=True: a câmera aproxima neste elemento, a partir da palavra-gatilho `de`."""
        i = D(n, t(n, de) + ini_d, tf(n, ate) + fim_d, sel, **kw)
        if zoom:
            D(n, t(n, de), None, sel, nth=kw.get("nth", 0), texto=kw.get("texto"), visivel=False, zoom=True, par=i)
        return i

    def zoom_uniao(n, gatilho, fim, alvos):
        """Zoom sobre a união de vários elementos (sem contorno próprio)."""
        D(n, gatilho, fim, None, alvos=[{"sel": s_, "nth": k, "texto": tx} for s_, k, tx in alvos], visivel=False, zoom=True)

    # ---------------- 01 abertura: as abas
    dest("01", "estoque", "estoque", "#abas a[data-aba='estoque']")
    dest("01", "vendas", "vendas", "#abas a[data-aba='vendas']")

    # ---------------- 02 início do dia
    dest("02", "quanto", "hoje", ".hoje-v", fixo=True)
    r0 = tf("02", "hoje") + 0.1       # a rolagem para antes de "peça esgotada": a tela fica parada nos três destaques
    g.rolar_para(r0, "a.at[href='#/mais/paradas']", bloco="end", dur=min(1.4, max(0.6, t("02", "peça") - 0.35 - r0)))
    dest("02", "peça", "esgotada", "a.at[data-st='zero']", ini_d=-0.05)
    dest("02", "acabando", "acabando", "a.at[data-st='baixo']", ini_d=-0.05)
    dest("02", "parada", "parada", "a.at[href='#/mais/paradas']", ini_d=-0.05, fim_d=0.25)
    zoom_uniao("02", t("02", "peça"), None, [("a.at[data-st='zero']", 0, None), ("a.at[data-st='baixo']", 0, None),
                                              ("a.at[href='#/mais/paradas']", 0, None)])

    # ---------------- 03 estoque por tamanho
    g.toca("03", A("03") - 0.25, "[data-a='ir-estoque'][data-st='baixo']")
    dest("03", "quantidade", "tamanho", "#lista .it:nth-child(1) .tams", zoom=True)
    for k in range(3):
        dest("03", "vermelho", "vermelho", "#lista .tams i.z", nth=k, ini_d=-0.2, fim_d=0.3)

    # ---------------- 04 busca
    g.toca("04", A("04") - 0.25, "#q", foco=True)
    g.digitar(t("04", "é só"), "#q", "jaqueta")
    dest("04", "digitar", "digitar", "label.busca", fim_d=0.2)
    dest("04", "nome", "cor", "#lista .it:nth-child(1)", fim_d=0.3)

    # ---------------- 05 dentro da peça
    g.toca("05", A("05") - 0.25, f".it[href='#/estoque/p/{JAQUETA}']")
    g.rolar_para(t("05", "ajusta") - 0.5, ".tg", dur=1.0)
    dest("05", "cada", "tamanho", ".tg")
    g.rolar_para(tf("05", "tamanho") - 0.1, ".kv", texto="Margem", dur=1.0)
    dest("05", "margem", "margem", ".kv", texto="Margem", ini_d=-0.15, fim_d=0.2, zoom=True)
    g.rolar_para(tf("05", "margem") + 0.05, ".dica", dur=1.0)
    dest("05", "quanto", "dura", ".dica", ini_d=-0.1, fim_d=0.25, zoom=True)

    # ---------------- 06 vender
    g.toca("06", A("06") - 0.25, "#abas a[data-aba='vender']")
    t6 = t("06", "peça") + 0.0
    dest("06", "toca", "peça", f".tile[data-id='{JAQUETA}']", ini_d=-0.1, fim_d=0.05, fixo=True)
    g.toca("06", t6, f".tile[data-id='{JAQUETA}']")
    t6b = t("06", "tamanho") + 0.0
    D("06", t("06", "escolhe") - 0.1, t6b + 0.1, "#folha .tm", fixo=True)
    g.toca("06", t6b, "[data-a='add'][data-tam='M']")
    t6c = t("06", "cobra") + 0.05
    D("06", t6c - 0.4, t6c + 0.05, "#cobrar", fixo=True)
    g.toca("06", t6c, "#cobrar")
    D("06", t6c + 0.2, t6c + 0.95, ".pgs", fixo=True)
    g.rolar_para(t6c + 1.0, "[data-a='concluir']", bloco="center", dur=0.8)

    # ---------------- 07 baixa automática
    g.toca("07", A("07") - 0.25, "[data-a='concluir']")
    dest("07", "estoque", "sozinho", ".dp", ini_d=-0.05)
    dest("07", "avisa", "esgota", ".alerta", ini_d=-0.1, fim_d=0.25)
    zoom_uniao("07", t("07", "estoque"), tf("07", "esgota") + 0.25, [(".dp", 0, None), (".alerta", 0, None)])
    g.rolar_para(tf("07", "esgota") + 0.5, "[data-a='comprovante']", bloco="center", dur=0.8)

    # ---------------- 08 comprovante
    t8 = A("08") - 0.25
    D("08", t8 - 0.55, t8 + 0.1, "[data-a='comprovante']", fixo=True)
    g.toca("08", t8, "[data-a='comprovante']")
    dest("08", "pronto", "pronto", "#folha .msg", ini_d=-0.1, fim_d=0.25, zoom=True)
    dest("08", "whatsapp", "whatsapp", "#folha a.btn.cheio", ini_d=-0.1, fim_d=0.3)
    g.toca("08", A("08") + dur_pos("08", 0.85), "#folha [data-a='fechar']")

    # ---------------- 09 pedido do site
    g.toca("09", A("09") - 0.6, "#abas a[data-aba='vendas']")
    g.toca("09", A("09") - 0.25, "[data-a='aba'][data-v='pedidos']")
    dest("09", "com", "ligado", ".seg [data-v='pedidos']", ini_d=0.05, fim_d=0.1)
    dest("09", "pedido", "aqui", ".ped", ini_d=-0.15, fim_d=0.2, zoom=True)
    t9a = t("09", "confirmou") + 0.08
    D("09", t9a - 0.35, t9a + 0.05, "[data-a='ped-ok']", fixo=True)
    g.toca("09", t9a, "[data-a='ped-ok']")
    t9b = t("09", "pagamento") + 0.1
    g.toca("09", t9b, "[data-a='ped-pg'][data-v='pix']")
    dest("09", "virou", "venda", ".okc", ini_d=-0.05, fim_d=0.35)

    # ---------------- 10 entrada de mercadoria
    g.toca("10", A("10") - 0.6, "#abas a[data-aba='mais']")
    g.toca("10", A("10") - 0.25, "a[href='#/estoque/entrada']")
    t10 = t("10", "dá") + 0.0
    D("10", t10 - 0.15, t10 + 0.1, f"#lista .it[data-id='{JAQUETA}']", fixo=True)
    g.toca("10", t10, f"#lista .it[data-id='{JAQUETA}']")
    t10q = t("10", "por") + 0.05
    for k, tam in enumerate(("M", "M", "G")):
        g.toca("10", t10q + 0.27 * k, f"[data-a='en-q'][data-tam='{tam}'][data-q='1']")
    for k in range(4):
        D("10", t10q - 0.1, tf("10", "tamanho") + 0.3, "#folha .en", nth=k)
    t10ok = t("10", "poucos") + 0.12
    D("10", t10ok - 0.35, t10ok + 0.1, "[data-a='en-ok']", fixo=True)
    g.toca("10", t10ok, "[data-a='en-ok']")

    # ---------------- 11 peças paradas
    g.toca("11", A("11") - 0.6, "#abas a[data-aba='mais']")
    g.toca("11", A("11") - 0.25, "a[href='#/mais/paradas']")
    dest("11", "peças", "dias", ".rs", ini_d=-0.05, fim_d=0.1)
    for k in range(3):
        dest("11", "quarenta", "dias", "button.ln[data-a='par-sel']", nth=k, ini_d=0.0, fim_d=0.15)
    t11 = t("11", "oferta") - 0.05
    D("11", t("11", "viram") - 0.1, t11 + 0.1, "[data-a='msg-oferta']", fixo=True)
    g.toca("11", t11, "[data-a='msg-oferta']")
    dest("11", "grupo", "vip", "#folha .msg", ini_d=-0.1, fim_d=0.3, zoom=True)

    # ---------------- 12 reposição
    g.toca("12", A("12") - 1.0, "#folha [data-a='fechar']")
    g.toca("12", A("12") - 0.63, "[data-a='voltar']")
    g.toca("12", A("12") - 0.25, "a[href='#/mais/reposicao']")
    dest("12", "lista", "fornecedor", "[data-a='msg-rep']", ini_d=-0.05)
    for k in range(3):
        dest("12", "monta", "sozinha", "#tela a.ln[href^='#/estoque/p/'] .tams", nth=k, ini_d=-0.2, fim_d=0.3)
    dest("12", "com", "vende", "#tela a.ln[href^='#/estoque/p/'] small", nth=0, ini_d=-0.05, fim_d=0.3)

    # ---------------- 13 resumo
    g.toca("13", A("13") - 0.63, "#abas a[data-aba='vendas']")
    g.toca("13", A("13") - 0.25, "[data-a='aba'][data-v='resumo']")
    dest("13", "vendas", "vendas", ".rs-v", ini_d=-0.1, fim_d=0.2)
    dest("13", "lucro", "estimado", ".fatos > div:nth-child(4)", ini_d=-0.1, fim_d=0.15, zoom=True)
    g.rolar_para(tf("13", "estimado") - 0.25, "#tela .hb", dur=0.9)
    for k in range(3):
        dest("13", "formas", "pagamento", "#tela .hb", nth=k, ini_d=-0.05, fim_d=0.0)
    zoom_uniao("13", t("13", "formas"), tf("13", "pagamento") - 0.1, [("#tela .hb", k, None) for k in range(3)])
    g.rolar_topo(tf("13", "pagamento") - 0.05)
    t13 = t("13", "período") + 0.25
    D("13", t("13", "período") - 0.1, t13 + 0.15, "[data-a='per'][data-v='30']", fixo=True)
    g.toca("13", t13, "[data-a='per'][data-v='30']")

    # ---------------- 14 fechamento
    g.toca("14", A("14") - 0.63, "#abas a[data-aba='mais']")
    g.toca("14", A("14") - 0.25, "a[data-a='fechamento']")
    dest("14", "fechamento", "fechamento", "#folha .rs-v", ini_d=-0.1, fim_d=0.2, zoom=True)
    dest("14", "sai", "toque", "#folha [data-a='msg-fech']", ini_d=-0.05, fim_d=0.4)

    # ---------------- 15 cartela final: o app volta ao início fora de quadro (a janela já saiu)
    g.silencioso(S("15") + 0.5, "document.querySelector('#folha [data-a=fechar]') && document.querySelector('#folha [data-a=fechar]').click()")
    g.silencioso(S("15") + 0.8, "document.querySelector('#abas a[data-aba=inicio]').click()")


def dur_pos(n, frac):
    """Instante relativo (a A(n)) a `frac` da duração da fala."""
    return L.dur(n) * frac


async def principal():
    shutil.rmtree(SAIDA, ignore_errors=True)
    (SAIDA / "q").mkdir(parents=True)
    porta = porta_livre()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(porta), "--bind", "127.0.0.1", "--directory", str(APP)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    try:
        async with async_playwright() as p:
            nav = await p.chromium.launch(channel="chrome", headless=True)
            ctx = await nav.new_context(viewport={"width": VIEW_W, "height": VIEW_H}, device_scale_factor=ESCALA, locale="pt-BR")
            pg = await ctx.new_page()
            url = f"http://127.0.0.1:{porta}/index.html{RELOGIO}"
            await pg.goto(url)
            await pg.evaluate("localStorage.clear()")
            await pg.goto(url)
            await pg.reload()
            await pg.locator(".hoje-v").wait_for()
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(1500)
            cdp = await ctx.new_cdp_session(pg)
            g = Gravacao(pg, cdp)
            cdp.on("Page.screencastFrame", g.chegou)
            roteiro(g)
            g.estender()
            await cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 92, "maxWidth": round(VIEW_W * ESCALA), "maxHeight": round(VIEW_H * ESCALA),
                                                   "everyNthFrame": 1})
            while not g.marcas:
                await pg.wait_for_timeout(20)
            amostrador = asyncio.ensure_future(g.amostrar())
            try:
                await g.executar()
                await g.ate(L.TOTAL)
            finally:
                g.fim = True
                await asyncio.sleep(0.15)
                await cdp.send("Page.stopScreencast")
                await pg.wait_for_timeout(300)
                await nav.close()
            if g.erro:
                raise g.erro
            await amostrador
    finally:
        srv.terminate()

    quadros = [[round(ts - g.marcas[0][0], 4), str(f.relative_to(SAIDA).as_posix())] for ts, f in g.marcas]
    (SAIDA / "quadros.json").write_text(json.dumps(quadros), encoding="utf-8")
    ev = {"assinatura": L.assinatura(), "total": L.TOTAL, "viewport": [VIEW_W, VIEW_H], "escala": ESCALA, "toques": g.toques,
          "destaques": g.destaques, "movimentos": g.movimentos}
    (SAIDA / "eventos.json").write_text(json.dumps(ev, ensure_ascii=False), encoding="utf-8")

    # buracos de verdade: intervalo > 120 ms no meio de um trecho em movimento (quadros vizinhos a < 60 ms)
    ts = [q[0] for q in quadros]
    gaps = [(ts[i], ts[i + 1] - ts[i]) for i in range(len(ts) - 1)]
    buracos = [(round(gaps[i][0], 2), round(gaps[i][1] * 1000)) for i in range(1, len(gaps) - 1)
               if 0.12 < gaps[i][1] < 0.4 and gaps[i - 1][1] < 0.06 and gaps[i + 1][1] < 0.06]
    print(f"gravado: {len(quadros)} quadros em {ts[-1]:.1f} s, {len(g.toques)} toques, {len(g.destaques)} destaques")
    print(f"buracos de 120-400 ms no meio de movimento: {len(buracos)} {buracos[:8]}")
    sem = [d for d in g.destaques if not d["rects"]]
    for d in sem:
        print("AVISO: destaque sem nenhuma amostra:", d["fala"], d["sel"], d["nth"])


def main():
    asyncio.run(principal())


if __name__ == "__main__":
    main()
