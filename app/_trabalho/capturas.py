"""Abre o aplicativo no tamanho de um celular, passa pelas telas principais fazendo uma venda de verdade
e guarda uma foto de cada tela em ../telas/. No fim monta folhas de conferência (_folha-N.jpg).

Uso:  python capturas.py            (todas as telas, tema claro)
Sobe um servidor local só durante a execução. Erros de console aparecem no fim.
"""
import subprocess
import sys
import time
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
TELAS = APP / "telas"
TELAS.mkdir(exist_ok=True)
PORTA = 4188
BASE = f"http://localhost:{PORTA}/index.html?agora=2026-10-08T18:40"
L, A = 390, 844

srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORTA), "--directory", str(APP)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
erros, feitas = [], []
try:
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome", headless=True)
        ctx = nav.new_context(viewport={"width": L, "height": A}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="pt-BR")
        pg = ctx.new_page()
        pg.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: erros.append("ERRO " + str(e)))

        def foto(nome, espera=450):
            pg.wait_for_timeout(espera)
            pg.screenshot(path=str(TELAS / f"{nome}.png"))
            feitas.append(nome)

        def ir(rota):
            pg.evaluate("r => { location.hash = r }", rota)
            pg.wait_for_timeout(350)

        def rolar(y):
            pg.evaluate("y => document.getElementById('tela').scrollTo(0, y)", y)

        pg.goto(BASE)
        pg.evaluate("localStorage.clear()")
        pg.reload()
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(900)
        foto("01-inicio")
        rolar(520); foto("02-inicio-atencao")

        ir("#/estoque"); foto("03-estoque", 700)
        pg.click("[data-a='f-st'][data-v='baixo']"); foto("04-estoque-acabando")
        pg.click("[data-a='f-st'][data-v='']")
        pg.fill("#q", "moletom"); foto("05-estoque-busca")
        pg.fill("#q", "")

        ir("#/estoque/p/1914784"); foto("06-produto", 700)
        rolar(430); foto("07-produto-tamanhos")
        rolar(1100); foto("08-produto-giro")

        ir("#/vender"); foto("09-vender", 700)
        pg.click(".tile[data-id='1914784']"); foto("10-vender-tamanho")
        pg.click("[data-a='add'][data-tam='M']"); pg.wait_for_timeout(500)
        pg.click(".tile[data-id='1849734']"); pg.wait_for_timeout(400)
        pg.click("[data-a='add']"); foto("11-vender-sacola", 2600)
        pg.click("#cobrar"); foto("12-cobrar", 600)
        rolar(600); foto("13-cobrar-total")
        pg.click("[data-a='concluir']"); foto("14-venda-registrada", 700)
        pg.click("[data-a='comprovante']"); foto("15-comprovante", 600)
        pg.click("[data-a='fechar']"); pg.wait_for_timeout(400)

        ir("#/"); foto("16-inicio-depois", 600)
        ir("#/vendas"); foto("17-vendas-historico", 600)
        pg.click("[data-a='aba'][data-v='resumo']"); foto("18-vendas-resumo")
        rolar(560); foto("19-vendas-resumo-2")
        pg.click("[data-a='aba'][data-v='pedidos']"); foto("20-pedidos")

        ir("#/mais"); foto("21-mais", 600)
        ir("#/mais/paradas"); foto("22-paradas", 700)
        pg.click("[data-a='msg-oferta']"); foto("23-oferta-vip", 600)
        pg.click("[data-a='fechar']"); pg.wait_for_timeout(400)
        ir("#/mais/reposicao"); foto("24-reposicao", 700)
        ir("#/estoque/entrada"); pg.wait_for_timeout(500)
        pg.click(".it[data-id='1914784']"); pg.wait_for_timeout(400)
        pg.click("[data-a='en-q'][data-tam='M'][data-q='1']"); pg.click("[data-a='en-q'][data-tam='M'][data-q='1']")
        pg.click("[data-a='en-q'][data-tam='G'][data-q='1']"); foto("25-entrada")
        pg.click("[data-a='en-ok']"); foto("26-entrada-feita", 2600)
        ir("#/estoque/novo"); foto("27-cadastrar", 600)
        ir("#/mais/clientes"); foto("28-clientes", 600)
        ir("#/mais"); pg.click("[data-a='fechamento']"); foto("29-fechamento", 600)
        pg.click("[data-a='fechar']"); pg.wait_for_timeout(400)
        pg.click("[data-a='tema']"); ir("#/"); foto("30-inicio-escuro", 600)
        ir("#/estoque"); foto("31-estoque-escuro", 700)
        nav.close()
finally:
    srv.terminate()

POR = 8
for k in range(0, len(feitas), POR):
    grupo = feitas[k:k + POR]
    folha = Image.new("RGB", (POR * 310, 660), "#2b2b2b")
    for i, n in enumerate(grupo):
        folha.paste(Image.open(TELAS / f"{n}.png").convert("RGB").resize((300, 649), Image.LANCZOS), (i * 310 + 5, 5))
    folha.save(AQUI / f"_folha-{k // POR + 1}.jpg", quality=86)
print("telas", len(feitas))
print("erros:", erros if erros else "nenhum")
