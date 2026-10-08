"""Biblioteca de gravação quadro a quadro (tempo virtual do Chromium).

O relógio do navegador é pausado e avança 1/30 s por quadro; cada quadro é capturado em JPEG q=93.
Resultado: 30 fps exatos, sem quadro repetido nem salto, independente da carga da máquina.
Nada aqui altera a pasta site/: tudo é injetado pelo Playwright.
"""
import math, pathlib, shutil, subprocess, base64

BASE = "http://localhost:4174"
FPS = 30
DT = 1000.0 / FPS
K = 1.0  # fator de ritmo global (1.0 = durações como escritas no roteiro)

CURSOR_JS = """
(() => {
  const mk = () => {
    if (document.getElementById('__cur')) return;
    const c = document.createElement('div'); c.id = '__cur';
    c.style.cssText = 'position:fixed;left:-50px;top:-50px;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;'
      + 'background:rgba(243,240,234,.30);border:2px solid rgba(243,240,234,.95);box-shadow:0 0 0 1px rgba(0,0,0,.45),0 2px 10px rgba(0,0,0,.35);'
      + 'z-index:2147483647;pointer-events:none;';
    document.documentElement.appendChild(c);
    addEventListener('mousemove', e => { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px'; }, true);
    addEventListener('mousedown', () => { c.style.width = c.style.height = '18px'; c.style.margin = '-9px 0 0 -9px'; c.style.background = 'rgba(243,240,234,.8)'; }, true);
    addEventListener('mouseup', () => { c.style.width = c.style.height = '26px'; c.style.margin = '-13px 0 0 -13px'; c.style.background = 'rgba(243,240,234,.30)'; }, true);
  };
  if (document.readyState !== 'loading') mk(); else addEventListener('DOMContentLoaded', mk);
})();
"""

# ponto do dedo: aparece onde toca e some (posição e opacidade dirigidas por quadro)
TOUCH_JS = """
(() => {
  const mk = () => {
    if (document.getElementById('__dot')) return;
    const d = document.createElement('div'); d.id = '__dot';
    d.style.cssText = 'position:fixed;left:0;top:0;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;'
      + 'background:rgba(243,240,234,.42);border:2px solid rgba(243,240,234,.92);z-index:2147483647;pointer-events:none;opacity:0;';
    document.documentElement.appendChild(d);
    window.__dot = (x, y, o, s) => { d.style.left = x + 'px'; d.style.top = y + 'px'; d.style.opacity = o; d.style.transform = 'scale(' + s + ')'; };
  };
  if (document.readyState !== 'loading') mk(); else addEventListener('DOMContentLoaded', mk);
})();
"""

ease_io = lambda t: 4 * t * t * t if t < .5 else 1 - pow(-2 * t + 2, 3) / 2   # acelera e freia
smooth = lambda t: t * t * (3 - 2 * t)


class Rec:
    def __init__(self, page, pasta, w, h, quality=93, escala=1):
        self.p = page
        self.dir = pathlib.Path(pasta); shutil.rmtree(self.dir, ignore_errors=True); self.dir.mkdir(parents=True)
        self.n = 0; self.q = quality; self.w, self.h, self.esc = w, h, escala
        self.x, self.y = w / 2, h / 2
        self.cdp = page.context.new_cdp_session(page)
        self.done = []
        self.cdp.on("Emulation.virtualTimeBudgetExpired", lambda e: self.done.append(1))
        self.rec = False

    # ---------- relógio ----------
    # O tempo virtual do Chromium trava a página ao rolar, então o relógio é por quadro:
    # todas as animações e transições CSS (Web Animations) ficam pausadas e recebem
    # currentTime = (quadro atual - quadro em que nasceram) x 33,3 ms. Rolagem e mouse são aplicados por quadro.
    ADV = """(f) => { for (const a of document.getAnimations()) {
        if (a.__f === undefined) { a.__f = f; a.pause(); }
        a.currentTime = (f - a.__f) * %f; } return 1; }""" % DT

    def pause(self):
        self.frame = 0

    def tick(self, gravar=True):
        """avança 1 quadro (33,3 ms de animação) e captura"""
        self.frame = getattr(self, "frame", 0) + 1
        self.p.evaluate(self.ADV, self.frame)
        self.p.wait_for_timeout(8)         # deixa observers (IntersectionObserver) e decodificação de imagem andarem
        self.p.evaluate(self.ADV, self.frame)
        if gravar and self.rec:
            if self.esc != 1:
                (self.dir / f"{self.n:06d}.jpg").write_bytes(self.p.screenshot(type="jpeg", quality=self.q, scale="device")); self.n += 1
                return
            r = self.cdp.send("Page.captureScreenshot", {"format": "jpeg", "quality": self.q})
            (self.dir / f"{self.n:06d}.jpg").write_bytes(base64.b64decode(r["data"])); self.n += 1

    def frames(self, s):
        return max(1, round(s * K * FPS))

    def wait(self, s):
        for _ in range(self.frames(s)): self.tick()

    # ---------- rolagem ----------
    def scroll_to(self, y, s, sel=None):
        n = self.frames(s)
        get = "document.querySelector(%r).scrollTop" % sel if sel else "window.scrollY"
        y0 = self.p.evaluate(get)
        for i in range(1, n + 1):
            v = y0 + (y - y0) * ease_io(i / n)
            self.p.evaluate(("document.querySelector(%r).scrollTop=%f" % (sel, v)) if sel else f"window.scrollTo({{top:{v},behavior:'instant'}})")
            self.tick()

    def top_of(self, sel, off=0):
        return self.p.evaluate("([s,o]) => document.querySelector(s).getBoundingClientRect().top + scrollY + o", [sel, off])

    def scroll_sel(self, sel, off=0, s=2.2):
        self.scroll_to(self.top_of(sel, off), s)

    def scroll_x(self, sel, to, s=0.9):
        n = self.frames(s)
        x0 = self.p.evaluate("document.querySelector(%r).scrollLeft" % sel)
        self.p.evaluate("document.querySelector(%r).style.scrollSnapType='none'" % sel)
        for i in range(1, n + 1):
            self.p.evaluate("document.querySelector(%r).scrollLeft=%f" % (sel, x0 + (to - x0) * ease_io(i / n)))
            self.tick()
        self.p.evaluate("document.querySelector(%r).style.scrollSnapType=''" % sel)

    # ---------- mouse (desktop) ----------
    def move(self, x, y, s=0.9):
        x0, y0 = self.x, self.y
        dx, dy = x - x0, y - y0
        dist = math.hypot(dx, dy) or 1
        nx, ny = -dy / dist, dx / dist
        bend = min(110, dist * .16) * (1 if (int(x0 + y) % 2) else -1)
        cx, cy = x0 + dx / 2 + nx * bend, y0 + dy / 2 + ny * bend
        n = self.frames(s)
        for i in range(1, n + 1):
            e = smooth(i / n)
            px = (1 - e) ** 2 * x0 + 2 * (1 - e) * e * cx + e * e * x
            py = (1 - e) ** 2 * y0 + 2 * (1 - e) * e * cy + e * e * y
            self.p.mouse.move(px, py); self.tick()
        self.x, self.y = x, y

    def center(self, sel, nth=0):
        b = self.p.locator(sel).nth(nth).bounding_box()
        return b["x"] + b["width"] / 2, b["y"] + b["height"] / 2

    def go(self, sel, s=0.9, nth=0):
        x, y = self.center(sel, nth); self.move(x, y, s)

    def click(self, sel, s=0.9, nth=0, pausa=0.25):
        self.go(sel, s, nth); self.wait(pausa)
        self.p.mouse.down(); self.tick(); self.tick(); self.p.mouse.up(); self.tick()

    # ---------- toque (celular) ----------
    def tap(self, sel, nth=0, pausa=0.3):
        b = self.p.locator(sel).nth(nth).bounding_box()
        self.tap_xy(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2, pausa)

    def tap_xy(self, x, y, pausa=0.3):
        n = self.frames(pausa)
        for i in range(n):   # o ponto aparece e cresce antes do toque
            t = (i + 1) / n
            self.p.evaluate("([x,y,o,s]) => window.__dot(x,y,o,s)", [x, y, min(1, t * 2), 1.25 - .25 * t]); self.tick()
        self.p.touchscreen.tap(x, y)
        n = self.frames(0.3)
        for i in range(n):   # some devagar, depois do toque
            self.p.evaluate("([x,y,o,s]) => window.__dot(x,y,o,s)", [x, y, 1 - (i + 1) / n, 1 + .2 * (i + 1) / n]); self.tick()

    def finger(self, x, y0, y1, s, fn):
        """dedo arrastando de y0 a y1 durante s segundos, enquanto fn(t) aplica a rolagem (t de 0 a 1)"""
        n = self.frames(s)
        for i in range(1, n + 1):
            t = ease_io(i / n)
            fn(t)
            o = min(1, i / 4) if i < n - 4 else max(0, (n - i) / 4)
            self.p.evaluate("([x,y,o]) => window.__dot(x,y,o,1)", [x, y0 + (y1 - y0) * t, o]); self.tick()
        self.p.evaluate("window.__dot(0,0,0,1)")

    # ---------- saída ----------
    def render(self, saida, crf=20, maxrate="2800k", scale=None):
        vf = "format=yuv420p"
        if scale: vf = f"scale={scale}:flags=lanczos," + vf
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(self.dir / "%06d.jpg"),
                        "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-maxrate", maxrate,
                        "-bufsize", "8000k", "-r", str(FPS), "-an", "-movflags", "+faststart", str(saida)], check=True)
        return self.n / FPS
