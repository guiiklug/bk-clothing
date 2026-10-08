"""Fotografa a primeira tela de lojas de streetwear de referência e monta uma folha de comparação."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / 'referencias'
SAIDA.mkdir(exist_ok=True)
SITES = {
    'guadalupe': 'https://www.guadalupestore.com.br/',
    'cartel011': 'https://shop.cartel011.com.br/',
    'yourid': 'https://www.youridstore.com.br/',
    'ostore': 'https://www.ostore.com.br/',
    'kith': 'https://kith.com/',
    'aimeleondore': 'https://www.aimeleondore.com/',
    'stussy': 'https://www.stussy.com/',
    'pace': 'https://www.pacecompany.com.br/',
    'piet': 'https://www.piet.com.br/',
}
ok = []
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR',
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36')
    for nome, url in SITES.items():
        pg = ctx.new_page()
        try:
            pg.goto(url, timeout=25000, wait_until='domcontentloaded')
            pg.wait_for_timeout(3500)
            a = SAIDA / f'{nome}-1.jpg'
            pg.screenshot(path=str(a), type='jpeg', quality=70)
            pg.mouse.wheel(0, 900)
            pg.wait_for_timeout(1500)
            c = SAIDA / f'{nome}-2.jpg'
            pg.screenshot(path=str(c), type='jpeg', quality=70)
            ok.append(nome)
        except Exception as e:
            print('falhou', nome, str(e)[:80])
        pg.close()
    b.close()
w, h = 480, 300
S = Image.new('RGB', (len(ok) * w, 2 * h + 22), 'white')
d = ImageDraw.Draw(S)
for i, n in enumerate(ok):
    d.text((i * w + 6, 4), n, fill='black')
    for k in (1, 2):
        S.paste(Image.open(SAIDA / f'{n}-{k}.jpg').resize((w, h)), (i * w, 22 + (k - 1) * h))
S.save(SAIDA / '_folha.jpg', quality=80)
print('ok', ok)
