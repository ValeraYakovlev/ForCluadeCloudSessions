import numpy as np
from pymol import cmd
from scipy import ndimage
from PIL import Image
def _hue(i,n):
    import colorsys
    r,g,b=colorsys.hsv_to_rgb(i/n,1.0,1.0); return [r,g,b]
def calibrate(W,H,pts,tmp="/tmp/claude-0/calib.png"):
    """pts: list of xyz; returns 3x4 DLT matrix mapping world->pixel"""
    on=list(cmd.get_names("objects",enabled_only=1))
    for o in on: cmd.disable(o)
    n=len(pts)
    for i,p in enumerate(pts):
        cmd.set_color(f"ctrl{i}",_hue(i,n))
        cmd.pseudoatom("ctrl",pos=list(map(float,p)),color=f"ctrl{i}",vdw=1.2,resi=str(i+1),name="C")
    cmd.show("spheres","ctrl")
    old={k:cmd.get(k) for k in ("ambient","direct","specular","reflect","depth_cue","antialias","cartoon_transparency")}
    cmd.set("ambient",1.0); cmd.set("direct",0.0); cmd.set("specular",0.0); cmd.set("reflect",0.0); cmd.set("depth_cue",0); cmd.set("antialias",0); cmd.set("sphere_scale",1.0)
    cmd.png(tmp,width=W,height=H,dpi=-1,ray=0)
    cmd.delete("ctrl")
    for k,v in old.items(): cmd.set(k,v)
    cmd.set("sphere_scale",0.25)
    for o in on: cmd.enable(o)
    im=np.array(Image.open(tmp).convert("RGB")).astype(int)
    uv=[]; used=[]
    for i,p in enumerate(pts):
        r,g,b=[int(round(255*c)) for c in _hue(i,n)]
        mask=(abs(im[:,:,0]-r)<12)&(abs(im[:,:,1]-g)<12)&(abs(im[:,:,2]-b)<12)
        ys,xs=np.nonzero(mask)
        if len(xs)>20:
            uv.append((xs.mean(),ys.mean())); used.append(i)
    A=[]
    for i,(u,v) in zip(used,uv):
        X,Y,Z=pts[i]
        A.append([X,Y,Z,1,0,0,0,0,-u*X,-u*Y,-u*Z,-u]); A.append([0,0,0,0,X,Y,Z,1,-v*X,-v*Y,-v*Z,-v])
    A=np.array(A)
    _,_,Vt=np.linalg.svd(A); P=Vt[-1].reshape(3,4)
    # reprojection error
    err=[]
    for i,(u,v) in zip(used,uv):
        x=P@np.array([*pts[i],1.0]); err.append(np.hypot(x[0]/x[2]-u,x[1]/x[2]-v))
    return P,len(used),float(np.mean(err)),float(np.max(err))
def project(P,xyz):
    x=P@np.array([*xyz,1.0]); return x[0]/x[2],x[1]/x[2]
