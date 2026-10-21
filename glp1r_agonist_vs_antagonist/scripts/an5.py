import numpy as np, warnings, sys
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from an2 import *
m=load("6X18"); P=aa(m["P"]); R=aa(m["R"]); rn={r.id[1]:r.get_resname() for r in R}
ns=NeighborSearch([a for r in R for a in r])
print("GLP-1 residue -> receptor residues within 4.0 A (TMD/ECL, numbering UniProt)")
for r in P:
    if r.id[1]>20: break
    s=set()
    for a in r:
        for nb in ns.search(a.coord,4.0,'R'):
            if nb.id[1]>137: s.add(nb.id[1])
    print(f"{r.get_resname()}{r.id[1]:>3}:", " ".join(f"{rn[n]}{n}" for n in sorted(s)))
ca={r.id[1]:r['CA'].coord for r in P}
d=lambda a,b: np.linalg.norm(ca[a]-ca[b])
print("\nCa distances in GLP-1 (6X18): H7-F12 %.1f, H7-S18 %.1f, H7-F28 %.1f, H7-W31 %.1f, H7-R36 %.1f"%(d(7,12),d(7,18),d(7,28),d(7,31),d(7,36)))
# helix check: i,i+4 distance ~6.2 for alpha
print("i,i+4 Ca distances: "+" ".join(f"{i}-{i+4}:{d(i,i+4):.1f}" for i in range(7,33,3)))
# nearest ECD residue Ca to His7 Ca
E={r.id[1]:r['CA'].coord for r in R if r.id[1]<=137 and 'CA' in r}
dm=min((np.linalg.norm(ca[7]-v),k) for k,v in E.items()); print("nearest ECD Ca to H7 Ca: %.1f A (res %d)"%dm)
# groove centroid (ECD residues W39,E68,Y69,L32,Y88,W91) to H7
gr=np.mean([E[k] for k in (32,39,68,69,88,91) if k in E],axis=0); print("ECD groove centroid -> H7 Ca: %.1f A"%np.linalg.norm(gr-ca[7]))
