"""Fotografa as telas que os aplicativos de venda e estoque mais usados mostram na loja do Google Play.

Só abre a página pública de cada aplicativo, sem login e sem clicar em nada, e fotografa as capturas de tela
que o próprio fabricante publica. Saída: referencias/ e folha-referencias-N.jpg (uma linha por aplicativo).
"""
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
SAIDA = AQUI / "referencias"
SAIDA.mkdir(exist_ok=True)
APPS = {
    "kyte": "com.kyte",
    "loyverse": "com.loyverse.sale",
    "shopify-pos": "com.shopify.pos",
    "shopify": "com.shopify.mobile",
    "square": "com.squareup",
    "zoho-inventory": "com.zoho.inventory",
    "sumup": "com.kaching.merchant",
    "sortly": "com.sortly.android",
    "nuvemshop": "com.tiendanube.app",
    "bling": "br.com.bling.app",
    "lightspeed": "com.vendhq.scanner",
}
POR_APP = 5
ALT = 560

feitos = []
with sync_playwright() as pw:
    nav = pw.chromium.launch(channel="chrome", headless=True)
    ctx = nav.new_context(viewport={"width": 1500, "height": 1000}, device_scale_factor=2, locale="pt-BR")
    for nome, pacote in APPS.items():
        pg = ctx.new_page()
        try:
            resp = pg.goto(f"https://play.google.com/store/apps/details?id={pacote}&hl=pt_BR&gl=BR",
                           wait_until="domcontentloaded", timeout=35000)
            if not resp or resp.status != 200:
                print(nome, "sem página", resp.status if resp else "?")
                pg.close()
                continue
            pg.wait_for_timeout(2500)
            titulo = pg.title()[:70]
            imgs = pg.locator("img[src*='play-lh.googleusercontent.com']")
            achadas = 0
            for i in range(imgs.count()):
                if achadas >= POR_APP:
                    break
                el = imgs.nth(i)
                cx = el.bounding_box()
                if not cx or cx["height"] < 180 or cx["height"] < cx["width"] * 1.4:
                    continue  # só captura em pé (tela de celular)
                el.scroll_into_view_if_needed(timeout=4000)
                pg.wait_for_timeout(250)
                el.screenshot(path=str(SAIDA / f"{nome}-{achadas}.png"))
                achadas += 1
            print(nome, "|", titulo.encode("ascii", "replace").decode(), "| telas", achadas)
            if achadas:
                feitos.append((nome, achadas))
        except Exception as e:
            print(nome, "FALHOU", repr(e)[:120])
        pg.close()
    nav.close()

LINHAS = 4
for k in range(0, len(feitos), LINHAS):
    grupo = feitos[k:k + LINHAS]
    larg = 300
    folha = Image.new("RGB", (POR_APP * (larg + 10) + 130, len(grupo) * (ALT + 14)), "#2b2b2b")
    d = ImageDraw.Draw(folha)
    for li, (nome, n) in enumerate(grupo):
        y = li * (ALT + 14)
        d.text((8, y + 10), nome, fill="white")
        for j in range(n):
            im = Image.open(SAIDA / f"{nome}-{j}.png").convert("RGB")
            im = im.resize((round(im.width * ALT / im.height), ALT), Image.LANCZOS)
            folha.paste(im.crop((0, 0, min(im.width, larg), ALT)), (130 + j * (larg + 10), y))
    destino = AQUI / f"folha-referencias-{k // LINHAS + 1}.jpg"
    folha.save(destino, quality=82)
    print(destino.name, folha.size)
