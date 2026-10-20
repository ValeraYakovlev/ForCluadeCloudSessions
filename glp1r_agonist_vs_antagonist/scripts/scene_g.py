import sys; sys.path.insert(0,'.')
from scenes import *
base()
cmd.load("work/pdb/6X18.cif","c"); cmd.remove("not (chain R or chain P)"); cmd.remove("hydrogens")
cmd.create("rec","c and chain R and resi 24-145"); cmd.create("pep","c and chain P"); cmd.delete("c")
cmd.hide("everything"); cmd.show("cartoon","rec or pep and resi 20-36")
cmd.color(C_ECD,"rec"); cmd.set("cartoon_transparency",0.25,"rec")
cmd.color(C_BLUE,"pep"); cmd.hide("cartoon","pep and resi 1-19")
cmd.set("cartoon_oval_width",0.35,"pep"); cmd.set("cartoon_oval_length",1.6,"pep")
groove=[29,32,36,39,68,69,88,91,121,128]
cmd.show("sticks","rec and resi "+"+".join(map(str,groove))); cmd.color(C_BLUE,"rec and resi "+"+".join(map(str,groove))+" and elem C")
cmd.show("sticks","rec and resi 123"); cmd.color("0xd02020","rec and resi 123 and elem C")
cmd.show("spheres","rec and resi 123 and not name N+C+O+CA"); cmd.set("sphere_scale",0.55,"rec and resi 123"); cmd.color("0xd02020","rec and resi 123")
cmd.show("sticks","pep and resi 28+29+32+33"); cmd.color(C_BLUE,"pep and resi 28+29+32+33 and elem C")
cmd.util.cnc("all")
cmd.orient("rec or (pep and resi 24-36)"); cmd.turn("z",90)
anchors=[("rec",r,"","#1f5fb5","L" if r in (29,32,36,39) else "R") for r in groove]
anchors+=[("pep",r,"GLP-1 ","#1f5fb5","L") for r in (28,29,32)]
anchors+=[("rec",123,"хотспот Baker: ","#c01818","R")]
render_scene("scene_g",1800,2200,anchors,"rec",title="Хотспот Baker «Leu95» = Leu123 (UniProt) в борозде ECD, 6X18",
  legend=[("красный: Leu123 (хотспот Baker; реконструкция нумерации, см. текст)","#c01818"),("синий: остатки борозды ECD и спираль GLP-1 24–36","#1f5fb5")],legend_loc="bottom",
  zoom_sel="rec or (pep and resi 24-36)",zoom_buf=3,pad=(0,380))
