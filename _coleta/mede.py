"""Mede elementos do site2 para depurar layout. Uso: python mede.py"""
from pathlib import Path
from playwright.sync_api import sync_playwright
S2 = Path(__file__).resolve().parent.parent / 'site2'
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    pg.goto((S2 / 'index.html').as_uri())
    pg.wait_for_timeout(1500)
    print(pg.evaluate('''() => { const r = s => { const e = document.querySelector(s); const b = e.getBoundingClientRect(); const c = getComputedStyle(e);
        return s + ' ' + [b.left, b.top + scrollY, b.width, b.height].map(Math.round).join(',') + ' pos=' + c.position + ' fit=' + c.objectFit + ' tr=' + c.transform; };
        return [r('.catg .bn'), r('.catg .bn .md'), r('.catg .bn .md img.ft'), r('.catg .bn .pal b')].join('\\n'); }'''))
    pg.locator('.catg').scroll_into_view_if_needed()
    pg.evaluate("document.querySelectorAll('.rv').forEach(e=>{e.style.transition='none';e.classList.add('in')})")
    pg.wait_for_timeout(500)
    pg.locator('.catg').screenshot(path=str(S2.parent / '_coleta' / 'conf2' / 'catg.jpg'), type='jpeg', quality=80)
    b.close()
