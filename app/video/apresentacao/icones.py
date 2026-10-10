"""Renderiza os ícones do plano (traço off-white, sem preenchimento) em PNG transparente 240x240.

Saída: _trabalho/icones/<nome>.png. A marca usa a fonte Jost local (fontes/Jost.ttf).
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "_trabalho" / "icones"
FONTE = AQUI / "fontes" / "Jost.ttf"

ICONES = {
    "marca": ('0 0 30 34', '<path d="M10 2H2v30h8M20 2h8v30h-8"/><text x="15" y="21" text-anchor="middle" font-family="Jost" font-weight="300" font-size="11" fill="#f3f0ea" stroke="none">BK</text>'),
    "inicio": ('0 0 24 24', '<path d="M4 10.5 12 4l8 6.5V20h-5.5v-6h-5v6H4z"/>'),
    "estoque": ('0 0 24 24', '<path d="M4 8l8-4 8 4v9l-8 4-8-4z"/><path d="M4 8l8 4 8-4M12 12v9"/>'),
    "venda": ('0 0 24 24', '<path d="M5 8h14l-1 12H6z"/><path d="M9 8V7a3 3 0 0 1 6 0v1"/>'),
    "baixa": ('0 0 24 24', '<path d="M12 3v9M8.5 8.5 12 12l3.5-3.5"/><path d="M4 14v6h16v-6"/>'),
    "site": ('0 0 24 24', '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c-3.2 3.2-3.2 13.8 0 17M12 3.5c3.2 3.2 3.2 13.8 0 17"/>'),
    "entrada": ('0 0 24 24', '<path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.5v2.5h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>'),
    "paradas": ('0 0 24 24', '<path d="M7 3.5h10M7 20.5h10"/><path d="M8 3.5c0 4 3 5.5 4 8.5-1 3-4 4.5-4 8.5M16 3.5c0 4-3 5.5-4 8.5 1 3 4 4.5 4 8.5"/>'),
    "reposicao": ('0 0 24 24', '<path d="M9 6.5h11M9 12h11M9 17.5h11"/><path d="M3.5 6.5l1.2 1.2 2.3-2.4M3.5 12l1.2 1.2L7 10.8M3.5 17.5l1.2 1.2 2.3-2.4"/>'),
    "resumo": ('0 0 24 24', '<path d="M4 20h16"/><rect x="5.5" y="12" width="3" height="8"/><rect x="10.5" y="6" width="3" height="14"/><rect x="15.5" y="9" width="3" height="11"/>'),
    "fechamento": ('0 0 24 24', '<rect x="5" y="10.5" width="14" height="10"/><path d="M8.5 10.5V7.5a3.5 3.5 0 0 1 7 0v3"/><path d="M12 14.5v2.5"/>'),
}


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    pagina = SAIDA / "_icones.html"
    # os 10 ícones (viewBox 24) usam todos stroke-width 1.5; a marca (viewBox 30x34) leva 2,1 para o traço sair do mesmo peso
    corpo = "".join(
        f'<div class="i" id="{n}"><svg viewBox="{vb}" width="240" height="240" fill="none" stroke="#f3f0ea" '
        f'stroke-width="{2.1 if n == "marca" else 1.5}" stroke-linecap="square" stroke-linejoin="miter">{d}</svg></div>'
        for n, (vb, d) in ICONES.items())
    pagina.write_text(
        "<!doctype html><meta charset='utf-8'><style>"
        f"@font-face{{font-family:Jost;src:url('{FONTE.as_uri()}');font-weight:100 900}}"
        "html,body{margin:0;background:transparent}.i{width:240px;height:240px;margin:0 0 10px 0}"
        "</style>" + corpo, encoding="utf-8")
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome", headless=True)
        pg = nav.new_page(viewport={"width": 260, "height": 400})
        pg.goto(pagina.as_uri())
        pg.evaluate("document.fonts.load('300 11px Jost')")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        for n in ICONES:
            pg.locator(f"#{n}").screenshot(path=str(SAIDA / f"{n}.png"), omit_background=True)
        nav.close()
    print("ícones:", ", ".join(ICONES))


if __name__ == "__main__":
    main()
