import numpy as np, warnings, sys
warnings.filterwarnings("ignore")
from Bio.PDB import MMCIFParser, ShrakeRupley, NeighborSearch
from Bio.PDB.Structure import Structure
from Bio.PDB.Model import Model
from Bio.PDB.Chain import Chain
P = MMCIFParser(QUIET=True)
def load(pid): return P.get_structure(pid, f"work/pdb/{pid}.cif")[0]
def aa(chain): return [r for r in chain if r.id[0]==' ']
def sasa(groups):
    """groups: dict name->list residues ; returns per-residue sasa for first group (key 'T')"""
    s=Structure("t"); m=Model(0); s.add(m)
    for k,(cid,res) in enumerate(groups):
        c=Chain(cid); m.add(c)
        for i,r in enumerate(res):
            rr=r.copy(); 
            if k>0: rr.id=(' ',i+1,' ')
            c.add(rr)
    ShrakeRupley(probe_radius=1.4,n_points=200).compute(s,level="R")
    return {r.id[1]:r.sasa for r in m[groups[0][0]]}
def buried_by(target, partner):
    """per-residue burial of target residues by partner residues"""
    a=sasa([("T",target)]); b=sasa([("T",target),("O",partner)])
    return {n:a[n]-b[n] for n in a}, a
def interface_residues(model, tch, pch, cutoff=0.5):
    t=aa(model[tch]); p=sum([aa(model[c]) for c in pch],[])
    # partner residues renumbered inside sasa(); keep a map
    d,_=buried_by(t,p); return d
if __name__=="__main__":
    res={}
    # 3C5T: Ex4(9-39) chain B on ECD chain A ; 3IOL GLP-1 chain B on ECD chain A
    for pid,lig in (("3C5T","B"),("3IOL","B")):
        m=load(pid); L=aa(m[lig]); R=aa(m["A"])
        bl,al=buried_by(L,R); br,ar=buried_by(R,L)
        print(f"\n== {pid}: ligand chain {lig} ({L[0].id[1]}-{L[-1].id[1]}) buried by ECD total {sum(bl.values()):.0f} A^2 (free ligand SASA {sum(al.values()):.0f}); ECD buried by ligand {sum(br.values()):.0f}")
        print(" ligand residues burial>20A2:", " ".join(f"{r.get_resname()}{r.id[1]}:{bl[r.id[1]]:.0f}" for r in L if bl[r.id[1]]>20))
        res[pid]={n:v for n,v in br.items() if v>10}
        print(" ECD residues buried>10A2:", " ".join(f"{r.get_resname()}{r.id[1]}:{br[r.id[1]]:.0f}" for r in R if br[r.id[1]]>10))
    # 6X18: ECD burial by GLP-1
    m=load("6X18"); L=aa(m["P"]); R=aa(m["R"]); E=[r for r in R if r.id[1]<=137]
    be,_=buried_by(E,L); res["6X18"]={n:v for n,v in be.items() if v>10}
    print("\n== 6X18 ECD residues buried by GLP-1:", " ".join(f"{r.get_resname()}{r.id[1]}:{be[r.id[1]]:.0f}" for r in E if be[r.id[1]]>10))
    # overlap of ECD interface residue sets
    s1=set(res["3C5T"]); s2=set(res["3IOL"]); s3=set(res["6X18"])
    print("\nECD interface residues (>10 A2): Ex4(9-39)",len(s1),"GLP-1 isolated",len(s2),"GLP-1 in 6X18",len(s3))
    print(" shared Ex4(9-39)&GLP-1(isolated):",len(s1&s2)," shared GLP-1 iso & 6X18:",len(s2&s3)," Ex4&6X18:",len(s1&s3))
    # Fab 3F52 (5E94): find which ECD chain pairs with which Fab chains
    m=load("5E94")
    for ec in ("G","H"):
        E=aa(m[ec]); 
        best=[]
        for fc in ("A","B","C","D"):
            b,_=buried_by(E,aa(m[fc])); best.append((fc,sum(b.values())))
        print("\n5E94 ECD chain",ec,"buried by Fab chains:",[(c,round(v)) for c,v in best])
