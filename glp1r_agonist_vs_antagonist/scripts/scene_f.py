import sys; sys.path.insert(0,'.')
from scenes import *
import numpy as np
from an4 import cadict, superpose_core, REF
from an2 import load
base()
cmd.load("work/pdb/6X18.cif","c"); cmd.remove("not (chain R or chain P)"); cmd.remove("hydrogens")
cmd.create("rec","c and chain R"); cmd.create("pep","c and chain P"); cmd.delete("c")
cmd.load("work/pdb/5VEW.cif","tmpo"); cmd.remove("hydrogens")
cmd.create("nam_r","tmpo and chain A and resi 136-422"); cmd.create("nam_l","tmpo and chain A and resn 97Y"); cmd.delete("tmpo")
m=load("5VEW"); X={r.id[1]:r['CA'].coord.copy() for r in m["A"] if r.id[0]==' ' and 'CA' in r and 136<=r.id[1]<=422}
R,t,nc,rm=superpose_core(X,REF); print("5VEW core",nc,"rmsd %.2f"%rm)
M=[float(R[0][0]),float(R[0][1]),float(R[0][2]),float(t[0]),float(R[1][0]),float(R[1][1]),float(R[1][2]),float(t[1]),float(R[2][0]),float(R[2][1]),float(R[2][2]),float(t[2]),0.0,0.0,0.0,1.0]
cmd.transform_selection("nam_r or nam_l",M,homogenous=0)
cmd.hide("everything"); cmd.show("cartoon","rec or pep"); cmd.hide("cartoon","rec and resi 24-137")
cmd.color(C_TMD,"rec"); cmd.set("cartoon_transparency",0.5,"rec")
cmd.color(C_ORANGE,"pep and resi 7-17"); cmd.color(C_GRAY,"pep and resi 18-23"); cmd.color(C_BLUE,"pep and resi 24-36")
cmd.show("sticks","pep and resi 7-15"); cmd.color(C_ORANGE,"pep and resi 7-15 and elem C")
cmd.show("sticks","nam_l"); cmd.color(C_GREEN,"nam_l and elem C")
cmd.show("cartoon","nam_r and resi 330-422"); cmd.color("0x6b6a66","nam_r"); cmd.set("cartoon_transparency",0.4,"nam_r")
cmd.hide("cartoon","nam_r and not resi 340-395")  # keep TM6/TM7 of inactive structure for contrast
cmd.color(C_ORANGE,"rec and resi 340-395")
cmd.util.cnc("all")
cmd.orient("rec and resi 140-423"); cmd.turn("z",270)
def cen(sel):
    l=[]; cmd.iterate_state(1,sel,"stored_l.append((x,y,z))",space={'stored_l':l}); return np.mean(l,axis=0)
custom=[("GLP-1 N-конец (7–15): внеклеточный карман",cen("pep and resi 7-15"),"#c4501f","R"),
        ("NAM PF-06372222: внутриклеточный карман",cen("nam_l"),"#13805a","R")]
render_scene("scene_f",1800,2400,[],"rec and resi 140-400",custom=custom,fontpx=30,pad=(0,560),zoom_sel="(rec and resi 140-400) or nam_l or (pep and resi 7-36)",zoom_buf=4,
  title="Два конца рецептора: агонист-карман и сайт NAM",
  legend=[("GLP-1 (6X18) в активном комплексе","#c4501f"),("PF-06372222 в неактивном TMD (5VEW), совмещено по ядру TMD","#13805a"),("персиковым: TM6/TM7 активной формы 6X18 на внутриклеточной стороне","#c4501f")],legend_loc="bottom")
