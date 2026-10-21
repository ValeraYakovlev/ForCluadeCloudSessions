import sys; sys.path.insert(0,'.')
from scenes import *
base()
cmd.load("work/pdb/6X18.cif","c"); cmd.remove("not (chain R or chain P)"); cmd.remove("hydrogens")
cmd.create("rec","c and chain R"); cmd.create("pep","c and chain P"); cmd.delete("c")
cmd.load("work/pdb/3C5T.cif","p3c5t"); cmd.remove("hydrogens"); cmd.remove("het"); cmd.remove("solvent")
cmd.align("p3c5t and chain A and resi 29-128 and name CA","rec and resi 29-128 and name CA",cycles=5)
cmd.create("ecd2","p3c5t and chain A"); cmd.create("ex4","p3c5t and chain B"); cmd.delete("p3c5t")
cmd.remove("rec and not resi 29-137"); cmd.remove("ecd2")
cmd.remove("pep and resi 7-17")
cmd.hide("everything"); cmd.show("cartoon","rec or pep or ex4")
cmd.color(C_ECD,"rec"); cmd.color(C_BLUE,"pep"); cmd.color(C_VIOLET,"ex4")
cmd.set("cartoon_oval_width",0.4,"pep or ex4"); cmd.set("cartoon_oval_length",1.8,"pep or ex4")
cmd.set("cartoon_transparency",0.35,"rec")
gro=[29,32,39,68,69,88,91,121,123]
cmd.show("sticks","rec and resi "+"+".join(map(str,gro))); cmd.color(C_BLUE,"rec and resi "+"+".join(map(str,gro))+" and elem C")
cmd.show("sticks","pep and resi 28+29+32+33"); cmd.show("sticks","ex4 and resi 19+22+23+26")
cmd.color(C_BLUE,"pep and elem C"); cmd.color(C_VIOLET,"ex4 and elem C")
cmd.util.cnc("all")
cmd.orient("rec or pep or ex4"); cmd.turn("x",100); cmd.turn("z",90)
anch=[("rec",r,"","#1f5fb5","L") for r in gro]
anch+=[("pep",r,"GLP-1 ","#1f5fb5","R") for r in (28,29,32,33)]+[("ex4",r,"Ex4 ","#4a3aa7","R") for r in (19,22,23,26)]
render_scene("scene_b",1800,1900,anch,"rec",title="Одна и та же борозда ECD: GLP-1 (6X18, синий) и Exendin-4(9–39) (3C5T, фиолетовый)",
  legend=[("остатки ECD борозды (общие для агониста и антагониста)","#1f5fb5"),("GLP-1 24–36 (6X18)","#1f5fb5"),("Exendin-4(9–33), кристалл ECD (3C5T)","#4a3aa7")],legend_loc="bottom")
