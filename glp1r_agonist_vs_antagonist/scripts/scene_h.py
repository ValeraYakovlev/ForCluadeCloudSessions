import sys; sys.path.insert(0,'.')
from scenes import *
import numpy as np, urllib.request, warnings; warnings.filterwarnings("ignore")
from Bio import Align
from Bio.Align import substitution_matrices
from an2 import load, aa
from an4 import kabsch
def seq(acc):
    t=urllib.request.urlopen(f"https://rest.uniprot.org/uniprot/{acc}.fasta",timeout=60).read().decode()
    return "".join(t.split("\n")[1:])
G,GC,GI=seq("P43220"),seq("P47871"),seq("P48546")
al=Align.PairwiseAligner(); al.substitution_matrix=substitution_matrices.load("BLOSUM62"); al.open_gap_score=-10; al.extend_gap_score=-0.5; al.mode="global"
def mapping(other,lo,hi):
    a=al.align(G[23:139],other[lo-1:hi])[0]; m={}
    for (s1,e1),(s2,e2) in zip(*a.aligned):
        for k in range(e1-s1): m[s2+k+lo]=s1+k+24
    return m
mGC,mGI=mapping(GC,26,136),mapping(GI,22,138)
ref=load("6X18"); gc=load("4ERS"); gi=load("2QKH")
R={r.id[1]:r['CA'].coord.copy() for r in aa(ref["R"]) if 'CA' in r}
def tf(other_chain,mp,lo,hi):
    O={r.id[1]:r['CA'].coord.copy() for r in aa(other_chain) if 'CA' in r}
    com=[(o,g) for o,g in mp.items() if o in O and g in R and lo<=g<=hi]
    A=np.array([O[o] for o,g in com]); B=np.array([R[g] for o,g in com])
    Rm,tv=kabsch(A,B)
    rms=float(np.sqrt(((A@np.array(Rm).T+np.array(tv)-B)**2).sum(1).mean()))
    print("superposed",len(com),"CA pairs, rmsd %.2f"%rms)
    return [float(Rm[0][0]),float(Rm[0][1]),float(Rm[0][2]),float(tv[0]),float(Rm[1][0]),float(Rm[1][1]),float(Rm[1][2]),float(tv[1]),float(Rm[2][0]),float(Rm[2][1]),float(Rm[2][2]),float(tv[2]),0.0,0.0,0.0,1.0]
base()
cmd.load("work/pdb/6X18.cif","c"); cmd.remove("not (chain R or chain P)"); cmd.remove("hydrogens")
cmd.create("rec","c and chain R and resi 24-145"); cmd.create("pep","c and chain P and resi 20-36"); cmd.delete("c")
cmd.load("work/pdb/4ERS.cif","g1"); cmd.create("gcgr","g1 and chain A"); cmd.delete("g1"); cmd.remove("gcgr and not polymer"); 
cmd.load("work/pdb/2QKH.cif","g2"); cmd.create("gipr","g2 and chain A"); cmd.delete("g2"); cmd.remove("gipr and not polymer")
cmd.transform_selection("gcgr",tf(gc["A"],mGC,29,125),homogenous=0)
cmd.transform_selection("gipr",tf(gi["A"],mGI,29,125),homogenous=0)
cmd.hide("everything"); cmd.show("cartoon","rec or pep or gcgr or gipr")
cmd.color(C_ECD,"rec"); cmd.color("0xb7e4d1","gcgr"); cmd.color("0xd8d2f5","gipr"); cmd.color(C_BLUE,"pep")
cmd.set("cartoon_transparency",0.35,"gcgr or gipr")
cmd.set("cartoon_oval_width",0.35,"pep"); cmd.set("cartoon_oval_length",1.6,"pep")
G_=[33,39,68,91,123]; 
cmd.show("sticks","rec and resi "+"+".join(map(str,G_))); cmd.color(C_BLUE,"rec and resi "+"+".join(map(str,G_))+" and elem C")
cmd.show("sticks","gcgr and resi 33+36+87"); cmd.color(C_GREEN,"gcgr and resi 33+36+87 and elem C")
cmd.show("sticks","gipr and resi 67"); cmd.color(C_VIOLET,"gipr and resi 67 and elem C")
cmd.show("spheres","rec and resi 123 and not name N+C+O+CA"); cmd.set("sphere_scale",0.5,"rec and resi 123"); cmd.color("0xd02020","rec and resi 123")
cmd.util.cnc("all")
cmd.orient("rec or pep"); cmd.turn("z",90)
def cen(sel):
    l=[]; cmd.iterate_state(1,sel+" and not name N+C+O+CA","stored_l.append((x,y,z))",space={'stored_l':l}); return np.mean(l,axis=0)
def cenca(sel):
    l=[]; cmd.iterate_state(1,sel+" and name CA","stored_l.append((x,y,z))",space={'stored_l':l}); return np.mean(l,axis=0)
custom=[("GLP1R W33",cen("rec and resi 33"),"#1f5fb5","L"),("GLP1R W39",cen("rec and resi 39"),"#1f5fb5","L"),("GLP1R E68",cen("rec and resi 68"),"#1f5fb5","R"),
        ("GLP1R W91",cen("rec and resi 91"),"#1f5fb5","R"),("GLP1R L123 (= «Leu95» Baker)",cen("rec and resi 123"),"#c01818","R"),
        ("GCGR F33 (хотспот)",cen("gcgr and resi 33"),"#13805a","L"),("GCGR W36 (хотспот)",cen("gcgr and resi 36"),"#13805a","L"),("GCGR W87 (хотспот)",cen("gcgr and resi 87"),"#13805a","R"),
        ("GIPR M67 (= «Met32» Baker)",cen("gipr and resi 67"),"#5a47c0","R")]
render_scene("scene_h",1800,2200,[],"rec",title="Хотспоты Baker на ECD GLP1R, GCGR и GIPR, совмещённых по ECD",custom=custom,fontpx=30,pad=(0,420),
  legend=[("синий: GLP1R (6X18) с GLP-1 24–36; красные сферы — Leu123","#1f5fb5"),("зелёный: GCGR (4ERS), хотспоты F33, W36, W87","#13805a"),("фиолетовый: GIPR (2QKH), хотспот Met67","#5a47c0")],legend_loc="bottom",
  zoom_sel="rec or pep or gcgr or gipr",zoom_buf=3)
