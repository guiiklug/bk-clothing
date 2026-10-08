"""Monta a tela de celular (1080x1920) do perfil da BK como está hoje, a partir do mock do documento."""
from pathlib import Path
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
CSS = '''
body>*{display:none!important}
#perfil-hoje{display:block!important;position:fixed;left:0;top:0;width:360px!important;max-width:none!important;border:0!important;font-size:13px}
html{font-size:13.3px!important}
'''
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 360, 'height': 640}, device_scale_factor=3)
    pg.goto((AQUI.parent / 'index.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(1200)
    pg.evaluate('''css => { const el = document.getElementById('perfil-hoje'); document.body.appendChild(el);
        const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s); }''', CSS)
    pg.wait_for_timeout(400)
    pg.screenshot(path=str(AQUI / 'insta-atual-celular.jpg'), type='jpeg', quality=92)
    b.close()
print('ok')
