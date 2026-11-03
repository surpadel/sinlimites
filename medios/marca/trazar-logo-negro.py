"""Vectoriza las letras negras del logo desde la referencia de Instagram (fuentes/logo-referencia-instagram.png)."""
import os, numpy as np, potrace
from PIL import Image, ImageFilter
D=os.path.dirname(os.path.abspath(__file__))
src=Image.open(f"{D}/fuentes/logo-referencia-instagram.png").convert("RGB").crop((60,40,540,250))
K=8
up=src.resize((src.width*K,src.height*K),Image.LANCZOS).filter(ImageFilter.GaussianBlur(2.6))
a=np.asarray(up).astype(float); lum=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
ink=lum<88
bm=potrace.Bitmap(~ink)
path=bm.trace(turdsize=60, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0, opticurve=True, opttolerance=0.25)
parts=[]
for c in path:
    s=c.start_point; d=[f"M{s.x:.1f},{s.y:.1f}"]
    for seg in c.segments:
        if seg.is_corner: d.append(f"L{seg.c.x:.1f},{seg.c.y:.1f}L{seg.end_point.x:.1f},{seg.end_point.y:.1f}")
        else: d.append(f"C{seg.c1.x:.1f},{seg.c1.y:.1f} {seg.c2.x:.1f},{seg.c2.y:.1f} {seg.end_point.x:.1f},{seg.end_point.y:.1f}")
    parts.append("".join(d)+"Z")
W,H=up.size; d=" ".join(parts)
open(f"{D}/fuentes/letras-negras-paths.txt","w").write(d)
for nombre,col in [("tinta","#1A1A1A"),("blanco","#FFFFFF")]:
    open(f"{D}/sin-limites-logo-{nombre}.svg","w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><path fill="{col}" fill-rule="evenodd" d="{d}"/></svg>')
print(W,H,len(parts))
