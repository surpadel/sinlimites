import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, DUR = 1080, 1920, 30, 19.5
NAVY = (31, 42, 90)
PINK = (236, 112, 160)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"

src = Image.open(os.path.join(D, "flyer.png")).convert("RGB")
SW, SH = src.size
K = 2  # pre-upscale
big = src.resize((SW * K, SH * K), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))

# background: flyer cover-scaled, blurred, lightened
s = max(W / SW, H / SH)
bg = src.resize((int(SW * s), int(SH * s)), Image.LANCZOS)
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
bg = bg.filter(ImageFilter.GaussianBlur(40))
bg = Image.blend(bg, Image.new("RGB", (W, H), (252, 247, 242)), 0.45)

PX, PY, PW, PH = 60, 250, 960, 1200  # panel
mask = Image.new("L", (PW, PH), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, PW - 1, PH - 1), 44, fill=255)
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle((PX, PY + 18, PX + PW, PY + PH + 18), 44, fill=(60, 40, 90, 70))
shadow = shadow.filter(ImageFilter.GaussianBlur(24))

def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)

# camera keyframes: (t, crop width in flyer px, center y in flyer px); aspect 4:5
KF = [(2.6, 470, 235), (5.4, 440, 225), (6.3, 540, 445), (11.8, 540, 610),
      (12.6, 500, 775), (15.0, 470, 780), (15.9, 738, 462), (DUR, 738, 462)]

def cam(t):
    if t <= KF[0][0]:
        return KF[0][1:]
    for (t0, w0, y0), (t1, w1, y1) in zip(KF, KF[1:]):
        if t <= t1:
            e = ease((t - t0) / (t1 - t0))
            return w0 + (w1 - w0) * e, y0 + (y1 - y0) * e
    return KF[-1][1:]

def panel(t):
    cw, cy = cam(t)
    ch = cw * PH / PW
    cx = SW / 2
    x0 = max(0, min(SW - cw, cx - cw / 2)); y0 = max(0, min(SH - ch, cy - ch / 2))
    box = tuple(int(round(v * K)) for v in (x0, y0, x0 + cw, y0 + ch))
    return big.crop(box).resize((PW, PH), Image.LANCZOS)

def pill(img, lines, cy, size, alpha, scale):
    if alpha <= 0:
        return
    f = ImageFont.truetype(FB, int(size * scale))
    d0 = ImageDraw.Draw(img)
    widths = [d0.textlength(l, font=f) for l in lines]
    lh = int(size * scale * 1.22)
    bw = int(max(widths) + 90 * scale); bh = int(lh * len(lines) + 50 * scale)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0 = (W - bw) // 2; y0 = int(cy - bh / 2)
    d.rounded_rectangle((x0, y0 + 8, x0 + bw, y0 + bh + 8), bh // 2 if len(lines) == 1 else 40, fill=(80, 50, 110, int(50 * alpha)))
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), bh // 2 if len(lines) == 1 else 40, fill=(255, 255, 255, int(240 * alpha)))
    for i, l in enumerate(lines):
        d.text(((W - widths[i]) / 2, y0 + 25 * scale + i * lh - size * scale * 0.08), l, font=f, fill=NAVY + (int(255 * alpha),))
    img.alpha_composite(layer)

def popin(t, a, b, fade=0.22):
    if t < a or t > b:
        return 0, 1
    al = min(1, (t - a) / fade, (b - t) / fade)
    sc = 0.85 + 0.15 * ease((t - a) / fade)
    return max(0, al), sc

SERV = ["Psicología", "Fonoaudiología", "Psicopedagogía", "Terapia Ocupacional",
        "Habilidades sociales", "Evaluación neurocognitiva"]

def hook(img, t):
    lines = ["¿Buscás lugar", "para tu hijo", "en 2027?"]
    f = ImageFont.truetype(FB, 118)
    d = ImageDraw.Draw(img)
    a_out = 1 - ease((t - 2.35) / 0.3)
    for i, l in enumerate(lines):
        ti = 0.15 + i * 0.35
        a = ease((t - ti) / 0.3) * a_out
        if a <= 0:
            continue
        dy = (1 - ease((t - ti) / 0.3)) * 40
        w = d.textlength(l, font=f)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text(((W - w) / 2, 690 + i * 150 + dy), l, font=f,
                                   fill=(PINK if i == 2 else NAVY) + (int(255 * a),))
        img.alpha_composite(layer)
    # underline swash
    a = ease((t - 1.3) / 0.4) * a_out
    if a > 0:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        L = 520 * ease((t - 1.3) / 0.4)
        ImageDraw.Draw(layer).rounded_rectangle((W / 2 - L / 2, 1130, W / 2 + L / 2, 1146), 8, fill=(244, 196, 80, int(220 * a)))
        img.alpha_composite(layer)

def frame(t):
    img = bg.convert("RGBA")
    if t < 2.65:
        hook(img, t)
    pa = ease((t - 2.45) / 0.45)
    if pa > 0:
        sh = shadow.copy(); sh.putalpha(sh.getchannel("A").point(lambda v: int(v * pa)))
        img.alpha_composite(sh)
        p = panel(t).convert("RGBA")
        m = mask.point(lambda v: int(v * pa))
        p.putalpha(m)
        sc = 0.94 + 0.06 * pa
        if sc < 0.999:
            p = p.resize((int(PW * sc), int(PH * sc)), Image.LANCZOS)
        img.alpha_composite(p, (int(W / 2 - p.width / 2), int(PY + PH / 2 - p.height / 2)))
    CY = 1525
    a, s_ = popin(t, 2.9, 5.7); pill(img, ["¡Abrimos las admisiones!"], CY, 58, a, s_)
    for i, sname in enumerate(SERV):
        a0 = 6.2 + i * 0.93
        a, s_ = popin(t, a0, a0 + 0.93, 0.15); pill(img, [sname], CY, 62, a, s_)
    a, s_ = popin(t, 12.5, 15.1); pill(img, ["Atendemos con CUD", "por obra social"], CY, 56, a, s_)
    a, s_ = popin(t, 16.0, DUR + 1); pill(img, ["¡Escribinos hoy!"], 165, 58, a, s_)
    return img.convert("RGB")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for t in [1.8, 4.0, 7.0, 10.5, 13.5, 18.0]:
            frame(t).resize((360, 640)).save(os.path.join(D, f"still_{t}.png"))
        sys.exit()
    n = int(DUR * FPS)
    out = os.path.join(D, "Reel-Admisiones-2027-Sin-Limites.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out],
                         stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    cover = frame(18.0)
    cover.save(os.path.join(D, "Portada-Reel-Admisiones-2027.jpg"), quality=92)
    print(out, p.returncode)
