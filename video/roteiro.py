"""Roteiro dos vídeos de demonstração da BK Clothing (site2 no computador e no celular, Instagram de verão).

    python preparar.py           (uma vez: logo, capas e fonte)
    python roteiro.py            (grava tudo e monta as apresentações)
    python roteiro.py computador (só um trecho: computador, celular ou instagram)

O botão que abre o WhatsApp nunca é clicado: o ponteiro chega até ele e para.
"""
import subprocess
import sys
from pathlib import Path

SKILL = Path(r"C:\Users\guilherme\.claude\skills\video-demonstracao") / "scripts"
sys.path.insert(0, str(SKILL))
from filme import gravar, gravar_instagram, ig_roteiro_padrao  # noqa: E402

AQUI = Path(__file__).parent
PROJETO = AQUI.parent
SITE = (PROJETO / "site2/index.html").resolve().as_uri()
VIDEOS = PROJETO / "videos"
COR = "#dce8ef"
CABECALHO = ".tb, .hd"
# as seções entram com transição quando aparecem; no vídeo quem faz o movimento é o roteiro
CSS = ".rv{opacity:1!important;transform:none!important}"


def preparar(pg):
    # cada quadro leva mais tempo que 1/30 s para ser tirado; sem isto os vídeos da página parecem acelerados
    pg.evaluate("document.querySelectorAll('video').forEach(v => { v.playbackRate = 0.3 })")


def roteiro_computador(f):
    f.pausa(2.4)
    f.mover(".hero .bl.a", 0.9)                       # a peça acompanha o ponteiro
    f.pausa(0.6)
    f.rolar("#categorias", 1.6)
    f.pausa(0.8)
    f.mover("#cats a:nth-child(5)", 0.8)
    f.pausa(0.7)
    f.rolar("#selecao", 1.5)
    f.pausa(0.9)
    f.clicar('#sel .card[data-p="1914786"]')          # abre a jaqueta bomber
    f.pausa(1.4)
    f.clicar('.sizes [data-size="M"]')
    f.pausa(0.5)
    f.clicar("[data-add]")                            # adiciona à sacola
    f.pausa(1.3)
    f.mover("#bagFoot a", 0.9)                        # chega no botão do WhatsApp e não clica
    f.pausa(1.4)
    f.clicar("#bag [data-close]")
    f.pausa(0.6)
    f.rolar("#vitrines-1 .vit", 1.6)
    f.pausa(0.9)
    f.clicar('#vitrines-1 .vit .setas button[data-s="1"]')
    f.pausa(1.0)
    f.rolar("#corpo", 1.8)
    f.pausa(1.0)
    f.clicar("[data-tema]")                           # tema escuro
    f.pausa(1.5)
    f.clicar("[data-tema]")
    f.pausa(0.6)
    f.rolar("#loja", 1.9)
    f.pausa(1.2)
    f.rolar(f.fim(), 1.7)
    f.pausa(1.8)


def roteiro_celular(f):
    f.pausa(2.2)
    f.clicar("header .burger", 0.7)                   # o menu recolhido
    f.pausa(1.0)
    f.clicar('#mnav a[href="index.html#selecao"]', 0.6)
    f.pausa(0.5)
    f.rolar("#selecao", 0.8)
    f.pausa(0.9)
    f.clicar('#sel .card[data-p="1688777"]')          # abre a camiseta
    f.pausa(1.2)
    f.rolar(430, 1.0, dentro="#pm")              # desce dentro do painel do produto até os tamanhos
    f.pausa(0.5)
    f.clicar('.sizes [data-size="G"]')
    f.pausa(0.4)
    f.clicar("[data-add]")
    f.pausa(1.3)
    f.mover("#bagFoot a", 0.8)
    f.pausa(1.2)
    f.clicar("#bag [data-close]")
    f.pausa(0.5)
    f.rolar("#vitrines-1 .vit .lado", 1.5)
    f.pausa(0.6)
    f.deslizar("#vitrines-1 .trilho", 300)            # o carrossel com o dedo
    f.pausa(0.8)
    f.rolar("#corpo", 1.7)
    f.pausa(0.9)
    f.rolar("#loja", 1.8)
    f.pausa(1.1)
    f.rolar(f.fim(), 1.7)
    f.pausa(1.6)


TRECHOS = {
    "computador": lambda: gravar(SITE, roteiro_computador, VIDEOS / "site-computador.mp4", cabecalho=CABECALHO, cor_fundo=COR, css_extra=CSS, preparar=preparar),
    "celular": lambda: gravar(SITE, roteiro_celular, VIDEOS / "site-celular.mp4", celular=True, cabecalho=CABECALHO, cor_fundo=COR, css_extra=CSS, preparar=preparar),
    "instagram": lambda: gravar_instagram(PROJETO / "instagram/simulacao.html", VIDEOS / "instagram-celular.mp4", roteiro=ig_roteiro_padrao, cor_fundo=COR),
}

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(TRECHOS)
    for nome in pedidos:
        TRECHOS[nome]()
    if not sys.argv[1:]:
        subprocess.run([sys.executable, str(SKILL / "apresentacao.py"), str(AQUI / "apresentacao.json")], check=True)
