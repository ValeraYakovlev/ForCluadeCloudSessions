import numpy as np, warnings, sys
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from an2 import *
from an4 import kabsch
def ecd_ca(model,chain,lo=29,hi=128):
    return {r.id[1]:r['CA'].coord.copy() for r in aa(model[chain]) if lo<=r.id[1]<=hi and 'CA' in r}
fab=load("5E94")
# Fab 3F52 on ECD chain G (Fab chains A,B) and second copy chain H (C,D)
def test(refpdb,refchain,label, ecd_chain="G", fab_chains=("A","B")):
    ref=load(refpdb); R=ecd_ca(ref,refchain); S=ecd_ca(fab,ecd_chain)
    com=sorted(set(R)&set(S))
    A=np.array([S[n] for n in com]); B=np.array([R[n] for n in com])
    Rm,t=kabsch(A,B); rm=np.sqrt((((A@Rm.T+t)-B)**2).sum(1).mean())
    fatoms=np.array([a.coord@Rm.T+t for c in fab_chains for r in aa(fab[c]) for a in r if a.element!='H'])
    # receptor atoms excluding ECD (>137) and ECD
    rec_tmd=np.array([a.coord for r in aa(ref[refchain]) if r.id[1]>137 for a in r if a.element!='H'])
    rec_ecd=np.array([a.coord for r in aa(ref[refchain]) if r.id[1]<=137 for a in r if a.element!='H'])
    from scipy.spatial import cKDTree
    tt=cKDTree(rec_tmd); d,_=tt.query(fatoms)
    n_clash2=(d<2.0).sum(); n_clash3=(d<3.0).sum(); dmin=d.min()
    # also peptide in 6X18 (chain P) clash check
    print(f"{label}: ECD superposition RMSD {rm:.2f} A over {len(com)} CA; Fab heavy atoms vs receptor TMD/ECL: min dist {dmin:.2f} A; atoms <2.0A: {n_clash2}; <3.0A: {n_clash3}; Fab atoms total {len(fatoms)}")
    return Rm,t
test("6X18","R","Fab 3F52 modelled on ECD of 6X18 (active, open) [copy1]")
test("6X18","R","Fab 3F52 modelled on ECD of 6X18 (active, open) [copy2]","H",("C","D"))
test("6LN2","A","Fab 3F52 modelled on ECD of 6LN2 (inactive, closed) [copy1]")
test("6LN2","A","Fab 3F52 modelled on ECD of 6LN2 (inactive, closed) [copy2]","H",("C","D"))
