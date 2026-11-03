import numpy as np, subprocess, os
from PIL import Image, ImageFilter
R="/home/claude/sinlimites/medios/marca"
src=np.asarray(Image.open(f"{R}/fuentes/pincelada-openai-1.png").convert("RGB")).astype(float)
mn=src.min(axis=2); alpha=np.clip((241-mn)/(241-175),0,1)**0.7
alpha[alpha<0.04]=0
col=np.clip((src-(1-alpha[...,None])*249)/np.maximum(alpha[...,None],1e-3),0,255)
rgba=np.dstack([col,alpha*255]).astype(np.uint8)
im=Image.fromarray(rgba,"RGBA")
bb=im.getchannel("A").point(lambda v:255 if v>20 else 0).getbbox(); print("bbox",bb)
sw=im.crop(bb)
# letras: tinta + borde blanco, desde el SVG vectorial
subprocess.run(["rsvg-convert","-w","2400",f"{R}/sin-limites-logo-tinta.svg","-o","/tmp/_t.png"],check=True)
L=Image.open("/tmp/_t.png").convert("RGBA"); lb=L.getbbox(); L=L.crop(lb)
W=2600; H=1300
canvas=Image.new("RGBA",(W,H),(0,0,0,0))
# pincelada detrás, un poco más ancha que las letras
sw=sw.resize((int(L.width*1.12), int(L.width*1.12*sw.height/sw.width*1.05)), Image.LANCZOS)
canvas.alpha_composite(sw,((W-sw.width)//2,(H-sw.height)//2+20))
# borde blanco de las letras
a=L.getchannel("A"); border=a.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(2))
wl=Image.new("RGBA",L.size,(255,255,255,0)); wl.putalpha(border)
ox,oy=(W-L.width)//2,(H-L.height)//2
canvas.alpha_composite(wl,(ox,oy)); canvas.alpha_composite(L,(ox,oy))
canvas.save("/tmp/_c.png")

# estrellitas pastel alrededor
from PIL import ImageDraw
def estrella(d,x,y,r,col):
    k=r*0.28; pts=[]
    import math
    for i in range(16):
        ang=math.pi/2+i*math.pi/8
        rr=r if i%4==0 else (k if i%2==1 else r*0.38)
        pts.append((x+rr*math.cos(ang), y-rr*math.sin(ang)))
    d.polygon(pts, fill=col)
lay=Image.new("RGBA",canvas.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
for (x,y,r,c) in [(330,250,60,(245,205,90,235)),(430,150,30,(240,150,185,230)),(2300,330,48,(160,200,240,235)),
                  (2390,980,62,(245,205,90,235)),(2240,1080,30,(200,170,235,230)),(260,1010,34,(150,215,195,230)),(1330,110,26,(200,170,235,220))]:
    estrella(d,x,y,r,c)
canvas.alpha_composite(lay)
bb=canvas.getbbox(); m=40
canvas=canvas.crop((bb[0]-m,bb[1]-m,bb[2]+m,bb[3]+m))
canvas.save(f"{R}/sin-limites-logo-acuarela.png")
# SVG: pincelada y estrellas como imagen + letras como vector encima no aplica (borde); se guarda PNG de 2400 px
print(canvas.size)
