import sys, random; sys.path.insert(0,'.')
import numpy as np
from render_common import *
from project import calibrate, project
from annotate import annotate
one={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
def anchor(obj,resi):
    pts=[]
    cmd.iterate_state(1,f"{obj} and resi {resi} and not name N+C+O+CA","stored_l.append((x,y,z))",space={'stored_l':pts})
    if not pts: cmd.iterate_state(1,f"{obj} and resi {resi} and name CA","stored_l.append((x,y,z))",space={'stored_l':pts})
    rn=[]; cmd.iterate(f"{obj} and resi {resi} and name CA","stored_l.append(resn)",space={'stored_l':rn})
    return np.mean(pts,axis=0), one[rn[0]]
def control_points(sel,n=14,seed=1):
    lst=[]; cmd.iterate_state(1,f"({sel}) and name CA","stored_l.append((x,y,z))",space={'stored_l':lst})
    random.seed(seed); return random.sample(lst,min(n,len(lst)))
def render_scene(name,W,H,anchors,sel_ctrl,title=None,legend=None,center=None,fontpx=34,custom=(),legend_loc='top',zoom_sel='all',zoom_buf=2,pad=(0,0)):
    cmd.zoom(zoom_sel,buffer=zoom_buf)
    pts=control_points(sel_ctrl)
    P,n,me,mx=calibrate(W,H,pts)
    print(name,"calib used",n,"mean err %.2f max %.2f px"%(me,mx))
    cmd.png(f"renders/{name}_raw.png",width=W,height=H,dpi=-1,ray=1)
    items=[]
    for obj,resi,pre,col,side in anchors:
        xyz,aa=anchor(obj,resi); u,v=project(P,xyz)
        d=dict(text=f"{pre}{aa}{resi}",uv=(u,v),color=col)
        if side: d["side"]=side
        items.append(d)
    for text,xyz,col,side in custom:
        u,v=project(P,xyz); d=dict(text=text,uv=(u,v),color=col)
        if side: d['side']=side
        items.append(d)
    annotate(f"renders/{name}_raw.png",f"renders/{name}.png",items,W,H,title=title,legend=legend,center=center,fontpx=fontpx,legend_loc=legend_loc,pad=pad)
