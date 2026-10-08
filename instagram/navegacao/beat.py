"""Gera um beat instrumental (trap, 140 BPM, fá menor) por síntese, sem samples. Saída: beat.wav
Uso:  python beat.py [segundos]
"""
import sys
import wave
from pathlib import Path
import numpy as np

SR = 44100
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 26.6
BPM = 140
B = 60 / BPM                      # um tempo
N = int(SR * (DUR + 1))
mix = np.zeros(N)
rng = np.random.default_rng(7)


def por(buf, som, t, g=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    f = min(len(som), len(buf) - i)
    buf[i:i + f] += som[:f] * g


def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-t / d)


def kick():
    n = int(SR * 0.32)
    t = np.arange(n) / SR
    f = 46 + 120 * np.exp(-t / 0.022)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.11)


def sub808(freq, dur, desliza=None):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = np.full(n, freq)
    if desliza:
        f = freq + (desliza - freq) * np.clip((t - dur * 0.45) / (dur * 0.3), 0, 1)
    f = f + 40 * np.exp(-t / 0.018)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    s = np.tanh(2.6 * s) * 0.8 + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR)   # harmônicos para caixa pequena
    e = np.minimum(t / 0.003, 1) * np.exp(-t / (dur * 0.75)) * np.clip((dur - t) / 0.03, 0, 1)
    return s * e


def clap():
    n = int(SR * 0.28)
    r = rng.standard_normal(n)
    r = np.diff(r, prepend=0)                                  # tira grave
    t = np.arange(n) / SR
    e = sum(np.exp(-np.maximum(t - d, 0) / 0.012) * (t >= d) for d in (0, 0.011, 0.023)) + 1.2 * np.exp(-t / 0.09)
    return r * e * 0.16 + 0.3 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)


def hat(d=0.03, aberto=False):
    n = int(SR * (0.3 if aberto else 0.07))
    r = np.diff(np.diff(rng.standard_normal(n), prepend=0), prepend=0)
    return r * env(n, 0.0005, 0.12 if aberto else d) * 0.11


def sino(freq, dur=1.3):
    n = int(SR * dur)
    t = np.arange(n) / SR
    mod = np.sin(2 * np.pi * freq * 3.01 * t) * 2.2 * np.exp(-t / 0.25)
    s = np.sin(2 * np.pi * freq * t + mod) + 0.4 * np.sin(2 * np.pi * freq * 2 * t)
    return s * env(n, 0.004, 0.42)


F = {'F1': 43.65, 'Ab1': 51.91, 'C2': 65.41, 'Db2': 69.30, 'Eb2': 77.78, 'F2': 87.31,
     'F4': 349.23, 'Ab4': 415.30, 'C5': 523.25, 'Db5': 554.37, 'Eb5': 622.25, 'G4': 392.0, 'Bb4': 466.16, 'C4': 261.63}
compasso = 4 * B
ncomp = int(DUR / compasso) + 1
mel = np.zeros(N)
# melodia de dois compassos, em colcheias (None = pausa)
frase = [['F4', None, 'Ab4', 'C5', None, 'Ab4', 'Db5', 'C5'], ['Ab4', None, 'F4', 'G4', None, 'Eb5', 'C5', None]]
for c in range(ncomp):
    t0 = c * compasso
    for k, nota in enumerate(frase[c % 2]):
        if nota:
            por(mel, sino(F[nota]), t0 + k * B / 2, 0.16)
    if c < 2:                       # introdução: só melodia e chimbal leve
        for k in range(8):
            por(mix, hat(0.02), t0 + k * B / 2, 0.5)
        continue
    # bateria
    for b in (0, 2.5):
        por(mix, kick(), t0 + b * B, 0.9)
    por(mix, clap(), t0 + 2 * B, 0.9)
    for k in range(8):
        por(mix, hat(), t0 + k * B / 2, 0.9 if k % 2 == 0 else 0.55)
    if c % 2 == 1:                  # rufo de chimbal no fim do compasso
        for k in range(6):
            por(mix, hat(0.018), t0 + 3 * B + k * B / 6, 0.4 + 0.1 * k)
    else:
        por(mix, hat(aberto=True), t0 + 3.5 * B, 0.7)
    # 808
    linha = [('F1', 0, 1.4, None), ('F1', 1.5, 0.9, None), ('Ab1', 2.5, 1.4, 'F1')] if c % 2 == 0 else \
            [('Db2', 0, 1.4, None), ('C2', 1.5, 0.9, None), ('Eb2', 2.5, 1.4, 'C2')]
    for nota, b, d, gl in linha:
        por(mix, sub808(F[nota] * 2, d * B, F[gl] * 2 if gl else None), t0 + b * B, 0.62)

# eco na melodia
atraso = int(SR * B * 0.75)
eco = mel.copy()
for r in range(1, 4):
    eco[atraso * r:] += mel[:-atraso * r] * (0.38 ** r)
mix += eco
mix = mix[:int(SR * DUR)]
fade = int(SR * 1.2)
mix[-fade:] *= np.linspace(1, 0, fade) ** 2
mix = np.tanh(mix * 1.5)
mix /= np.max(np.abs(mix)) / 0.92
pcm = (mix * 32767).astype('<i2')
est = np.column_stack([pcm, pcm]).tobytes()
saida = Path(__file__).resolve().parent / 'beat.wav'
with wave.open(str(saida), 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(est)
print('ok', saida.name, round(len(mix) / SR, 2), 's')
