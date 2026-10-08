"""Grava o vídeo de navegação do aplicativo (1080x1920, 30 quadros por segundo, sem som).

O que aparece é o aplicativo de verdade, aberto dentro de palco.html: o roteiro abaixo toca nos botões,
digita na busca, faz uma venda, confirma um pedido e dá uma entrada, e o navegador manda cada quadro.
Uso:  python gravar.py          Saída: ../video/bk-gestao-navegacao.mp4 e _conf-video.jpg (12 quadros).
Para mudar a ordem, o tempo ou as frases, editar a função roteiro().
"""
import asyncio
import base64
import shutil
import subprocess
import sys
import time
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
SAIDA = APP / "video"
SAIDA.mkdir(exist_ok=True)
QUADROS = AQUI / "_quadros"
PORTA = 4189
RELOGIO = "?agora=2026-10-08T18:40"   # dia e hora que o aplicativo mostra no vídeo
FPS = 30


async def main():
    shutil.rmtree(QUADROS, ignore_errors=True)
    QUADROS.mkdir()
    marcas = []   # (instante, arquivo)
    async with async_playwright() as p:
        nav = await p.chromium.launch(channel="chrome", headless=True)
        ctx = await nav.new_context(viewport={"width": 1080, "height": 1920}, device_scale_factor=1, locale="pt-BR")
        pg = await ctx.new_page()
        await pg.goto(f"http://localhost:{PORTA}/index.html{RELOGIO}")
        await pg.evaluate("localStorage.clear()")
        await pg.goto(f"http://localhost:{PORTA}/_trabalho/palco.html")
        await pg.evaluate("q => abrir(q)", RELOGIO)
        app = pg.frame_locator("#app")
        await app.locator(".hoje-v").wait_for()
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(1500)

        cdp = await ctx.new_cdp_session(pg)

        def chegou(ev):
            nome = QUADROS / f"{len(marcas):05d}.jpg"
            nome.write_bytes(base64.b64decode(ev["data"]))
            marcas.append((ev["metadata"]["timestamp"], nome))
            asyncio.ensure_future(cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]}))

        cdp.on("Page.screencastFrame", chegou)

        async def espera(s):
            await pg.wait_for_timeout(int(s * 1000))

        async def legenda(t, depois=0.0):
            await pg.evaluate("t => legenda(t)", t)
            await espera(0.45 + depois)

        async def toque(sel, antes=0.45, depois=0.9, n=0, leg=None):
            loc = app.locator(sel).nth(n)
            await loc.scroll_into_view_if_needed()
            await espera(0.1)
            c = await loc.bounding_box()
            await pg.evaluate("([x, y]) => dedo(x, y)", [c["x"] + c["width"] / 2, c["y"] + c["height"] / 2])
            await espera(antes)
            await pg.evaluate("toca()")
            await espera(0.14)
            if leg:   # a frase troca junto com a tela
                await pg.evaluate("t => legenda(t)", leg)
            await loc.click()
            await espera(depois)

        async def rolar(y, s=1.3):
            await app.locator("#tela").evaluate("(el, y) => el.scrollTo({ top: y, behavior: 'smooth' })", y)
            await espera(s)

        async def digita(sel, texto, depois=1.4):
            await app.locator(sel).press_sequentially(texto, delay=110)
            await espera(depois)

        async def roteiro():
            await legenda("Estoque e vendas da BK Clothing, no celular", 1.9)
            await legenda("Abriu, já mostra quanto vendeu hoje e o que precisa de atenção", 1.6)
            await rolar(300, 1.3)
            await espera(1.5)

            await toque("[data-a='ir-estoque'][data-st='baixo']", depois=1.9, leg="Cada peça com a quantidade por tamanho. O que falta fica em vermelho")
            await rolar(330, 1.3)
            await espera(0.9)
            await rolar(0, 0.8)

            await toque("#q", depois=0.2, leg="Busca por peça, marca ou cor")
            await digita("#q", "jaqueta", 1.1)
            await toque(".it[href='#/estoque/p/1914784']", depois=1.6, leg="Na peça: estoque por tamanho, margem e quanto tempo o estoque dura")
            await rolar(300, 1.3)
            await espera(1.9)
            await rolar(640, 1.3)
            await espera(1.5)

            await toque("#abas a[data-aba='vender']", depois=1.1, leg="Para vender: toca na peça, escolhe o tamanho e cobra")
            await toque(".tile[data-id='1914784']", depois=0.8)
            await toque("[data-a='add'][data-tam='M']", depois=0.9)
            await toque("#cobrar", depois=1.2)
            await rolar(420, 1.1)
            await espera(0.5)
            await toque("[data-a='concluir']", depois=3.3, leg="Vendeu: o estoque baixa sozinho e avisa o que esgotou")
            await toque("[data-a='comprovante']", depois=2.7, leg="Comprovante pronto para mandar no WhatsApp do cliente")
            await toque("[data-a='fechar']", depois=0.3)

            await toque("#abas a[data-aba='vendas']", depois=0.5)
            await toque("[data-a='aba'][data-v='pedidos']", depois=2.0, leg="Pedido que chega pelo site vira venda com um toque")
            await toque("[data-a='ped-ok']", depois=0.8)
            await toque("[data-a='ped-pg'][data-v='pix']", depois=2.5)

            await toque("#abas a[data-aba='mais']", depois=0.5)
            await toque("a[href='#/estoque/entrada']", depois=0.9, leg="Chegou mercadoria: entrada por tamanho")
            await toque(".it[data-id='1914784']", depois=0.8)
            for tam in ("M", "M", "G"):
                await toque(f"[data-a='en-q'][data-tam='{tam}'][data-q='1']", antes=0.38, depois=0.18)
            await espera(0.3)
            await toque("[data-a='en-ok']", depois=2.0)

            await toque("#abas a[data-aba='mais']", depois=0.5)
            await toque("a[href='#/mais/paradas']", depois=2.0, leg="Peças paradas há mais de 45 dias viram oferta para o grupo VIP")
            await rolar(250, 1.1)
            await espera(0.9)
            await rolar(0, 0.7)
            await toque("[data-a='msg-oferta']", depois=3.1)
            await toque("[data-a='fechar']", depois=0.3)

            await toque("[data-a='voltar']", depois=0.5)
            await toque("a[href='#/mais/reposicao']", depois=1.9, leg="A lista do que pedir ao fornecedor se monta sozinha")
            await rolar(280, 1.2)
            await espera(1.0)

            await toque("#abas a[data-aba='vendas']", depois=0.5)
            await toque("[data-a='aba'][data-v='resumo']", depois=1.6, leg="Vendas, lucro e formas de pagamento do período")
            await toque("[data-a='per'][data-v='30']", depois=1.3)
            await rolar(470, 1.4)
            await espera(1.5)

            await toque("#abas a[data-aba='mais']", depois=0.5)
            await toque("[data-a='fechamento']", depois=2.9, leg="Fechamento do dia em um toque, pronto para enviar")
            await toque("[data-a='fechar']", depois=0.3)
            await toque("#abas a[data-aba='inicio']", depois=0.3)
            await pg.evaluate("dedo(540, 2100)")
            await legenda("BK Gestão. Demonstração feita para a BK Clothing", 2.8)

        await cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 94, "maxWidth": 1080, "maxHeight": 1920, "everyNthFrame": 2})
        t_ini = time.time()
        await roteiro()
        fim = time.time()
        await cdp.send("Page.stopScreencast")
        await espera(0.3)
        await nav.close()
    print("quadros recebidos", len(marcas), "| duração", round(fim - t_ini, 1), "s")

    # cada quadro fica na tela até o seguinte chegar; o ffmpeg completa para 30 por segundo
    linhas = []
    for i, (t, nome) in enumerate(marcas):
        prox = marcas[i + 1][0] if i + 1 < len(marcas) else t + 0.5
        linhas.append(f"file '{nome.as_posix()}'\nduration {max(prox - t, 0.001):.4f}")
    linhas.append(f"file '{marcas[-1][1].as_posix()}'")
    (QUADROS / "lista.txt").write_text("\n".join(linhas), encoding="utf-8")
    saida = SAIDA / "bk-gestao-navegacao.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(QUADROS / "lista.txt"),
                    "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-crf", "19", "-preset", "slow",
                    "-movflags", "+faststart", str(saida)], check=True)

    idx = [int(len(marcas) * (k + 0.5) / 12) for k in range(12)]
    folha = Image.new("RGB", (6 * 270, 2 * 480))
    for n, i in enumerate(idx):
        folha.paste(Image.open(marcas[i][1]).resize((270, 480)), ((n % 6) * 270, (n // 6) * 480))
    folha.save(AQUI / "_conf-video.jpg", quality=85)
    shutil.rmtree(QUADROS, ignore_errors=True)
    print("ok", saida.name, round(saida.stat().st_size / 1e6, 1), "MB")


srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORTA), "--directory", str(APP)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    asyncio.run(main())
finally:
    srv.terminate()
