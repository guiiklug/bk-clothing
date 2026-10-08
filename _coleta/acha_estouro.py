"""Lista os elementos que passam da largura da tela no celular (para achar rolagem lateral)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
S2 = Path(__file__).resolve().parent.parent / 'site2'
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 375, 'height': 760})
    pg.goto((S2 / 'index.html').as_uri())
    pg.wait_for_timeout(1500)
    print(pg.evaluate('''() => [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.right > 376 && getComputedStyle(e).position !== 'fixed' && !e.closest('.trilho') && !e.closest('.tb') && !e.closest('.bag') && !e.closest('.pm'); })
        .slice(0, 12).map(e => e.tagName + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().right)).join('\\n')'''))
    b.close()
