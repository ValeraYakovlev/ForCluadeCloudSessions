import numpy as np, warnings, sys
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from an4 import *
ref=load("6X18"); pep=np.array([a.coord for r in aa(ref["P"]) if 7<=r.id[1]<=15 for a in r])
for pid,rc in (("7DUR","R"),("7EVM","R"),("8WG7","R"),("7RG9","R"),("6X18","R"),("6LN2","A")):
    try:
        m=load(pid); X=cadict(m,rc); R,t,nc,rm=superpose_core(X,REF)
        best=[]
        for r in aa(m[rc]):
            if r.id[1]>137: continue
            d=min(np.min(np.linalg.norm(pep-(a.coord@R.T+t),axis=1)) for a in r)
            best.append((round(float(d),1),r.get_resname()+str(r.id[1])))
        best.sort(); print(pid,"closest ECD residues to GLP-1 7-15 site:",best[:6])
    except Exception as e: print(pid,"ERR",e)
