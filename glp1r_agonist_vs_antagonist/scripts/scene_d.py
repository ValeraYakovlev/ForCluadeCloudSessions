import sys; sys.path.insert(0,'.')
from scenes import *
import numpy as np
from an4 import cadict, superpose_core, REF
from an2 import load
base()
cmd.load("work/pdb/6X18.cif","c"); cmd.remove("not (chain R or chain P)"); cmd.remove("hydrogens")
cmd.create("rec","c and chain R"); cmd.create("pep","c and chain P"); cmd.delete("c")
def bring(pid,chain,obj,het):
    cmd.load(f"work/pdb/{pid}.cif","tmpo"); cmd.remove("hydrogens")
    ch=cmd.get_chains("tmpo"); print(pid,"chains",ch)
    cmd.create(obj+"_r",f"tmpo and chain {chain}"); cmd.create(obj+"_l",f"tmpo and resn {het}")
    m=load(pid); X=cadict(m,chain); R,t,nc,rm=superpose_core(X,REF)
    M=[float(R[0][0]),float(R[0][1]),float(R[0][2]),float(t[0]),float(R[1][0]),float(R[1][1]),float(R[1][2]),float(t[1]),float(R[2][0]),float(R[2][1]),float(R[2][2]),float(t[2]),0.0,0.0,0.0,1.0]
    cmd.transform_selection(obj+"_r or "+obj+"_l",M,homogenous=0); cmd.delete("tmpo"); print(pid,"core",nc,"rmsd %.2f"%rm)
bring("6X1A","R","pf","UK4"); bring("6ORV","RP","tt","N2V"); bring("6XOX","R","ly","V6G")
cmd.hide("everything"); cmd.show("cartoon","rec"); cmd.color(C_TMD,"rec"); cmd.set("cartoon_transparency",0.6,"rec")
cmd.remove("pf_r or tt_r or ly_r")
cmd.show("sticks","pep and resi 7-15"); cmd.color(C_ORANGE,"pep and resi 7-15 and elem C"); cmd.show("cartoon","pep and resi 7-17"); cmd.color(C_ORANGE,"pep")
cmd.show("sticks","pf_l"); cmd.color(C_GREEN,"pf_l and elem C")
cmd.show("sticks","tt_l"); cmd.color(C_VIOLET,"tt_l and elem C")
cmd.show("sticks","ly_l"); cmd.color(C_MAG,"ly_l and elem C")
pocket=[152,190,197,234,306,310,380,388]
cmd.show("sticks","rec and resi "+"+".join(map(str,pocket))); cmd.color("0x5a5853","rec and resi "+"+".join(map(str,pocket))+" and elem C")
cmd.hide("cartoon","rec and resi 24-137")
cmd.util.cnc("all")
cmd.orient("pep and resi 7-15 or pf_l or tt_l or ly_l or (rec and resi "+"+".join(map(str,pocket))+")")
cmd.turn("x",-90)
cmd.show("cartoon","pep and resi 7-17"); cmd.set("cartoon_oval_width",0.3,"pep")
anch=[("rec",r,"","#4a4944","L" if r in (152,190,380,388) else "R") for r in pocket]+[("pep",r,"GLP-1 ","#c4501f","R") for r in (7,9,12,13,15)]
def cen(sel):
    l=[]; cmd.iterate_state(1,sel,"stored_l.append((x,y,z))",space={'stored_l':l}); return np.mean(l,axis=0)
custom=[("PF-06882961 (данаглипрон)",cen("pf_l"),"#13805a","L"),("TT-OAD2",cen("tt_l"),"#4a3aa7","L"),("LY3502970 (орфорглипрон)",cen("ly_l"),"#b04a78","L")]
render_scene("scene_d",2000,1500,anch,"(rec and resi 140-400) within 18 of (pep and resi 7-15)",zoom_sel="pep and resi 7-15 or pf_l or tt_l or ly_l",zoom_buf=8,title="Карман TMD: N-конец GLP-1 и три непептидных агониста",custom=custom,
  legend=[("GLP-1 7–15 (6X18)","#c4501f"),("PF-06882961 (6X1A)","#13805a"),("TT-OAD2 (6ORV)","#4a3aa7"),("LY3502970 (6XOX)","#b04a78"),("TMD 6X18, остатки кармана серым; структуры совмещены по ядру TMD","#4a4944")],legend_loc="bottom")
