"""Grava o vídeo de navegação no computador (1920x1080, 30 fps) -> entregas/bk-site-desktop.mp4
Uso: .venv/Scripts/python scripts/gravar_desktop.py   (com o servidor em http://localhost:4174)
Quadro a quadro com tempo virtual (ver gravacao_lib.py). Não clica em wa.me, grupo VIP nem em
"Fechar pedido no WhatsApp".
"""
import pathlib, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gravacao_lib as L
from gravacao_lib import Rec, CURSOR_JS, BASE

H = pathlib.Path(__file__).resolve().parent.parent
OUT = H / "entregas" / "bk-site-desktop.mp4"
SETUP = "try{localStorage.setItem('bk_tema','dark');localStorage.setItem('bk_arte','a');localStorage.removeItem('bk_sacola')}catch(e){}"
L.K = 0.72


def carrega_tudo(page):
    page.goto(BASE + "/index.html", wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    h = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < h:
        page.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})"); page.wait_for_timeout(150); y += 500
    page.goto(BASE + "/index.html#p=1914786", wait_until="networkidle"); page.wait_for_timeout(1500)
    page.evaluate("localStorage.removeItem('bk_sacola')")


with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--hide-scrollbars"])
    ctx = b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    ctx.add_init_script(SETUP); ctx.add_init_script(CURSOR_JS)
    page = ctx.new_page()
    carrega_tudo(page)
    page.goto(BASE + "/index.html", wait_until="networkidle")     # abre a home de verdade, com os colchetes por desenhar
    page.evaluate("document.fonts.ready")
    r = Rec(page, H / "scripts" / "_tmp_desktop", 1920, 1080)
    page.mouse.move(1500, 700); r.x, r.y = 1500, 700
    r.pause(); r.rec = True

    # 1. hero: os colchetes se desenham
    r.wait(5.8)
    # 2. Seleção BK, passa o cursor por dois cards
    r.scroll_sel("#destaques", -10, 2.4); r.wait(1.0)
    r.go("#rail .card", 0.9, nth=1); r.wait(1.3)
    r.go("#rail .card", 0.7, nth=2); r.wait(1.3)
    # 3. jaqueta bege: abre, rola as fotos, escolhe M, adiciona
    r.click("#rail .card[data-p='1914786']", 0.8); r.wait(1.6)
    r.scroll_to(520, 1.8, sel="#pm"); r.wait(0.9)
    r.scroll_to(0, 1.2, sel="#pm"); r.wait(0.6)
    r.click(".sizes [data-size='M']", 0.9); r.wait(0.8)
    r.click("[data-add]", 0.8); r.wait(2.4)
    # 4. sacola com item e total; fecha
    r.click("#bag [data-close]", 0.9); r.wait(1.0)
    # 5. categorias, lookbook com filtro, como comprar
    r.scroll_sel("#categorias", -10, 2.4); r.wait(1.8)
    r.scroll_sel("#lookbook", -10, 2.2); r.wait(1.0)
    r.click("#lookChips .chip[data-l='conjuntos']", 1.0); r.wait(1.2)
    r.scroll_sel("#como-comprar", -10, 2.2); r.wait(1.2)
    # 6. tema claro
    r.scroll_to(0, 1.8); r.wait(0.8)
    r.click("[data-tema]", 1.0); r.wait(2.4)
    r.scroll_sel("#destaques", -10, 2.2); r.wait(1.4)
    # 7. a loja e o rodapé
    r.scroll_sel("#loja", 0, 2.4); r.wait(2.0)
    r.scroll_to(page.evaluate("document.documentElement.scrollHeight - innerHeight"), 2.6); r.wait(2.6)
    r.rec = False
    b.close()

dur = r.render(OUT, crf=20, maxrate="2800k")
print("quadros:", r.n, "| duração:", round(dur, 1), "s |", OUT.stat().st_size // 1024, "KB")
