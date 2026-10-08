"""Grava o vídeo de navegação no celular (360x640 @3x = 1080x1920, 30 fps) -> entregas/bk-site-celular.mp4
Uso: .venv/Scripts/python scripts/gravar_celular.py   (com o servidor em http://localhost:4174)
Mostra um ponto onde o dedo toca. Não toca em wa.me, grupo VIP nem em "Fechar pedido no WhatsApp".
"""
import pathlib, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gravacao_lib as L
from gravacao_lib import Rec, TOUCH_JS, BASE

H = pathlib.Path(__file__).resolve().parent.parent
OUT = H / "entregas" / "bk-site-celular.mp4"
SETUP = "try{localStorage.setItem('bk_tema','dark');localStorage.setItem('bk_arte','a');localStorage.removeItem('bk_sacola')}catch(e){}"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
L.K = 0.95
W, HH = 360, 640


def carrega_tudo(page):
    page.goto(BASE + "/index.html", wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    h = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < h:
        page.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})"); page.wait_for_timeout(150); y += 400
    page.goto(BASE + "/index.html#p=1914786", wait_until="networkidle"); page.wait_for_timeout(1500)
    page.goto(BASE + "/links.html", wait_until="networkidle")
    page.evaluate("localStorage.removeItem('bk_sacola')")


with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--hide-scrollbars"])
    ctx = b.new_context(viewport={"width": W, "height": HH}, device_scale_factor=3, is_mobile=True, has_touch=True, user_agent=UA)
    ctx.add_init_script(SETUP); ctx.add_init_script(TOUCH_JS)
    page = ctx.new_page()
    carrega_tudo(page)
    page.goto(BASE + "/index.html", wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    sobra = page.evaluate("document.documentElement.scrollWidth - innerWidth")
    print("rolagem lateral (px):", sobra)
    r = Rec(page, H / "scripts" / "_tmp_celular", W, HH, quality=90, escala=3)
    r.pause(); r.rec = True
    sy = lambda a, b: (lambda t: page.evaluate(f"window.scrollTo({{top:{a + (b - a) * t},behavior:'instant'}})"))
    ys = lambda: page.evaluate("window.scrollY")

    def rola_dedo(destino, s):
        a = ys(); r.finger(W * .5, 520, 520 - min(380, max(-380, (destino - a) * .5)), s, sy(a, destino))

    # 1. hero com a logo
    r.wait(4.0)
    # 2. rolagem pela Seleção BK
    rola_dedo(r.top_of("#destaques", -20), 1.6); r.wait(1.2)
    rola_dedo(r.top_of("#rail .card[data-p='1914786']", -150), 1.4); r.wait(0.9)
    print("frames", r.n, "-> toque na jaqueta", flush=True)
    # 3. toca na jaqueta bege
    r.tap("#rail .card[data-p='1914786']", pausa=0.5); r.wait(1.6)
    print("frames", r.n, "-> fotos", flush=True)
    # desliza as fotos para o lado
    n = r.frames(1.0)
    print("pm aberto:", page.evaluate("document.querySelector('#pm').classList.contains('open')"), flush=True)
    larg = page.evaluate("document.querySelector('.pm-ph').clientWidth")
    for i in range(1, n + 1):
        t = L.ease_io(i / n)
        page.evaluate("([t,l]) => document.querySelector('.pm-ph').scrollLeft = l*t", [t, larg * .88])
        o = min(1, i / 4) if i < n - 4 else max(0, (n - i) / 4)
        page.evaluate("([x,o]) => window.__dot(x, 300, o, 1)", [260 - 140 * t, o]); r.tick()
    page.evaluate("window.__dot(0,0,0,1)"); r.wait(0.8)
    print("frames", r.n, "-> tamanho", flush=True)
    # rola até o tamanho
    pm = lambda a, b: (lambda t: page.evaluate("([a,b,t]) => document.querySelector('#pm').scrollTop = a + (b-a)*t", [a, b, t]))
    alvo = page.evaluate("document.querySelector('.sizes').getBoundingClientRect().top + document.querySelector('#pm').scrollTop - 380")
    r.finger(W * .5, 520, 360, 1.2, pm(0, alvo)); r.wait(0.5)
    r.tap(".sizes [data-size='M']", pausa=0.4); r.wait(0.6)
    r.tap("[data-add]", pausa=0.4); r.wait(2.2)
    # sacola aberta: fecha
    r.tap("#bag [data-close]", pausa=0.4); r.wait(0.9)
    # 4. menu: abre e fecha
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})"); r.wait(0.5)
    r.tap(".hd .burger", pausa=0.4); r.wait(1.8)
    r.tap("#mnav [data-menu]", pausa=0.4); r.wait(0.8)
    # 5. lookbook
    rola_dedo(r.top_of("#lookbook", -20), 2.2); r.wait(1.2)
    rola_dedo(r.top_of("#lookbook", 700), 1.4); r.wait(1.0)
    rola_dedo(r.top_of("#lookbook", 1500), 1.4); r.wait(0.9)
    # 6. Visite a loja
    rola_dedo(r.top_of("#loja", -20), 2.2); r.wait(2.0)
    # 7. links.html (bio do Instagram)
    page.goto(BASE + "/links.html", wait_until="networkidle"); page.evaluate("document.fonts.ready")
    r.pause(); r.wait(3.2)
    r.rec = False
    b.close()

dur = r.render(OUT, crf=21, maxrate="3000k")
print("quadros:", r.n, "| duração:", round(dur, 1), "s |", OUT.stat().st_size // 1024, "KB")
