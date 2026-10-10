"""Orquestra tudo: ícones, alinhamento das falas, gravação do app e montagem do vídeo.

Uso: py -3.12 fazer.py [--so-montar]   (--so-montar reaproveita _trabalho/gravacao/ e só refaz a montagem)
"""
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def passo(nome, script, *args):
    print(f"\n== {nome}", flush=True)
    subprocess.run([sys.executable, str(AQUI / script), *args], check=True, cwd=AQUI)


if __name__ == "__main__":
    so_montar = "--so-montar" in sys.argv
    extra = []
    if "--trilha" in sys.argv:          # versão com música por baixo, sem narração (sai em ...-trilha.mp4)
        trilha = Path(sys.argv[sys.argv.index("--trilha") + 1]).resolve()
        if not trilha.exists():
            sys.exit(f"trilha não encontrada: {trilha}")
        extra = ["--trilha", str(trilha)]
    passo("ícones", "icones.py")
    passo("alinhar falas", "alinhar.py")
    if not so_montar:
        passo("gravar o aplicativo", "gravar.py")
    passo("montar o vídeo", "montar.py", *extra)
