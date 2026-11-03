"""Reel "¿Quién dijo que hay límites?" · Admisiones 2027 · Sin Límites.

Uso:  python3 reel.py            -> render completo
      python3 reel.py tira        -> tira de cuadros de control
Entradas: tomas de medios/banco/, voz de medios/voces/, flyer en medios/banco/.
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BANCO = os.path.join(ROOT, "medios", "banco")
VOZ = os.path.join(ROOT, "medios", "voces", "2026-11-admisiones-sol-v4-toma1.mp3")
SINVOZ = os.environ.get("SINVOZ") == "1"
OUT = os.path.join(HERE, "Reel-Admisiones-2027-Sin-Limites-v2" + ("-sin-voz" if SINVOZ else "") + ".mp4")

W, H, FPS = 1080, 1920, 24
DUR = 28.0
V = 0.40  # la voz entra a los 0,40 s

NAVY = (31, 42, 90)
PINK = (236, 112, 160)
PASTELES = [(246, 179, 203), (201, 182, 236), (169, 216, 242), (168, 226, 207), (247, 222, 138), (246, 179, 203)]
WA = (37, 211, 102)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
FI = "/usr/share/fonts/truetype/google-fonts/Poppins-MediumItalic.ttf"

TEL1, TEL2 = "11 3142-9090", "11 6025-9276"
DIRECCION = "Calle 143 N° 1624 · Berazategui"

def font(p, s):
    return ImageFont.truetype(p, int(s))

def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def back(x):  # entrada con rebote suave
    x = max(0.0, min(1.0, x)); c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------- tomas ----------
class Toma:
    def __init__(self, nombre, src0, r0):
        self.path = os.path.join(BANCO, nombre); self.src0 = src0; self.r0 = r0
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{src0}", "-i", self.path,
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.idx = -1; self.last = None
    def frame(self, t):
        want = int(round((t - self.r0) * FPS))
        while self.idx < want:
            b = self.p.stdout.read(W * H * 3)
            if len(b) < W * H * 3: break
            self.last = Image.frombytes("RGB", (W, H), b); self.idx += 1
        return self.last

# gancho: se usa de 0,9 s a 6,3 s de la toma (sin la mano del lápiz)
A = ("2026-11-recuadro-que-se-rompe.mp4", 0.9, 0.0, 5.4)
B = ("2026-11-avion-entre-nubes.mp4", 0.0, 5.0, 12.83)
C = ("2026-11-rompecabezas-corazon.mp4", 0.0, 12.4, 20.2)
FIN0 = 19.6

# ---------- cierre (fondo animado por código) ----------
flyer = Image.open(os.path.join(BANCO, "flyer-admisiones-2027.png")).convert("RGB")
s = max(W / flyer.width, H / flyer.height) * 1.15
bgf = flyer.resize((int(flyer.width * s), int(flyer.height * s)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(45))
bgf = Image.blend(bgf, Image.new("RGB", bgf.size, (252, 247, 242)), 0.5)
# logo vectorizado (medios/marca), ancho 860 px en pantalla
logo = Image.open(os.path.join(ROOT, "medios", "marca", "sin-limites-logo-acuarela.png")).convert("RGBA")
logo = logo.resize((820, int(logo.height * 820 / logo.width)), Image.LANCZOS)
rng = np.random.default_rng(7)
CORAZONES = [(rng.uniform(60, W - 60), rng.uniform(0, H), rng.uniform(16, 34), rng.uniform(40, 90), PASTELES[i % 6]) for i in range(26)]

def corazon(d, x, y, r, col, a):
    d.ellipse((x - r, y - r, x, y), fill=col + (a,)); d.ellipse((x, y - r, x + r, y), fill=col + (a,))
    d.polygon([(x - r, y - r / 2), (x + r, y - r / 2), (x, y + r)], fill=col + (a,))

def fondo_cierre(t):
    k = (t - FIN0) / (DUR - FIN0)
    z = 1.0 + 0.06 * k
    w, h = int(W * z), int(H * z)
    b = bgf.resize((w, h), Image.BILINEAR)
    ox = (b.width - w) // 2; oy = (b.height - h) // 2
    b = bgf.crop(((bgf.width - int(W / z)) // 2, (bgf.height - int(H / z)) // 2,
                  (bgf.width + int(W / z)) // 2, (bgf.height + int(H / z)) // 2)).resize((W, H), Image.BILINEAR)
    img = b.convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for (x, y0, r, v, col) in CORAZONES:
        y = (y0 - v * (t - FIN0) * 2.2) % H
        corazon(d, x + 10 * np.sin(t * 1.3 + x), y, r, col, 150)
    img.alpha_composite(lay)
    return img

# ---------- textos ----------
def texto_con_borde(img, txt, f, cx, cy, fill, a=1.0, scale=1.0, stroke=10):
    if a <= 0: return
    f = font(f.path, f.size * scale)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    w = d.textlength(txt, font=f)
    d.text((cx - w / 2, cy - f.size * 0.62), txt, font=f, fill=fill + (int(255 * a),),
           stroke_width=int(stroke * scale), stroke_fill=(255, 255, 255, int(245 * a)))
    sh = lay.filter(ImageFilter.GaussianBlur(14)); sh = Image.eval(sh, lambda v: v)
    img.alpha_composite(Image.merge("RGBA", (*[Image.new("L", (W, H), 60)] * 3, sh.getchannel("A").point(lambda v: v // 3))), (0, 10))
    img.alpha_composite(lay)

def pill(img, lineas, cy, size, a, sc=1.0, bg=(255, 255, 255), fg=NAVY):
    if a <= 0: return
    f = font(FB, size * sc); d0 = ImageDraw.Draw(img)
    ws = [d0.textlength(l, font=f) for l in lineas]; lh = int(size * sc * 1.2)
    bw = int(max(ws) + 80 * sc); bh = int(lh * len(lineas) + 44 * sc)
    x0 = (W - bw) // 2; y0 = int(cy - bh / 2)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    rad = bh // 2 if len(lineas) == 1 else 44
    d.rounded_rectangle((x0, y0 + 8, x0 + bw, y0 + bh + 8), rad, fill=(80, 50, 110, int(55 * a)))
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), rad, fill=bg + (int(245 * a),))
    for i, l in enumerate(lineas):
        d.text(((W - ws[i]) / 2, y0 + 20 * sc + i * lh - size * sc * 0.06), l, font=f, fill=fg + (int(255 * a),))
    img.alpha_composite(lay)

def ventana(t, a, b, fi=0.2, fo=0.2):
    if t < a or t > b: return 0.0, 0.0
    return max(0.0, min(1.0, (t - a) / fi, (b - t) / fo)), min(1.0, (t - a) / fi)

SUBS = [(1.84, 4.03, ["Cada niño tiene", "su propio camino…"]),
        (4.05, 6.80, ["y en Sin Límites", "lo recorremos juntos"]),
        (14.48, 18.48, ["Atendemos con CUD", "por obra social", "o en forma particular"])]
SERV = [(6.84, "Psicología"), (7.80, "Fonoaudiología"), (8.76, "Psicopedagogía"),
        (10.00, "Terapia Ocupacional"), (11.36, "Habilidades sociales"), (12.56, "Evaluación neurocognitiva")]

logo_ap = logo.resize((620, int(logo.height * 620 / logo.width)), Image.LANCZOS)

def apertura(img, t):
    # marca visible desde el primer cuadro: logo + "Admisiones 2027 · Berazategui"
    if t > 5.45: return
    fo = 1.0 - ease((t - 5.0) / 0.4)
    p = min(1.0, 0.55 + t / 0.35 * 0.45)
    lg = logo_ap.resize((int(logo_ap.width * (0.9 + 0.1 * back(p))), int(logo_ap.height * (0.9 + 0.1 * back(p)))), Image.LANCZOS)
    lg.putalpha(lg.getchannel("A").point(lambda v: int(v * fo)))
    img.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(345 - lg.height / 2)))
    p2 = min(1.0, max(0.0, (t - 0.2) / 0.3))
    pill(img, ["Admisiones 2027 · Berazategui"], 560, 44, ease(p2) * fo, 0.85 + 0.15 * back(p2), bg=(255, 255, 255))

def textos(img, t):
    tv = t - V
    apertura(img, t)
    # gancho
    a, p = ventana(tv, 0.05, 1.75, 0.25, 0.3)
    if a: texto_con_borde(img, "¿Quién dijo que", font(FB, 96), W / 2, 820, NAVY, a, 0.85 + 0.15 * back(p))
    if a and tv > 0.7:
        p2 = min(1.0, (tv - 0.7) / 0.3)
        texto_con_borde(img, "hay límites?", font(FB, 128), W / 2, 960, PINK, a * ease(p2), 0.8 + 0.2 * back(p2))
    # subtítulos
    for a0, a1, ls in SUBS:
        a, p = ventana(tv, a0 - 0.05, a1 + 0.1, 0.18, 0.18)
        pill(img, ls, 1330, 60, a, 0.9 + 0.1 * ease(p))
    # servicios apilados
    if 6.75 <= tv <= 14.5:
        fo = min(1.0, (14.5 - tv) / 0.3)
        for i, (t0, sname) in enumerate(SERV):
            if tv < t0 - 0.05: continue
            p = min(1.0, (tv - t0 + 0.05) / 0.28)
            pill(img, [sname], 520 + i * 138, 54, ease(p) * fo, 0.7 + 0.3 * back(p), bg=PASTELES[i])
    a, p = ventana(tv, 15.0, FIN0 - V + 0.3, 0.4, 0.3)
    if a: texto_con_borde(img, "Pequeños avances, grandes logros", font(FI, 52), W / 2, 380, NAVY, a, 1.0, 8)

def cierre(img, t):
    k = t - FIN0
    def ent(d0, dur=0.45): return ease((k - d0) / dur), back((k - d0) / dur)
    a, b = ent(0.2)
    if a:
        lg = logo.resize((int(logo.width * (0.85 + 0.15 * b)), int(logo.height * (0.85 + 0.15 * b))), Image.LANCZOS).convert("RGBA")
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(305 - lg.height / 2)))
    a, b = ent(0.2)   # voz: "Ya están abiertas las admisiones 2027"
    texto_con_borde(img, "Admisiones 2027", font(FB, 92), W / 2, 580, NAVY, a, 0.85 + 0.15 * b)
    a, b = ent(2.3)   # voz: "Estamos en Berazategui"
    texto_con_borde(img, "Estamos en Berazategui", font(FB, 70), W / 2, 715, PINK, a, 0.85 + 0.15 * b, 8)
    a, b = ent(2.5)
    pill(img, ["Calle 143 N° 1624"], 820, 46, a, 0.9 + 0.1 * b)
    a, b = ent(3.9)   # voz: "escribinos cuando quieras"
    pill(img, ["Escribinos por WhatsApp"], 965, 50, a, 0.85 + 0.15 * b, bg=WA, fg=(255, 255, 255))
    for i, tel in enumerate([TEL1, TEL2]):
        a, b = ent(4.1 + i * 0.2)
        texto_con_borde(img, tel, font(FB, 112), W / 2, 1105 + i * 145, NAVY, a, 0.85 + 0.15 * b, 9)
    a, b = ent(4.8)
    texto_con_borde(img, "Juntos potenciamos posibilidades", font(FI, 52), W / 2, 1420, PINK, a, 1.0, 7)

# ---------- composición ----------
def mezcla(i1, i2, k):
    return Image.blend(i1, i2, ease(k))

def render(times, sink):
    ta, tb, tc = Toma(A[0], A[1], A[2]), Toma(B[0], B[1], B[2]), Toma(C[0], C[1], C[2])
    for t in times:
        if t < B[2]:
            base = ta.frame(t)
        elif t < A[3]:
            base = mezcla(ta.frame(t), tb.frame(t), (t - B[2]) / (A[3] - B[2]))
        elif t < C[2]:
            base = tb.frame(t)
        elif t < B[3]:
            base = mezcla(tb.frame(t), tc.frame(t), (t - C[2]) / (B[3] - C[2]))
        elif t < FIN0:
            base = tc.frame(t)
        else:
            fc = fondo_cierre(t).convert("RGB")
            base = mezcla(tc.frame(min(t, C[3] - 0.05)), fc, (t - FIN0) / 0.5) if t < FIN0 + 0.5 else fc
        img = base.convert("RGBA")
        if t < FIN0 + 0.3: textos(img, t)
        if t >= FIN0: cierre(img, t)
        sink(img.convert("RGB"), t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "tira":
        marcas = [0.0, 0.6, 1.6, 3.5, 5.2]
        frames = []
        allt = [i / FPS for i in range(int(max(marcas) * FPS) + 1)]
        want = {int(round(m * FPS)) for m in marcas}
        def sink(im, t):
            if int(round(t * FPS)) in want: frames.append(im.resize((270, 480)))
        render(allt, sink)
        tira = Image.new("RGB", (270 * len(frames), 480), "white")
        for i, f in enumerate(frames): tira.paste(f, (i * 270, 0))
        tira.save(os.path.join(HERE, "tira.png")); sys.exit()

    n = int(DUR * FPS)
    tmp = os.path.join(HERE, "_video.mp4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", "unsharp=5:5:0.35", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-pix_fmt", "yuv420p", tmp],
                         stdin=subprocess.PIPE)
    render([i / FPS for i in range(n)], lambda im, t: p.stdin.write(im.tobytes()))
    p.stdin.close(); p.wait()
    # audio: voz adelante, ambiente de las tomas a -20 dB con fundidos
    fc = (f"[1:a]atrim=0.9:6.3,asetpts=PTS-STARTPTS,afade=t=out:st=5.0:d=0.4[a1];"
          f"[2:a]atrim=0:7.83,asetpts=PTS-STARTPTS,afade=t=in:d=0.4,afade=t=out:st=7.4:d=0.4,adelay={int(B[2]*1000)}|{int(B[2]*1000)}[a2];"
          f"[3:a]atrim=0:7.83,asetpts=PTS-STARTPTS,afade=t=in:d=0.4,afade=t=out:st=6.6:d=1.2,adelay={int(C[2]*1000)}|{int(C[2]*1000)}[a3];"
          f"[a1][a2][a3]amix=inputs=3:normalize=0,volume=-20dB[amb];"
          f"[4:a]adelay={int(V*1000)}|{int(V*1000)},volume={0.0 if SINVOZ else 1.0}[voz];"
          f"[voz][amb]amix=inputs=2:normalize=0,apad,atrim=0:{DUR},afade=t=out:st={DUR-0.8}:d=0.8,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp,
                    "-i", os.path.join(BANCO, A[0]), "-i", os.path.join(BANCO, B[0]), "-i", os.path.join(BANCO, C[0]), "-i", VOZ,
                    "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", "-t", str(DUR), OUT], check=True)
    os.remove(tmp)
    print(OUT)
