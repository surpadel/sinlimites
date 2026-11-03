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
d=open(f"{D}/fuentes/letras-negras-paths.txt").read()
LW,LH=3840,1680
# lienzo
W,H=4200,2000
sx=(W-LW)/2; sy=(H-LH)/2
swW=3900; swH=int(swW*sw.height/sw.width*1.15)
def pieza(x,y,s,rot,colr,op):
    # pieza de rompecabezas de 100x100 con dos pestañas
    p=("M0,0 H35 C35,-18 65,-18 65,0 H100 V35 C118,35 118,65 100,65 V100 H65 C65,82 35,82 35,100 H0 V65 "
       "C18,65 18,35 0,35 Z")
    return f'<path d="{p}" fill="{colr}" opacity="{op}" transform="translate({x},{y}) rotate({rot}) scale({s})" stroke="#ffffff" stroke-width="3" stroke-opacity="0.5"/>'
piezas="".join([pieza(330,170,1.55,-18,"#B79AE0",0.85), pieza(3790,560,1.75,22,"#B79AE0",0.85),
                pieza(240,1270,1.35,12,"#58BFC4",0.85), pieza(3650,1660,1.45,-25,"#F08A7E",0.85),
                pieza(2050,60,0.9,30,"#F4C65E",0.7)])
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<image x="{(W-swW)/2}" y="{(H-swH)/2+40}" width="{swW}" height="{swH}" preserveAspectRatio="none" xlink:href="data:image/png;base64,{b64}"/>
{piezas}
<path transform="translate({sx},{sy})" fill="#1A1A1A" fill-rule="evenodd" d="{d}"/>
</svg>'''
open(f"{D}/sin-limites-logo-acuarela.svg","w").write(svg)
subprocess.run(["rsvg-convert","-w","2600",f"{D}/sin-limites-logo-acuarela.svg","-o",f"{D}/sin-limites-logo-acuarela.png"],check=True)
im=Image.open(f"{D}/sin-limites-logo-acuarela.png"); bb=im.getbbox(); m=30
im.crop((max(0,bb[0]-m),max(0,bb[1]-m),min(im.width,bb[2]+m),min(im.height,bb[3]+m))).save(f"{D}/sin-limites-logo-acuarela.png")
print(Image.open(f"{D}/sin-limites-logo-acuarela.png").size)
