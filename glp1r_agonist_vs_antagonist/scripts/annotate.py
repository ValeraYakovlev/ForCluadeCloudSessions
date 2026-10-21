import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from PIL import Image
rcParams["font.family"]="DejaVu Sans"
def place_column(items, x, ymin, ymax, gap):
    items=sorted(items,key=lambda it:it["uv"][1])
    ys=[it["uv"][1] for it in items]
    pos=ys[:]
    for i in range(1,len(pos)):
        if pos[i]-pos[i-1]<gap: pos[i]=pos[i-1]+gap
    over=(pos[-1]-ymax) if pos else 0
    if over>0:
        pos=[p-over for p in pos]
        for i in range(len(pos)-2,-1,-1):
            if pos[i+1]-pos[i]<gap: pos[i]=pos[i+1]-gap
    return items,pos
def annotate(png_in,png_out,items,W,H,title=None,legend=None,fontpx=34,dpi=100,left_x=0.02,right_x=0.98,center=None,legend_loc='top',pad=(0,0)):
    im=np.array(Image.open(png_in).convert("RGB"))
    pl,pr=pad; Wi=W; W=W+pl+pr
    items=[dict(it,uv=(it['uv'][0]+pl,it['uv'][1])) for it in items]
    fig=plt.figure(figsize=(W/dpi,H/dpi),dpi=dpi); ax=fig.add_axes([0,0,1,1]); ax.imshow(im,extent=(pl,pl+Wi,H,0)); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
    fs=fontpx*72/dpi
    if center is None: center=W/2
    else: center=center+pl
    def side(it): return it.get("side",("L" if it["uv"][0]<center else "R"))
    left=[it for it in items if side(it)=="L"]; right=[it for it in items if side(it)=="R"]
    for group,xcol,ha in ((left,left_x*W,"left"),(right,right_x*W,"right")):
        if not group: continue
        its,pos=place_column(group,xcol,fontpx*3.2,H*0.97,fontpx*1.25)
        for it,y in zip(its,pos):
            u,v=it["uv"]
            ax.text(xcol,y,it["text"],ha=ha,va="center",fontsize=fs,color=it["color"],fontweight="bold")
            tw=len(it["text"])*fontpx*0.66
            xe = xcol+tw+8 if ha=="left" else xcol-tw-8
            ax.plot([xe,u],[y,v],color="#6b6a66",lw=1.1,zorder=3)
            ax.plot([u],[v],marker="o",ms=5.5,color=it["color"],mec="white",mew=1.0,zorder=4)
    if title: ax.text(0.5*W,0.012*H,title,ha="center",va="top",fontsize=fs*0.95,color="#0b0b0b",fontweight="bold")
    if legend:
        y=0.055*H if legend_loc=='top' else (0.985*H-len(legend)*fontpx*1.2)
        for text,col in legend:
            ax.text(0.02*W,y,"■ "+text,ha="left",va="top",fontsize=fs*0.8,color=col); y+=fontpx*1.2
    fig.savefig(png_out,dpi=dpi); plt.close(fig)
