"""Grava o vídeo explicado do aplicativo: a mesma navegação de gravar.py, no tempo da narração.

Cada cena tem uma fala (FALAS). Se existir o áudio da fala em ../video/voz/NN.mp3 (ou .wav), a cena dura o
tempo desse áudio e a voz entra no vídeo no instante em que a cena abre. Enquanto o áudio não existe, o tempo
da fala é estimado pelo número de palavras e o vídeo sai mudo, só para conferir o ritmo.

Uso:  python gravar_narrado.py
Saída: ../video/bk-gestao-explicado.mp4, ../video/roteiro-de-voz.md (o texto para ler ou gerar) e _conf-narrado.jpg.
Para mudar uma fala, editar FALAS aqui, gerar de novo só o áudio daquela fala e rodar outra vez.
"""
import asyncio
import base64
import shutil
import subprocess
import sys
import time
from pathlib import Path
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
SAIDA = APP / "video"
VOZ = SAIDA / "voz"
VOZ.mkdir(parents=True, exist_ok=True)
QUADROS = AQUI / "_quadros_n"
PORTA = 4191
RELOGIO = "?agora=2026-10-08T18:40"
FPS = 30
RESPIRO = 0.45     # silêncio depois de cada fala
ENTRADA = 0.25     # a voz entra um instante depois de a tela abrir

# número da cena: (fala narrada, frase curta que aparece em cima do aplicativo)
FALAS = {
    "01": ("Bruno, esse é o BK Gestão: o estoque e as vendas da loja, no teu celular.",
           "Estoque e vendas da BK Clothing, no celular"),
    "02": ("Abriu, tu já vê quanto vendeu hoje e o que precisa de atenção: peça esgotada, acabando ou parada.",
           "Quanto vendeu hoje e o que precisa de atenção"),
    "03": ("No estoque, cada peça mostra a quantidade por tamanho. O que está faltando aparece em vermelho.",
           "Cada peça com a quantidade por tamanho"),
    "04": ("Para achar uma peça, é só digitar o nome, a marca ou a cor.",
           "Busca por peça, marca ou cor"),
    "05": ("Dentro da peça, tu ajusta cada tamanho, vê a margem e quanto tempo o estoque dura no ritmo de venda.",
           "Estoque por tamanho, margem e duração do estoque"),
    "06": ("Para vender, toca na peça, escolhe o tamanho e cobra.",
           "Para vender: peça, tamanho e cobrar"),
    "07": ("Vendeu, o estoque baixa sozinho. E o aplicativo avisa quando um tamanho esgota.",
           "Vendeu, o estoque baixa sozinho"),
    "08": ("O comprovante já sai pronto para mandar no WhatsApp do cliente.",
           "Comprovante pronto para o WhatsApp"),
    "09": ("Com o site ligado, o pedido de lá aparece aqui. Confirmou o pagamento, virou venda.",
           "Pedido do site vira venda com um toque"),
    "10": ("Chegou mercadoria? Tu dá entrada por tamanho, em poucos toques.",
           "Chegou mercadoria: entrada por tamanho"),
    "11": ("Peças paradas há mais de quarenta e cinco dias viram uma oferta pronta para o grupo VIP.",
           "Peças paradas viram oferta para o grupo VIP"),
    "12": ("A lista do que pedir ao fornecedor se monta sozinha, com base no que mais vende.",
           "A lista de reposição se monta sozinha"),
    "13": ("No resumo, tu acompanha as vendas, o lucro estimado e as formas de pagamento do período.",
           "Vendas, lucro e formas de pagamento"),
    "14": ("E no fim do dia, o fechamento sai em um toque.",
           "Fechamento do dia em um toque"),
    "15": ("Tudo isso feito para a BK, com as tuas peças, no teu celular.",
           "BK Gestão. Feito para a BK Clothing"),
}


def audio_de(n):
    for ext in ("mp3", "wav", "m4a"):
        a = VOZ / f"{n}.{ext}"
        if a.exists():
            return a
    return None


def duracao(n):
    a = audio_de(n)
    if a:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(a)],
                           capture_output=True, text=True, check=True)
        return float(r.stdout.strip())
    return max(1.8, len(FALAS[n][0].split()) / 2.5 + 0.5)   # estimativa: 2,5 palavras por segundo


def escrever_roteiro():
    palavras = sum(len(f.split()) for f, _ in FALAS.values())
    l = ["# BK Gestão: roteiro de voz", "",
         f"{len(FALAS)} falas, {palavras} palavras, perto de {round(sum(duracao(n) for n in FALAS))} segundos de fala.",
         "Texto gerado por `_trabalho/gravar_narrado.py`; para mudar uma fala, editar lá.", ""]
    for n, (fala, leg) in FALAS.items():
        l += [f"**{n}** ({leg})", "", fala, ""]
    (SAIDA / "roteiro-de-voz.md").write_text("\n".join(l), encoding="utf-8")


async def main():
    shutil.rmtree(QUADROS, ignore_errors=True)
    QUADROS.mkdir()
    marcas = []
    inicios = {}                 # cena -> segundo do vídeo em que a fala começa
    estado = {"fim": 0.0}        # segundo em que a fala atual termina
    dur = {n: duracao(n) for n in FALAS}
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

        def agora():
            return time.time() - marcas[0][0] if marcas else 0.0

        async def espera(s):
            if s > 0:
                await pg.wait_for_timeout(int(s * 1000))

        async def fecha_fala(folga=0.0):
            """Espera a fala anterior acabar (menos a folga, que é o tempo do dedo indo até o próximo toque)."""
            await espera(estado["fim"] - agora() - folga)

        def abre_fala(n):
            inicios[n] = agora() + ENTRADA
            estado["fim"] = inicios[n] + dur[n] + RESPIRO

        async def legenda(n):
            await fecha_fala()
            await pg.evaluate("t => legenda(t)", FALAS[n][1])
            abre_fala(n)
            await espera(0.45)

        async def toque(sel, antes=0.45, depois=0.9, n=0, fala=None):
            if fala:
                await fecha_fala(folga=antes + 0.25)
            loc = app.locator(sel).nth(n)
            await loc.scroll_into_view_if_needed()
            await espera(0.1)
            c = await loc.bounding_box()
            await pg.evaluate("([x, y]) => dedo(x, y)", [c["x"] + c["width"] / 2, c["y"] + c["height"] / 2])
            await espera(antes)
            await pg.evaluate("toca()")
            await espera(0.14)
            if fala:
                await pg.evaluate("t => legenda(t)", FALAS[fala][1])
            await loc.click()
            if fala:
                abre_fala(fala)
            await espera(depois)

        async def rolar(y, s=1.3):
            await app.locator("#tela").evaluate("(el, y) => el.scrollTo({ top: y, behavior: 'smooth' })", y)
            await espera(s)

        async def digita(sel, texto, depois=1.4):
            await app.locator(sel).press_sequentially(texto, delay=110)
            await espera(depois)

        async def roteiro():
            await espera(0.4)
            await legenda("01")
            await legenda("02")
            await espera(1.2)
            await rolar(300, 1.4)

            await toque("[data-a='ir-estoque'][data-st='baixo']", depois=1.6, fala="03")
            await rolar(330, 1.4)
            await espera(1.0)
            await rolar(0, 0.8)

            await toque("#q", depois=0.2, fala="04")
            await digita("#q", "jaqueta", 1.0)
            await toque(".it[href='#/estoque/p/1914784']", depois=1.6, fala="05")
            await rolar(300, 1.4)
            await espera(2.2)
            await rolar(640, 1.4)
            await espera(1.4)

            await toque("#abas a[data-aba='vender']", depois=1.1, fala="06")
            await toque(".tile[data-id='1914784']", depois=0.8)
            await toque("[data-a='add'][data-tam='M']", depois=0.9)
            await toque("#cobrar", depois=1.2)
            await rolar(420, 1.1)
            await espera(0.4)
            await toque("[data-a='concluir']", depois=1.5, fala="07")
            await toque("[data-a='comprovante']", depois=1.5, fala="08")
            await fecha_fala()
            await toque("[data-a='fechar']", depois=0.3)

            await toque("#abas a[data-aba='vendas']", depois=0.5)
            await toque("[data-a='aba'][data-v='pedidos']", depois=2.2, fala="09")
            await toque("[data-a='ped-ok']", depois=0.8)
            await toque("[data-a='ped-pg'][data-v='pix']", depois=1.6)

            await toque("#abas a[data-aba='mais']", depois=0.5, fala=None)
            await fecha_fala(folga=0.7)
            await toque("a[href='#/estoque/entrada']", depois=0.9, fala="10")
            await toque(".it[data-id='1914784']", depois=0.8)
            for tam in ("M", "M", "G"):
                await toque(f"[data-a='en-q'][data-tam='{tam}'][data-q='1']", antes=0.38, depois=0.18)
            await espera(0.3)
            await toque("[data-a='en-ok']", depois=1.4)

            await fecha_fala(folga=1.6)
            await toque("#abas a[data-aba='mais']", depois=0.5)
            await toque("a[href='#/mais/paradas']", depois=2.0, fala="11")
            await rolar(250, 1.1)
            await espera(0.9)
            await rolar(0, 0.7)
            await toque("[data-a='msg-oferta']", depois=2.2)
            await fecha_fala()
            await toque("[data-a='fechar']", depois=0.3)

            await toque("[data-a='voltar']", depois=0.5)
            await toque("a[href='#/mais/reposicao']", depois=1.9, fala="12")
            await rolar(280, 1.3)

            await fecha_fala(folga=1.6)
            await toque("#abas a[data-aba='vendas']", depois=0.5)
            await toque("[data-a='aba'][data-v='resumo']", depois=1.5, fala="13")
            await toque("[data-a='per'][data-v='30']", depois=1.2)
            await rolar(470, 1.5)

            await fecha_fala(folga=1.6)
            await toque("#abas a[data-aba='mais']", depois=0.5)
            await toque("[data-a='fechamento']", depois=1.5, fala="14")
            await fecha_fala()
            await toque("[data-a='fechar']", depois=0.3)
            await toque("#abas a[data-aba='inicio']", depois=0.3)
            await pg.evaluate("dedo(540, 2100)")
            await legenda("15")
            await fecha_fala()
            await espera(1.0)

        await cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 94, "maxWidth": 1080, "maxHeight": 1920, "everyNthFrame": 2})
        while not marcas:
            await pg.wait_for_timeout(30)
        await roteiro()
        total = agora()
        await cdp.send("Page.stopScreencast")
        await pg.wait_for_timeout(300)
        await nav.close()

    linhas = []
    for i, (t, nome) in enumerate(marcas):
        prox = marcas[i + 1][0] if i + 1 < len(marcas) else marcas[0][0] + total
        linhas.append(f"file '{nome.as_posix()}'\nduration {max(prox - t, 0.001):.4f}")
    linhas.append(f"file '{marcas[-1][1].as_posix()}'")
    (QUADROS / "lista.txt").write_text("\n".join(linhas), encoding="utf-8")

    com_voz = [n for n in FALAS if audio_de(n)]
    saida = SAIDA / "bk-gestao-explicado.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(QUADROS / "lista.txt")]
    for n in com_voz:
        cmd += ["-i", str(audio_de(n))]
    video = f"[0:v]fps={FPS},format=yuv420p[v]"
    if com_voz:
        partes = [f"[{k + 1}:a]aresample=48000,adelay={round(inicios[n] * 1000)}:all=1[a{k}]" for k, n in enumerate(com_voz)]
        mix = "".join(f"[a{k}]" for k in range(len(com_voz))) + f"amix=inputs={len(com_voz)}:normalize=0:dropout_transition=0,apad[a]"
        cmd += ["-filter_complex", ";".join([video] + partes + [mix]), "-map", "[v]", "-map", "[a]", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}"]
    else:
        cmd += ["-filter_complex", video, "-map", "[v]"]
    cmd += ["-c:v", "libx264", "-crf", "19", "-preset", "slow", "-movflags", "+faststart", str(saida)]
    subprocess.run(cmd, check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(saida), "-vf", f"fps=18/{total:.1f},scale=270:480,tile=9x2",
                    "-frames:v", "1", "-q:v", "3", str(AQUI / "_conf-narrado.jpg")], check=True)
    shutil.rmtree(QUADROS, ignore_errors=True)

    print(f"duração {total:.1f} s | falas com áudio: {len(com_voz)} de {len(FALAS)}" + ("" if com_voz else " (vídeo mudo, tempos estimados)"))
    for n in FALAS:
        print(f"  {n}  entra {inicios[n]:6.1f} s  dura {dur[n]:4.1f} s  {'voz' if audio_de(n) else 'est.'}  {FALAS[n][0][:58]}")
    print("ok", saida.name, round(saida.stat().st_size / 1e6, 1), "MB")


escrever_roteiro()
if "--roteiro" not in sys.argv:
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORTA), "--directory", str(APP)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    try:
        asyncio.run(main())
    finally:
        srv.terminate()
