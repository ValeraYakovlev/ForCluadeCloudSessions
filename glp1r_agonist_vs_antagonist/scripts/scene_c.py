import sys; sys.path.insert(0,'.')
from scenes import *
import numpy as np
base()
cmd.load("work/pdb/6X18.cif","c"); cmd.remove("not (chain R or chain P)"); cmd.remove("hydrogens")
cmd.create("act","c and chain R"); cmd.create("pep","c and chain P"); cmd.delete("c")
cmd.load("work/pdb/6LN2.cif","ina0"); cmd.remove("hydrogens"); cmd.remove("het"); cmd.remove("solvent")
cmd.create("ina","ina0 and chain A"); cmd.delete("ina0")
core="resi 150-196+225-262+270-296+308-337"
from an4 import superpose_core, REF, INA
Rm,tv,nc,rm=superpose_core(INA,REF)
M=[float(Rm[0][0]),float(Rm[0][1]),float(Rm[0][2]),float(tv[0]),float(Rm[1][0]),float(Rm[1][1]),float(Rm[1][2]),float(tv[1]),float(Rm[2][0]),float(Rm[2][1]),float(Rm[2][2]),float(tv[2]),0.0,0.0,0.0,1.0]
cmd.transform_selection("ina",M,homogenous=0)
print("my superposition core",nc,"rmsd",rm)
cmd.hide("everything"); cmd.show("cartoon","act or ina or pep")
cmd.color(C_TMD,"act"); cmd.color(C_ECD,"act and resi 29-137"); cmd.color("0xb9b7b0","ina"); cmd.color("0x8a8782","ina and resi 29-137")
cmd.color(C_ORANGE,"act and resi 340-395"); cmd.color("0x7a5b4f","ina and resi 340-395")
cmd.color(C_GRAY,"pep"); cmd.color(C_ORANGE,"pep and resi 7-17"); cmd.color(C_BLUE,"pep and resi 24-36")
cmd.set("cartoon_transparency",0.55,"act or ina")
cmd.set("cartoon_transparency",0.15,"act and resi 29-137"); cmd.set("cartoon_transparency",0.15,"ina and resi 29-137")
cmd.set("cartoon_transparency",0.1,"act and resi 340-395"); cmd.set("cartoon_transparency",0.1,"ina and resi 340-395")
# centroids / TM6 points
ecdA=[]; ecdI=[]
cmd.iterate_state(1,"act and name CA and resi 29-130","stored_l.append((x,y,z))",space={'stored_l':ecdA})
cmd.iterate_state(1,"ina and name CA and resi 29-130","stored_l.append((x,y,z))",space={'stored_l':ecdI})
cA=np.mean(ecdA,axis=0); cI=np.mean(ecdI,axis=0)
t6A=[]; t6I=[]
cmd.iterate_state(1,"act and name CA and resi 346","stored_l.append((x,y,z))",space={'stored_l':t6A})
cmd.iterate_state(1,"ina and name CA and resi 346","stored_l.append((x,y,z))",space={'stored_l':t6I})
t6A=np.array(t6A[0]); t6I=np.array(t6I[0])
print("ECD centroid shift %.1f ; TM6 346 shift %.1f"%(np.linalg.norm(cA-cI),np.linalg.norm(t6A-t6I)))
for nm,p,q in (("d_ecd",cI,cA),("d_tm6",t6I,t6A)):
    cmd.pseudoatom(nm+"_a",pos=list(map(float,p))); cmd.pseudoatom(nm+"_b",pos=list(map(float,q)))
    cmd.show("spheres",nm+"_a or "+nm+"_b"); cmd.color("black",nm+"_a or "+nm+"_b")
    cmd.distance(nm,nm+"_a",nm+"_b"); cmd.hide("labels",nm)
    cmd.set("dash_gap",0.25,nm); cmd.set("dash_radius",0.25,nm); cmd.color("black",nm)
cmd.orient("act or ina or pep"); cmd.turn("z",90)
custom=[("ECD: сдвиг центра %.0f Å"%np.linalg.norm(cA-cI),(cI+cA)/2,"#0b0b0b","L"),
        ("Cα 346 (TM6): сдвиг %.1f Å наружу"%np.linalg.norm(t6A-t6I),(t6I+t6A)/2,"#0b0b0b","R"),
        ("ECD открытой формы (6X18)",cA,"#1f5fb5","L"),("ECD закрытой формы (6LN2)",cI,"#5a5853","L"),
        ("TM6 активной (6X18)",t6A,"#c4501f","R"),("TM6 неактивной (6LN2)",t6I,"#5a5853","R")]
render_scene("scene_c",1800,2400,[],"act or ina",title="Неактивная (6LN2) → активная (6X18): ECD и TM6",
  legend=[("активный комплекс 6X18 (цвет), GLP-1: 7–17 оранжевый, 24–36 синий","#1f5fb5"),("неактивный рецептор 6LN2 (серый); TMD совмещён по ядру","#5a5853")],custom=custom,fontpx=30,pad=(0,340),legend_loc='bottom')
