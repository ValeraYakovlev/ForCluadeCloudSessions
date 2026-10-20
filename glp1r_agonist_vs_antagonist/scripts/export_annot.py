import warnings; warnings.filterwarnings("ignore")
from Bio.PDB import MMCIFParser, PDBIO, Select
m=MMCIFParser(QUIET=True).get_structure("6X18","work/pdb/6X18.cif")[0]
CLASSES={
 10:[29,30,32,35,36,39,67,68,69,88,89,90,91,121,123,128],       # ECD groove
 20:[152,190,235,363,364],                                         # TMD, shared agonist/antagonist-sensitive
 30:[197,198,234,284,288,310],                                     # TMD, agonist-selective (Coopman 2011; Al-Sabah 2003)
 40:[141,144,148,211,212,298,299,306,380,384,388],                 # TMD/ECL structural contacts with GLP-1 N-terminus
}
code={}
for c,res in CLASSES.items():
    for r in res: code[r]=c
class Sel(Select):
    def accept_chain(self,ch): return ch.id in ("R","P")
    def accept_residue(self,r): return r.id[0]==' '
for ch in m:
    if ch.id=="R":
        for r in ch:
            b=code.get(r.id[1],0)
            for a in r: a.set_bfactor(float(b))
    elif ch.id=="P":
        for r in ch:
            n=r.id[1]; b=50 if n<=17 else (60 if n<=23 else 70)
            for a in r: a.set_bfactor(float(b))
io=PDBIO(); io.set_structure(m)
out="renders/6X18_GLP1R_hotspots.pdb"
io.save(out,Sel())
hdr=("REMARK   1 6X18 GLP-1R (chain R) + GLP-1(7-36) (chain P); G protein removed. B-factor column = annotation class, NOT crystallographic B.\n"
"REMARK   2 Receptor (UniProt P43220 numbering): 0 none; 10 ECD groove (shared by agonist and antagonist);\n"
"REMARK   3   20 TMD shared (Ala lowers affinity of both GLP-1 and exendin(9-39)); 30 TMD agonist-selective (Ala lowers GLP-1 affinity preferentially);\n"
"REMARK   4   40 structural contact with the GLP-1 N-terminus (<=4 A in 6X18).\n"
"REMARK   5 Peptide: 50 residues 7-17 (N-terminal module, TMD only); 60 residues 18-23 (transition); 70 residues 24-36 (ECD groove helix).\n"
"REMARK   6 Sources: Coopman 2011 Mol Endocrinol; Al-Sabah & Donnelly 2003 FEBS Lett; own SASA analysis. PyMOL: spectrum b, rainbow / color by b-factor in ChimeraX.\n")
t=open(out).read(); open(out,"w").write(hdr+t)
print("saved",out)
