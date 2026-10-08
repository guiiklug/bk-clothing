"""Prints do site novo (local) e do site atual para a apresentação.
Uso: .venv/Scripts/python scripts/prints.py   (servidor em http://localhost:4174 com site/ ligado)
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

BASE = "http://localhost:4174"
OUT = pathlib.Path(__file__).resolve().parent.parent / "apresentacao" / "img"
OUT.mkdir(parents=True, exist_ok=True)

SETUP = """(()=>{try{localStorage.setItem('bk_tema','%s');localStorage.setItem('bk_arte','a');localStorage.removeItem('bk_sacola')}catch(e){}})()"""
FREEZE = "document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'));document.querySelectorAll('.draw').forEach(e=>{e.style.transition='none';e.style.strokeDashoffset=0});document.querySelectorAll('.fade').forEach(e=>{e.style.transition='none';e.style.opacity=1})"


def prep(page, tema):
    page.add_init_script(SETUP % tema)


def settle(page):
    page.evaluate("document.fonts.ready")
    # percorre a página para carregar imagens preguiçosas
    h = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < h:
        page.evaluate(f"window.scrollTo(0,{y})"); page.wait_for_timeout(120); y += 600
    page.evaluate("window.scrollTo(0,0)")
    page.evaluate(FREEZE)
    page.wait_for_timeout(1800)


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for tema in ("dark", "light"):
            # desktop
            ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
            pg = ctx.new_page(); prep(pg, tema)
            pg.goto(BASE + "/index.html", wait_until="networkidle"); settle(pg)
            pg.screenshot(path=OUT / f"home-desktop-{tema}.png")
            pg.evaluate("document.querySelector('#destaques').scrollIntoView()"); pg.wait_for_timeout(600)
            pg.screenshot(path=OUT / f"selecao-desktop-{tema}.png")
            pg.evaluate("document.querySelector('#lookbook').scrollIntoView()"); pg.wait_for_timeout(600)
            pg.screenshot(path=OUT / f"lookbook-desktop-{tema}.png")
            # produto aberto
            pg.evaluate("window.scrollTo(0,0)")
            pg.goto(BASE + "/index.html#p=1914786", wait_until="networkidle"); pg.wait_for_timeout(1500)
            pg.screenshot(path=OUT / f"produto-desktop-{tema}.png")
            pg.click("[data-size='M']"); pg.click("[data-add]"); pg.wait_for_timeout(900)
            pg.screenshot(path=OUT / f"sacola-desktop-{tema}.png")
            pg.goto(BASE + "/catalogo.html", wait_until="networkidle"); settle(pg)
            pg.screenshot(path=OUT / f"catalogo-desktop-{tema}.png")
            ctx.close()
            # celular
            ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True)
            pg = ctx.new_page(); prep(pg, tema)
            pg.goto(BASE + "/index.html", wait_until="networkidle"); settle(pg)
            pg.screenshot(path=OUT / f"home-mobile-{tema}.png")
            pg.evaluate("document.querySelector('#destaques').scrollIntoView()"); pg.wait_for_timeout(600)
            pg.screenshot(path=OUT / f"selecao-mobile-{tema}.png")
            pg.goto(BASE + "/index.html#p=1914786", wait_until="networkidle"); pg.wait_for_timeout(1500)
            pg.screenshot(path=OUT / f"produto-mobile-{tema}.png")
            pg.click("[data-size='M']"); pg.click("[data-add]"); pg.wait_for_timeout(900)
            pg.screenshot(path=OUT / f"sacola-mobile-{tema}.png")
            pg.goto(BASE + "/links.html", wait_until="networkidle"); settle(pg)
            pg.screenshot(path=OUT / f"links-mobile-{tema}.png")
            ctx.close()
        # site atual
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        pg = ctx.new_page()
        try:
            pg.goto("https://bkclothing.com.br/", wait_until="load", timeout=30000); pg.wait_for_timeout(4000)
            pg.screenshot(path=OUT / "site-atual-desktop.png")
            print("site atual: ok", pg.title())
        except Exception as e:
            print("site atual: FALHOU", e)
        ctx.close(); b.close()


if __name__ == "__main__":
    main()
