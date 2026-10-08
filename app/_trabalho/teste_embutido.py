"""Confere a versão que abre dentro do Claude (artefato.html) antes de publicar.

Monta a página como o Claude monta (casca com doctype em volta do conteúdo), abre dentro de uma moldura
do tamanho de um celular e navega só por toques: abas, peça, voltar, venda inteira. O endereço da moldura
não pode mudar. Saída: _teste-embutido.jpg e a lista de erros.
"""
import subprocess
import sys
import time
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
PORTA = 4190
CASCA = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
         '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
         '<style>:root{color-scheme:light;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}'
         'body{margin:0;font:14px system-ui,sans-serif;background:#faf9f5}img{max-width:100%}[hidden]{display:none!important}</style>'
         '</head><body>')
(APP / "_artefato_teste.html").write_text(CASCA + (APP / "artefato.html").read_text(encoding="utf-8") + "</body></html>", encoding="utf-8")
(APP / "_moldura_teste.html").write_text(
    '<!doctype html><meta charset="utf-8"><body style="margin:0;background:#222">'
    '<iframe id="app" src="_artefato_teste.html" style="display:block;border:0;width:390px;height:780px"></iframe></body>', encoding="utf-8")

srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORTA), "--directory", str(APP)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
erros, fotos = [], []
try:
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome", headless=True)
        pg = nav.new_page(viewport={"width": 390, "height": 780}, device_scale_factor=2)
        pg.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: erros.append("ERRO " + str(e)))
        pg.goto(f"http://localhost:{PORTA}/_moldura_teste.html")
        app = pg.frame_locator("#app")
        app.locator(".hoje-v").wait_for()
        pg.wait_for_timeout(900)

        def foto(n):
            pg.wait_for_timeout(500)
            arq = AQUI / f"_t{n}.png"
            pg.screenshot(path=str(arq))
            fotos.append(arq)

        def titulo():
            return app.locator("#topo h1").inner_text() if app.locator("#topo:not([hidden])").count() else "(início)"

        passos = []
        foto(1)
        app.locator("#abas a[data-aba='estoque']").click(); passos.append(("aba estoque", titulo()))
        app.locator(".it[href='#/estoque/p/1914784']").click(); pg.wait_for_timeout(300); passos.append(("abre peça", titulo())); foto(2)
        app.locator("[data-a='voltar']").click(); pg.wait_for_timeout(300); passos.append(("voltar", titulo()))
        app.locator("#abas a[data-aba='vender']").click()
        app.locator(".tile[data-id='1914784']").click(); pg.wait_for_timeout(400)
        app.locator("[data-a='add'][data-tam='M']").click(); pg.wait_for_timeout(500)
        app.locator("#cobrar").click(); pg.wait_for_timeout(300); passos.append(("cobrar", titulo())); foto(3)
        app.locator("[data-a='concluir']").click(); pg.wait_for_timeout(400); passos.append(("venda", titulo())); foto(4)
        app.locator("a.lk[href='#/']").click(); pg.wait_for_timeout(300); passos.append(("início", titulo()))
        app.locator("[data-a='ir-estoque'][data-st='zero']").click(); pg.wait_for_timeout(300); passos.append(("esgotadas", titulo()))
        app.locator("#abas a[data-aba='mais']").click()
        app.locator("a[href='#/mais/paradas']").click(); pg.wait_for_timeout(300); passos.append(("paradas", titulo())); foto(5)
        app.locator("[data-a='voltar']").click(); pg.wait_for_timeout(300); passos.append(("voltar", titulo()))
        endereco = pg.frames[1].url
        nav.close()
finally:
    srv.terminate()
    for f in ("_artefato_teste.html", "_moldura_teste.html"):
        (APP / f).unlink(missing_ok=True)

folha = Image.new("RGB", (len(fotos) * 400, 790), "#222")
for i, f in enumerate(fotos):
    folha.paste(Image.open(f).convert("RGB").resize((390, 780), Image.LANCZOS), (i * 400 + 5, 5))
    f.unlink()
folha.save(AQUI / "_teste-embutido.jpg", quality=86)
print("passos:", passos)
print("endereço da moldura no fim:", endereco)
print("erros:", erros if erros else "nenhum")
