import numpy as np, potrace
from PIL import Image, ImageFilter
src=Image.open("/home/claude/sinlimites/medios/banco/flyer-admisiones-2027.png").convert("RGB").crop((140,15,580,180))
K=6
up=src.resize((src.width*K,src.height*K),Image.LANCZOS).filter(ImageFilter.GaussianBlur(2.2))
a=np.asarray(up).astype(float)
lum=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
ink=lum<95
bm=potrace.Bitmap(~ink)
path=bm.trace(turdsize=30, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.1, opticurve=True, opttolerance=0.3)
W,H=up.size
parts=[];xs=[];ys=[]
for curve in path:
    s=curve.start_point; d=[f"M{s.x:.1f},{s.y:.1f}"]; xs.append(s.x); ys.append(s.y)
    for seg in curve.segments:
        if seg.is_corner: d.append(f"L{seg.c.x:.1f},{seg.c.y:.1f}L{seg.end_point.x:.1f},{seg.end_point.y:.1f}")
        else: d.append(f"C{seg.c1.x:.1f},{seg.c1.y:.1f} {seg.c2.x:.1f},{seg.c2.y:.1f} {seg.end_point.x:.1f},{seg.end_point.y:.1f}")
        xs.append(seg.end_point.x); ys.append(seg.end_point.y)
    parts.append("".join(d)+"Z")
open("paths.txt","w").write(" ".join(parts))
print(W,H,len(parts),min(xs),max(xs),min(ys),max(ys))
