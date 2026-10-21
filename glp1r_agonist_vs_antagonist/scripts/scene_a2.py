import sys; sys.path.insert(0,'.')
from scenes import *
base()
cmd.load("work/pdb/6X18.cif","c"); cmd.remove("not (chain R or chain P)"); cmd.remove("hydrogens")
cmd.create("rec","c and chain R"); cmd.create("pep","c and chain P"); cmd.delete("c")
cmd.hide("everything"); cmd.show("cartoon","rec or pep")
cmd.color(C_TMD,"rec"); cmd.color(C_ECD,"rec and resi 29-137")
cmd.color(C_GRAY,"pep"); cmd.color(C_ORANGE,"pep and resi 7-17"); cmd.color(C_BLUE,"pep and resi 24-36")
cmd.set("cartoon_transparency",0.45,"rec"); cmd.set("cartoon_oval_width",0.35,"pep"); cmd.set("cartoon_oval_length",1.6,"pep")
ecd=[29,32,39,68,69,88,91,121]; tmd=[152,190,197,234,299,306,310,380,384,388]
cmd.show("sticks","rec and resi "+"+".join(map(str,ecd+tmd)))
cmd.color(C_BLUE,"rec and resi "+"+".join(map(str,ecd))+" and elem C"); cmd.color(C_ORANGE,"rec and resi "+"+".join(map(str,tmd))+" and elem C")
pepres=[7,9,12,13,15,28,29,32]
cmd.show("sticks","pep and resi "+"+".join(map(str,pepres)))
cmd.color(C_ORANGE,"pep and resi 7+9+12+13+15 and elem C"); cmd.color(C_BLUE,"pep and resi 28+29+32 and elem C")
cmd.util.cnc("all")
cmd.orient("rec or pep"); cmd.turn("z",90)
anchors=[("rec",r,"","#1f5fb5","R") for r in ecd]+[("rec",r,"","#c4501f","L" if r in (299,306,310,380,384) else "R") for r in tmd]
anchors+=[("pep",r,"GLP-1 ","#c4501f","L") for r in (7,9,12,13,15)]+[("pep",r,"GLP-1 ","#1f5fb5","L") for r in (28,29,32)]
render_scene("scene_a",1800,2400,anchors,"rec",title="GLP-1R–GLP-1 (6X18): ECD-борозда и TMD-карман",
  legend=[("пептид 7–17: N-модуль в TMD (оранжевый)","#c4501f"),("пептид 24–36: спираль в борозде ECD (синий)","#1f5fb5")],legend_loc="bottom")
