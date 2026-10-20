import sys; sys.path.insert(0,'.')
from scenes import *
import numpy as np
base()
cmd.load("work/pdb/6X18.cif","c"); cmd.remove("not (chain R or chain P)"); cmd.remove("hydrogens")
cmd.create("rec","c and chain R"); cmd.create("pep","c and chain P"); cmd.delete("c")
cmd.load("work/pdb/5E94.cif","fabx"); cmd.remove("hydrogens"); cmd.remove("het"); cmd.remove("solvent")
cmd.create("fabecd","fabx and chain G"); cmd.create("fabL","fabx and chain A"); cmd.create("fabH","fabx and chain B"); cmd.delete("fabx")
import numpy as np
from an2 import load, aa
from an4 import kabsch
ref=load("6X18"); fab=load("5E94")
R_={r.id[1]:r['CA'].coord.copy() for r in aa(ref["R"]) if 29<=r.id[1]<=128 and 'CA' in r}
S_={r.id[1]:r['CA'].coord.copy() for r in aa(fab["G"]) if 29<=r.id[1]<=128 and 'CA' in r}
com=sorted(set(R_)&set(S_)); A=np.array([S_[n] for n in com]); B=np.array([R_[n] for n in com])
Rm,tv=kabsch(A,B)
M=[float(Rm[0][0]),float(Rm[0][1]),float(Rm[0][2]),float(tv[0]),float(Rm[1][0]),float(Rm[1][1]),float(Rm[1][2]),float(tv[1]),float(Rm[2][0]),float(Rm[2][1]),float(Rm[2][2]),float(tv[2]),0.0,0.0,0.0,1.0]
cmd.transform_selection("fabecd or fabL or fabH",M,homogenous=0)
cmd.hide("everything"); cmd.show("cartoon","rec or pep or fabL or fabH")
cmd.color(C_TMD,"rec"); cmd.color(C_ECD,"rec and resi 29-137"); cmd.set("cartoon_transparency",0.55,"rec and not resi 29-137")
cmd.color(C_ORANGE,"pep and resi 7-17"); cmd.color(C_GRAY,"pep and resi 18-23"); cmd.color(C_BLUE,"pep and resi 24-36")
cmd.color("0xb04a78","fabH"); cmd.color("0xe9a3c3","fabL"); cmd.set("cartoon_transparency",0.35,"fabH or fabL")
epi=[29,30,31,32,33,35,36,39,40,43,68,137,138,141,142,144,145]
cmd.show("sticks","rec and resi "+"+".join(map(str,epi))); cmd.color("0xd02020","rec and resi "+"+".join(map(str,epi))+" and elem C")
# clash atoms
cmd.select("clash","(fabL or fabH) within 2.0 of (rec and resi 138-423)")
print("fab atoms <2A from TMD/ECL:",cmd.count_atoms("clash"))
cmd.util.cnc("all")
cmd.show("spheres","clash"); cmd.set("sphere_scale",0.3,"clash"); cmd.color("0xff3030","clash")
cmd.orient("rec or pep or fabL or fabH"); cmd.turn("z",90)
def cen(sel):
    l=[]; cmd.iterate_state(1,sel,"stored_l.append((x,y,z))",space={'stored_l':l}); return np.mean(l,axis=0)
custom=[("Fab 3F52, тяжёлая цепь",cen("fabH and name CA"),"#8e2f63","L"),("Fab 3F52, лёгкая цепь",cen("fabL and name CA"),"#b0608a","L"),
        ("GLP-1 7–17 (карман TMD)",cen("pep and resi 7-17 and name CA"),"#c4501f","R"),("GLP-1 24–36 (борозда ECD)",cen("pep and resi 24-36 and name CA"),"#1f5fb5","R"),
        ("перекрытие Fab с TMD (<2 Å)",cen("clash"),"#c01818","R")]
render_scene("scene_e",1800,2400,[],"rec",title="Fab 3F52 на ECD, наложенный на активный рецептор (6X18)",custom=custom,fontpx=30,pad=(0,520),zoom_sel="rec or pep or fabL or fabH",zoom_buf=14,
  legend=[("красные палочки ECD: эпитоп Fab 3F52 (17 остатков, 29–145)","#c01818"),("красные точки: атомы Fab ближе 2 Å к TMD/ECL","#c01818"),("пептид GLP-1: 7–17 оранжевый, 24–36 синий","#1f5fb5")],legend_loc="bottom")
