import numpy as np, warnings, sys
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from an4 import *
pid=sys.argv[1]; rc=sys.argv[2]
m=load(pid); X=cadict(m,rc); R,t,nc,rm=superpose_core(X,REF); print(pid,"core",nc,"rmsd %.2f"%rm)
ref=load("6X18"); pepatoms=[a.coord for r in aa(ref["P"]) if 7<=r.id[1]<=15 for a in r]
pep=np.array(pepatoms)
# receptor atoms in 6X18 frame
hits={}
for r in aa(m[rc]):
    for a in r:
        c=a.coord@R.T+t
        d=np.min(np.linalg.norm(pep-c,axis=1))
        if d<3.5: hits.setdefault(r.id[1],[]).append(round(float(d),1))
ecdres=[(n,min(v)) for n,v in hits.items() if n<=137]
tmdres=[(n,min(v)) for n,v in hits.items() if n>137]
print("receptor residues within 3.5A of where GLP-1 res 7-15 sits (in this structure):")
print("  ECD residues:",sorted(ecdres)); print("  TMD/ECL residues:",len(tmdres))
# first resolved residues of chain
rs=aa(m[rc]); print("first modelled residues:",[(r.get_resname(),r.id[1]) for r in rs[:6]])
