"""Arma el logo principal de Sin Límites: pincelada (fuentes/pincelada-openai-3.png, generada con OpenAI)
+ piezas de rompecabezas sutiles + letras negras vectoriales (fuentes/letras-negras-paths.txt)."""
import os, base64, io, subprocess, numpy as np
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
# 1. pincelada: fondo blanco -> transparente
src=np.asarray(Image.open(f"{D}/fuentes/pincelada-openai-3.png").convert("RGB")).astype(float)
mn=src.min(axis=2); alpha=np.clip((252-mn)/(252-170),0,1)**0.75; alpha[alpha<0.03]=0
col=np.clip((src-(1-alpha[...,None])*255)/np.maximum(alpha[...,None],1e-3),0,255)
sw=Image.fromarray(np.dstack([col,alpha*255]).astype(np.uint8),"RGBA"); sw=sw.crop(sw.getbbox())
buf=io.BytesIO(); sw.save(buf,"PNG"); b64=base64.b64encode(buf.getvalue()).decode()
# 2. letras (viewBox 3840x1680 del trazado)
letras=open(f"{D}/fuentes/letras-logo.svgfrag").read()
LW,LH=3840,1680
# lienzo
W,H=4200,2000
sx=(W-LW)/2; sy=(H-LH)/2
swW=3900; swH=int(swW*sw.height/sw.width*1.15)
def pieza(x,y,s,rot,colr,op=0.9):
    # pieza clásica: pestaña redonda arriba y a la derecha, encastre abajo y a la izquierda (cuadrado de 100)
    p=("M0,0 H36 C38,-3 34,-8 34,-13 A16,16 0 1 1 66,-13 C66,-8 62,-3 64,0 H100 "
       "V36 C103,38 108,34 113,34 A16,16 0 1 1 113,66 C108,66 103,62 100,64 V100 "
       "H64 C62,97 66,92 66,87 A16,16 0 1 0 34,87 C34,92 38,97 36,100 H0 "
       "V64 C-3,62 -8,66 -13,66 A16,16 0 1 0 -13,34 C-8,34 -3,38 0,36 Z")
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s}) translate(-50,-50)">'
            f'<path d="{p}" fill="{colr}" opacity="{op}"/>'
            f'<path d="{p}" fill="none" stroke="#ffffff" stroke-opacity="0.55" stroke-width="4"/></g>')
def estrella(x,y,r,colr,op=0.9):
    k=r*0.22
    return (f'<path d="M{x},{y-r} Q{x+k},{y-k} {x+r},{y} Q{x+k},{y+k} {x},{y+r} Q{x-k},{y+k} {x-r},{y} Q{x-k},{y-k} {x},{y-r}Z" '
            f'fill="{colr}" opacity="{op}"/>')
piezas="".join([pieza(390,260,1.5,-16,"#B79AE0"), pieza(3900,820,1.6,20,"#58BFC4"), pieza(3640,1780,1.3,-28,"#F08A7E")])
piezas+="".join([estrella(3420,170,62,"#F2C14E"), estrella(3560,300,30,"#F5A3B9"),
                 estrella(300,1560,52,"#F2C14E"), estrella(470,1700,26,"#A9CDEB"), estrella(2000,110,30,"#C9B0EC")])
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<image x="{(W-swW)/2}" y="{(H-swH)/2+40}" width="{swW}" height="{swH}" preserveAspectRatio="none" xlink:href="data:image/png;base64,{b64}"/>
{piezas}
<g transform="translate({sx},{sy})" fill="#1A1A1A">{letras}</g>
</svg>'''
open(f"{D}/sin-limites-logo-acuarela.svg","w").write(svg)
subprocess.run(["rsvg-convert","-w","2600",f"{D}/sin-limites-logo-acuarela.svg","-o",f"{D}/sin-limites-logo-acuarela.png"],check=True)
im=Image.open(f"{D}/sin-limites-logo-acuarela.png"); bb=im.getbbox(); m=30
im.crop((max(0,bb[0]-m),max(0,bb[1]-m),min(im.width,bb[2]+m),min(im.height,bb[3]+m))).save(f"{D}/sin-limites-logo-acuarela.png")
print(Image.open(f"{D}/sin-limites-logo-acuarela.png").size)
