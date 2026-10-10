"""Duração e tempo de cada palavra das falas.

Com o áudio (video/voz/NN.mp3): duração via ffprobe e palavras via faster_whisper, casadas com as palavras
do TEXTO de falas.falada(n). Sem o áudio: tempos estimados por proporção de caracteres (e dur = palavras/2,6 + 0,4).
Saída: _trabalho/tempos.json -> {"01": {"dur", "audio", "palavras": [{"w", "ini", "fim"}]}}
"""
import difflib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from falas import FALAS, falada  # noqa: E402

VOZ = AQUI.parent / "voz"
SAIDA = AQUI / "_trabalho" / "tempos.json"


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s)


def duracao(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(arq)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def por_caracteres(palavras, ini, fim):
    """Distribui as palavras entre ini e fim na proporção de caracteres."""
    pesos = [max(len(norm(w)), 1) + 1 for w in palavras]
    tot = sum(pesos)
    out, acc = [], 0
    for w, p in zip(palavras, pesos):
        a = ini + (fim - ini) * acc / tot
        acc += p
        b = ini + (fim - ini) * (acc - 1) / tot   # o +1 do peso é a pausa entre palavras
        out.append({"w": w, "ini": round(a, 3), "fim": round(b, 3)})
    return out


def casar(palavras, trans, dur):
    """Palavras do texto com tempo da transcrição; as sem par recebem tempo interpolado."""
    a = [norm(w) for w in palavras]
    b = [norm(t["w"]) for t in trans]
    ini = [None] * len(palavras)
    fim = [None] * len(palavras)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                ini[i1 + k], fim[i1 + k] = trans[j1 + k]["ini"], trans[j1 + k]["fim"]
    # interpolação dos buracos entre âncoras
    n = len(palavras)
    i = 0
    while i < n:
        if ini[i] is not None:
            i += 1
            continue
        j = i
        while j < n and ini[j] is None:
            j += 1
        t0 = fim[i - 1] if i > 0 else max(0.0, trans[0]["ini"] if trans else 0.0)
        t1 = ini[j] if j < n else min(dur, trans[-1]["fim"] if trans else dur)
        if t1 < t0:
            t1 = t0 + 0.05 * (j - i)
        for k, d in enumerate(por_caracteres(palavras[i:j], t0, t1)):
            ini[i + k], fim[i + k] = d["ini"], d["fim"]
        i = j
    return [{"w": w, "ini": round(ini[k], 3), "fim": round(max(fim[k], ini[k] + 0.04), 3)} for k, w in enumerate(palavras)]


_modelo = None


def decodificar(arq):
    """Áudio mono 16 kHz (float32) decodificado com o ffmpeg (o av instalado não casa com o faster_whisper)."""
    import numpy as np
    bruto = subprocess.run(["ffmpeg", "-v", "error", "-i", str(arq), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                           capture_output=True, check=True).stdout
    return np.frombuffer(bruto, dtype=np.float32)


def limites_da_voz(audio):
    """(início, fim) da voz em segundos, por energia: os mp3 têm silêncio antes e depois da fala."""
    import numpy as np
    n = len(audio) // 160
    rms = np.sqrt((audio[:n * 160].reshape(n, 160) ** 2).mean(axis=1))
    lim = max(0.008, 0.06 * np.percentile(rms, 99))
    forte = rms > lim
    ini = next((i for i in range(n - 6) if forte[i:i + 6].all()), 0)
    fim = next((i for i in range(n - 1, 5, -1) if forte[i - 5:i + 1].all()), n - 1)
    return ini / 100, (fim + 1) / 100


def trechos_de_voz(audio, lim_db=-38, pausa=0.08, minimo=0.06):
    """Trechos contínuos com voz [(ini, fim)], pausas menores que `pausa` unidas."""
    import numpy as np
    n = len(audio) // 160
    rms = np.sqrt((audio[:n * 160].reshape(n, 160) ** 2).mean(axis=1))
    forte = rms > 10 ** (lim_db / 20)
    runs, i = [], 0
    while i < n:
        if forte[i]:
            j = i
            while j < n and forte[j]:
                j += 1
            if runs and i / 100 - runs[-1][1] < pausa:
                runs[-1] = (runs[-1][0], j / 100)
            else:
                runs.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    return [r for r in runs if r[1] - r[0] >= minimo]


def prender_nos_trechos(pal, runs, corte):
    """O Whisper adianta o início das palavras que vêm depois de uma pausa: prende ao começo do trecho com voz."""
    for p in pal:
        a = p["ini"] + corte
        if any(r[0] - 0.01 <= a <= r[1] for r in runs):
            continue
        prox = next((r[0] for r in runs if r[0] > a), None)
        if prox is not None and prox - a <= 0.4:
            p["ini"] = round(prox - corte, 3)
            p["fim"] = round(max(p["fim"], p["ini"] + 0.08), 3)
    return pal


def transcrever(audio):
    global _modelo
    if _modelo is None:
        from faster_whisper import WhisperModel
        _modelo = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = _modelo.transcribe(audio, language="pt", word_timestamps=True, vad_filter=False)
    return [{"w": w.word.strip(), "ini": w.start, "fim": w.end} for s in segs for w in (s.words or []) if w.word.strip()]


def main():
    res = {}
    for n in FALAS:
        palavras = falada(n).split()
        arq = VOZ / f"{n}.mp3"
        if arq.exists():
            dur_arq = duracao(arq)
            audio = decodificar(arq)
            voz_ini, voz_fim = limites_da_voz(audio)
            corte = max(0.0, voz_ini - 0.05)          # a montagem corta o silêncio inicial (atrim)
            dur = voz_fim + 0.08 - corte
            trans = transcrever(audio)
            for x in trans:
                x["ini"] -= corte
                x["fim"] -= corte
            pal = casar(palavras, trans, dur) if trans else por_caracteres(palavras, 0.05, dur - 0.1)
            pal = prender_nos_trechos(pal, trechos_de_voz(audio), corte)
            pal[0]["ini"] = 0.05                       # a voz começa onde a energia começa; o Whisper erra a 1ª palavra
            pal[-1]["fim"] = round(dur - 0.08, 3)
            res[n] = {"dur": round(dur, 3), "corte": round(corte, 3), "audio": True, "palavras": pal}
            print(f"{n}: arquivo {dur_arq:5.2f} s, voz {voz_ini:4.2f}-{voz_fim:5.2f} s, dur útil {dur:5.2f} s, {len(trans)}/{len(palavras)} palavras")
        else:
            dur = len(palavras) / 2.6 + 0.4
            res[n] = {"dur": round(dur, 3), "corte": 0.0, "audio": False, "palavras": por_caracteres(palavras, 0.05, dur - 0.1)}
            print(f"{n}: sem áudio, duração estimada {dur:5.2f} s")
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
