"""Exporta a apresentação (HTML) para dois PDFs 1920x1080, um por tema, e mede estouros.
Uso: .venv/Scripts/python scripts/exportar_pdf.py
Saída: entregas/bk-apresentacao-escura.pdf e entregas/bk-apresentacao-clara.pdf
"""
import pathlib, json
from playwright.sync_api import sync_playwright

H = pathlib.Path(__file__).resolve().parent.parent
HTML = (H / "apresentacao" / "apresentacao.html").as_uri()
OUT = H / "entregas"; OUT.mkdir(exist_ok=True)

# mede: texto cortado/estourando caixa e elementos fora da área útil
CHECK = """() => {
  const probs = [];
  document.querySelectorAll('.pg').forEach(pg => {
    const pr = pg.getBoundingClientRect();
    const area = pg.querySelector('.area').getBoundingClientRect();
    pg.querySelectorAll('.area *').forEach(el => {
      if (el.closest('svg') || el.tagName === 'IMG') return;
      const r = el.getBoundingClientRect(); if (!r.width) return;
      if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).display !== 'inline')
        probs.push([pg.id, 'estoura-largura', el.className || el.tagName, el.scrollWidth, el.clientWidth]);
      if (r.bottom > area.bottom + 1 || r.right > area.right + 1 || r.left < area.left - 1)
        probs.push([pg.id, 'fora-da-area', el.className || el.tagName, Math.round(r.bottom - area.bottom), Math.round(r.right - area.right)]);
    });
    pg.querySelectorAll('.mold img').forEach(i => { if (!i.complete || !i.naturalWidth) probs.push([pg.id, 'imagem-quebrada', i.src]); });
  });
  return probs;
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for nome, q in (("escura", ""), ("clara", "?tema=claro")):
        ctx = b.new_context(viewport={"width": 1920, "height": 1080})
        pg = ctx.new_page()
        pg.goto(HTML + q, wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        fam = pg.evaluate("[document.fonts.check('40px \"Bebas Neue\"'), document.fonts.check('300 20px Jost')]")
        pg.wait_for_timeout(800)
        probs = pg.evaluate(CHECK)
        print(nome, "fontes ok:", fam, "| problemas:", json.dumps(probs, ensure_ascii=False))
        pg.pdf(path=str(OUT / f"bk-apresentacao-{nome}.pdf"), width="1920px", height="1080px",
               print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        # PNG por página para conferir
        for i in range(1, 12):
            pg.locator(f"#p{i}").screenshot(path=str(H / "apresentacao" / f"_p{i:02d}-{nome}.png"))
        ctx.close()
    b.close()
