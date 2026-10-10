"""Linha do tempo do vídeo, em segundos. Lê _trabalho/tempos.json (gerado por alinhar.py).

Cena n começa em S(n); a voz entra em A(n) = S(n) + 0,35 (na fala 01, S=0 e A=0,6); a cena termina em
A(n) + dur + 0,55, que é S(n+1). A fala 15 termina em A + dur + 1,2.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TEMPOS = AQUI / "_trabalho" / "tempos.json"

NUMS = [f"{i:02d}" for i in range(1, 16)]
ENTRADA = 0.35
FOLGA = 0.55
FOLGA_FINAL = 1.2

# bloco -> (número no cabeçalho, título, arquivo do ícone, subtítulo). Bloco 0 = abertura, 11 = cartela final.
BLOCOS = {
    0: (None, "BK GESTÃO", "marca", None),
    1: (1, "INÍCIO DO DIA", "inicio", None),
    2: (2, "ESTOQUE POR TAMANHO", "estoque", None),
    3: (3, "VENDA", "venda", None),
    4: (4, "BAIXA AUTOMÁTICA", "baixa", None),
    5: (5, "PEDIDO DO SITE", "site", None),
    6: (6, "ENTRADA DE PEÇAS", "entrada", None),
    7: (7, "PEÇAS PARADAS", "paradas", None),
    8: (8, "REPOSIÇÃO", "reposicao", None),
    9: (9, "RESUMO", "resumo", None),
    10: (10, "FECHAMENTO", "fechamento", None),
    11: (None, "BK GESTÃO", "marca", None),
}
BLOCO_DA_FALA = {"01": 0, "02": 1, "03": 2, "04": 2, "05": 2, "06": 3, "07": 4, "08": 4, "09": 5, "10": 6,
                 "11": 7, "12": 8, "13": 9, "14": 10, "15": 11}
N_BLOCOS = 10   # blocos numerados (NN / 10)


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", "", s).strip()


def _carregar():
    if not TEMPOS.exists():
        sys.exit("falta _trabalho/tempos.json: rode alinhar.py antes")
    return json.loads(TEMPOS.read_text(encoding="utf-8"))


TP = _carregar()


def _k(n):
    return n if isinstance(n, str) else f"{n:02d}"


def dur(n):
    return TP[_k(n)]["dur"]


def palavras(n):
    return TP[_k(n)]["palavras"]


def tem_audio(n):
    return TP[_k(n)]["audio"]


def A(n):
    """Instante em que a voz da fala n entra."""
    n = _k(n)
    if n == "01":
        return 0.6
    return S(n) + ENTRADA


def S(n):
    """Início da cena n."""
    n = _k(n)
    if n == "01":
        return 0.0
    ant = f"{int(n) - 1:02d}"
    return fim(ant)


def fim(n):
    """Fim da cena n (= S(n+1))."""
    n = _k(n)
    return A(n) + dur(n) + (FOLGA_FINAL if n == "15" else FOLGA)


TOTAL = fim("15")


def bloco_da_fala(n):
    return BLOCO_DA_FALA[_k(n)]


def _achar(n, trecho, ocorrencia=0):
    alvo = norm(trecho).split()
    pal = palavras(n)
    nomes = [norm(p["w"]) for p in pal]
    achados = []
    for i in range(len(pal) - len(alvo) + 1):
        if nomes[i:i + len(alvo)] == alvo or (len(alvo) == 1 and nomes[i].startswith(alvo[0])):
            achados.append(i)
        elif len(alvo) > 1 and all(nomes[i + k] == alvo[k] for k in range(len(alvo) - 1)) and nomes[i + len(alvo) - 1].startswith(alvo[-1]):
            achados.append(i)
    if len(achados) <= ocorrencia:
        raise KeyError(f"trecho '{trecho}' não achado na fala {n} (ocorrência {ocorrencia})")
    return achados[ocorrencia], len(alvo)


def t(n, trecho, ocorrencia=0):
    """Tempo absoluto de início da primeira palavra do trecho na fala n."""
    i, _ = _achar(n, trecho, ocorrencia)
    return A(n) + palavras(n)[i]["ini"]


def tf(n, trecho, ocorrencia=0):
    """Tempo absoluto do fim da última palavra do trecho na fala n."""
    i, k = _achar(n, trecho, ocorrencia)
    return A(n) + palavras(n)[i + k - 1]["fim"]


def assinatura():
    """Resumo da linha do tempo, gravado junto da gravação para detectar áudio trocado depois."""
    return {n: [round(S(n), 3), round(A(n), 3), round(dur(n), 3)] for n in NUMS}


if __name__ == "__main__":
    for n in NUMS:
        print(f"{n} S={S(n):6.2f} A={A(n):6.2f} dur={dur(n):5.2f} fim={fim(n):6.2f} bloco={bloco_da_fala(n)}")
    print("total", round(TOTAL, 2))
