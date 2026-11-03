"""Título "Sin Límites" del logo de Instagram + "Espacio Interdisciplinario" del flyer (más nítido), ambos vectoriales."""
import os, re
D=os.path.dirname(os.path.abspath(__file__))
def partes(f): return [p+"Z" for p in open(f"{D}/fuentes/{f}").read().split("Z") if p.strip()]
def bbox(ps):
    xs=[];ys=[]
    for p in ps:
        n=[float(x) for x in re.findall(r"-?\d+\.?\d*",p)]; xs+=n[0::2]; ys+=n[1::2]
    return min(xs),min(ys),max(xs),max(ys)
def miny(p): return bbox([p])[1]
ig=partes("letras-negras-paths.txt"); fl=partes("letras-flyer-paths.txt")
titulo=[p for p in ig if miny(p)<1190]; sub_ig=[p for p in ig if miny(p)>=1190]; sub_fl=[p for p in fl if miny(p)>=650]
tb=bbox(titulo); sb=bbox(sub_ig); fb=bbox(sub_fl)
# el subtítulo nuevo ocupa un poco más de ancho que el original para leerse mejor
ancho=(sb[2]-sb[0])*1.08; s=ancho/(fb[2]-fb[0])
cx=(sb[0]+sb[2])/2; top=sb[1]-10
tx=cx-(fb[0]+(fb[2]-fb[0])/2)*s; ty=top-fb[1]*s
g_sub=f'<g transform="translate({tx:.1f},{ty:.1f}) scale({s:.4f})"><path fill-rule="evenodd" d="{" ".join(sub_fl)}"/></g>'
g_tit=f'<path fill-rule="evenodd" d="{" ".join(titulo)}"/>'
open(f"{D}/fuentes/letras-logo.svgfrag","w").write(g_tit+g_sub)
for nombre,col in [("tinta","#1A1A1A"),("blanco","#FFFFFF")]:
    open(f"{D}/sin-limites-logo-{nombre}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3840 1680" width="3840" height="1680"><g fill="{col}">{g_tit}{g_sub}</g></svg>')
print("ok", s)
